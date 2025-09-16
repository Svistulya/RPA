from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import NoSuchElementException


options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--no-proxy-server')
options.add_argument('--disable-extensions')

driver = webdriver.Chrome()

driver.get("https://www.saucedemo.com/")

username = "standard_user"
password = "secret_sauce"

    
login_field = driver.find_element(By.ID, "user-name") 
login_field.send_keys(username)

password_field = driver.find_element(By.ID, "password") 
password_field.send_keys(password)

login_button = driver.find_element(By.CLASS_NAME, "submit-button")
login_button.click()



dropdown_element = driver.find_element(By.CLASS_NAME, "product_sort_container")

select = Select(dropdown_element)
select.select_by_value("za")

cart_elements = driver.find_elements(By.CLASS_NAME, "inventory_item")

print("_____________________________________:", len(cart_elements))

cheapest_product = None
lowest_price = float('inf')


for product in cart_elements:
    title = product.find_element(By.CLASS_NAME, "inventory_item_name ").text
    
    price_text = product.find_element(By.CLASS_NAME, "inventory_item_price").text
    
    price = float(price_text.replace('$', '').replace('₽', '').replace(',', '').strip())
    
    add_to_cart_button = product.find_element(By.CLASS_NAME, "btn_inventory")
    
    if price < lowest_price:
        lowest_price = price
        cheapest_product = {
            'title': title,
            'price': price,
            'button': add_to_cart_button
        }


print("_____________________________________", cheapest_product)

add_to_cart_button.click()
cart = driver.find_element(By.CLASS_NAME,"shopping_cart_link")

cart.click()

checkout = driver.find_element(By.CLASS_NAME, "checkout_button")

checkout.click()

time.sleep(10)



