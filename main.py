from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Setup Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URLs of the pages to scrape
urls = [
    ("https://www.ifood.com.br/delivery/sao-paulo-sp/coco-bambu---analia-franco-vila-gomes-cardim/4cdd2e7d-36b6-47e3-b435-428a77a7d967", "Coco Bambu"),
    ("https://www.ifood.com.br/delivery/sao-paulo-sp/republica-dos-camaroes-chacara-california/8c7e9b76-7963-4258-8f7d-4727a241543d", "República dos Camarões")
]

# List to store all dishes
all_dishes = []

# Function to extract dishes from a given URL
def extract_dishes(url, source):
    driver.get(url)
    time.sleep(10)
    dish_elements = driver.find_elements(By.CSS_SELECTOR, 'div.dish-card__info.dish-card__info--horizontal')
    dishes = []
    for element in dish_elements:
        name = element.find_element(By.CSS_SELECTOR, 'h3.dish-card__description').text
        details = element.find_element(By.CSS_SELECTOR, 'span.dish-card__details').text
        
        # Extract price and discount details
        try:
            discount_element = element.find_element(By.CSS_SELECTOR, 'span.dish-card__price--discount')
            original_price_element = discount_element.find_element(By.CSS_SELECTOR, 'span.dish-card__price--original')
            discount = discount_element.text.split(original_price_element.text)[0].replace('R$', '').strip()
            original_price = original_price_element.text.replace('R$', '').strip()
        except:
            discount = element.find_element(By.CSS_SELECTOR, 'span.dish-card__price[data-test-id="dish-card-price"]').text.replace('R$', '').strip()
            original_price = ''

        if 'camarão' in name.lower():
            # Clean and convert prices
            discount = discount.replace('A partir de', '').strip()
            try:
                discount_price_float = float(discount.replace(',', '.'))
                if original_price:
                    original_price = original_price.replace('A partir de', '').strip()
                    original_price_float = float(original_price.replace(',', '.'))
                    dishes.append((name, details, discount_price_float, original_price_float, source))
                else:
                    dishes.append((name, details, discount_price_float, '', source))
            except ValueError:
                continue
    return dishes

# Loop through each URL and extract dishes
for url, source in urls:
    dishes_from_url = extract_dishes(url, source)
    all_dishes.extend(dishes_from_url)

# Close the WebDriver
driver.quit()

# Sort dishes by price (discounted price)
all_dishes.sort(key=lambda dish: dish[2])

# Print the filtered and sorted dishes
for dish in all_dishes:
    if dish[3]:
        print(f"Name: {dish[0]}\nDetails: {dish[1]}\nDiscount Price: R$ {dish[2]:.2f}\nOriginal Price: R$ {dish[3]:.2f}\nSource: {dish[4]}\n")
    else:
        print(f"Name: {dish[0]}\nDetails: {dish[1]}\nPrice: R$ {dish[2]:.2f}\nSource: {dish[4]}\n")

# Define the CSV file name
csv_file_name = 'camarao_dishes_with_discount.csv'

# Write the data to a CSV file
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Details', 'Discount Price', 'Original Price', 'Source'])  # Writing the header
    for dish in all_dishes:
        if dish[3]:
            writer.writerow([dish[0], dish[1], dish[2], dish[3], dish[4]])
        else:
            writer.writerow([dish[0], dish[1], dish[2], '', dish[4]])

print(f"Data has been written to {csv_file_name}")
#changes
