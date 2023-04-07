from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
import time
import pandas as pd

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
driver.set_window_size(1024, 600)
driver.maximize_window()
driver.get('https://www.etf.com/etfanalytics/etf-finder')
time.sleep(10)
button_100 = driver.find_element("xpath", "/html/body/div[5]/section/div/div[3]/section/div/div/div/div/div[2]/section[2]/div[2]/section[2]/div[1]/div/div[4]/button")
driver.execute_script("arguments[0].click();",button_100)
numeroPaginas = driver.find_element("xpath",'//*[@id="totalPages"]')
numeroPaginas = numeroPaginas.text.replace("of","")

numeroPaginas = int(numeroPaginas)

botaoNext = driver.find_element("xpath",'//*[@id="nextPage"]')

TabelaFind = driver.find_element("xpath",'//*[@id="finderTable"]')
listaTabelas = []

for Tabela in range(0,numeroPaginas):
        htmlTabela = TabelaFind.get_attribute('outerHTML')
        tabela = pd.read_html(str(htmlTabela))[0]
        listaTabelas.append(tabela)
        driver.execute_script("arguments[0].click();",botaoNext)

tabelaCadastoETFS = pd.concat(listaTabelas)

inputGoToPage = driver.find_element("xpath",'//*[@id="goToPage"]')
inputGoToPage.clear()
inputGoToPage.send_keys("1")
inputGoToPage.send_keys(u'\ue007')

perfomanceField = driver.find_element("xpath","/html/body/div[5]/section/div/div[3]/section/div/div/div/div/div[2]/section[2]/div[2]/ul/li[2]/span")
driver.execute_script("arguments[0].click();",perfomanceField)

TabelaFind = driver.find_element("xpath",'//*[@id="finderTable"]')
listaTabelas = []

for Tabela in range(0,numeroPaginas):
        htmlTabela = TabelaFind.get_attribute('outerHTML')
        tabela = pd.read_html(str(htmlTabela))[0]
        listaTabelas.append(tabela)
        driver.execute_script("arguments[0].click();",botaoNext)

tabelaRentabilidadeETFS = pd.concat(listaTabelas)


tabelaRentabilidadeETFS = tabelaRentabilidadeETFS.set_index("Ticker")
tabelaRentabilidadeETFS = tabelaRentabilidadeETFS[["1 Year", "3 Years", "5 Years"]]
tabelaCadastoETFS = tabelaCadastoETFS.set_index("Ticker")

baseDeDadosFinal = tabelaCadastoETFS.join(tabelaRentabilidadeETFS, how='inner')

print(baseDeDadosFinal)
   






