###########################
# файл: main.py
# version: 0.1.11
###########################

import json
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from modules.API.ClassVK import ClassVK
from modules.logic.logic import Logic
from modules.data.data import API_VERSION, GROUP_ID, CALLBACK_TYPES
from modules.db.databases import DataBase
from modules.db.dataclasses import VKUserData
from modules.keyboard.keyboard import ClassKeyboard
from modules.utils import utils

# Инициализация
vk_session = VkApi(token=utils.get_token('VKinder'), api_version=API_VERSION)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
myApi = ClassVK(utils.get_token('access_token'))
db = DataBase(utils.get_token('db_connection'))
logic = Logic(db, myApi)
print(f"Бот запущен")

# Основной цикл
for event in longpoll.listen():
    user_id = logic.get_user_id(event)
    # = aos ==============================
    vk_user = VKUserData(myApi.get_info(user_id))
    logic.new_vk_user(vk_user)
    # = aos ==============================
    if user_id:
        logic.get_settings(vk_user)
        comand = logic.run_comand(comand=utils.get_comand(logic.get_command_text(event)))
        if event.type == VkBotEventType.MESSAGE_NEW:
            # Если пришло новое сообщение
            if event.obj.message['text'] != '':
                if event.from_user:
                    vk.messages.send(
                        user_id=user_id,
                        attachment=comand.get('attachment'),
                        random_id=get_random_id(),
                        peer_id=event.obj.message['from_id'],
                        keyboard=ClassKeyboard.get_keyboard(comand['keyboard']),
                        message=utils.get_answer(comand))
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            # Пришло событие от кнопки
            if event.object.payload.get('type') in CALLBACK_TYPES:
                if event.object.payload.get('type') == 'show_snackbar':
                    if 'черный' in event.object.payload.get('text'):
                        db.new_black_id(event.object.user_id, logic.get_user(user_id))
                    elif 'избранное' in event.object.payload.get('text'):
                        db.new_favorite(event.object.user_id, logic.get_user(user_id))
                r = vk.messages.sendMessageEventAnswer(
                    event_id=event.object.event_id,
                    user_id=user_id,
                    peer_id=event.object.peer_id,
                    event_data=json.dumps(event.object.payload))
            else:
                print(comand.get('attachment'))
                vk.messages.send(
                    user_id=user_id,
                    attachment=comand.get('attachment'),
                    random_id=get_random_id(),
                    peer_id=event.object.peer_id,
                    keyboard=ClassKeyboard.get_keyboard(comand['keyboard']),
                    message=utils.get_answer(comand))
        logic.upd_settings()

if __name__ == '__main__':
    print("test")
