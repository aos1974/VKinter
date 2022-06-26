#
# тестирование работы с БД
#

from modules.db.databases import DataBase
import modules.db.dataclasses as datacls
import modules.db.databases as dbs

vk_db = DataBase(dbs.POSTGRES_DB)

