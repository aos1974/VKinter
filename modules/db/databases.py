###########################
# файл: databases2.py
# version: 0.3.1
# Работа с БД используя SQLAlchemy.ORM
###########################

from sqlalchemy import Column, Integer, PrimaryKeyConstraint, String, and_, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from modules.db.dataclasses import VKUserData

# Глобальный переменные и классы модуля
POSTGRES_DB = 'postgresql://vkdbadmin:vk2022boT!!!@172.18.89.161:5432/vkusers'

# Определяем объекты связанные с Базой данных
Base = declarative_base()

# таблица vk_users
class vk_users(Base):
    __tablename__ = 'vk_users'

    vk_id = Column(Integer(), primary_key=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40))
    bdate = Column(String(40))
    gender = Column(Integer())
    city_id  = Column(Integer())
    city_title = Column(String(60))
    vkdomain = Column(String(100))
    last_visit = Column(String(40))

    def __repr__(self) -> str:
        return "vk_users(vk_id='{self.vk_id}', " \
                        "first_name='{self.first_name}', " \
                        "last_name='{self.last_name}', " \
                        "bdate='{self.bdate}', " \
                        "gender='{self.gender}', " \
                        "city_id='{self.city_id}', " \
                        "city_title='{self.city_title}', " \
                        "vkdomain='{self.vkdomain}', " \
                        "last_visit='{self.last_visit}')".format(self=self)

# end class vk_users

# таблица settings
class settings(Base):
    __tablename__ = 'settings'

    vk_id = Column(Integer(), primary_key=True)
    access_token = Column(String(255))
    srch_offset = Column(Integer())
    age_from = Column(Integer())
    age_to = Column(Integer())
    last_command = Column(String(100))

    def __repr__(self) -> str:
        return "setting(vk_id='{self.vk_id}', " \
                       "access_token='{self.access_token}', " \
                       "srch_offset='{self.srch_offset}', " \
                       "age_from='{self.age_from}', " \
                       "age_to='{self.age_to}', " \
                       "last_command='{self.last_command}')".format(self=self)

# end class settings

# таблица last_search
class last_search(Base):
    __tablename__ = 'last_search'
    __table_args__ = (PrimaryKeyConstraint('vk_id', 'lst_id', name='last_search_pk'),)

    vk_id = Column(Integer(), nullable=False)
    lst_id = Column(Integer(), nullable=False)
    srch_number = Column(Integer())

    def __repr__(self) -> str:
        return "last_search(vk_id='{self.vk_id}', " \
                           "lst_id='{self.lst_id}', " \
                           "srch_number='{self.srch_number}')".format(self=self)

# end class last_search

# таблица favorites
class favorites(Base):
    __tablename__ = 'favorites'
    __table_args__ = (PrimaryKeyConstraint('vk_id', 'fav_id', name='favorites_pk'),)

    vk_id = Column(Integer(), nullable=False)
    fav_id = Column(Integer(), nullable=False)

    def __repr__(self) -> str:
        return "favorites(vk_id='{self.vk_id}', " \
                         "fav_id='{self.fav_id}')".format(self=self)

# end class favorites

# таблица black_list
class black_list(Base):
    __tablename__ = 'black_list'
    __table_args__ = (PrimaryKeyConstraint('vk_id', 'blk_id', name='black_list_pk'),)

    vk_id = Column(Integer(), nullable=False)
    blk_id = Column(Integer(), nullable=False)

    def __repr__(self) -> str:
        return "black_list(vk_id='{self.vk_id}', " \
                          "blk_id='{self.blk_id}')".format(self=self)    

# end class black_list

