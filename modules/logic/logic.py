###########################
# файл: logic.py
# version: 0.1.7
###########################

# класс "Бизнес логики" для взаимодействия API бота и базой даных
from modules.db.databases import DataBase
from modules.db.dataclasses import OFFSET_NOTDEFINED, VK_ID_NOTDEFINED, VKUserData


class Logic(object):
    
    # указатель на объект базы данных (создается за пределами класса логики)
    db : DataBase
    
    # функция инициализации класса
    def __init__(self, db : DataBase):
        self.db = db
    # end __init__()

    # функция обновления информации о пользователе начавшем диалог с ВКБотом
    # функция вызывается ВКБотом при начале диалога пользователя
    # возвращае True, если данные сохранены, иначе False
    def new_vk_user(self, vk_user : VKUserData) -> bool:
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

    # функция получает следующий id ВКонтакте из списка поискового запроса для ВКБота
    # принимает аргументом vk_id текущего пользователя и возвращает id ВКонтакте для
    # загрузки фотографий и данных профиля из поиска
    def get_next_search_id(self, vk_id : int) -> int:
        # получаем данные о пользователе по его vk_id
        vk_user = self.get_vk_user(vk_id)
        # если информации о таком пользователе нет, возвращаем "-1"
        if vk_user is None:
            return VK_ID_NOTDEFINED
        # если текущая позиция в списке поиска не задана
        if vk_user.settings.get('srch_offset') == OFFSET_NOTDEFINED:
            pass
        
        # заглушка
        next_id = VK_ID_NOTDEFINED
    
        return next_id
    # get_next_search_id()

    def get_next_user(self, user_id : int) -> int:
        position = self.db.move_offset(user_id, 1)
        id = self.db.get_user(user_id, position)
        return id

    def get_current_user(self, user_id):
          position = self.db.move_offset(user_id, 0)
          id = self.db.get_user(user_id, position)
          return id

    # Предыдущий обрабатываемый пользователь
    def get_previous_user(self, user_id):
        position = self.db.move_offset(user_id, -1)
        id = self.db.get_user(user_id, position)
        return id

    # получить список избранных контактов
    def get_favorites(self, vk_id : int) -> list:
        pass
        favorites = [1000, 1001]
        return favorites
