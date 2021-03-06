###########################
# файл: test.py
# version: 0.1.8
###########################

#
# тестирование работы с БД
#

from modules.utils import utils
from modules.db.databases import DataBase
from modules.logic.logic import Logic
import modules.db.dataclasses as datacls
import modules.db.databases as dbs

# инициализация БД
#vk_db = DataBase(dbs.POSTGRES_DB)
vk_db = DataBase(utils.get_token('db_connection'))

# инициализация подсистемы "Бизнес логики"
vk_logic = Logic(vk_db, None)

# тест запрос к БД на получение данных о пользователе
vk_id = 37584229
vk_user = vk_db.get_vkuser(vk_id)
print(vk_user.vk_id, vk_user.first_name, vk_user.last_name)

# тестовые данные для загрузки в БД
# информация получается от бота о "новом" пользователе который начал диалог
# эту информацию мы апдэйтим в БД
test_dict = {'id': 20910114, 'bdate': '21.11.1991', 'city': {'id': 110, 'title': 'Пермь'}, 'sex': 2, 'screen_name': 'mgarbuzenko', 'first_name': 'Михаил', 'last_name': 'Гарбузенко', 'can_access_closed': True, 'is_closed': False}

# Бизнес-логика: передаем данные нового пользователя для записи в базу
# создаем объект пользователя из данных (словаря) от vk_api
vk_user = datacls.VKUserData(test_dict)
# передаем данные пользователя для записи/обновления БД
if vk_logic.new_vk_user(vk_user):
    print('OK')
else:
    print('ERROR')

# Бизнес-логика: получить данные о пользователе ВКонтакте
vk_id = 695117549
vk_user = vk_logic.get_vk_user(vk_id)
print(vk_user.vk_id, vk_user.first_name, vk_user.last_name, vk_user.settings.get('srch_offset'))

# Бизнес-логика: добавление поискового списка
srch_list = [695117551, 695117555, 695107558, 695107560, 695108562, 695108463, 695108464]
srch_list2 = [595108464, 595108463, 595108462, 595108461, 595108460, 595108459, 595108458]

# тест записи в избранное
for lst in srch_list:
    print(vk_db.new_favorite(vk_user.vk_id, lst))
    
# тест чтения избранного
print(vk_db.get_favorites(vk_user.vk_id))

# тест записи в блэк лист
for lst in srch_list2:
    print(vk_db.new_black_id(vk_user.vk_id, lst))
    
# тест чтения избранного
print(vk_db.get_black_list(vk_user.vk_id))
