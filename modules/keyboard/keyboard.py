from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from modules.data.data import settings
class ClassKeyboard:
    def __init__(self):
        print('init')

    @staticmethod
    def settings():

        keyboard = VkKeyboard(**settings)
        keyboard.add_callback_button(label='Получить токен', color=VkKeyboardColor.PRIMARY,
                                     payload={"type": "open_link",
                                              "link": "https://oauth.vk.com/authorize?client_id=8116853&scope=wall,offline&redirect_uri=https://cosmio.io/api/vkinder/api.php&display=page&v=5.24&response_type=token"})
        keyboard.add_line()
        keyboard.add_callback_button('Назад', color=VkKeyboardColor.NEGATIVE, payload={"type": "menu"})
        return keyboard

    @staticmethod
    def search():
        keyboard = VkKeyboard(**settings)

        keyboard.add_callback_button(label='Предыдущий', color=VkKeyboardColor.PRIMARY,
                                     payload={"type": "previous", "text": "Ищем"})

        keyboard.add_callback_button(label='Следующий', color=VkKeyboardColor.PRIMARY,
                                     payload={"type": "next", "text": "Ищем"})
        keyboard.add_line()
        keyboard.add_callback_button(label='В избранное', color=VkKeyboardColor.POSITIVE,
                                     payload={"type": "show_snackbar", "text": "Добавлен в избранное"})

        keyboard.add_callback_button(label='В чёрный список', color=VkKeyboardColor.SECONDARY,
                                     payload={"type": "show_snackbar", "text": "Добавлен в черный список"})
        keyboard.add_line()
        keyboard.add_callback_button(label='Меню', color=VkKeyboardColor.NEGATIVE,
                                     payload={"type": "menu"})
        return keyboard

    @staticmethod
    def menu():
        keyboard = VkKeyboard(**settings)
        keyboard.add_callback_button(label='Поиск', color=VkKeyboardColor.POSITIVE,
                                     payload={"type": "search", "text": "Ищем"})

        keyboard.add_line()
        keyboard.add_callback_button(label='Избранное', color=VkKeyboardColor.PRIMARY,
                                     payload={"type": "favorites", "text": "Фавориты"})

        keyboard.add_callback_button(label='Чёрный список', color=VkKeyboardColor.SECONDARY,
                                     payload={"type": "black_list", "text": "Черный список"})

        keyboard.add_line()

        keyboard.add_callback_button(label='Настройки', color=VkKeyboardColor.SECONDARY,
                                     payload={"type": "settings", "text": "Настройки"})

        return keyboard

    @staticmethod
    def get_keyboard(type_keyboard: str):
        if type_keyboard == 'menu':
            keyboard = ClassKeyboard.menu()
        elif type_keyboard == 'settings':
            keyboard = ClassKeyboard.settings()
        elif type_keyboard == 'search':
            keyboard = ClassKeyboard.search()
        else:
            keyboard = ClassKeyboard.menu()
        return keyboard.get_keyboard()
