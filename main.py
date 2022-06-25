import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from modules.db.sql_class import SqlClass
from modules.utils import utils

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=utils.get_token('VKinder'))

# Работа с сообщениями
longpoll = VkLongPoll(vk)

print(f"Бот запущен")

#Тест базы данных
sql = SqlClass()
print(f"База данных {sql.get_test(id=1)}")

# Основной цикл
for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:
            # Сообщение от пользователя
            request = event.text
            print(request)
            # Каменная логика ответа
            if request == "привет":
                write_msg(event.user_id, "Хай")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            elif request.split()[0] == "command":
                write_msg(event.user_id, "Команды")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")