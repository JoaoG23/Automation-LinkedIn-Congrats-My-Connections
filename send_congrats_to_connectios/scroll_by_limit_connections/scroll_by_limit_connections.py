from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from utils.logging.log_manager.log_manager import write_to_log #utils\logging\log_manager\log_manager.py

def scroll_by_limit_connections(driver, limit_scrolling:int = 20):
    webpage = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    navbar = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="workspace"]/div/div/div[2]/div/section/div/div/nav'))
    )
    navbar.click()

    for _ in range(limit_scrolling):
        webpage.send_keys(Keys.PAGE_DOWN)
        print("Page Down executado")
        sleep(6)
    for _ in range(limit_scrolling):
        webpage.send_keys(Keys.PAGE_UP)
        print("Page Up executado")
        sleep(2)
    # write_to_log(f"Scrolling {limit_scrolling} vezes.", type='info')