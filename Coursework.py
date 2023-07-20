import json
import requests
import time
from tqdm import tqdm

with open('token_yd.txt','r') as token_file2:
    token_yd = token_file2.readline()
with open('token_vk.txt','r') as token_file1:
        token_vk = token_file1.readline()
with open('vk_id.txt','r') as id_file1:
        vk_id = id_file1.readline()

def get_user_photo(token,id):
    url = 'https://api.vk.com/method/photos.get'
    params = {'owner_id' : id,
              'album_id' : 'profile',
              'extended' : '1',
              'photo_ids': '0',
              'count' : '5',
              'photo_sizes' : '1',
              'access_token' : token,
              'v' : '5.131'}
    response = requests.get(url, params=params)
    data = response.json()
    return data

def new_folder():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'OAuth {}'.format(token_yd)                
    }
    upload_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    pararms = {"path" : "Своя папка для фото" ,"overwrite" : "true"}
    response = requests.put(upload_url,headers=headers,params=pararms)
    response_data = response.json()

def upload_yd(file_url,filename):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'OAuth {}'.format(token_yd)                
    }
    upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    pararms = {"path" : filename, "url" : file_url, "overwrite" : "true"}
    response = requests.post(upload_url,headers=headers,params=pararms)
    response_data = response.json()

def vk_to_yd():
    result = get_user_photo(token_vk,vk_id)
    data1 = result['response']['items']
    data2 = []
    data4 = []
    for element in data1:
        data3 = element['likes']['count'],['date'],sorted(element['sizes'], key=lambda d: d['height'], reverse=True)[0]
        data2.append(data3)
    for el in data2:
        res = {
            'file name' : str(el[0]),
            'size' : el[2]['type'],
            'url' : el[2]['url']
            }
        if res['file name'] not in data4:
            data4.append(res)
        else:
            {
            'file name' : str(el[0])+str(time.strftime("%B %d %Y", [1])),
            'size' : el[2]['type'],
            'url' : el[2]['url']
            }
            data4.append(res)
    for i in tqdm(data4,desc='Загрузка фото из Вконтакте'):
        time.sleep(0.5)
    print()
    new_folder()
    for dict in data4:
        dict['file name'] = str(dict['file name'])+'.jpg'
        upload_yd(dict['url'],("Своя папка для фото/"+str(''.join([dict['file name']]))))
    for i in tqdm(data4,desc='Загрузка фото на Яндекс Диск'):
        time.sleep(0.5)
    print()

def info_file():
    with open('info.json','w') as info_file:
        result = get_user_photo(token_vk,vk_id)
        data1 = result['response']['items']
        data2 = []
        data4 = []
        for element in data1:
            data3 = element['likes']['count'],['date'],sorted(element['sizes'], key=lambda d: d['height'], reverse=True)[0]
            data2.append(data3)
        for el in data2:
            res = {
                'file name' : str(el[0]),
                'size' : el[2]['type'],
                'url' : el[2]['url']
                }
            if res['file name'] not in data4:
                data4.append(res)
            else:
                res = {
                'file name' : str(el[0])+time.strftime("%B %d %Y", [1]),
                'size' : el[2]['type'],
                'url' : el[2]['url']
                }
                data4.append(res)
        for i in tqdm(data4,desc='Создание json-файла'):
            time.sleep(0.5)
        print()
        for dict in data4:
            dict['file name'] = str(dict['file name'])+'.jpg'
        json.dump(data4,info_file,ensure_ascii=True,indent=2)
        
vk_to_yd()
info_file()