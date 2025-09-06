from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from utils.logging.log_manager.log_manager import write_to_log #utils\logging\log_manager\log_manager.py

def scroll_by_limit_connections(driver, limit_scrolling:int = 20):
    for _ in range(limit_scrolling):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        print("Page Down executado")
        sleep(6)
    for _ in range(limit_scrolling):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
        print("Page Up executado")
        sleep(2)
    # write_to_log(f"Scrolling {limit_scrolling} vezes.", type='info')