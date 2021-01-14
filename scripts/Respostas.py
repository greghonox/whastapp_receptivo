from random import randint
from datetime import datetime

from scripts.Selenium.Bot import *

class Respostas:
    def __init__(self):
        print('GERANDO RESPOSTA AUTOMATICA')
        horarios = {}

        for i in range(7): horarios[i] = 'madrugada'
        for i in range(7, 13): horarios[i] = 'manha'
        for i in range(13, 19): horarios[i] = 'tarde'
        for i in range(19, 24): horarios[i] = 'noite'
        
        mensagens_comuns = ['Oi,', 'Ola', 'Tudo bem?', 'Como vai?', 'Eai tudo certo?', f'Seja bem vindo(a) ao {TITULO}, eu sou {BOT}. ']
        corpo_saudacoes = {'madrugada': mensagens_comuns + ['Boa noite', 'Boa madruga', 'Excelente noite', 'Excenlente madrugada'],
                        'manha': mensagens_comuns + ['Boa dia', 'Boa manhã', 'Excelente dia', 'Excenlente manhã'],
                        'tarde': mensagens_comuns + ['Boa tarde', 'Excelente tarde'],
                        'noite': mensagens_comuns + ['Boa noite', 'Excelente noite']}
        
        self.mensagens_saudacoes = {}
        for horario in horarios: self.mensagens_saudacoes[horario] = corpo_saudacoes[horarios[horario]]
        d = datetime.now().hour
        mas = len(self.mensagens_saudacoes[d])
        self.mensagem = self.mensagens_saudacoes[d][randint(0, mas) - 1]
    