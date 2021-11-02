import json
import requests
from pprint import pprint

vk_token = '041fac02147390f8d1ea02ed6895175c4dcb52f32e02c7fe03bd6c10fc4c65165f3970a3bac51617f2bd0'


def photos_get(photo_sizes=1, extended=1):
    url = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': vk_ID,
        'photo_sizes': photo_sizes,
        'access_token': vk_token,
        'v': '5.81',
        'extended': extended,
        'count': 300,
        'album_id': 'profile'
    }
    res = requests.get(url=url, params=params).json()
    return res


def name_photo(photo):
    filename = []
    for files in photo['response']['items']:
        filename.append(files['likes']['count'])
    return filename


def size_file(photo):
    all_sizes = []
    for files in photo['response']['items']:
        name_and_size = {}
        name_and_size['file_name'] = files['likes']['count']
        all_sizes.append(name_and_size)
        for size in files['sizes']:
            name_and_size['size'] = size['type']
    return all_sizes


def writing_to_a_file():
    with open('Photos.json', 'w', encoding='utf-8') as file:
        json.dump(size_file(photos_get()), file, indent=4, ensure_ascii=False)


def getting_link_photo(photo):
    photo_url = []
    for files in photo['response']['items']:
        photo_url.append(files['sizes'][-1]['url'])
    return photo_url


def creating_folder_on_disk():
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {
        'Content-Type': 'application/json',
        "Accept": "application/json",
        "Authorization": f"OAuth {ya_token}"
    }
    params = {'path': 'PhotoVK'}
    response = requests.put(url=url, headers=headers, params=params)
    return response.json()


def uploading_to_disk(photo_url):
    headers = {
        "Accept": "application/json",
        "Authorization": "OAuth " + ya_token
    }
    file_name = 1
    for link in photo_url[:5]:
        params = {
            'path': f'PhotoVK/{file_name}',
            'url': link
        }
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
        r = requests.post(url=url, params=params, headers=headers)
        res = r.json()
        print(f'Фотографий загружено: {file_name}')
        file_name += 1


if __name__ == '__main__':
    vk_ID = input('Введите ID пользователя ВК: ')
    ya_token = input('Введите ваш токен: ')
    photos_get()
    name_photo(photos_get())
    writing_to_a_file()
    size_file(photos_get())
    getting_link_photo(photos_get())
    creating_folder_on_disk()
    uploading_to_disk(getting_link_photo(photos_get()))
