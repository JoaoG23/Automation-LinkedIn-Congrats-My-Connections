
import os
from time import sleep
import traceback

from dotenv import load_dotenv

from httpcore import TimeoutException
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.common.exceptions import InvalidSelectorException

from send_congrats_to_connectios.do_login.do_login import do_login
from send_congrats_to_connectios.send_congrats_to_connectios import send_congrats_to_connectios
from utils.logging.log_manager.log_manager import write_to_log

options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

load_dotenv()

    
if __name__ == '__main__':
    try:
        driver.maximize_window()
        
        user_login = {
            'email': os.getenv("USER_LINKEDIN" or ''),
            'password': os.getenv("PASSWORD_LINKEDIN" or '')
        }
        do_login(driver, user_login)
        sleep(11)
        
        send_congrats_to_connectios(driver)
   
    except WebDriverException as e:
        write_to_log(f"WebDriverException: {traceback.format_exc()}", type='error')
    except NoSuchElementException as e:
        write_to_log(f"NoSuchElementException: {traceback.format_exc()}", type='error')
    except InvalidSelectorException as e:
        write_to_log(f"InvalidSelectorException: {traceback.format_exc()}", type='error')
    except TimeoutException as e:
        write_to_log(f"TimeoutException: {traceback.format_exc()}", type='error')
    except Exception as e:
        write_to_log(f"Exception: {traceback.format_exc()}", type='error')
    finally:
        print("Encerrando automação")
        driver.quit()   