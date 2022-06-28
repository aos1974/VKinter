###########################
# файл: logic.py
# version: 0.1.8
###########################

from pprint import pprint
from modules.db.databases import DataBase
from vk_api.bot_longpoll import VkBotEventType
from modules.db.dataclasses import OFFSET_NOTDEFINED, VK_ID_NOTDEFINED, VKUserData

class Logic(object):

    # функция инициализации класса
    def __init__(self, db: DataBase, api):
        self.db = db
        self.api = api
        self.position = 0
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
    # end get_vk_user()

    def update_search_list(self, user_id):
        count = 5 #Размер пакета данных
        offset = self.position + 1
        position = self.position
        list = self.api.search(user_id, offset, count)
        self.db.insert_last_search(user_id, list, position)

    def get_user(self, user_id):
        user = self.db.get_user(user_id, self.position)
        if user is None:
            self.update_search_list(user_id)
            user = self.db.get_user(user_id, self.position)
        return user[0]

    #Следующий обрабатываемый пользователь
    def get_next_user(self, user_id):
        self.position += 1
        return self.api.get_user_data(self.get_user(user_id))

    #Предыдущий обрабатываемый пользователь
    def get_previous_user(self, user_id):
        self.position += -1
        return self.api.get_user_data(self.get_user(user_id))

    #Текущий обрабатываемый пользователь
    def get_current_user(self, user_id):
        return self.api.get_user_data(self.get_user(user_id))

    #получить список избранных контактов
    def get_favorites(self, vk_id : int) -> list:
        pass
        favorites = [1000, 1001]
        return favorites

    def get_settings(self, user_id: int):
        vkUser = VKUserData(self.api.get_info(user_id))
        self.position = self.db.get_setings_smart(vkUser).settings['srch_offset']

    def set_settings(self, user_id: int):
        self.db.set_setings(user_id=user_id,srch_offset=self.position)

    def upd_settings(self, user_id: int):
        self.db.upd_setings(user_id=user_id, srch_offset=self.position)

    def get_user_id(self, event):
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
