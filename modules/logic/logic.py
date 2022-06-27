###########################
# файл: logic.py
# version: 0.1.1
###########################

# класс "Бизнес логики" для взаимодействия API бота и базой даных
class Logic(object):
    # функция инициализации класса
    def __init__(self, db):
        self.db = db
    # end __init__()

    # функция обновления информации о пользователе начавшем диалог с ВКБотом
    def new_vk_user(self, vk_dict : dict) -> bool:
        vk_user = 
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
