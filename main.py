from scripts.Selenium import *

class Recptivo(Driver):
    def __init__(self):
        self.caminho_qrcode = CAMINHO_QRCODE
        #if(not self.carregarCsv()): return
        super().__init__(CAMINHO_DOWNLOADS)
        
        self.dr.get('https://web.whatsapp.com/')
        self.verifica_entrada()
        self.ouvirConversas()
        
    def carregarCsv(self):
        try: 
            self.csv = {}
            with open(CSV, encoding='utf-8', errors='ignore') as csv: 
                for x in [x for x in reader(csv, delimiter=';')]: self.csv[x[0]] = x[1:]
                return True
        except Exception as erro: self.print(f'ERRO EM CARREGAR A LISTA DE CLIENTES(CSV) {erro}'); return False

    def verifica_entrada(self):
        """ AGUARDA A LEITURA DO QR CODE """
        contagem = 0
        while True:
          try:
              print(f"AGUARDANDO LEITURA DO QR CODE {contagem}                                                    ")
              contagem += 1
              if('Mantenha seu celular conectado' in self.dr.find_element_by_class_name("_27KDP").text): return True
          except Exception as erro: pass
          sleep(1)        
          self.gravarQrCode()

    def gravarQrCode(self):
        try:
            self.dr.save_screenshot(self.caminho_qrcode)
            img = Image.open(self.caminho_qrcode).crop((570, 191, 834, 454))
            img.save(self.caminho_qrcode)
            print(f'CONVERTIDO A IMAGEM COM SUCESSO {self.caminho_qrcode}')
        except Exception as erro: print(f'ERRO EM ABRIR A IMAGEM PARA RECORTAR {erro}')
        
    def ouvirConversas(self):
        ' METODO PRINCIPAL DE INTERACAO DO CHATBOT '
        contagem = 0
        while True:
            try:
                print(f'[{contagem}] AGUARDANDO SER CHAMADO!', end='\r')
                contagem += 1
                if(self.pegarConversas()): 
                    self.interceptarMensagem(self.pegarMensagem())                            
                    
                if(self.verifica_quantidade_abas() >= 2): 
                    self.fechar_aba()
                self.voltarTopoConversasBarra()
                self.dr.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
                
            except Exception as erro: pass 
            sleep(.5)

    def pegarConversas(self):
        ' APENAS CLICA NOS ICONES VERDES DE CONVERSAS NA TELA (VISIVEL) '
        try: 
            self.dr.find_element_by_id('pane-side').find_elements_by_class_name('VOr2j')[0].click()
            return True            
        except Exception as erro: print(f'\033[31mPAINEL SEM CONVERSAS\033[0;0m                                  ', end='\r'); return False
            
    def pegarMensagem(self):
        ' PEGA A MENSAGEM DA ULTIMA CONVERSA NA TELA '
        try: contato = self.dr.find_element_by_class_name('YEe1t').text.replace(' ', '')
        except Exception as erro: self.print(f'NÃO FOI POSSIVEL PEGAR O CONTATO {erro}')
        
        try: self.tela = self.dr.find_element_by_class_name('_26MUt')
        except Exception as erro: self.print(f'ERRO EM PEGAR A TELA {erro}'); return False        

        try: conversa = self.tela.find_elements_by_class_name('_1dB-m')[-1].text
        except Exception as erro: print(f'ERRO EM PEGAR A CONVERSA {erro}'); conversa = ''

        
        try: hora = self.tela.find_elements_by_class_name('_1dB-m')[-1].find_element_by_class_name('_2JNr-').text
        except Exception as erro: print(f'ERRO EM PEGAR A CONVERSA {erro}', end='\r'); hora = ''
        
        return {'contato': contato, 'conversa': conversa, 'hora':hora}

    def baixarAudioEncaminhada(self): 
        action = ActionChains(self.dr)
        audio = self.tela.find_elements_by_css_selector("div[tabindex='-1']")[-1]
        audio = audio.find_element_by_class_name('_2PKDl').find_elements_by_tag_name('span')[-1]
        action.move_to_element(audio).perform()
        self.dr.find_element_by_css_selector("span[data-icon='down-context']").click()
        self.dr.find_elements_by_css_selector("div[title='Baixar']")[-1].click()
    
    def baixarImagemEncaminhada(self): self.baixarImg()
    
    def baixarArquivoEncaminhada(self): self.baixarArquivo()
    
    def baixarImg(self):
        try: 
            self.verificarPastaExst(CAMINHO_DOWNLOADS)
            self.tela.find_elements_by_class_name('_1mTER')[-1].click()
            self.dr.find_elements_by_css_selector("span[data-testid='download']")[0].click()
            self.dr.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)            
        except Exception as erro: self.print(f'ERRO EM PEGAR IMAGEM {erro}')
        
    def baixarAudio(self):
        try:
            action = ActionChains(self.dr)
            audio = self.tela.find_elements_by_css_selector("div[tabindex='-1']")[-1]
            audio = audio.find_element_by_class_name('_2PKDl').find_elements_by_tag_name('span')[-1]
            action.move_to_element(audio).perform()
            self.tela.find_elements_by_css_selector("div[tabindex='-1']")[-1].find_elements_by_tag_name('span')[-1].click()
            self.dr.find_elements_by_css_selector("div[title='Baixar']")[-1].click()
            return True
        except Exception as erro: self.print(f'ERRO AO BAIXAR AUDIO {erro}'); return False
    
    def baixarArquivo(self): 
        try:
            arquivo = self.tela.find_elements_by_css_selector("div[tabindex='-1']")[-1]
            arquivo.find_element_by_css_selector("span[data-testid='audio-download']").click()
            return True
        except Exception as erro: self.print(f'ERRO AO BAIXAR ARQUIVO {erro}'); return False
        
    def modificarNomeDownload(self, entrada, saida):
        try: move(entrada, saida); self.print(f'MOVENDO {entrada} -> {saida}')
        except Exception as erro: self.print(f'ERRO EM MOVER ARQUIVO {erro}')
        
    def verificarDownload(self):
        '  RETORNAR OBJ, BOOL '
        try:
            self.dr.execute_script("window.open('')")
            self.ir_ultima_janela()
            self.dr.get('chrome://downloads/')
            for _ in range(TENTATIVAS_ACESSAR_ELEMENTO):
                html = self.dr.execute_script("""return document.querySelector('downloads-manager').shadowRoot.getElementById('downloadsList').items;""")
                print(f"ARQUIVO {html[0]['filePath']}")
                if(html[0]['state'] == 'COMPLETE'): 
                    self.print(f'DOWNLOAD DO ARQUIVO, REALIZADA COM SUCESSO')
                    self.fechar_aba()
                    return html[0]['filePath'], True
                sleep(2)                    
            else: self.print(f'ERRO EM REALIZADR DOWNLOAD, NÃO BAIXOU NO TEMPO ESPERADO'); return '', False
            
        except: pass
    
    def interceptarMensagem(self, msg):
        ' PEGA CADA MENSAGEM PARA SEU TRATAMENTO EXPECIFICO '
        data = datetime.now().strftime('%d/%m/%Y ') + msg['hora']
        self.print(f"{data} {msg['contato']}: {msg['conversa']}")
        
        self.agora = self.gerarTimesTamp()
        
        self.arquivo = ''        

        self.contatoMsg = msg['contato']
        self.conversaMsg = msg['conversa'].split('\n')[0]
        # TENTAR BAIXAR MIDIAS
        midia = self.verificarTipoMidia()

        if(midia == 'texto'): 
            self.midia = False; self.gerarLogConversa(); self.voltarTopoConversasBarra(); return True
        tipos = {'audio': self.baixarAudio,'imagem': self.baixarImg,'arquivo': self.baixarArquivo, 
                 'audioEncaminhada': self.baixarAudioEncaminhada, 'imagemEncaminhada': self.baixarImagemEncaminhada, 
                 'arquivoEncaminhada': self.baixarArquivoEncaminhada}
        
        try: tipos[midia]()
        except Exception as erro: self.print(f'ERRO EM INICIAR O DOWNLOAD DA MIDIA {midia}: {erro}'); return False

        html = self.verificarDownload()

        if(html[1]): self.modificarNomeDownload(html[0], CAMINHO_DOWNLOADS + r'\\' + self.agora + self.contatoMsg +'.'+ html[0].split('.')[-1])
        
        self.midia = True
        self.arquivo = CAMINHO_DOWNLOADS + r'\\' + self.agora + self.contatoMsg +'.'+ html[0].split('.')[-1]
        self.gerarLogConversa()
        
        self.voltarTopoConversasBarra()
        
    def verificarTipoMidia(self):
        ' POR MEIO DE UM DICIONARIO ELE VERIFICA QUAL TIPO DE MIDIA DA ULTIMA MENSAGEM '
        txt = self.tela.find_elements_by_css_selector("div[tabindex='-1']")[-1].text

        tipos = {'audio': search('^\d+:\d+\n\d+:\d+$', txt),
                 'imagem': search('^\d+:\d+$', txt),
                 'arquivo': search('^\n\w*\d+\s[k|m]b\n\d\d\:\d\d$', txt, flags=2),
                 'audioEncaminhada': search('^Encaminhada\n\d\:\d\d\n\d\d\:\d\d$', txt),
                 'imagemEncaminhada': search('^Encaminhada\n\d\d\:\d\d$', txt),
                 'arquivoEncaminhada': search('^Encaminhada\n[\w|\d]+\.\w*\n\w*\s[k|m]b\n\d\d:\d\d$', txt, flags=2)}

        for exe in tipos:
            if(tipos[exe]): 
                self.print(f'TIPO DE MENSAGEM: {exe}\n')
                return exe            
        return 'texto'
        
    def voltarTopoConversasBarra(self):
        ' QUANDO O BOT ENCONTRA UMA CONVERSA, DE IMEDIATO ELE JÁ CLICA PARA RESPONDER. ' 
        ' PORÉM SE O USUÁRIO NOVAMENTE PERGUTNAR ELE FICA PRESO NA CONVERSA COM O CONTATO E OS STATUS NAO MUDA. '
        ' BASICAMENTE O BOT TEM QUE RESPONDER A PERGUNTA E SAIR DA CONVERSA PARA NAO FICAR SEM RESPONDER AO CONTATO CHAMDO. '
        sleep(1)
        try: self.dr.find_element_by_css_selector("span[data-testid='pinned']").click(); return True
        except Exception as erro: self.print(f'ERRO EM ACHAR A CONVERSA DE ESCUTA {erro}'); return False        
    
    def responderMensagem(self, msg):
        try:
            self.dr.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]').send_keys(msg) 
            sleep(1)
            self.dr.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]').send_keys(Keys.ENTER)
            return f'ENVIANDO MSG: {msg}'
        except Exception as erro: self.print(f'ERRO ENCONTRADO AO ENVIAR MENSAGEM {erro}')

    def gerarLogConversa(self):
        try:
            self.verificarPastaExst(CONVERSAS)
            json = {'identificador': self.contatoMsg, 'canal': 'whatsapp', 'timestamp': self.agora, 'tipo': '1' if(self.midia) else '0', 'mensagem': self.conversaMsg, 'midia': self.arquivo}
            with open(CONVERSAS + '\\' + self.agora + self.contatoMsg +'.json', 'w', encoding='utf-8', errors='ignore') as arq: dump(json, arq, indent=4, ensure_ascii=False)
        except Exception as erro: self.print(f'ERRO EM ESCREVER ARQUIVO {erro}')
        
    def gerarTimesTamp(self): return datetime.now().strftime('%Y%m%d%S%f')
        
    def verificarPastaExst(self, caminho):
        try: 
            if(not isdir(caminho)): makedirs(caminho); self.print(f'CRIANDO A PASTA {caminho} COM SUCESSO')
        except Exception as erro: self.print(f'ERRO EM CRIAR A PASTA {erro}')
        
Recptivo()