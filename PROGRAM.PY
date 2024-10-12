import os
import datetime
import requests

YANDEX_DISK_TOKEN = ''
YANDEX_DISK_FOLDER_NAME = 'test4' # имя папки, в которую будут загружаться файлы
local_folder_path = 'c://stady/python' # папка, из которой будут загружаться файлы

def get_today_files(folder_path):
    today = datetime.date.today()
    files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_creation_date = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).date()
            if file_creation_date == today:
                files.append(file_path)
    return files

def get_upload_link(folder_name, filename, token):
    url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = {'Authorization': f'OAuth {token}'}
    data = {'path': f'/{folder_name}/{filename}'}
    response = requests.get(url, headers=headers, params=data)
    if response.status_code == 200:
        return response.json()['href']
    else:
        return None

def upload_file(file_path, upload_url):
    with open(file_path, 'rb') as f:
        response = requests.put(upload_url, data=f)
    if response.status_code == 201:
        print(f'Файл {os.path.basename(file_path)} успешно загружен на Яндекс.Диск.')
    else:
        print(f'Ошибка при загрузке файла {os.path.basename(file_path)}: {response.text}')

if __name__ == '__main__':
    today_files = get_today_files(local_folder_path)
    if today_files:
        print(f'Найдено {len(today_files)} файлов, созданных сегодня:')
        for file_path in today_files:
            filename = os.path.basename(file_path)
            upload_link = get_upload_link(YANDEX_DISK_FOLDER_NAME, filename, YANDEX_DISK_TOKEN)
            if upload_link:
                upload_file(file_path, upload_link)
            os.remove(file_path)
    else:
        print(f'В папке {local_folder_path} нет файлов, созданных сегодня.')
