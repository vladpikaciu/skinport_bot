from playsound import playsound
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from termcolor import colored
from selenium.webdriver.chrome.options import Options

link = "https://skinport.com/market?sort=date&order=desc"
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--user-data-dir=C:/data")
s=Service("chromedriver.exe")
driver = webdriver.Chrome(service=s, options=chrome_options)
a = ActionChains(driver)

driver.get(link)

status = input("Please log in. Type 1 if logged in: ")
driver.get(link)
low_price = 2
high_price = 1000
list = set()
sleep(2)
driver.find_element(by=By.CLASS_NAME, value="LiveBtn").click()

while True:
    cart = False
    while True:
        try:
            parent = driver.find_element(by=By.CSS_SELECTOR, value="#content > div > div.CatalogPage-content > div.CatalogPage-items.CatalogPage-items--grid")
            items = parent.find_elements(by=By.CLASS_NAME, value="ItemPreview-content")[0:]
            for item in items:
                data = item.text.split("\n")
                data.remove(data[-1])
                clean_data = '\n'.join(data)
                price_bloc = item.find_element(by=By.CLASS_NAME, value="ItemPreview-price")
                dirty_price = price_bloc.find_element(by=By.CLASS_NAME, value="Tooltip-link").text.strip("€")
                price_list = dirty_price.split(",")
                price = ""
                for x in price_list:
                    price = price + x
                price = float(price)
                print(price)
                try:
                    discount = int(item.find_element(by=By.CLASS_NAME, value="ItemPreview-discount").text[2:].strip("%"))
                    if discount > 15 and clean_data not in list and price > low_price and price < high_price:
                        list.add(clean_data)
                        b = item.find_element(by=By.CLASS_NAME, value="ItemPreview-mainAction")
                        a.move_to_element(b).perform()
                        b.click()
                        playsound('beep.wav', False)
                        print(item.text)
                        cart = True
                except:
                    pass
        except:
            print("Error")
        if cart == True:
            driver.get("https://skinport.com/cart")
            sleep(1)
            driver.find_element(by=By.ID, value="cb-tradelock-1").click()
            driver.find_element(by=By.ID, value="cb-cancellation-2").click()
            driver.find_element(by=By.CLASS_NAME, value="CartSummary-checkoutBtn").click()
            sleep(1)
            card_num = driver.find_element(by=By.CLASS_NAME, value="adyen-checkout__card__cardNumber__input")
            expiry_date = driver.find_element(by=By.CLASS_NAME, value="adyen-checkout__card__exp-date__input")
            cvv = driver.find_element(by=By.CLASS_NAME, value="adyen-checkout__card__cvc__input")
            pay = driver.find_element(by=By.CLASS_NAME, value="adyen-checkout__button--pay")

            a.move_to_element(card_num).click().send_keys("4511292059118965").perform()
            a.move_to_element(expiry_date).click().send_keys("06/29").perform()
            a.move_to_element(cvv).click().send_keys("942").perform()
            a.move_to_element(pay).click().perform()
            sleep(3)
            driver.get(link)
            sleep(1)
            driver.find_element(by=By.CLASS_NAME, value="LiveBtn").click()
            cart = False


driver.quit()