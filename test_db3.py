###########################
# файл: test_db3.py
# version: 0.3.1
# Тестирование работы с БД через databases3.py
###########################

from datetime import datetime
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
#vk_id = 37584277
vk_user = vk_db.get_vkuser(vk_id)
print(vk_user.vk_id, vk_user.first_name, vk_user.last_name)

dt = datetime.now()
vk_user.last_visit = dt.strftime('%Y-%m-%d %H:%M:%S')
vk_db.vk_user_update_last_visit(vk_user)

dt = datetime.now()
vk_user.last_visit = dt.strftime('%Y-%m-%d %H:%M:%S')
vk_user.vk_id = 77700000
vk_user.first_name = 'Каролина'
vk_user.vkdomain = 'KarolinaT'
vk_db.new_vkuser(vk_user)

print('End')



