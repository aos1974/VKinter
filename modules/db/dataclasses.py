###########################
# файл: dataclasses.py
# version: 0.1.5
###########################

from datetime import datetime

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
    def __init__(self, lst = []):
        super().__init__()

        # если никакие аргументы не переданы
        if len(lst) == 0:
            # инициализация данных "по умолчанию"
            self.set_default_attrs()
        else:
            # если заполнение из переданного списка было не корректным
            if not self.set_attr_from_list(lst):
                # то также заполняем параметрами "по умолчанию"
                self.set_default_attrs()
        # инициализируем дополниетльные параметры класса (settings)
        self.set_default_settings()
    # end __init__()

    # функция заполнения атрибутов класса "по умолчанию"
    def set_default_attrs(self):
        self.vk_id = -1
        self.first_name = ''
        self.last_name = ''
        self.bdate = ''
        self.gender = VK_UNKNOWN_GENDER
        self.city_id = -1
        self.city_title = ''
        self.vkdomain = ''
        self.last_visit = ''
        dt = datetime.now()
        self.last_visit = dt.strftime('%Y-%M-%D %H:%M:%S')
    # end set_default_attrs()

    # функция заполнения "по умолчанию" дополнительных параметров (settings)
    def set_default_settings(self):
        self.settings = {'access_token' : '', 'srch_offset' : -1, 'age_from' : -1, 'age_to' : -1, 'last_command' : ''}
    # end set_default_settings

    # заполнение атрибутов класса (данные) из списка, по порядку
    def set_attr_from_list(self, lst : list) -> bool:
        # проверяем, что переданы все атрибуты (пока без settings)
        if len(lst) != 9:
            return False
        # заполняем атрибуты класса из списка
        self.vk_id = lst[0]
        self.first_name = lst[1]
        self.last_name = lst[2]
        self.bdate = lst[3]
        self.gender = lst[4]
        self.city_id = lst[5]
        self.city_title = lst[6]
        self.vkdomain = lst[7]
        self.last_visit = lst[8]
        dt = datetime.now()
        self.last_visit = dt.strftime('%Y-%M-%D %H:%M:%S')
        return True
    # end set_attr_from_list()
    
    # заполнение атрибутов класса из словаря vk
    # {'id': int, 'bdate': str, 'city': {'id': int, 'title': str}, 'sex': int, 
    #  'screen_name': str, 'first_name': str, 'last_name': str, 'can_access_closed': bool, 'is_closed': bool}
    def set_attr_from_dict(self, vk_dict: dict) -> bool:          
        # проверяем, что все необходимые ключи нам переданы
        if 'id' in vk_dict.keys():
            self.vk_id = vk_dict.get('id')
        if 'first_name' in vk_dict.keys():
            self.first_name = vk_dict.get('first_name')
        if 'last_name' in vk_dict.keys():
            self.last_name = vk_dict.get('last_name')    
        if 'bdate' in vk_dict.keys():
            self.bdate = vk_dict.get('bdate')
        if 'city' in vk_dict.keys():
            self.city_id = vk_dict.get('city').get('id')
            self.city_title = vk_dict.get('city').get('title')
        if 'sex' in vk_dict.keys():
            self.gender = vk_dict.get('sex')
        if 'screen_name' in vk_dict.keys():
            self.vkdomain = vk_dict.get('screen_name')
        dt = datetime.now()
        self.last_visit = dt.strftime('%Y-%M-%D %H:%M:%S')
    # end set_attr_from_dict
        
    # вывод данных о пользователе в формате json
    def json():
        pass

# end class VKUserData
