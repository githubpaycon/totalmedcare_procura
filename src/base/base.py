from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager
from funcsforspo_l.fpython.functions_for_py import *
from funcsforspo_l.fselenium.functions_selenium import *
from funcsforspo_l.fregex.functions_re import *
import pandas as pd
import json
import os
import streamlit as st

# -- GLOBAL -- #
URL_SUPORTE = f'https://api.whatsapp.com/send?phone=5511985640273'
CONFIG_PATH = arquivo_com_caminho_absoluto('bin', 'config.json')
BASE = os.path.abspath('base')
# -- GLOBAL -- #

class Bot:    
    def __init__(self, headless, download_files) -> None:
        # --- CHROME OPTIONS --- #
        self._options = ChromeOptions()
        self.DOWNLOAD_DIR =  cria_dir_no_dir_de_trabalho_atual(dir='downloads', print_value=False, criar_diretorio=True)
        limpa_diretorio(self.DOWNLOAD_DIR)

        if download_files:
            # --- PATH BASE DIR --- #
            self._SETTINGS_SAVE_AS_PDF = {
                        "recentDestinations": [
                            {
                                "id": "Save as PDF",
                                "origin": "local",
                                "account": ""
                            }
                        ],
                        "selectedDestinationId": "Save as PDF",
                        "version": 2,
                    }


            self._PROFILE = {'printing.print_preview_sticky_settings.appState': json.dumps(self._SETTINGS_SAVE_AS_PDF),
                    "savefile.default_directory":  f"{self.DOWNLOAD_DIR}",
                    "download.default_directory":  f"{self.DOWNLOAD_DIR}",
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "profile.managed_default_content_settings.images": 2,
                    "safebrowsing.enabled": True}
                
            self._options.add_experimental_option('prefs', self._PROFILE)
        
        if headless == True:
            self._options.add_argument('--headless')
            
        self._options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        self._options.add_experimental_option('useAutomationExtension', False)
        self.user_agent = cria_user_agent()
        self._options.add_argument(f"--user-agent=self.user_agent")
        self._options.add_argument("--disable-web-security")
        self._options.add_argument("--allow-running-insecure-content")
        self._options.add_argument("--disable-extensions")
        self._options.add_argument("--start-maximized")
        self._options.add_argument("--no-sandbox")
        self._options.add_argument("--disable-setuid-sandbox")
        self._options.add_argument("--disable-infobars")
        self._options.add_argument("--disable-webgl")
        self._options.add_argument("--disable-popup-blocking")
        self._options.add_argument('--disable-gpu')
        self._options.add_argument('--disable-software-rasterizer')
        self._options.add_argument('--no-proxy-server')
        self._options.add_argument("--proxy-server='direct://'")
        self._options.add_argument('--proxy-bypass-list=*')
        self._options.add_argument('--disable-dev-shm-usage')
        self._options.add_argument('--block-new-web-contents')
        self._options.add_argument('--incognito')
        self._options.add_argument('–disable-notifications')
        self._options.add_argument("--window-size=1920,1080")
        
        self.__service = Service(ChromeDriverManager().install())
        
        # create DRIVER
        self.DRIVER = Chrome(service=self.__service, options=self._options)
        
        def enable_download_in_headless_chrome(driver, download_dir):
            '''
            Esse código adiciona suporte ao navegador Chrome sem interface gráfica (headless) no Selenium WebDriver para permitir o download automático de arquivos em um diretório especificado.

            Mais especificamente, o código adiciona um comando ausente "send_command" ao executor de comando do driver e, em seguida, executa um comando "Page.setDownloadBehavior" para permitir o download automático de arquivos no diretório especificado.

            O primeiro passo é necessário porque o suporte para o comando "send_command" não está incluído no Selenium WebDriver por padrão. O segundo passo usa o comando "Page.setDownloadBehavior" do Chrome DevTools Protocol para permitir o download automático de arquivos em um diretório especificado.

            Em resumo, o código adiciona suporte para o download automático de arquivos em um diretório especificado no Chrome sem interface gráfica usando o Selenium WebDriver.
            '''
            driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

            params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
            command_result = driver.execute("send_command", params)
        enable_download_in_headless_chrome(self.DRIVER, self.DOWNLOAD_DIR)
        
        
        self.WDW3 = WebDriverWait(self.DRIVER, timeout=3)
        self.WDW5 = WebDriverWait(self.DRIVER, timeout=5)
        self.WDW7 = WebDriverWait(self.DRIVER, timeout=7)
        self.WDW10 = WebDriverWait(self.DRIVER, timeout=10)
        self.WDW30 = WebDriverWait(self.DRIVER, timeout=30)
        self.WDW = self.WDW7

        self.DRIVER.maximize_window()
        return self.DRIVER

def faz_log_st(msg):
    st.text(msg)
    faz_log(str(msg))