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
import pprint
import base64
import shutil
import time
import glob
import re
import os

class TCC (webdriver.Firefox):
"""
Classe TCC para automação de processos no sistema SEI usando Selenium WebDriver. Esta classe herda da classe webdriver.Firefox do Selenium e encapsula métodos específicos para a automação de procedimentos relacionados ao Trabalho de Conclusão de Curso (TCC). Os métodos fornecem funcionalidades para interagir com a interface do usuário do sistema SEI, como a criação de processos, inclusão de documentos, geração de documentos, registro de documentos externos, inclusão de ofícios, etc.
Nota: Certifique-se de fornecer as credenciais necessárias e os caminhos corretos para os arquivos ao utilizar os métodos desta classe.
Exemplo de uso:
```
tcc_instance = TCC()
credenciais = {"USUARIO": " seu_usuario", "SENHA": "sua_senha"}
sentenca_perdimento = "/caminho/para/ sentenca_perdimento.pdf"
transito_julgado = "/caminho/para/transito_julgado.pdf"

tcc_instance.login(credenciais)
tcc_instance.executa_procedimento(sentenca_perdimento, transito_julgado)

# Outras operações e interações podem ser realizadas utilizando os métodos da classe.
```
Certifique-se de encerrar a instância da classe após a conclusão das operações.
"""
def__init__(self):
"""
Inicializa a instância da classe TCC.
O método utiliza o Selenium WebDriver para configurar a automação do navegador.

- Configura o serviço do WebDriver usando o GeckoDriverManager.
- Chama o construtor da classe base com o serviço configurado.
- Define o tempo de espera implícito como 60 segundos.
"""
service = Service (GeckoDriverManager().install())
super (TCC, self).__init__(service = service)
self.implicitly_wait (60)

def pagina_inicial (self):
"""
Navega para a página inicial do sistema.
Este método utiliza o Selenium WebDriver para acessar a página inicial do sistema SEI hospedado no URL "https://sipseiteste.fiocruz.br/sip/login.php?sigla_orgao_sistema=FIOCRUZ&sigla_sistema=SEI".
"""
self.get("https://sipseiteste.fiocruz.br/sip/login.php?sigla_orgao_sistema=FIOCRUZ&sigla_sistema=SEI")

def login(self,credenciais):
"""
Realiza o login no sistema SEI.
Este método utiliza o Selenium WebDriver para preencher o formulário de login com as credenciais fornecidas e clicar no botão de entrar.
Parâmetros:
credenciais(dict): Um dicionário contendo as credenciais de login, com as chaves "USUARIO" e "SENHA".
"""
usuario = self.find_element(By.ID, "txtUsuario")
usuario.send_keys(credenciais["USUARIO"])

senha = self.find_element(By.ID, "pwdSenha")
senha.send_keys(credenciais["SENHA"])

entrar = self.find_element(By.ID, "sbmAcessar")
entrar.click()

def tela_iniciar_processo(self, tipo_processo):
"""
Navega para a tela de iniciar um novo processo no sistema SEI.
Este método utiliza o Selenium WebDriver para interagir com a interface do usuário, selecionando o tipo de processo, configurando o nível de acesso restrito, escolhendo uma hipótese legal e salvando as configurações.

Parâmetros:
tipo_processo (str): O tipo de processo a ser iniciado, identificado pelo texto do link.
"""
link_tipo_processo = self.find_element(By.LINK_TEXT, tipo_processo)
link_tipo_processo.click()

time.sleep(1)

nivel_acesso_restrito = self.find_element(By.ID, "divOptRestrito")
nivel_acesso_restrito.click()

time.sleep(1)

hipotese_legal = Select(self.find_element(By.ID, 'selHipoteseLegal'))
hipotese_legal.select_by_visible_text("Documento Preparatório(Art. 7Âs, , Â§ 3Âs, , da Lei nÂs,12.527/2011)")

time.sleep(1)

salvar = self.find_element(By.ID, "btnSalvar")
salvar.click()

def criar_processo(self):
"""
Inicia o processo de criação de um novo processo no sistema SEI.
Este método utiliza o Selenium WebDriver para encontrar e clicar no link que inicia o processo de escolha do tipo de procedimento.
"""
link_iniciar_processo = self.find_element(By.CSS_SELECTOR, "a[link='procedimento_escolher_tipo']")
link_iniciar_processo.click()

def incluir_documento(self):
"""
Inicia o processo de inclusão de um novo documento no sistema SEI.
Este método utiliza o Selenium WebDriver para alternar para o frame de visualização, encontrar e clicar no link que inicia o processo de escolha do tipo de documento.
"""
self.switch_to.default_content()
self.switch_to.frame("ifrVisualizacao")
incluir_documento = self.find_element(By.CSS_SELECTOR, "a[href*='documento_escolher_tipo']")
incluir_documento.click()

def tela_gerar_documento (self, tipo_documento):
"""
Navega para a tela de escolha do tipo de documento a ser gerado no sistema SEI.
Este método utiliza o Selenium WebDriver para interagir com a interface do usuário, selecionando o tipo de documento desejado identificado pelo texto do link.

Parâmetros:
tipo_documento (str): O tipo de documento a ser gerado, identificado pelo texto do link.
"""
link_escolha_tipo_documento = self.find_element(By.LINK_TEXT, tipo_documento)
link_escolha_tipo_documento.click()

