###########################
# файл: logic.py
# version: 0.1.11
###########################
from modules.db.databases import DataBase
from vk_api.bot_longpoll import VkBotEventType
from modules.db.dataclasses import VK_ID_NOTDEFINED, VKUserData

class Logic(object):

    # функция инициализации класса
    def __init__(self, db: DataBase, api):
        self.db = db
        self.api = api
        self.vkUser = VKUserData()
    # end __init__()

    # функция обновления информации о пользователе начавшем диалог с ВКБотом
    # функция вызывается ВКБотом при начале диалога пользователя
    # возвращае True, если данные сохранены, иначе False
    def new_vk_user(self, vk_user: VKUserData) -> bool:
        # проверка на "чистого" пользователя или некорректные данные в ключевом поле
        if vk_user.vk_id == VK_ID_NOTDEFINED:
            return False
        # создаем или обновляем (если существует) данные о пользователе
        if not self.db.new_vkuser(vk_user):
            return False
        return True
    # end new_vk_user

    # Получить информацию о пользователе по его id
    # возвращается объект VKUserData или None если нет записей в базе данных
    def get_vk_user(self, vk_id) -> VKUserData:
        # запрашиваем базу данных
        vk_user = self.db.get_vkuser(vk_id)
        # если пользователь записан в базу данных
        if vk_user is not None:
            # считываем дополнительные настройки пользователя из базы данных
            self.db.get_setings(vk_user)
        return vk_user

    def get_list(self, content, _list):
        for l in _list:
            content += f'{self.api.get_user_data(l)[1]}'
        return content
    
    def run_comand(self, comand):
        content = ''
        key = comand.get('key')
        if not key is None and key != 'none':
            print(f'Запустить команду {key}')
            if key == 'next':
                [comand['attachment'], content] = self.get_next_user()
            elif key == 'previous':
                [comand['attachment'], content] = self.get_previous_user()
            elif key == 'search':
                [comand['attachment'], content] = self.get_next_user()
            elif key == 'black_list':
                content = self.get_list(content, self.db.get_black_list(self.vkUser.vk_id))
            elif key == 'favorites':
                content = self.get_list(content, self.db.get_black_list(self.vkUser.vk_id))
        comand['content'] = content
        return comand

    def update_search_list(self):
        count = 10 #Размер пакета данных
        position = self.vkUser.settings.get('srch_offset')
        offset = position + 1
        list = self.api.search(self.vkUser, offset, count)
        self.db.insert_last_search(self.vkUser.vk_id, list, position)

    def get_user(self, user_id):
        print(self.vkUser.settings['srch_offset'])
        user = self.db.get_user(user_id, self.vkUser.settings['srch_offset'])
        if user is None:
            self.update_search_list()
            user = self.db.get_user(user_id, self.vkUser.settings['srch_offset'])
        print(self.vkUser.settings['srch_offset'])
        if user is None:
            return None
        else:
            return user[0]

    #Следующий обрабатываемый пользователь
    def get_next_user(self):
        self.vkUser.settings['srch_offset'] += 1

        id = self.get_user(self.vkUser.vk_id)

        if id is None:
            return self.get_next_user()
        else:
            if  self.db.is_black(self.vkUser.vk_id, id) == True:
                return self.get_next_user()
            else:
                return self.api.get_user_data(id)

    #Предыдущий обрабатываемый пользователь
    def get_previous_user(self):
        self.vkUser.settings['srch_offset'] -= 1
        if self.vkUser.settings.get('srch_offset') > 1:
            id = self.get_user(self.vkUser.vk_id)
            print(id)
            if id is None:
                return self.get_previous_user()
            else:
                if self.db.is_black(self.vkUser.vk_id, id) == True:
                    return self.get_previous_user()
                else:
                    return self.api.get_user_data(id)
        else:
            return [None, "не существует"]

    # функция получения дополнительных настроек пользователя
    def get_settings(self, vk_instance):
        # если параметр это id пользователя
        if type(vk) is int:
            self.vkUser.vk_id = vk_instance
        # если параметр это объект VKUserData
        elif type(vk) is VKUserData:
            self.vkUser.copy(vk_instance)
        self.get_setings_smart(self.vkUser)
    # end get_settings

    def upd_settings(self):
        self.db.upd_setings(self.vkUser)

    @staticmethod
    def get_user_id(event):
        if  event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.obj.message['from_id']
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            user_id = event.object.user_id
        elif event.type == VkBotEventType.MESSAGE_REPLY:
            user_id = None
        else:
            user_id = None
            print(f'ERROR EVENT {event}')
        return user_id

    @staticmethod
    def get_command_text(event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            return event.obj.message['text']
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            return event.object.payload.get('type')
        elif event.type == VkBotEventType.MESSAGE_REPLY:
            return None
        else:
            print(f'ERROR EVENT {event}')
            return None

    # считать дополнительные данные о пользователе из базы данных
    def get_setings_smart(self, vk_user: VKUserData):
        if not self.db.get_setings(vk_user):
            # если запрос к базе данных ничего не вернул
            vk_user.set_default_settings()
            # сохраняем исходные данные в базе данных
            self.db.set_setings(vk_user)