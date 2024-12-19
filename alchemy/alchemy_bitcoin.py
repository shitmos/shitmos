import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


# Fixed inputs
bitcoin_deposit = 0.00890047  # Fixed Bitcoin deposit
btc_price_usd = 97856.026748  # Bitcoin price in USD
shitmos_price_usd = 0.025290  # Market price of Shitmos in USD

# Pool weighting
weight_bitcoin = 0.40
weight_shitmos = 0.60

# Calculate the total pool value in USD
value_bitcoin_usd = bitcoin_deposit * btc_price_usd
total_pool_value_usd = value_bitcoin_usd / weight_bitcoin

# Calculate the required value of Shitmos
value_shitmos_usd = total_pool_value_usd * weight_shitmos

# Generate a range of price deviations (-20% to +20%)
price_deviations = [i / 100 for i in range(-20, 21)]  # -20% to +20% in increments of 1%
shitmos_prices = [shitmos_price_usd * (1 + dev) for dev in price_deviations]
shitmos_quantities = [value_shitmos_usd / price for price in shitmos_prices]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(price_deviations, shitmos_quantities, label="Shitmos Quantity", color="blue")
plt.axvline(x=0, color="red", linestyle="--", label="Market Price (0% Deviation)")
plt.axhline(y=value_shitmos_usd / shitmos_price_usd, color="green", linestyle="--", label="Quantity at Market Price")

# Add labels, legend, and title
plt.title("Effect of Shitmos Price Deviation on Required Pool Quantity", fontsize=14)
plt.xlabel("Shitmos Price Deviation (%)", fontsize=12)
plt.ylabel("Shitmos Quantity Required", fontsize=12)
plt.xticks(ticks=[i / 100 for i in range(-20, 21, 5)], labels=[f"{i}%" for i in range(-20, 21, 5)])
plt.legend()
plt.grid(alpha=0.3)


# Show plot
plt.show()
