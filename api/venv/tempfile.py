from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
driver = webdriver.Chrome(options=options)

# Step 1: Login
driver.get('http://192.168.202.128:3000/#/login')  # Navigate to the login page
username_field = driver.find_element(By.ID, 'email')  # Locate username input field
password_field = driver.find_element(By.ID, 'password')  # Locate password input field
submit_button = driver.find_element(By.ID, 'loginButton')  # Locate submit button

# Enter login credentials
username_field.send_keys('admin@juice-sh.op')
password_field.send_keys('admin123')

# Submit the login form
submit_button.click()

# Step 2: Wait for the page to load after login
wait = WebDriverWait(driver, 10)
wait.until(EC.url_to_be('http://192.168.202.128:3000/#/search'))  # Wait until the desired URL is reached

# Step 3: Retrieve the page source
page_source = driver.page_source

# Step 4: Use BeautifulSoup to parse the page source
soup = BeautifulSoup(page_source, 'html.parser')

# Process the parsed HTML with BeautifulSoup
# Extract information, navigate the DOM, etc.
# Example: print the page title
title = soup.title.string
print(f'Page title: {title}')

# Close the driver
driver.quit()