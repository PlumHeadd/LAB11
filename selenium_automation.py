from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Browser configuration
alt_options = ChromeOptions()
alt_options.add_experimental_option("detach", True)
service_instance = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service_instance, options=alt_options)
driver.maximize_window()

# Navigate to Amazon EG
driver.get("https://www.amazon.eg/?language=en_AE")
time.sleep(2)

# Set locale cookies to English and USD
driver.add_cookie({'name': 'i18n-prefs', 'value': 'USD'})
driver.add_cookie({'name': 'lc-acbeg', 'value': 'en_AE'})
driver.refresh()
time.sleep(2)

# Search for "MacBook" instead of "Laptop"
search_input = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
)
search_input.clear()
search_input.send_keys("MacBook")
search_input.submit()

# Attempt to identify and click the first product result
locators_for_first_item = [
    "[data-component-type='s-search-result'] h2 a",
    ".s-result-item h2 a",
    "a[href*='/dp/']"
]

product_link = None
for locator in locators_for_first_item:
    try:
        product_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, locator))
        )
        if product_link:
            break
    except:
        continue

# Scroll to product and click using normal click
if product_link:
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", product_link)
    time.sleep(1)
    product_link.click()
else:
    print("No product link found.")
    driver.quit()
    exit()

# Extract product title
item_title = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "productTitle"))
).text.strip()
print("title:", item_title)

# Current product URL
current_page = driver.current_url
print("url:", current_page)

# Attempt to find product price using multiple selectors
price_selectors = [
    "span.a-price-whole",
    ".a-price .a-offscreen",
    "#priceblock_ourprice",
    "#priceblock_dealprice",
    ".a-price",
    "[data-a-color='price'] .a-offscreen"
]

found_price = None
for sel in price_selectors:
    try:
        price_el = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, sel))
        )
        price_text = price_el.get_attribute("textContent").strip()
        if price_text:
            found_price = price_text
            break
    except:
        continue

if not found_price:
    try:
        found_price = driver.find_element(By.CSS_SELECTOR, "[class*='price']").text.strip()
    except:
        found_price = "not found"

print("price:", found_price)

# Get product rating
try:
    product_rating = driver.find_element(By.ID, "acrPopover").get_attribute("title").strip()
except:
    product_rating = "no rating"

print("rating:", product_rating)

# Take a screenshot of the product page
screenshot_success = driver.save_screenshot("laptop_page.png")
if screenshot_success:
    print("saved screenshot as: laptop_page.png")
else:
    print("Screenshot not saved.")

time.sleep(3)
driver.quit()
