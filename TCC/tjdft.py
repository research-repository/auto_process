from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from unidecode import unidecode
from selenium import webdriver
from threading import Thread
import pandas as pd
import datetime
import pdfkit
import pprint
import base64
import shutil
import time
import glob
import re
import os

class TJDFT(webdriver.Firefox):
"""
Classe para interação automatizada com o site do Tribunal de Justiça do Distrito Federal e dos Territórios (TJDFT).

Atributos:
- diretorio_arquivos(str): Caminho para o diretório de arquivos da instância.
- config_kdfkit(pdfkit.configuration): Configuração para a conversão de HTML para PDF usando wkhtmltopdf.

Métodos Públicos:
- __init__(): Inicializa uma instância da classe.
- busca_processo(processo:str) -> None: Realiza a busca por um processo no site do TJDFT.
- busca_documento(processo:str) -> None: Busca documentos relacionados a um processo e salva em PDF se encontrados.
"""
def __init__(self):
"""
Inicializa uma instância da classe TJDFT.
- Define o diretório de arquivos como subdiretório "arquivos" no diretório de trabalho atual.
- Cria o diretório se ele não existir.
- Configura o serviço do WebDriver do Firefox.
- Configura um tempo de espera implícito de 60 segundos.
- Configura o caminho para o executável do wkhtmltopdf.
"""
self.diretorio_arquivos = os.path.join(os.getcwd(), "arquivos")

if not os.path.exists(self.diretorio_arquivos):
os.makedirs(self.diretorio_arquivos)

service = Service(GeckoDriverManager().install())
super(TJDFT, self).__init__(service = service)
self.implicitly_wait(60)

path_wkhtmltopdf = r'C:\ProgramFiles\wkhtmltopdf\bin\wkhtmltopdf.exe'
self.config_kdfkit = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

def busca_processo(self, processo):
"""
Realiza a busca por um processo no site do Tribunal de Justiça do Distrito Federal e dos Territórios (TJDFT).

Args:
- processo (str): Número do processo a ser pesquisado.

Returns:
None

Raises:
- WebDriverException: Se ocorrer um erro ao interagir com o navegador.
"""
self.get(f"https://cache-internet.tjdft.jus.br/cgi-bin/tjcgi1?NXTPGM=tjhtml105&SELECAO=1&ORIGEM=INTER&CIRCUN=1&CDNUPROC={processo}")

def busca_documento(self, processo):
"""
Realiza a busca por documentos relacionados a um processo no site do Tribunal de Justiça do Distrito Federal e dos Territórios (TJDFT).

Args:
- processo (str): Número do processo para o qual os documentos serão buscados.

Returns:
None

Raises:
- WebDriverException: Se ocorrer um erro ao interagir com o navegador.
"""
print(f"Buscando documentos do processo{processo}")
self.busca_processo(processo)

tabela = self.find_element(By.TAG_NAME, "table")
tags_a = tabela.find_elements(By.TAG_NAME, "a")

links = []
for a in tags_a:
links+=[a.get_attribute("href")]

encontrou_transito_em_julgado = False
encontrou_perdimento = False

for i in range(len(links)):
self.get(links[i])
texto_pagina = self.find_element(By.TAG_NAME, "body").text.replace ("\n", " ").upper()
if "PERDIMENTO" in texto_pagina:
if not encontrou_perdimento:
encontrou_perdimento = True
pdfkit.from_url(self.current_url, f"arquivos/{processo}_perdimento.pdf", configuration = self.config_kdfkit)
print (f"\tDocumento 'perdimento' encontrado no {i+1} Âs documento aberto")

elif "EM JULGADO" in texto_pagina:
if not encontrou_transito_em_julgado:
encontrou_transito_em_julgado = True
pdfkit.from_url(self.current_url, f"arquivos/{processo}_transito_em_julgado.pdf", configuration = self.config_kdfkit)
print (f"\tDocumento 'trânsito em julgado' encontrado no {i+1} Âs documentoaberto")

if encontrou_perdimento and encontrou_transito_em_julgado:
return
