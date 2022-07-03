###########################
# файл: utils.py
# version: 0.1.18
###########################
import os
import json
import random
from modules.data.data import comands

TOKEN_FILE = './token/tokens.json'

def get_token(name):
    # проверяем наличие файла с токеном
    if os.path.isfile(TOKEN_FILE):
        with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
            token_json = json.load(f)
        return token_json[name]
    else:
        # если файл с токеном не найден
        print('TOKEN NOT FOUNT IN PATH: ' + TOKEN_FILE )
        return None

def get_answer(el):
    answer = f'{random.choice(el["out"])} {el.get("content")}'
    return answer

