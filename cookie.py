from selenium import webdriver
from selenium.webdriver.common.by import By
from time import time

# Check and buy upgrades every 5 seconds
INTERVAL_SECONDS = 5
# How many minutes the game lasts
GAME_TIME_MINUTES = 5
# total number of upgrades
TOTAL_ROUNDS = GAME_TIME_MINUTES * 60 / 5

def get_price_and_item_list(selenium_driver):
    """
    Gets the upgraded element and price and returns it as a tuple of price list and item list
    return:
    price_list: Upgrade price list
    item_list: Upgrade element list
    """
    cursor = selenium_driver.find_element(By.CSS_SELECTOR, "#buyCursor b")
    grandmar = selenium_driver.find_element(By.CSS_SELECTOR, "#buyGrandma b")
    factory = selenium_driver.find_element(By.CSS_SELECTOR, "#buyFactory b")
    mine = selenium_driver.find_element(By.CSS_SELECTOR, "#buyMine b")
    shipment = selenium_driver.find_element(By.CSS_SELECTOR, "#buyShipment b")
    alchemy_lab = selenium_driver.find_element(By.XPATH, "//*[contains(@id, 'buyAlchemy')]")
    portal = selenium_driver.find_element(By.XPATH, "//*[contains(@id, 'buyPortal')]")
    time_machine = selenium_driver.find_element(By.XPATH, "//*[contains(@id, 'buyTime')]")

    cursor_price = int(cursor.text.split('-')[1].replace(',', ''))
    grandmar_price = int(grandmar.text.split('-')[1].replace(',', ''))
    factory_price = int(factory.text.split('-')[1].replace(',', ''))
    mine_price = int(mine.text.split('-')[1].replace(',', ''))
    shipment_price = int(shipment.text.split('-')[1].replace(',', ''))
    alchemy_lab_price = int(alchemy_lab.text.split('-')[1].split('\n')[0].replace(',', ''))
    portal_price = int(portal.text.split('-')[1].split('\n')[0].replace(',', ''))
    time_machine_price = int(time_machine.text.split('-')[1].split('\n')[0].replace(',', ''))

    price_list = [time_machine_price, portal_price, alchemy_lab_price, shipment_price, mine_price, factory_price,
                  grandmar_price, cursor_price]
    item_list = [time_machine, portal, alchemy_lab, shipment, mine, factory,
                 grandmar, cursor]
    return price_list, item_list


def buy_upgrades(selenium_driver):
    """
    check number of cookies available and buy the most expensive upgrade
    param: selenium_driver
    return: None
    """
    total_cookies = int(selenium_driver.find_element(By.ID, "money").text)
    price_list, item_list = get_price_and_item_list(selenium_driver)
    for i in range(len(price_list)):
        if total_cookies >= price_list[i]:
            item_list[i].click()
            break


def cookie_main_func():
    """
    main loop of cookie clicker
    :return
    None
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://orteil.dashnet.org/experiments/cookie/")

    cookie = driver.find_element(By.ID, "cookie")
    start = time()
    counter = 0
    print(TOTAL_ROUNDS)
    while counter < TOTAL_ROUNDS:
        cookie.click()
        time_now = time()
        if time_now - start >= INTERVAL_SECONDS:
            counter += 1
            buy_upgrades(driver)
            start = time_now

    # print out click per second
    cps = float(driver.find_element(By.ID, "cps").text.split(":")[1].replace(',', ''))
    print(cps)
    driver.quit()


cookie_main_func()
