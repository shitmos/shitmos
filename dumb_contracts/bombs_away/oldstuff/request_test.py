import requests
URL = "https://www.mintscan.io/osmosis/assets/native/ZmFjdG9yeS9vc21vMW42YXNyank5NzU0cTh5OWpzeHFmNTU3em1zdjNzM3hhNW05ZWc1L3VzcGljZQ==/?sector=holders"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(URL, headers=headers)
print(response.status_code)
print(response.text[:500])  # Print the first 500 characters of the response
