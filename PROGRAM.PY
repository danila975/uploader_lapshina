import glob
import requests
from environs import Env
import os

def get_files_by_date(folder_path, target_date):
    files = []
    for file_path in glob.glob(f"{folder_path}/**/*{target_date}*", recursive=True):
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
    env = Env()
    env.read_env()

    YANDEX_DISK_TOKEN = env('YANDEX_DISK_TOKEN')
    YANDEX_DISK_FOLDER_NAME = env('YANDEX_DISK_FOLDER_NAME', 'uploaded_files')
    LOCAL_FOLDER_PATH = env('LOCAL_FOLDER_PATH')
    TARGET_DATE = env('TARGET_DATE')

    files_by_date = get_files_by_date(LOCAL_FOLDER_PATH, TARGET_DATE)
    
    if files_by_date:
        print(f'Найдено {len(files_by_date)} файлов, содержащих дату {TARGET_DATE} в названии:')
        for file_path in files_by_date:
            filename = os.path.basename(file_path)
            upload_link = get_upload_link(YANDEX_DISK_FOLDER_NAME, filename, YANDEX_DISK_TOKEN)
            if upload_link:
                upload_file(file_path, upload_link)
            os.unlink(file_path)
    else:
        print(f'В папке {LOCAL_FOLDER_PATH} нет файлов с датой {TARGET_DATE} в названии.')