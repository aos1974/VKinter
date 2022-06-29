###########################
# файл: databases.py
# version: 0.1.11
###########################

import sqlalchemy
from modules.db.dataclasses import VKUserData

# Глобальный переменные и классы модуля
POSTGRES_DB = 'postgresql://vkdbadmin:vk2022boT!!!@172.18.89.161:5432/vkusers'

# класс для взаимодействия с базой данных
class DataBase(object):

    # функция инициализации класса
    def __init__(self, db: str):
        self.db = db
        self.engine = sqlalchemy.create_engine(self.db)
        self.connection = self.engine.connect()

    # end __init__()

    # функция получения данных пользователя ВКонтакте из базы данных
    # возвращает объект типа VKUserData или None, если запрос неудачный (нет данных)
    def get_vkuser(self, vk_id: int) -> VKUserData:
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

    # функция проверки, есть ли пользователь в базе данных
    def id_in_database(self, vk_id: int) -> bool:
        
        sql = f"""
            SELECT * FROM vk_users WHERE vk_id={vk_id};
            """
        result = self.connection.execute(sql).fetchone()
        # если данных нет
        if result is None:
            return False 
        # есд\ли данные есть     
        return True
    # end 

    # функция сохранения данных о пользователе ВКонтакте в базу данных
    # возвращае True, если данные сохранены в базе данных, иначе False
    def new_vkuser(self, vk_user: VKUserData) -> bool:
        
        if not self.id_in_database(vk_user.vk_id):
            # нет такого пользователя в базе данных
            sql = f"""
                INSERT INTO vk_users (vk_id,first_name,last_name,bdate,gender,city_id,city_title,vkdomain,last_visit) 
                VALUES ({vk_user.vk_id},'{vk_user.first_name}','{vk_user.last_name}','{vk_user.bdate}',{vk_user.gender},{vk_user.city_id},'{vk_user.city_title}','{vk_user.vkdomain}','{vk_user.last_visit}');
                """
        else:
            # пользователь уже существует в базе данных
            sql = f"""
                UPDATE vk_users SET last_visit = '{vk_user.last_visit}' WHERE vk_id = {vk_user.vk_id};
                """
        result = self.connection.execute(sql)
        # если запрос выполнился с ошибкой
        if result is None:
            return False
        # успешный результат
        return True

    # enf new_vk_user

    # Вставить массив данных в last_search
    def insert_last_search(self, user_id, lst_ids, position):
        for lst_id in lst_ids:
            sql = f"""SELECT * FROM last_search WHERE vk_id='{user_id}' and lst_id='{lst_id}';
            """
            result = self.connection.execute(sql).fetchone()
            if result is None:
                sql = f"""INSERT INTO last_search(vk_id, lst_id, srch_number) VALUES ('{user_id}','{lst_id}','{position}');
                              """
                result = self.connection.execute(sql)
                position += 1
    
    # end insert_last_search()

    # удалить пользователя ВКонтакте в базе данных
    def del_vkuser(self, vk_id: int) -> bool:
        pass
  
    # сохранить в базе данных информацию об избранном контакте
    def new_favorite(self, vk_id: int, fav_id: int) -> bool:
        # проверяем , есть ли уже такой id в избранных
        sql = f"""
            SELECT * FROM favorites WHERE vk_id={vk_id} and fav_id={fav_id};
            """
        result = self.connection.execute(sql).fetchone()
        # если есть то записей в базу данных не делаем
        if result is not None:
            return False
        # если это новый id, то записываем его в базу данных
        sql = f"""INSERT INTO favorites (vk_id, fav_id) VALUES ({vk_id}, {fav_id});
               """
        result = self.connection.execute(sql)
        return True
    # end new_favorite()
    
    # получить список избранных контактов
    def get_favorites(self, vk_id : int) -> list:
        sql = f"""
            SELECT fav_id FROM favorites WHERE vk_id={vk_id};
            """
        result = self.connection.execute(sql).fetchall()
        # если записей нет, то возвращаем пустой список
        if result is None or len(result) == 0:
            return list()
        # возвращаем список fav_id
        return list(zip(*list(result)))[0]
    # end get_favorites()

    # удалить избранный контакт у пользовалетя из базы данных
    def del_favotite(self, vk_id: int, fav_id: int) -> bool:
        pass

    # удалить все избранные контакты пользователя
    def del_all_favorites(self, vk_id: int) -> bool:
        pass

    # получить список заблокированных контактов
    def get_black_list(self, vk_id: int) -> list:
        sql = f"""
            SELECT blk_id FROM black_list WHERE vk_id={vk_id};
            """
        result = self.connection.execute(sql).fetchall()
        # если записей нет, то возвращаем пустой список
        if result is None or len(result) == 0:
            return list()
        # разбиваем список из пары vk_id, fav_id и получаем list(fav_id)
        return list(zip(*list(result)))[0]
    # end get_black_list()

    # # сохранить заблокированный контакт
    def new_black_id(self, vk_id: int, blk_id: int) -> bool:
        # проверяем , есть ли уже такой id в блэк-листе
        sql = f"""
            SELECT * FROM black_list WHERE vk_id={vk_id} and blk_id={blk_id};
            """
        result = self.connection.execute(sql).fetchone()
        # если есть то записей в базу данных не делаем
        if result is not None:
            return False
        # если это новый id, то записываем его в базу данных
        sql = f"""INSERT INTO black_list (vk_id, blk_id) VALUES ({vk_id}, {blk_id});
               """
        result = self.connection.execute(sql)
        return True

    # удалить контакт из заблокированных
    def del_black_id(self, vk_id: int, blk_id: int) -> bool:
        pass
    # end del_black_id()

    # удалить весь "блэк лист" пользователя
    def del_black_list(self, vk_id: int) -> bool:
        pass

    def is_black(self, vk_id: int, blk_id: int) -> bool:
        sql = f"""
              SELECT * FROM black_list WHERE vk_id={vk_id} AND blk_id={blk_id} ;
              """
        result = self.connection.execute(sql).fetchone()
        print(result)
        if result is None:
            return False
        else:
            return True

    # считать дополнительные данные о пользователе из базы данных
    def get_setings(self, vk_user: VKUserData) -> bool:
        sql = f"""
        SELECT * FROM settings WHERE vk_id={vk_user.vk_id};
        """
        result = self.connection.execute(sql).fetchone()
        # если запрос выполнился успешно
        if result is not None:
            # заполняем и возвращаем объект VKUserData
            # нулевой элемент списка это vk_id из таблицы bd.search
            vk_user.set_settings_from_list(list(result)[1:])
        else: 
            # если запрос к базе данных ничего не вернул
            vk_user.set_default_settings()
            return False
        return True

    def get_user(self, user_id, rch_number):
        sql = f"""
               SELECT lst_id FROM last_search WHERE vk_id={user_id} AND srch_number = {rch_number} LIMIT 1;
               """
        result = self.connection.execute(sql).fetchone()
        return result

    # сохранение дополнительных параметров пользователя в базе данных
    def set_setings(self, vk_user: VKUserData) -> bool:
        sql = f"""
        INSERT INTO settings(vk_id, access_token, srch_offset, age_from, age_to, last_command) 
        VALUES ('{vk_user.vk_id}','{vk_user.settings.get('access_token')}','{vk_user.settings.get('srch_offset')}','
        {vk_user.settings.get('age_from')}','{vk_user.settings.get('age_to')}','{vk_user.settings.get('last_command')}');
               """
        result = self.connection.execute(sql)
        return True

    # обновить данные параметров пользователя в базе данных
    def upd_setings(self, vk_user: VKUserData) -> bool:

        sql = f"""
        UPDATE settings SET srch_offset = '{vk_user.settings['srch_offset']}', access_token = '{vk_user.settings['access_token']}',
        age_from = '{vk_user.settings['age_from']}',age_to = '{vk_user.settings['age_to']}', last_command = '{vk_user.settings['last_command']}' 
        WHERE vk_id={vk_user.vk_id};
               """
        result = self.connection.execute(sql)
        return True


