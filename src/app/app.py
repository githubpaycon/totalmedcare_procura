from src.base.base import *
import json
from selenium.webdriver.support.ui import Select

class RobotClass(Bot):
    def __init__(self, cpf, especialidade) -> None:
        self.configs = read_json(CONFIG_PATH)
        self.HEADLESS = True
        self.DOWNLOAD_FILES = False
        self.URL = 'https://redecredenciada-tmc.sdasystems.org/Busca/Cliente.aspx'
        self.CPF = cpf
        self.ESPECIALIDADE = especialidade
        super().__init__(self.HEADLESS, self.DOWNLOAD_FILES)
        self.DRIVER.get(url=self.URL)
        self.DF_TEMPLATE = {
            "NOME DO LOCAL": [],
            "ENDERECO": [],
            'BAIRRO': [],
            'CEP': [],
            'TELEFONES': [],
            'ESPECIALIDADE': [],
        }
        
    def acessa(self):
        # envia o cpf
        espera_elemento_e_envia_send_keys(self.WDW,  pega_somente_numeros(self.CPF), (By.CSS_SELECTOR, 'input[value="Digite seu CPF"]'))
        # clica na opção por especialidade
        espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, 'input[value="Por Especialidade"]'))
        # clica na opção buscar
        espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, 'input[value="Buscar"]'))

    # def extrai_as_especialidades(self):
    #     selects = espera_e_retorna_lista_de_elementos_text(self.WDW, (By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_ddlEspec>option'))
    #     json_lista = json.dumps(selects)
    #     with open('list.json', 'w') as f:
    #         json.dump(json_lista, f)
    
    def preenche_especialidade(self):
        faz_log_st(f'Preenchendo especialidade {self.ESPECIALIDADE}')
        select = espera_elemento(self.WDW, (By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_ddlEspec'))
        select = Select(select)
        select.select_by_visible_text(text=self.ESPECIALIDADE)
        espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, 'input[value="Buscar"]'))

    def extrai_infos(self):
        qtd_extraida = 0
        qtd = espera_e_retorna_elemento_text(self.WDW, (By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_lblReg'))
        while True:
            if qtd == qtd_extraida:
                self.DRIVER.close()
                return self.DF_TEMPLATE
            registros = espera_e_retorna_lista_de_elementos(self.WDW10, (By.CSS_SELECTOR, '#PainelCredenciados>span>span .BlocoResultado'))
            for i, registro in enumerate(registros):
                faz_log_st(f'Recuperando registro {i} de {qtd}')
                nome_local = registro.find_element(By.CSS_SELECTOR, '.LabelTitulo').text
                endereco = registro.find_element(By.CSS_SELECTOR, 'span[id*="lblEnd"]').text
                bairro = registro.find_element(By.CSS_SELECTOR, 'span[id*="lblBairro"]').text
                cep = registro.find_element(By.CSS_SELECTOR, 'span[id*="lblCEP"]').text
                telefones = registro.find_element(By.CSS_SELECTOR, 'span[id*="lbltelefones"]').text.replace('(11) ', '').replace(' ', '')

                self.DF_TEMPLATE['NOME DO LOCAL'].append(nome_local)
                self.DF_TEMPLATE['ENDERECO'].append(endereco)
                self.DF_TEMPLATE['BAIRRO'].append(bairro)
                self.DF_TEMPLATE['CEP'].append(cep)
                self.DF_TEMPLATE['TELEFONES'].append(telefones)
                self.DF_TEMPLATE['ESPECIALIDADE'].append(self.ESPECIALIDADE)

            else:
                try:
                    espera_elemento_disponivel_e_clica(self.WDW3, (By.CSS_SELECTOR, '#ctl00_ContentPlaceHolder1_cmdNext'))
                except:
                    self.DRIVER.close()
                    return self.DF_TEMPLATE
        
        