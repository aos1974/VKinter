###########################
# файл: dataclasses.py
# version: 0.1.2
###########################

# Пол пользователя ВКонтакте
VK_MALE = 2
VK_FEMALE = 1
VK_UNKNOWN_GENDER = 0

# Класс определяющий набор данных пользователя ВКонтакте
class VKUserData(object): 
    # id пользователя ВКонтакте
    vk_id : int
    # Имя пользователя ВКонтакте
    first_name : str
    # Фамилия пользователя
    last_name: str
    # День рождения пользователя
    bdate: str
    # Пол пользоветеля
    gender : int
    # id города пользователя
    city_id: int
    # Название города пользователя
    city_title: str
    # адрес траницы ВКонтакте пользователя
    vkdomain: str
    # Дата время последнего общения с ботом
    last_visit: str
    # дополнительные свойства пользователя ВКонтакте
    settings : list

    #инициализация класса
    def __init__(self):
        super().__init__()

        # инициализация данных "по умолчанию"
        self.vk_id = -1
        self.first_name = ''
        self.last_name = ''
        self.bdate = ''
        self.gender = VK_UNKNOWN_GENDER
        self.city_id = -1
        self.city_title = ''
        self.vkdomain = ''
        self.last_visit = ''
        self.settings = {'access_token' : '', 'srch_offset' : -1, 'age_from' : -1, 'age_to' : -1, 'last_command' : ''}
    # end __init__()

    # вывод данных о пользователе в формате json
    def json():
        pass

# end class VKUserData
