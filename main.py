###########################
# файл: main.py
# version: 0.1.10
###########################

import json
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from modules.API.ClassVK import ClassVK
from modules.LOGIC.logic import Logic
from modules.data.data import settings, API_VERSION, GROUP_ID, CALLBACK_TYPES
from modules.db.databases import DataBase
from modules.keyboard.keyboard import ClassKeyboard
from modules.utils import utils

def run_comand(comand, user_id):
    content = ''
    key = comand.get('key')
    if key != 'none':
        print(f'Запустить команду {key}')
        if key == 'next':
            [comand['attachment'], content] = logic.get_next_user(user_id)
        elif key == 'previous':
            [comand['attachment'], content] = logic.get_previous_user(user_id)
        elif key == 'search':
            [comand['attachment'], content] = logic.get_next_user(user_id)
        elif key == 'age_from':
            pass
        elif key == 'age_to':
            pass
        elif key == 'black_list':
            for l in db.get_black_list(user_id):
                content += f'\n {l}'
        elif key == 'favorites':
            for l in db.get_favorites(user_id):
                content += f'\n {l}'
    comand['content'] = content
    return comand

# Инициализация
vk_session = VkApi(token=utils.get_token('VKinder'), api_version=API_VERSION)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
myApi = ClassVK(utils.get_token('VKinder'))
db = DataBase(utils.get_token('db_connection'))
logic = Logic(db, myApi)
print(f"Бот запущен")

# Основной цикл
for event in longpoll.listen():
    user_id = logic.get_user_id(event)
    if user_id:
        logic.get_settings(user_id)
        # pprint(settings)
        if event.type == VkBotEventType.MESSAGE_NEW:
            # Если пришло новое сообщение
            if event.obj.message['text'] != '':
                if event.from_user:
                    comand = utils.get_comand(event.obj.message['text'])
                    comand = run_comand(comand=comand, user_id=event.object.user_id)
                    vk.messages.send(
                        user_id=user_id,
                        attachment=comand.get('attachment'),
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        keyboard=ClassKeyboard.get_keyboard(comand['keyboard']).get_keyboard(),
                        message=utils.get_answer(comand))
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            #Пришло событие от кнопки
            if event.object.payload.get('type') in CALLBACK_TYPES:
                if event.object.payload.get('type') == 'show_snackbar':
                    if  'черный' in event.object.payload.get('text'):
                        print('add_black_list')
                        db.new_black_id(event.object.user_id, logic.get_current_user(event.object.user_id))
                        pass
                    elif 'избранное' in event.object.payload.get('text'):
                        print('add_favorites')
                        db.new_favorite(event.object.user_id, logic.get_current_user(event.object.user_id))
                        pass
                r = vk.messages.sendMessageEventAnswer(
                    event_id=event.object.event_id,
                    user_id=user_id,
                    peer_id=event.object.peer_id,
                    event_data=json.dumps(event.object.payload))
            else:
                #Кастомный тип
                comand = utils.get_comand(event.object.payload.get('type'))
                comand = run_comand(comand=comand, user_id=event.object.user_id)
                print(comand.get('attachment'))
                vk.messages.send(
                    user_id=user_id,
                    attachment=comand.get('attachment'),
                    random_id=get_random_id(),
                    peer_id=event.object.peer_id,
                    keyboard=ClassKeyboard.get_keyboard(comand['keyboard']).get_keyboard(),
                    message=utils.get_answer(comand))
        logic.upd_settings(user_id)

if __name__ == '__main__':
    print("test")