def tela_registrar_documento_externo(self, tipo_documento, nome_na_arvore, arquivo):
"""
Registra um documento externo no sistema SEI.
Este método utiliza o Selenium WebDriver para interagir com a interface do usuário, preenchendo informações como tipo de documento, data de elaboração, nome na árvore, formato (nato digital), nível de acesso restrito, hipótese legal e anexando um arquivo.

Parâmetros:
tipo_documento (str): O tipo de documento a ser registrado, identificado pelo texto visível na opção.
nome_na_arvore (str): O nome a ser exibido na árvore de documentos.
arquivo (str): O caminho do arquivo a ser anexado.
"""
select_tipo_documento = Select(self.find_element(By.ID, 'selSerie'))
select_tipo_documento.select_by_visible_text(tipo_documento)

time.sleep(1)

data_documento = self.find_element(By.ID, "txtDataElaboracao")
data_documento.send_keys(datetime.datetime.now().strftime("%d/%m/%Y"))

time.sleep(1)

input_nome_na_arvore = self.find_element(By.ID, "txtNomeArvore")
input_nome_na_arvore.send_keys(nome_na_arvore)

time.sleep(1)

div_formato_nato_digital = self.find_element(By.ID, "divOptNato")
div_formato_nato_digital.click()

time.sleep(1)

div_nivel_acesso_restrito = self.find_element(By.ID, "divOptRestrito")
div_nivel_acesso_restrito.click()

time.sleep(1)

select_hipotese_legal = Select(self.find_element(By.ID, 'selHipoteseLegal'))
select_hipotese_legal.select_by_visible_text("Documento Preparatório(Art. 7Âs, , Â§ 3Âs, , da Lei nÂs, 12.527/2011)")

time.sleep(1)

input_anexar_arquivo = self.find_element(By.ID, "filArquivo")
input_anexar_arquivo.send_keys(arquivo)

time.sleep(1)

button_salvar = self.find_element(By.ID, "btnSalvar")
button_salvar.click()

def incluir_oficio(self):
"""
Inclui um ofício no sistema SEI.
Este método utiliza métodos previamente definidos para incluir um documento, gerar um documento do tipo "Ofício", preencher informações específicas como número do documento base, número, nível de acesso restrito, hipótese legal, e, finalmente, salvar o ofício.
O método também realiza a manipulação da janela, fechando a janela recém-aberta.
Nota: Este método assume que os métodos `incluir_documento` e `tela_gerar_documento` foram implementados anteriormente na classe.
"""
self.incluir_documento()
self.tela_gerar_documento("Ofício")

time.sleep(1)

rb_documento_modelo = self.find_element(By.ID, "divOptProtocoloDocumentoTextoBase")
rb_documento_modelo.click()

time.sleep(1)

text_documento_base = self.find_element(By.ID, "txtProtocoloDocumentoTextoBase")
text_documento_base.send_keys("0029736")

time.sleep(1)

label_numero = self.find_element(By.ID, "txtNumero")
label_numero.send_keys("02")

time.sleep(1)

nivel_acesso_restrito = self.find_element(By.ID, "divOptRestrito")
nivel_acesso_restrito.click()

time.sleep(1)

hipotese_legal = Select(self.find_element(By.ID, 'selHipoteseLegal'))
hipotese_legal.select_by_visible_text("Documento Preparatório (Art.7Âs, , Â§ 3Âs, ,da Lei nÂs,12.527/2011)")

time.sleep(1)

salvar = self.find_element(By.ID, "btnSalvar")
salvar.click()

time.sleep(2)

janela_original = self.current_window_handle

self.switch_to.window(self.window_handles[-1])
self.close()
self.switch_to.window(janela_original)

def executa_procedimento(self, sentenca_perdimento, transito_julgado):
"""
Executa um procedimento espec í fico no sistema SEI.
Este método encapsula uma sequência específica de ações para criar um processo, iniciar um processo de "Gestão da Qualidade: Elaboração e Controle de Documentos", incluir documentos externos do tipo "Anexo" com os nomes "SENTENÇA DE PERDIMENTO" e "TRANSITO EM JULGADO", e finalmente, incluir um ofício.

Parâmetros:
sentenca_perdimento (str): O caminho do arquivo para a sentença de perdimento.
transito_julgado (str): O caminho do arquivo para o trânsito em julgado.
"""
self.criar_processo()

tipo_processo = "Gestão da Qualidade: Elaboração e Controle de Documentos"
self.tela_iniciar_processo(tipo_processo)

self.incluir_documento()

tipo_documento = "Externo"
self.tela_gerar_documento(tipo_documento)

tipo_documento = "Anexo"
nome_na_arvore = "SENTENÇA DE PERDIMENTO"
self.tela_registrar_documento_externo(tipo_documento, nome_na_arvore, sentenca_perdimento)

self.incluir_documento()

tipo_documento = "Externo"
self.tela_gerar_documento(tipo_documento)

tipo_documento = "Anexo"
nome_na_arvore = "TRANSITO EM JULGADO"
self.tela_registrar_documento_externo(tipo_documento, nome_na_arvore, transito_julgado)

time.sleep(1)

self.incluir_oficio()
