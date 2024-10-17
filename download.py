from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager
from verification import check_orders
from dotenv import load_dotenv

load_dotenv()

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

url_sharepoint = 'YourURL'
driver.get(url_sharepoint)

wait = WebDriverWait(driver, 60)

try:
    email_input = wait.until(EC.presence_of_element_located((By.ID, "i0116")))
    email_input.send_keys('user@email.com.br')
    email_input.send_keys(Keys.RETURN)
    time.sleep(5)

    password_input = wait.until(EC.presence_of_element_located((By.NAME, "passwd")))
    password_input.send_keys('***')
    password_input.send_keys(Keys.RETURN)

    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idSIButton9"]')))
    driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()

except Exception as e:
    print("Erro durante o login:", e)

time.sleep(20)

try:
    status_compra_xpath = '//*[@id="html-list_2"]/div[1]/div[7]/div[13]/div'
    wait.until(EC.element_to_be_clickable((By.XPATH, status_compra_xpath))).click()
    print("Filtro de 'STATUS - COMPRA' clicado.")
    time.sleep(10)

    filter_by_xpath = '//span[@class="ms-ContextualMenu-itemText label-90" and text()="Filtrar por"]'
    wait.until(EC.element_to_be_clickable((By.XPATH, filter_by_xpath))).click()
    print("Opção 'Filtrar por' selecionada.")
    time.sleep(10)

    in_transit_option_xpath = '//span[@title="EM TRÂNSITO"]'
    wait.until(EC.element_to_be_clickable((By.XPATH, in_transit_option_xpath))).click()
    print("Status 'EM TRÂNSITO' selecionado.")
    time.sleep(15)
 
    apply_button_xpath = '//button[@data-automationid="FilterPanel-Apply"]'
    wait.until(EC.element_to_be_clickable((By.XPATH, apply_button_xpath))).click()
    print("Botão 'Aplicar' clicado com sucesso.")
    time.sleep(10)

except Exception as e:
    print("Erro ao aplicar o filtro 'EM TRÂNSITO':", e)

try:
    export_button_xpath = '//button[contains(., "Exportar")]'
    wait.until(EC.visibility_of_element_located((By.XPATH, export_button_xpath)))
    export_button = driver.find_element(By.XPATH, export_button_xpath)
    export_button.click()
    print("Botão 'Exportar' clicado com sucesso.")

    time.sleep(2)
    export_excel_xpath = '//*[@id="command-bar-menu-id"]/div/ul/li[2]/button/div/span'
    wait.until(EC.element_to_be_clickable((By.XPATH, export_excel_xpath)))
    export_excel_button = driver.find_element(By.XPATH, export_excel_xpath)
    export_excel_button.click()
    print("Botão 'Exportar para CSV' clicado com sucesso.")

except Exception as e:
    print("Erro ao exportar o arquivo CSV:", e)

time.sleep(10)
driver.quit()
print("Download automático concluído.")

check_orders()
