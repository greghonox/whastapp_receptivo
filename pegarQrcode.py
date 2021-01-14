from requests import get
from PIL import Image

class PegarQrcode:
    def __init__(self, caminho):
        self.caminho = caminho
        url = "https://screenshotapi.net/api/v1/screenshot?url=https%3A%2F%2Fweb.whatsapp.com%2F&output=image"
        print(f'ENTRANDO NA PAGINA {url}')
        self.salvarImgTmp(url)
        self.recortarImagem()
    
    def salvarImgTmp(self, url):
        try:
            with open(self.caminho, 'wb') as arq:  arq.write(get(url).content)
            print('SALVANDO IMG NO DISCO RIGIDO')
        except Exception as erro: print(f'ERRO EM SALVAR A IMAGEM {erro}')
        
    def recortarImagem(self):
        try:
            img = Image.open(self.caminho).crop((972, 193, 1234, 460))
            img.save(self.caminho)
            print(f'CONVERTIDO A IMAGEM COM SUCESSO {self.caminho}')
        except Exception as erro: print(f'ERRO EM ABRIR A IMAGEM PARA RECORTAR {erro}')
        
PegarQrcode(r'C:\Users\Plus-TI\Desktop\processos\img.png')