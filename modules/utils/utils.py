###########################
# файл: utils.py
# version: 0.1.17
###########################

import json
import random
from modules.data.data import comands

def get_token(name):
    #with open('D:/token/tokens.json') as f:
    with open('./token/tokens.json') as f:
        token_json = json.load(f)
    return token_json[name]

def get_answer(el):
    answer = f'{random.choice(el["out"])} {el.get("content")}'
    return answer

