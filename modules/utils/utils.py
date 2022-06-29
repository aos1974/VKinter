import json
import random
from modules.data.data import comands

def get_token(name):
    #with open('C:/Users/a.sysoev.OEVRZ/Documents/Python/Netology/VKinder/tokens.json') as f:
    with open('D:/token/tokens.json') as f:
        token_json = json.load(f)
    return token_json[name]

def get_answer(el):
    answer = f'{random.choice(el["out"])} {el.get("content")}'
    return answer

def get_comand(request):
    request = request.lower()
    c = 'none'
    for c in comands:
        el = comands[c]
        if request in el.get('in') or request == c:
            break
    comand = comands[c]
    return comand
