from json import dump
from os import getcwd
from os.path import isfile
from ast import literal_eval

TITULO = 'WHATSAPP RECEPTIVO'
ARQ_CONFIG = getcwd() + '\\config.json'

class Config:
    def __init__(self):
        def lerConfig():
            with open(ARQ_CONFIG, 'r', encoding='utf-8', errors='ignore') as arq: 
                return literal_eval(arq.read())            
        
        if(isfile(ARQ_CONFIG)): 
            self.config = lerConfig()
        else: 
            self.config = {'usuarioB2w': 'contato@rbcglobalbusiness.com', 'senhaB2w': 'Ppswz67@',
                           'textoPadrao': 'Olá Sr. {}, esperamos que esteja bem!\nSou a Stéphany da RBC Global Business, Para atender com maior agilidade peço que envie uma mensagem de WhatsApp para (11) 97070-1502 .\nAguardo retorno.\nAtenciosamente, RBC Global Business', 'CAMINHO_EXTRACAO': '/tmp/respostas'}
            self.gravarConfig()
        
    def gravarConfig(self, avisar=False):
        try:
            with open(ARQ_CONFIG, 'w') as arq:
                dump(self.config, arq)
                if(avisar): print('GRAVADO AS CONFIGURACOES COM SUCESSO')
        except Exception as erro: print(f'ERRO ENCONTRADO <b>{erro}</b>')                