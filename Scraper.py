#Import selenium
from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


def get_data(driver):
    products = []
    driver_return = driver.find_elements(by=By.CSS_SELECTOR, value = '.col-xs-2-4')
    for i in range(len(driver_return)):
        product_name = driver_return[i].find_element(by = By.CSS_SELECTOR, value = '.ie3A\+n').text
        product_price = driver_return[i].find_element(by = By.CSS_SELECTOR, value = '.ZEgDH9').text
        product_price = float(
                 product_price
                 .strip()
                 .replace('.', '')
                 .replace(',', '.'))
        try:
            product_discount = driver_return[i].find_element(by = By.CSS_SELECTOR, value = '.percent').text
        except:
            product_discount = 0
        product_link = driver_return[i].find_element(by = By.TAG_NAME, value = 'a').get_attribute('href')
        products.append([product_name, product_price, product_discount[:-1] if product_discount != 0 else 0, product_link])
    return products

def scraper(url):
    n = 5
    j = 0
    produtos = []
    options = FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--enable-javascript')
    options.add_argument('--allow-running-insecure-content')
    driver = webdriver.Firefox(options = options)
    while n > 0:
        #Pegando os dados
        url_f = url + f'&page={j}'
        driver.switch_to.new_window('tab')
        driver.get(url_f)
        j += 1
        
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.col-xs-2-4')))
        # Definir o fundo da pagina
        bottom_height = driver.execute_script('return document.body.scrollHeight')
        try:
            for i in range(1,61):
                current_height = driver.execute_script('return document.body.scrollHeight')
                # Descer a pagina de em 1/60
                driver.execute_script(f'window.scrollTo({current_height}, {i*bottom_height/60});')

                # Esperar carregar
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.col-xs-2-4:nth-child({i})')))
        except:
            for i in range(1,5):
                current_height = driver.execute_script('return document.body.scrollHeight')
                # Descer a pagina de em 1/4
                driver.execute_script(f'window.scrollTo({current_height}, {i*bottom_height/4});')
                time.sleep(0.3)
        #Ajuste do while
        
        if n == 1 and j == 1:
            num_pags = driver.find_element(by = By.CSS_SELECTOR, value = '.shopee-mini-page-controller__total').text
            n = int(num_pags)-3
        else:
            n -= 1
        produtos.extend(get_data(driver))
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.quit()
    return produtos
#print(scraper('https://shopee.com.br/search?keyword=xiaomi%20redmi%20airdots&locations=Internacional&noCorrection=true&ratingFilter=4'))
#print(scraper('https://shopee.com.br/search?keyword=picareta&noCorrection=true&ratingFilter=5'))
