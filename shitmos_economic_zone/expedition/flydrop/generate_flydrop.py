#!/usr/bin/env python3
# generate_flydrop.py — chunked unsigned tx generator
#
# ONE `osmosisd tx bank send --generate-only` per chunk using positional FROM
# (your key NAME), then append remaining MsgSend in-memory.
#
# Use --verbose to print the exact generate-only command and temp file used.

import argparse, json, subprocess, sys, re, math, shutil, tempfile, os
from pathlib import Path
from datetime import datetime
from decimal import Decimal

BANNER = "═" * 66

# --- bech32 helpers -----------------------------------------------------------
try:
    from bech32 import bech32_decode, bech32_encode, convertbits
except Exception:
    sys.exit("❌ Please install:  pip install bech32")

def to_osmo(a: str) -> str:
    a = a.strip()
    if not a:
        raise ValueError("empty")
    hrp, data = bech32_decode(a)
    if hrp is None or data is None:
        raise ValueError(f"bad bech32: {a}")
    if hrp == "osmo":
        return a
    raw = convertbits(data, 5, 8, False)
    out5 = convertbits(raw, 8, 5, True)
    return bech32_encode("osmo", out5)

def run_visible_to_file(cmd, outfile: Path) -> int:
    with open(outfile, "w", encoding="utf-8") as f:
        proc = subprocess.Popen(cmd, stdout=f)
        return proc.wait()

def chunks(xs, n):
    for i in range(0, len(xs), n):
        yield xs[i:i+n]

def parse_gas_price(gp: str):
    m = re.match(r"^\s*([0-9]*\.?[0-9]+)\s*([a-zA-Z0-9/._-]+)\s*$", gp)
    if not m:
        raise ValueError(f"bad --gas-prices: {gp}")
    return Decimal(m.group(1)), m.group(2)

def build_msg(from_addr: str, to_addr: str, amount: int, denom: str) -> dict:
    return {
        "@type": "/cosmos.bank.v1beta1.MsgSend",
        "from_address": from_addr,
        "to_address": to_addr,
        "amount": [{"denom": denom, "amount": str(amount)}]
    }

