import os
from time import sleep
from connect_people.connect_people_of_page.connect_people_of_page import connect_people_of_page
from connect_people.encode_message_for_url.encode_message_for_url import encode_message_for_url
from selenium.webdriver.common.by import By

from utils.logging.log_manager.log_manager import write_to_log

    
def search_people_and_connect(driver, information_people):
    
    description_people = information_people['description']
    
    description_encoded = encode_message_for_url(description_people)
    sleep(5)
    driver.get(f'https://www.linkedin.com/search/results/people/?keywords={description_encoded}')
    sleep(12)
    
    limit_connects = os.getenv("LIMIT_CONNECTIONS")
    quantity_people_connects = 0
    
    while quantity_people_connects <= int(limit_connects):
        sleep(7)
        quantity_people_connects += connect_people_of_page(driver)
        write_to_log(f"conuctos realizados: {quantity_people_connects}", type='info')
        sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(6)
        next_page_button = driver.find_element(By.XPATH, '//*[@aria-label="Avançar"]')
        next_page_button.click()
        sleep(4)
    mgs = f"Total de conexões realizadas: {quantity_people_connects}"
    
    write_to_log(mgs, type='info')
    print(mgs)
    