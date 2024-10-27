from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from dotenv import load_dotenv
import cookies
import logging
import time
import os
load_dotenv()

headless=0
browser = 'chrome' # or 'firefox'

if browser == 'chrome':
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')

    driver = webdriver.Chrome(options)


elif browser == 'firefox':
    options = webdriver.FirefoxOptions()
    options.binary_location = '/usr/bin/firefox'
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)


def login(email, password):
    login_url = 'https://moogold.com/ru/account/'
    driver.get(login_url)
    login_input = driver.find_element(By.ID, 'username')
    login_input.clear()
    login_input.send_keys(email)
    password_input = driver.find_element(By.ID, 'password')
    password_input.clear()
    password_input.send_keys(password)
    remember_btn = driver.find_element(By.ID, 'rememberme')
    remember_btn.click()
    auth_btn = driver.find_element(By.NAME, 'login')
    auth_btn.click()
    time.sleep(5)
    cookies.save_cookies(driver)
    return driver


def check_login():
    login_url = 'https://moogold.com/ru/account/'
    driver.get(login_url)

    try:
        cookies.load_cookies(driver)
        driver.find_element(By.CLASS_NAME, 'woocommerce')
        return 1

    except Exception as e:
        logging.error(e)
        return 0


def select_usd():
    selector = driver.find_element(By.CLASS_NAME, 'widget_wc_aelia_currencyswitcher_widget')
    selector.click()
    time.sleep(5)
    usd_select = driver.find_element(By.XPATH, f'//option[@value="USD"]')
    usd_select.click()


def add_genshin(value, id, server):
    allowed_values = ['60', '300-30', '980-110', '1980-260', '3280-600', '6480-1600']
    allowed_servers = ['usa', 'euro', 'asia', 'cht']

    if value in allowed_values and server in allowed_servers:
        genshin_url = 'https://moogold.com/ru/product/genshin-impact/'
        driver.get(genshin_url)

        classname = f'variable-item button-variable-item button-variable-item-{value}-genesis-crystals'
        item_btn = driver.find_element(By.XPATH, f'//li[@class="{classname}"]')
        item_btn.click()
        id_input = driver.find_element(By.ID, 'field_wcpa-text-1609166509573')
        id_input.clear()
        id_input.send_keys(id)

        server_select = driver.find_element(By.XPATH, f'//option[@value="os_{server}"]')
        server_select.click()

        btn_text = 'single_add_to_cart_button button alt'
        cart_button = driver.find_element(By.XPATH, f'//button[@class="{btn_text}"]')
        cart_button.click()
        time.sleep(5)


def add_mobla(item, id, server, region):
    allowed_values = ['8-diamonds', '32-3-diamonds', '80-8-diamonds', '120-12-diamonds', '239-25-diamonds', '396-44-diamonds', '633-101-diamonds', '791-142-diamonds', '1186-224-diamonds', '1581-300-diamonds',
                      '2371-474-diamonds', '5136-1027-diamonds', 'weekly-pass', 'twilight-pass']

    mobla_url = 'https://moogold.com/ru/product/mobile-legends-russia/'
    driver.get(mobla_url)
    #time.sleep(30)

    #select_usd()

    classname = f'variable-item button-variable-item button-variable-item-{item}'
    item_btn = driver.find_element(By.XPATH, f'//li[@class="{classname}"]')
    item_btn.click()
    id_input = driver.find_element(By.ID, 'field_wcpa-text-5f6f144f8ffd7')
    id_input.clear()
    id_input.send_keys(id)

    server_input = driver.find_element(By.ID, "field_wcpa-text-1601115253775")
    server_input.clear()
    server_input.send_keys(server)

    btn_text = 'single_add_to_cart_button button alt'
    cart_button = driver.find_element(By.XPATH, f'//button[@class="{btn_text}"]')
    cart_button.click()
    time.sleep(5)


def checkout():
    checkout_url = 'https://moogold.com/ru/checkout/'
    driver.get(checkout_url)

    terms = driver.find_element(By.NAME, 'terms')
    terms.send_keys(Keys.SPACE)

    #order = driver.find_element(By.ID, 'place_order')
    #order.click()

    time.sleep(10)



if __name__ == '__main__':
    email = os.getenv('EMAIL')
    password = os.getenv('MOOGOLD_PASSWORD')

    driver.get('https://moogold.com/ru/account/')

    if not check_login():
        driver = login(email, password)

    add_genshin('60', '1234', 'usa')
    checkout()
