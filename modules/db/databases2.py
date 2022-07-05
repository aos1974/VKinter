###########################
# файл: databases2.py
# version: 0.1.1
# Работа с БД используя SQLAlchemy.ORM
###########################

from sqlalchemy import Column, Integer, MetaData, PrimaryKeyConstraint, String, create_engine, Table, select

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
            Column('citi_id', Integer()),
            Column('citi_title', String(60)),
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
            PrimaryKeyConstraint('vk_id', 'lst_is', name='last_search_pk')
        )
        
        self.favorites = Table('favorites', self.metadata,
            Column('vk_id', Integer(), nullable=False),
            Column('fav_id', Integer(), nullable=False),
            PrimaryKeyConstraint('vk_id', 'fav_is', name='favorites_pk')
        )
        
        self.black_list = Table('black_list', self.metadata,
            Column('vk_id', Integer(), nullable=False),
            Column('blk_id', Integer(), nullable=False),
            PrimaryKeyConstraint('vk_id', 'blk_is', name='black_list_pk')
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
