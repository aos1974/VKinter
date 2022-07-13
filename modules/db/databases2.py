###########################
# файл: databases2.py
# version: 0.2.1
# Работа с БД используя SQLAlchemy.metadata()
###########################

from sqlalchemy import Column, Integer, MetaData, PrimaryKeyConstraint, String, and_, create_engine, Table, delete, select, update
from modules.db.dataclasses import VKUserData

# Глобальный переменные и классы модуля
POSTGRES_DB = 'postgresql://vkdbadmin:vk2022boT!!!@172.18.89.161:5432/vkusers'

# класс для взаимодействия с базой данных
class DataBase(object):

    # функция инициализации класса
    def __init__(self, db: str):
        
        # инициализируем соединение с базой данных
        self.db = db
        self.engine = create_engine(self.db)
        self.connection = self.engine.connect()
                
        # создаем таблицы в Базе данных, только если они не существуют
        self.metadata = MetaData()
        self.create_tables()
        
    # end __init__()
    
    def create_tables(self):
        # определение таблиц Базы данных
        self.vk_users = Table('vk_users', self.metadata,
            Column('vk_id', Integer(), primary_key=True),
            Column('first_name', String(40), nullable=False),
            Column('last_name', String(40)),
            Column('bdate', String(40)),
            Column('gender', Integer()),
            Column('city_id', Integer()),
            Column('city_title', String(60)),
            Column('vkdomain', String(100)),
            Column('last_visit', String(40))
        )
        
        self.settings = Table('settings', self.metadata,
            Column('vk_id', Integer(), nullable=False, unique=True),
            Column('access_token', String(255)),
            Column('srch_offset', Integer()),
            Column('age_from', Integer()),
            Column('age_to', Integer()),
            Column('last_command', String(100))
        )
        
        self.last_search = Table('last_search', self.metadata,
            Column('vk_id', Integer(), nullable=False),
            Column('lst_id', Integer(), nullable=False),
            Column('srch_number', Integer()),
            PrimaryKeyConstraint('vk_id', 'lst_id', name='last_search_pk')
        )
        
        self.favorites = Table('favorites', self.metadata,
            Column('vk_id', Integer(), nullable=False),
            Column('fav_id', Integer(), nullable=False),
            PrimaryKeyConstraint('vk_id', 'fav_id', name='favorites_pk')
        )
        
        self.black_list = Table('black_list', self.metadata,
            Column('vk_id', Integer(), nullable=False),
            Column('blk_id', Integer(), nullable=False),
            PrimaryKeyConstraint('vk_id', 'blk_id', name='black_list_pk')
        )
        
        self.metadata.create_all(self.engine)
    # end create_tables()

    # функция получения данных пользователя ВКонтакте из базы данных
    # возвращает объект типа VKUserData или None, если запрос неудачный (нет данных)
    def get_vkuser(self, vk_id: int) -> VKUserData:
        # формируем заброс к базе данных
        query = select([self.vk_users]).where(self.vk_users.c.vk_id == vk_id)
        result = self.connection.execute(query).fetchone()
        # заполняем и возвращаем объект VKUserData
        if result is not None:
            vk_user = VKUserData(list(result))
        else:
            vk_user = None
        return vk_user        
    # end get_vkuser()

    # функция проверки, есть ли пользователь в базе данных
    def id_in_database(self, vk_id: int) -> bool:
        
        if self.get_vkuser(vk_id) is None:
            return False 
        
        return True
    # end id_in_database()
    
    # обновляем время последнего общения с ботом у существующего в базе пользователя
    def vk_user_update_last_visit(self, vk_user: VKUserData) -> bool:
        query = update(self.vk_users).where(self.vk_users.c.vk_id == vk_user.vk_id)
        query = query.values(
            last_visit = vk_user.last_visit
        )
        result = self.connection.execute(query)
        # если запрос выполнился с ошибкой
        if result is None:
            return False
        # успешный результат
        return True        
    # end vk_user_update_last_visit()
    
    # функция сохранения данных о пользователе ВКонтакте в базу данных
    # возвращае True, если данные сохранены в базе данных, иначе False
    def new_vkuser(self, vk_user: VKUserData) -> bool:
        res = True
        
        if not self.id_in_database(vk_user.vk_id):
            # нет такого пользователя в базе данных
            query = self.vk_users.insert().values(
                vk_id = vk_user.vk_id,
                first_name = vk_user.first_name,
                last_name = vk_user.last_name,
                bdate = vk_user.bdate,
                gender = vk_user.gender,
                city_id = vk_user.city_id,
                city_title = vk_user.city_title,
                vkdomain = vk_user.vkdomain,
                last_visit = vk_user.last_visit
            )
            result = self.connection.execute(query)
            # если запрос выполнился с ошибкой
            if result is None:
                res = False
        else:
            # пользователь уже существует в базе данных
            result = self.vk_user_update_last_visit(vk_user)
            # если запрос выполнился с ошибкой
            if result is None:
                res = False
        
        # успешный результат
        return res
    # enf new_vk_user()
    
    # Вставить массив данных в last_search
    def insert_last_search(self, user_id, lst_ids, position):
        
        for lst_id in lst_ids:
            query = select([self.last_search]).where(
                and_(
                    self.last_search.c.vk_id == user_id,
                    self.last_search.c.lst_id == lst_id
                )
            )
           
            result = self.connection.execute(query).fetchone()
            
            if result is None:
                query = self.last_search.insert().values(
                    vk_id = user_id,
                    lst_id = lst_id,
                    srch_number = position
                )
                result = self.connection.execute(query)
                position += 1
    # end insert_last_search()
    
    # удалить пользователя ВКонтакте в базе данных
    def del_vkuser(self, vk_id: int) -> bool:
        pass
    
    # удалить контакт из списка поиска
    def del_last_search_id(self, vk_id: int, lst_id: int) -> bool:
        query = delete(self.last_search).where(
            and_(
                self.last_search.c.vk_id == vk_id,
                self.last_search.c.lst_id == lst_id
            )
        )
        result = self.connection.execute(query)
        return True
    # end del_last_search_id()
    
    # удалить контакт из заблокированных
    def del_black_id(self, vk_id: int, blk_id: int) -> bool:
        
        query = delete(self.black_list).where(
            and_(
                self.black_list.c.vk_id == vk_id,
                self.black_list.c.blk_id == blk_id
            )
        )
        result = self.connection.execute(query)
        return True
    # end del_black_id()
    
    # сохранить в базе данных информацию об избранном контакте
    def new_favorite(self, vk_id: int, fav_id: int) -> bool:
        # проверяем , есть ли уже такой id в избранных
        query = select([self.favorites]).where(
            and_(
                self.favorites.c.vk_id == vk_id,
                self.favorites.c.fav_id == fav_id
            )
        )
        
        result = self.connection.execute(query).fetchone()
                # если есть то записей в базу данных не делаем
        if result is not None:
            return False
        
        # если это новый id, то записываем его в базу данных
        query = self.favorites.insert().values(
            vk_id = vk_id,
            fav_id = fav_id
        )
        result = self.connection.execute(query)
        # удаляем id из списка поиска
        self.del_last_search_id(vk_id, fav_id)
        # удаляем id из черного списка
        self.del_black_id(vk_id, fav_id)

        return True
    # end new_favorite()    
    
    # получить список избранных контактов
    def get_favorites(self, vk_id : int) -> list:
        query = select(self.favorites.c.fav_id).where(
            self.favorites.c.vk_id == vk_id
        )
        result = self.connection.execute(query).fetchall()
        # если записей нет, то возвращаем пустой список
        if result is None or len(result) == 0:
            return list()
        # возвращаем список fav_id
        return list(zip(*list(result)))[0]
    # end get_favorites()
    
    # удалить избранный контакт у пользовалетя из базы данных
    def del_favotite(self, vk_id: int, fav_id: int) -> bool:
        query = delete(self.favorites).where(
            and_(
                self.favorites.c.vk_id == vk_id,
                self.favorites.c.fav_id == fav_id
            )
        )
        self.connection.execute(query)
        return True
    # end del_favorite()

    # удалить все избранные контакты пользователя
    def del_all_favorites(self, vk_id: int) -> bool:
        
        query = delete(self.favorites).where(
            self.favorites.c.vk_id == vk_id,
        )
        self.connection.execute(query)
        
        return True
    # end del_all_favorites()
    
    # получить список заблокированных контактов
    def get_black_list(self, vk_id: int) -> list:
        query = select(self.black_list.c.blk_id).where(
            self.black_list.c.vk_id == vk_id
        )
        result = self.connection.execute(query).fetchall()
        # если записей нет, то возвращаем пустой список
        if result is None or len(result) == 0:
            return list()
        # разбиваем список из пары vk_id, fav_id и получаем list(fav_id)
        return list(zip(*list(result)))[0]
    # end get_black_list()
    
    # сохранить заблокированный контакт
    def new_black_id(self, vk_id: int, blk_id: int) -> bool:
    
        # проверяем, есть ли уже такой id в блэк-листе
        query = select([self.black_list]).where(
            and_(
                self.black_list.c.vk_id == vk_id,
                self.black_list.c.blk_id == blk_id
            )
        )
        
        result = self.connection.execute(query).fetchone()
        
        # если есть то записей в базу данных не делаем
        if result is not None:
            return False
        
        # если это новый id, то записываем его в базу данных
        query = self.black_list.insert().values(
            vk_id = vk_id,
            blk_id = blk_id
        )
        
        result = self.connection.execute(query)
        # удаляем id из списка поиска
        self.del_last_search_id(vk_id, blk_id)
        # удаляем id из списка фаворитов
        self.del_favotite(vk_id, blk_id)
        return True
    # end new_black_id()
    
    # удалить контакт из списка поиска
    def del_all_last_search(self, vk_id: int) -> bool:
        query = delete(self.last_search).where(
            self.last_search.c.vk_id == vk_id
        )
        result = self.connection.execute(query)
        return True
    # end del_all_last_search()
    
    # удалить весь "блэк лист" пользователя
    def del_black_list(self, vk_id: int) -> bool:
        query = delete(self.black_list).where(
            self.black_list.c.vk_id == vk_id
        )
        result = self.connection.execute(query)
        return True
    # end del_black_list
    
    # проверка ID пользователя на включенеи в черный список
    def is_black(self, vk_id: int, blk_id: int) -> bool:
        query = select([self.black_list]).where(
            and_(
                self.black_list.c.vk_id == vk_id,
                self.black_list.c.blk_id == blk_id
            )
        )
        result = self.connection.execute(query).fetchone()
        if result is None:
            return False
        else:
            return True
    # end is_black()
    
    # считать дополнительные данные о пользователе из базы данных
    def get_setings(self, vk_user: VKUserData) -> bool:
        query = select([self.settings]).where(
            self.settings.c.vk_id == vk_user.vk_id
        )
        result = self.connection.execute(query).fetchone()
        # если запрос выполнился успешно
        if result is None:
            return False
        # заполняем и возвращаем объект VKUserData
        # нулевой элемент списка это vk_id из таблицы bd.search
        vk_user.set_settings_from_list(list(result)[1:])
        return True
    # end get_settings()
    
    # получить из базы "наденного" по номеру смещения
    def get_user(self, user_id, srch_number):
        query = select(self.last_search.c.lst_id).where(
            and_(
                self.last_search.c.vk_id == user_id,
                self.last_search.c.srch_number == srch_number
            )
        )
        result = self.connection.execute(query).fetchone()
        return result
    # get_user()
    
    # сохранение дополнительных параметров пользователя в базе данных
    def set_setings(self, vk_user: VKUserData) -> bool:
        query = self.settings.insert().values(
            vk_id = vk_user.vk_id,
            access_token = vk_user.settings.access_token,
            srch_offset = vk_user.settings.srch_offset,
            age_from = vk_user.settings.age_from,
            age_to = vk_user.settings.age_to,
            last_command = vk_user.settings.last_command
        )
        self.connection.execute(query)
        return True
    # end set_settins()    
    
    # обновить данные параметров пользователя в базе данных
    def upd_setings(self, vk_user: VKUserData) -> bool:

        query = update(self.settings).where(
            self.settings.c.vk_id == vk_user.vk_id
        )
        query = query.values(
            srch_offset = vk_user.settings.srch_offset,            
            access_token = vk_user.settings.access_token,
            age_from = vk_user.settings.age_from,
            age_to = vk_user.settings.age_to, 
            last_command = vk_user.settings.last_command
        )
        self.connection.execute(query)
        return True
    # end upd_setings()
    