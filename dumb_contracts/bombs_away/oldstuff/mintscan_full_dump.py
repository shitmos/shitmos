from selenium import webdriver
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

# Print full page source to terminal
print("\n--- FULL PAGE SOURCE ---\n")
print(driver.page_source)

# Close the driver
driver.quit()
