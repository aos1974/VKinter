###########################
# файл: databases.py
# version: 0.1.3
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
    def get_vkuser(self, vk_id : int) -> VKUserData:
        pass

    # функция сохранения данных о пользователе ВКонтакте в базу данных
    def new_vkuser(self, vk_user : VKUserData) -> Boolean:
        pass

    # удалить пользователя ВКонтакте в базе данных
    def del_vkuser(self, vk_id : int) -> Boolean:
        pass

    # получить список избранных контактов
    def get_favorites(self, vk_id : int) -> list:
        pass

    # сохранить в базе данных информацию об избранном контакте
    def new_favirite(self, vk_id : int, fav_id : int) -> Boolean:
        pass

    # удалить избранный контакт у пользовалетя из базы данных
    def del_favotite(self, vk_id: int, fav_id : int) -> Boolean:
        pass

    # удалить все избранные контакты пользователя
    def del_all_favorites(self, vk_id : int) -> Boolean:
        pass

    # получить список заблокированных контактов
    def get_black_list(self, vk_id : int) -> list:
        pass

    # сохранить заблокированный контакт
    def new_black_id(self, vk_id: int, blk_id : int) -> Boolean:
        pass

    # удалить контакт из заблокированных
    def del_black_id(self, vk_id : int, blk_id : int) -> Boolean:
        pass

    # удалить весь "блэк лист" пользователя
    def del_black_list(self, vk_id : int) -> Boolean:
        pass

    # 
    def get_setings(self, vk_user: VKUserData) -> Boolean:
        pass

    #
    def update_settings(self, vk_user: VKUserData) -> Boolean:
        pass


# end class DataBase
