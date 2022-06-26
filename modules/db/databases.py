###########################
# файл: databases.py
# version: 0.1.4
###########################

import psycopg2
import sqlalchemy
from modules.db.dataclasses import VKUserData

# Глобальный переменные и классы модуля
POSTGRES_DB = 'postgresql://vkdbadmin:vk2022boT!!!@172.18.89.161:5432/vkusers'

# класс для взаимодействия с базой данных
class DataBase(object):

    # функция инициализации класса
    def __init__(self, db : str):
        self.db = db
        self.engine = sqlalchemy.create_engine(self.db)
        self.connection = self.engine.connect()
    # end __init__()

    # функция получения данных пользователя ВКонтакте из базы данных
    # возвращает объект типа VKUserData или None, если запрос неудачный (нет данных)
    def get_vkuser(self, vk_id : int) -> VKUserData:
        sql = f"""
        SELECT * FROM vk_users WHERE vk_id={vk_id};
        """
        result = self.connection.execute(sql).fetchone()
        # если запрос выполнился успешно
        if result is not None:
            # заполняем и возвращаем объект VKUserData
            vk_user = VKUserData(list(result))
        else: 
            # если запрос к базе данных ничего не вернул
            vk_user = None
        return vk_user
    # get_vkuser()

    # функция сохранения данных о пользователе ВКонтакте в базу данных
    def new_vkuser(self, vk_user : VKUserData) -> bool:
        pass

    # удалить пользователя ВКонтакте в базе данных
    def del_vkuser(self, vk_id : int) -> bool:
        pass

    # получить список избранных контактов
    def get_favorites(self, vk_id : int) -> list:
        pass

    # сохранить в базе данных информацию об избранном контакте
    def new_favirite(self, vk_id : int, fav_id : int) -> bool:
        pass

    # удалить избранный контакт у пользовалетя из базы данных
    def del_favotite(self, vk_id: int, fav_id : int) -> bool:
        pass

    # удалить все избранные контакты пользователя
    def del_all_favorites(self, vk_id : int) -> bool:
        pass

    # получить список заблокированных контактов
    def get_black_list(self, vk_id : int) -> list:
        pass

    # сохранить заблокированный контакт
    def new_black_id(self, vk_id: int, blk_id : int) -> bool:
        pass

    # удалить контакт из заблокированных
    def del_black_id(self, vk_id : int, blk_id : int) -> bool:
        pass

    # удалить весь "блэк лист" пользователя
    def del_black_list(self, vk_id : int) -> bool:
        pass

    # 
    def get_setings(self, vk_user: VKUserData) -> bool:
        pass

    #
    def update_settings(self, vk_user: VKUserData) -> bool:
        pass


# end class DataBase