# класс для взаимодействия с базой данных
class DataBase(object):

    # функция инициализации класса
    def __init__(self, db: str):
        
        # инициализируем соединение с базой данных
        self.db = db
        self.engine = create_engine(self.db)
                
        # создаем таблицы в Базе данных, только если они не существуют
        Base.metadata.create_all(self.engine)

        # открываем сессию для работы ORM  сБазой данных
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    # end __init__()

    # функция получения данных пользователя ВКонтакте из базы данных
    # возвращает объект типа VKUserData или None, если запрос неудачный (нет данных)
    def get_vkuser(self, vk_id: int) -> VKUserData:
        vk_user = None
        # формируем заброс к базе данных
        record = self.session.query(vk_users).filter(vk_users.vk_id == vk_id).first()

        # заполняем и возвращаем объект VKUserData
        if record is not None:
            vk_user = VKUserData([record.vk_id, record.first_name, record.last_name,
                                record.bdate, record.gender, record.city_id, record.city_title,
                                record.vkdomain, record.last_visit])

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
        query = self.session.query(vk_users)
        query = query.filter(vk_users.vk_id == vk_user.vk_id)
        if query.update({vk_users.last_visit: vk_user.last_visit}) == 0:
        # если update не выполнился
            return False
        # успешный результат
        self.session.commit()
        return True        
    # end vk_user_update_last_visit()

    # функция сохранения данных о пользователе ВКонтакте в базу данных
    # возвращае True, если данные сохранены в базе данных, иначе False
    def new_vkuser(self, vk_user: VKUserData) -> bool:
        res = True
        
        if not self.id_in_database(vk_user.vk_id):
            # нет такого пользователя в базе данных
            cc_vk_users = vk_users(
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

            self.session.add(cc_vk_users)
            self.session.commit()
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
        
        last_search_list = []

        # формируем список для сохранения в базе данных
        for lst_id in lst_ids:
            record = self.session.query(last_search).filter(
                and_(
                    last_search.vk_id == user_id, 
                    last_search.lst_id == lst_id
                    )
                ).first()
            
            if record is None:
                last_search_item = last_search(vk_id = user_id,
                                               lst_id = lst_id,
                                               srch_number = position)
                last_search_list.append(last_search_item)
                position += 1
        
        # записываем результат в базу данных
        if len(last_search_list) > 0:
            record = self.session.bulk_save_objects(last_search_list)
            self.session.commit()
    # end insert_last_search()

    # удалить пользователя ВКонтакте в базе данных
    def del_vkuser(self, vk_id: int) -> bool:
        pass
    
    # удалить контакт из списка поиска
    def del_last_search_id(self, vk_id: int, lst_id: int) -> bool:

        query = self.session.query(last_search)
        query = query.filter(
            and_(
                last_search.vk_id == vk_id,
                last_search.lst_id == lst_id
            )
        )
        dcc_last_search = query.one()
        self.session.delete(dcc_last_search)
        self.session.commit()
        
        return True
    # end del_last_search_id()

    # удалить контакта из заблокированных
    def del_black_id(self, vk_id: int, blk_id: int) -> bool:

        query = self.session.query(black_list)
        query = query.filter(
            and_(
                black_list.vk_id == vk_id,
                black_list.blk_id == blk_id
            )
        )
        dcc_black_id = query.first()
        self.session.delete(dcc_black_id)
        self.session.commit()
        
        return True
    # end del_black_id()

    # сохранить в базе данных информацию об избранном контакте
    def new_favorite(self, vk_id: int, fav_id: int) -> bool:
        # проверяем , есть ли уже такой id в избранных

        record = self.session.query(favorites).filter(
            and_(
                favorites.vk_id == vk_id, 
                favorites.fav_id == fav_id
                )
            ).first()
                
        # если есть то записей в базу данных не делаем
        if record is not None:
            return False
        
        # если это новый id, то записываем его в базу данных
        cc_favorite = favorites(
            vk_id = vk_id,
            fav_id = fav_id
            )
        self.session.add(cc_favorite)
        self.session.commit()
        # удаляем id из списка поиска
        self.del_last_search_id(vk_id, fav_id)
        # удаляем id из черного списка
        self.del_black_id(vk_id, fav_id)

        return True
    # end new_favorite()        

    