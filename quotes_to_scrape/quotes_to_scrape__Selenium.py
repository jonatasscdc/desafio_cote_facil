# Import the required modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Create a webdriver instance
driver = webdriver.Chrome()

# Define the url of the website
url = "http://quotes.toscrape.com/"

# Define a list to store the scraped data
data = []

# Define a function to scrape one page
def scrape_page():
    # Wait for the quotes to load
    quotes = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quote")))
    
    # Loop through each quote
    for quote in quotes:
        # Extract the text, author and tags
        text = quote.find_element(By.CLASS_NAME, "text").text
        author = quote.find_element(By.CLASS_NAME, "author").text
        tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]
        
        if author == 'J.K. Rowling':
            # Append the data to the list
            data.append((text, author, tags))
    
    # Return True if there is a next button, False otherwise
    try:
        next_button = driver.find_element(By.CLASS_NAME, "next")
        return True
    except:
        return False

# Navigate to the url
driver.get(url)

# Scrape the first page
has_next = scrape_page()

# Scrape the next pages until there is no next button
while has_next:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Click the next button
    next_button = driver.find_element(By.XPATH, "//li[@class='next']//a[last()]")
    next_button.click()
    # Scrape the current page
    has_next = scrape_page()

# Close the driver
driver.close()

# Print the scraped data
for item in data:
    print(item)

#Exporting the data to a json file 
with open('quotes.json', 'w') as f:
    json.dump(data, f, indent=2)
    
