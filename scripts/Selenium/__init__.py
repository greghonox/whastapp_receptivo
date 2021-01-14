from scripts.Config import *
from scripts.Respostas import *
from scripts.Log import log, Log
from scripts.Driver import Driver
from scripts.Selenium.Bot import *

from PIL import Image
from json import dump
from time import sleep
from csv import reader
from shutil import move
from re import split, sub
from ast import literal_eval
from datetime import datetime
from os.path import isfile, isdir
from os import getcwd, makedirs
from re import search, findall, IGNORECASE
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


TENTATIVAS_ACESSAR_ELEMENTO = 10
PATH_SCRIPT = getcwd()
CAMINHO_DOWNLOADS = PATH_SCRIPT + r'\downloads'
CAMINHO_QRCODE = PATH_SCRIPT + r'\img.png'
CONVERSAS = PATH_SCRIPT + r'\conversas'
LOG =  PATH_SCRIPT + r'\log.txt'
CSV = PATH_SCRIPT + r'\log.csv'

__version__ = '1.0'