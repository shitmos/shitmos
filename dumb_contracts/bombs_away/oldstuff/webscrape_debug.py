from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL of the Mintscan page
URL = "https://www.mintscan.io/osmosis/assets/native/ZmFjdG9yeS9vc21vMW42YXNyank5NzU0cTh5OWpzeHFmNTU3em1zdjNzM3hhNW05ZWc1L3VzcGljZQ==/?sector=holders"
driver.get(URL)

# Wait until the table rows are loaded
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr"))
    )
except Exception as e:
    print(f"Error loading page elements: {e}")
    driver.quit()
    exit()

# Extract table rows
rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

# Prepare lists for addresses and amounts
addresses = []
amounts = []

for row in rows:
    try:
        # Extract the address from the first cell
        address_element = row.find_element(By.CSS_SELECTOR, "td:first-child a")
        address = address_element.get_attribute("href").split("/")[-1]
        addresses.append(address)

        # Extract the amount from the second cell
        amount_element = row.find_element(By.CSS_SELECTOR, "td:nth-child(2) div")
        amount = amount_element.text.strip().replace(",", "")
        amounts.append(amount)
    except Exception as e:
        print(f"Error processing row: {e}")
        addresses.append("N/A")
        amounts.append("0.0")

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
