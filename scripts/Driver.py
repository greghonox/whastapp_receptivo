from selenium.webdriver.chrome.options import Options
#from pyvirtualdisplay import Display
from datetime import datetime
from selenium import webdriver
from time import sleep
from os import getcwd

from scripts.Padroes import DateTime
from scripts.Log import log, Log

class Driver:
    def __init__(self, caminho='', tempolimite=60):
        self.print('INICIANDO SCRIPT AGENTE DE RECEPCAO DE MENSAGEM DO WHASTAPP')
        #self.display = Display(visible=0, size=(3000, 3000))
        #self.definir_virtualDisplay()
        options = Options()

        options.add_argument("--start-maximized")
        #options.add_argument("user-data-dir="+ getcwd() + r'\DirUser')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        options.add_argument('--no-sandbox')        
        options.add_argument('ignore-certificate-erros')
        options.add_experimental_option('prefs',{
        "download.default_directory": caminho,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "plugins.plugins_disabled": ["Chrome PDF Viewer"],
        "plugins.always_open_pdf_externally": True})

        dr = getcwd() + r'\chromedriver.exe'
        self.dr = webdriver.Chrome(options=options, executable_path=dr)

        self.dr.set_script_timeout(tempolimite)
        self.dr.set_page_load_timeout(tempolimite)
        self.dr.implicitly_wait(1) # TEMPO DE INTERACAO COM A PAGINA

    def definir_virtualDisplay(self): self.display.start()

    def iniciliazar_driver(self): return self.dr

    @log
    def fechar_janela(self):
        sleep(5)
        try: 	
            self.dr.close()
            sleep(1)
            self.ir_ultima_janela()
            return "FECHADO A JANELA COM SUCESSO!", True
        except Exception as erro: return f"ERRO EM FECHAR JANELA({erro})", True

    def ir_ultima_janela(self):
        try: self.dr.switch_to_window(self.dr.window_handles[-1])
        except: pass

    @log
    def fechar_aba(self):
        try:
            self.ir_ultima_janela()
            self.dr.close()
            self.ir_ultima_janela()
            return "FECHADO ABA COM SUCESSO!", True   
        except Exception as erro: return f"ERRO EM FECHAR ABA ({erro})", False

    def verifica_quantidade_abas(self):
        try: return len(self.dr.window_handles)
        except: return 1

    def fechar_aba_vazia(self):
        for aba in range(self.verifica_quantidade_abas()):
            try:
                if(self.dr.window_handles[aba]):
                    if(self.dr.title == '' or 'Sem título' in self.dr.title): 
                        self.dr.close()
                        self.ir_ultima_janela()
                sleep(1)
            except Exception as erro: self.print(f"ERRO OCORRIDO EM FECHAR ABA VAZIA ({erro})")
        return "TENTATIVA DE FECHAR ABA VAZIA EXECUTADA!", False

    @log
    def recarregar_pagina(self):
        self.dr.refresh()
        return f"RECARREGANDO A PAGINA {self.dr.current_url}", True

    @log
    def abrir_url_aba(self, link):
        try: 
            self.dr.execute_script(f"window.open('{link}', '_blank')")
            self.ir_ultima_janela()
            return f"ABERTO ABA {link} COM SUCESSO!", True
        except Exception as erro:  return f"ERRO EM ABRIR ABA {link}", False

    @log
    def printscreen_pagina(self, caminho):
        try: 
            self.dr.get_screenshot_as_file(caminho)
            return f"TIRADO O PRINT {caminho} COM SUCESSO!", True
        except Exception as erro: f"ERRO EM TIRAR PRINT SCREEN PAGINA {erro}", False

    @log
    def voltar_pagina(self):
        try: self.dr.back(); return "VOLTANDO A PAGINA!", True
        except Exception as erro: return f"ERRO ENCONTRADO AO VOLTAR A PAGINA {erro}", False

    def pegarDataHora(self):
        return datetime.now().strftime('%d/%m/%y %H:%M:%S')

    @log
    def fechar_driver(self):
        try:self.dr.quit(); return f"FECHADO DRIVER COM SUCESSO", True
        except Exception as erro: return f"ERRO EM FECHAR CHROMEDRIVER {erro}", False

    def pegarDialog(self):
        sleep(5)
        try: return self.dr.switch_to.alert.text, True
        except: return "NAO EXISTE DIALOG", False

    def print(self, msg, *args): 
        msg = DateTime() + msg
        Log(msg, *args)
    
    def saidaErro(self, tipo, ex=''):
        tiposErros = {0: 'ERRO INESPERADO',
                      1: 'PAGINA INDISPONIVEL', 
                      2: 'PAGINA BLOQUEADA', 
                      3: 'SENHA BLOQUEADA',
                      4: 'NÃO FOI POSSIVEL PEGAR ELEMENTO',
                      5: 'ERRO EM PEGAR ELEMENTO DA PAGINA'}
        erro = ' ERRO: ' + str(ex) if(str(ex) != '') else ''
        self.print(tiposErros[tipo] + erro)
        
    def __del__(self):
        self.dr.close()
        self.dr.quit()
        #self.display.stop()
        self.print("FINALIZANDO O DISPLAY E CHROMEDRIVER")
        self.print('='*100)        