def main():
    ap = argparse.ArgumentParser(description="Generate unsigned multi-message tx JSONs (chunked, one prompt per chunk)")
    ap.add_argument("--input", default="addresses.txt")
    ap.add_argument("--denom", required=True)
    ap.add_argument("--amount", required=True, type=int)
    ap.add_argument("--from-key", required=True)        # key NAME used as positional FROM
    ap.add_argument("--from-address", required=True)    # address for message bodies
    ap.add_argument("--chunk", type=int, default=200)
    ap.add_argument("--memo", default="flydrop")
    ap.add_argument("--chain-id", default="osmosis-1")
    ap.add_argument("--node", default="https://rpc.osmosis.zone:443")
    ap.add_argument("--gas-prices", default="0.025uosmo")
    ap.add_argument("--gas-adjustment", default="1.2")
    ap.add_argument("--keyring-backend", default="file")
    ap.add_argument("--output-dir", default="./transactions")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if not shutil.which("osmosisd"):
        print("❌ osmosisd not found on PATH", file=sys.stderr)
        sys.exit(1)

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    debugdir = outdir / "_debug"
    debugdir.mkdir(exist_ok=True)

    # read + convert + de-dupe (preserve order)
    src = Path(args.input)
    if not src.exists():
        sys.exit(f"❌ missing input file: {src}")

    raw_lines = [ln for ln in src.read_text(encoding="utf-8").splitlines()]
    cleaned = [ln.strip() for ln in raw_lines if ln.strip()]
    converted, skipped = [], []
    for ln in cleaned:
        try:
            converted.append(to_osmo(ln))
        except:
            skipped.append(ln)

    seen, recips = set(), []
    for a in converted:
        if a not in seen:
            seen.add(a); recips.append(a)

    print(BANNER)
    print("📋 Inputs")
    print(f"  raw lines:      {len(raw_lines)}")
    print(f"  non-empty:      {len(cleaned)}")
    print(f"  convertible:    {len(converted)}")
    print(f"  unique outputs: {len(recips)}")
    if skipped:
        (debugdir/"skipped.txt").write_text("\n".join(skipped), encoding="utf-8")
        print(f"  skipped lines:  {len(skipped)}  (see {debugdir/'skipped.txt'})")
    print(BANNER)

    if not recips:
        sys.exit("❌ no valid osmo addresses")

    # chunked build
    idx = 0
    for group in chunks(recips, args.chunk):
        idx += 1
        first_to = group[0]
        amtdenom = f"{args.amount}{args.denom}"

        # 1) base generate-only with positional FROM (key NAME) → prompts once
        tmp_base = Path(tempfile.gettempdir()) / f"flydrop_base_{os.getpid()}_{idx}.json"
        gen_cmd = [
            "osmosisd","tx","bank","send",
            args.from_key, first_to, amtdenom,          # <-- POSITONAL: FROM TO AMOUNT
            "--chain-id", args.chain_id,
            "--node", args.node,
            "--gas","auto",
            "--gas-prices", args.gas_prices,
            "--gas-adjustment", args.gas_adjustment,
            "--keyring-backend", args.keyring_backend,
            "--generate-only",
            "--output","json"
        ]
        if args.verbose:
            print(f"   ▶ chunk {idx}: generate-only cmd:")
            print("     " + " ".join(gen_cmd))
            print(f"     stdout → {tmp_base}")

        rc = run_visible_to_file(gen_cmd, tmp_base)
        if rc != 0:
            (debugdir/"last_failed_cmd.txt").write_text(" ".join(gen_cmd), encoding="utf-8")
            print(f"❌ generate-only failed for chunk {idx}. See {debugdir/'last_failed_cmd.txt'}.", file=sys.stderr)
            sys.exit(1)

        try:
            base = json.loads(tmp_base.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            (debugdir/"last_failed_cmd.txt").write_text(" ".join(gen_cmd), encoding="utf-8")
            (debugdir/"last_failed_output.txt").write_text(tmp_base.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"❌ non-JSON output for chunk {idx}. See {debugdir/'last_failed_output.txt'}.", file=sys.stderr)
            sys.exit(1)
        finally:
            try: tmp_base.unlink(missing_ok=True)
            except: pass

        # 2) append remaining messages in memory
        base["body"]["memo"] = args.memo

        # guarantee first message fields
        base_msg = base["body"]["messages"][0]
        base_msg["from_address"] = args.from_address
        base_msg["to_address"] = first_to
        base_msg["amount"][0]["denom"] = args.denom
        base_msg["amount"][0]["amount"] = str(args.amount)

        # other recipients
        for to in group[1:]:
            base["body"]["messages"].append(
                build_msg(args.from_address, to, args.amount, args.denom)
            )

        # 3) scale gas/fee with msg count
        try:
            per = int(base["auth_info"]["fee"].get("gas_limit") or "200000")
        except Exception:
            per = 200000
        mcount = len(base["body"]["messages"])
        gas = math.ceil(per * mcount * float(args.gas_adjustment))
        base["auth_info"]["fee"]["gas_limit"] = str(gas)

        price, fee_denom = parse_gas_price(args.gas_prices)
        fee = (price * Decimal(gas)).quantize(Decimal("1"))
        base["auth_info"]["fee"]["amount"] = [{"denom": fee_denom, "amount": str(fee)}]

        # 4) save
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        outpath = outdir / f"flydrop_tx_{ts}_{idx:04d}.json"
        outpath.write_text(json.dumps(base, indent=2), encoding="utf-8")
        print(f"saved: {outpath}")

    print(BANNER)
    print("✅ Generation complete")
    print(f"  tx files dir: {outdir}")
    print(BANNER)

if __name__ == "__main__":
    main()
