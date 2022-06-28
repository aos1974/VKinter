import json

def get_token(name):
    with open('D:/token/tokens.json') as f:
    #with open('C:/Users/a.sysoev.OEVRZ/Documents/Python/Netology/VKinder/tokens.json') as f:
        token_json = json.load(f)
    return token_json[name]
