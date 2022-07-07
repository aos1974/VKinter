###########################
# файл: test_db2.py
# version: 0.1.1
# Тестирование работы с БД через databases2.py
###########################

from modules.utils import utils
from modules.db.databases import DataBase

# инициализация БД
#db_name = dbs.POSTGRES_DB

db_name = utils.get_token('db_connection')

if db_name is not None:
    vk_db = DataBase(db_name)
else:
    exit()

# тест запрос к БД на получение данных о пользователе
vk_id = 37584229
vk_user = vk_db.get_vkuser(vk_id)
print(vk_user.vk_id, vk_user.first_name, vk_user.last_name)

vk_db.insert_last_search(vk_id, [22211333, 22211334, 22211335], 1)

print('End')



