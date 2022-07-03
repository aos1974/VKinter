###########################
# файл: main.py
# version: 0.1.18
###########################

import json
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from modules.API.ClassVK import ClassVK
from modules.logic.logic import Logic
from modules.data.data import API_VERSION, GROUP_ID, CALLBACK_TYPES
from modules.db.databases import DataBase
from modules.keyboard.keyboard import ClassKeyboard
from modules.utils import utils

# основаная функция программы
def main():
    # загружаем токен для инициализации API
    token = utils.get_token('VKinder')
    # если токен не удалось загрузить бот не стартует
    if token == None:
        print('Инициализация бота невозможна!')
        return False
    # Инициализация объектов
    vk_session = VkApi(token=token, api_version=API_VERSION)
    vk = vk_session.get_api()
    try:
        longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
    except Exception as err:
        # обработка ошибки инициализации обработчика событий Бота
        print('Ошибка инициализации API VK')
        print(err)
        return False
    logic = Logic(DataBase(utils.get_token('db_connection')), ClassVK(utils.get_token('access_token')))
    print(f"Бот запущен")

    # Основной цикл обработки событий 
    for event in longpoll.listen():
        user_id = logic.get_user_id(event)
        if user_id:
            logic.new_vk_user(user_id) #Инициализируем пользователя
            comand = logic.run_comand(comand=logic.get_comand(event))
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
                            logic.add_black_list(event.object.user_id)

                        elif 'избранное' in event.object.payload.get('text'):
                            logic.add_favorite_list(event.object.user_id)

                    vk.messages.sendMessageEventAnswer(
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
            else:
                continue
            logic.upd_settings()
# end main()

if __name__ == '__main__':
    main()

