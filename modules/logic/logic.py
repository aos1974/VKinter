###########################
# файл: logic.py
# version: 0.1.1
###########################

# класс "Бизнес логики" для взаимодействия API бота и базой даных
from modules.db.databases import DataBase
from modules.db.dataclasses import VK_ID_NOTDEFINED, VKUserData


class Logic(object):
    
    # указатель на объект базы данных (создается за пределами класса логики)
    db : DataBase
    
    # функция инициализации класса
    def __init__(self, db : DataBase):
        self.db = db
    # end __init__()

    # функция обновления информации о пользователе начавшем диалог с ВКБотом
    def new_vk_user(self, vk_user : VKUserData) -> bool:
        # проверка на "чистого" пользователя или некорректные данные в ключевом поле
        if vk_user.vk_id == VK_ID_NOTDEFINED:
            return False
        # создаем или обновляем (если существует) данные о пользователе
        if not self.db.new_vkuser(vk_user):
            return False
        return True
    # end new_vk_user
    
    # Следующий обрабатываемый пользователь
    def get_next_user(self, user_id):
        position = self.db.move_offset(user_id, 1)
        id = self.db.get_user(user_id, position)
        return id

    # Предыдущий обрабатываемый пользователь
    def get_previous_user(self, user_id):
        position = self.db.move_offset(user_id, -1)
        id = self.db.get_user(user_id, position)
        return id

    # Текущий обрабатываемый пользователь
    def get_current_user(self, user_id):
        position = self.db.move_offset(user_id, 0)
        id = self.db.get_user(user_id, position)
        return id

    # получить список избранных контактов
    def get_favorites(self, vk_id : int) -> list:
        pass
        favorites = [1000, 1001]
        return favorites
