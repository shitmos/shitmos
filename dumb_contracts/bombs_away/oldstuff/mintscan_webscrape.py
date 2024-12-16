from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL of the Mintscan page
URL = "https://www.mintscan.io/osmosis/assets/native/ZmFjdG9yeS9vc21vMW42YXNyank5NzU0cTh5OWpzeHFmNTU3em1zdjNzM3hhNW05ZWc1L3VzcGljZQ==/?sector=holders"
driver.get(URL)

# Allow the page to load
time.sleep(5)

# Extract <a> elements containing addresses and data
a_elements = driver.find_elements(By.CSS_SELECTOR, "a.svelte-756ck7")

# Prepare lists for addresses and amounts
addresses = []
amounts = []

for a_element in a_elements:
    # Print the raw HTML of each <a> element for debugging
    print("\n--- <a> Element HTML ---")
    print(a_element.get_attribute("outerHTML"))

    # Extract the address from the href attribute
    href = a_element.get_attribute("href")
    if href:
        address = href.split("/")[-1]
        addresses.append(address)

    try:
        # Try to extract integer and decimal parts
        integer_part = a_element.find_element(By.CSS_SELECTOR, "div.typo.svelte-dotpqq[data-mono='true']").text.strip()
        decimal_part = a_element.find_element(By.CSS_SELECTOR, "div.typo.svelte-dotpqq[data-inline='true']").text.strip()

        # Combine integer and decimal parts
        full_amount = f"{integer_part}.{decimal_part}"
        amounts.append(full_amount)
    except Exception as e:
        # Print an error if elements are not found
        print(f"Error finding amount elements for address {address}: {e}")
        amounts.append("0.0")  # Default to 0.0 if amounts can't be parsed

# Ensure addresses and amounts match
if len(addresses) != len(amounts):
    print("\nMismatch between addresses and amounts.")
else:
    print("\nMatched Addresses and Amounts:")
    for address, amount in zip(addresses, amounts):
        print(f"{address}: {amount}")

# Save results to a file
with open("holders.txt", "w") as file:
    for address, amount in zip(addresses, amounts):
        file.write(f"{address}: {amount}\n")

print("Data saved to holders.txt")

# Close the driver
driver.quit()
