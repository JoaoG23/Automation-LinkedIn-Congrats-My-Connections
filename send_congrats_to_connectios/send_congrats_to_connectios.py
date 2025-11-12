from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from send_congrats_to_connectios.scroll_by_limit_connections.scroll_by_limit_connections import scroll_by_limit_connections
from selenium.webdriver.common.keys import Keys
from utils.logging.log_manager.log_manager import write_to_log


def send_congrats_to_connectios(driver):
    wait = WebDriverWait(driver, 20)
    button_my_network = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="global-nav"]/div/nav/ul/li[2]/a'))
    )
    button_my_network.click()
    
    sleep(3)
    driver.get("https://www.linkedin.com/mynetwork/catch-up/all/")
    
    sleep(7)
    
    # scroll_by_limit_connections(driver)
    
    list_congrats = driver.find_elements(By.XPATH, './/*[@id="send-privately-small"]')
    
    print(f"Encontrados {len(list_congrats)} botões de congratulações")
    
    for i, congrat in enumerate(list_congrats):
        try:
            # Tentar clicar no SVG primeiro
            try:
                wait.until(EC.element_to_be_clickable(congrat))
                # congrat.click()
                parent_element = congrat.find_element(By.XPATH, "./..")
                if parent_element.tag_name == "span":
                    parent_element.click()
                    sleep(7)
                    # Envia a mensagem usando Ctrl+Enter
                    actions = ActionChains(driver)

                    actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
                    sleep(3)
                    
                    # Pressiona ESC para fechar qualquer popup
                    actions = ActionChains(driver)
                    actions.send_keys(Keys.ESCAPE).perform()
                    sleep(2)
                print(f"Congratulação {i+1} enviada com sucesso")
            except ElementClickInterceptedException:
                    driver.execute_script("arguments[0].click();", congrat)
                    print(f"Congratulação {i+1} enviada com JavaScript")
            
            sleep(2)
            
        except Exception as e:
            print(f"Erro ao clicar no botão {i+1}: {e}")
