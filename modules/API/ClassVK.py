###########################
# файл: ClassVK.py
# version: 0.1.11
###########################

from pprint import pprint
import requests
from modules.db.dataclasses import VKUserData


class ClassVK(object):
    API_URL = 'https://api.vk.com/method/'

    def __init__(self, access_token=None):
        self.access_token = access_token
        # self.offset = 0 #Сдвиг для поиска
        
    @staticmethod
    def sex_invert(sex):
        if sex == 1:
            sex = 2
        elif sex == 2:
            sex = 1
        else:
            sex = 0
        return sex

    def search(self, vk_user: VKUserData, offset, count):
        params = self.get_info(vk_user.vk_id)
        search_list = self.users_search(vk_user, params, count=count, offset=offset)
        # pprint(search_list)
        return search_list
    
    def get_user_data(self, id):
        attachments = []
        content = ''
        if id != 0:
            params = self.get_info(id)
            # pprint(params)
            if params:
                content = f'\n{params.get("first_name")} {params.get("last_name")} https://vk.com/id{id}'
                self.get_info(id)  # Параметры пользователя

                photos = self.photos_get(id, 3)
                if photos.get('response') is not None:
                    items = photos['response']['items']
                    for item in items:
                        attachments.append(f'photo{id}_{item.get("id")}')
        return [','.join(attachments), content]

    def users_search(self, vk_user: VKUserData, params_data, count=1, offset=0):
        method = 'users.search'
        url = self.API_URL + method
        access_token = vk_user.settings['access_token']
        if params_data.get("city"):
            city = params_data.get("city").get("id")
        if not access_token:
            access_token = self.access_token
        params = dict(count=count, city=city, offset=offset,
                      age_from=vk_user.settings['age_from'], age_to=vk_user.settings['age_to'],
                      sex=self.sex_invert(params_data.get("sex")), access_token=access_token, v='5.131', has_photo=1, status=6, sort=0)

        # pprint(params)
        res = requests.get(url, params=params)
        response = res.json().get("response")
        ids = []
        for r in response.get('items'):
            if r.get("can_access_closed"):
                # print(r)
                ids.append(r.get("id"))
        return ids

    def get_info(self, user_ids):
        # print(user_ids)
        method = 'users.get'
        url = self.API_URL + method
        params = {
            'user_ids': user_ids,
            'access_token': self.access_token,
            'fields': 'screen_name, city, bdate, sex, screen_name',
            'v': '5.131'
        }
        res = requests.get(url, params=params)
        response = res.json().get("response")
        # print(response)
        if response:
            return response[0]
        else:
            return None

    def photos_get(self, owner_id: str, count=3):
        method = 'photos.get'
        url = self.API_URL + method
        params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'access_token': self.access_token,
            'extended': 1,
            'count': count,
            'v': '5.131'
        }
        res = requests.get(url, params=params).json()

        if res.get('error') is not None:
            print(res['error']['error_msg'])
        return res
