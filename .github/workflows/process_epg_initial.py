import requests
import os
from datetime import datetime, timedelta
import re

EPG_FILES_DIR = '/tmp/epg'
DAYS_TO_KEEP = 15

def fetch_and_save_epg_file(url, file_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)

def parse_and_save_daily_files():
    # Eliminar archivos antiguos
    now = datetime.now()
    for file_name in os.listdir(EPG_FILES_DIR):
        if file_name.endswith('.xml') and file_name != 'EPGactual.xml':
            file_path = os.path.join(EPG_FILES_DIR, file_name)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if now - file_mtime > timedelta(days=DAYS_TO_KEEP):
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")

    # Aquí puedes añadir el código para dividir y guardar archivos diarios

def main():
    os.makedirs(EPG_FILES_DIR, exist_ok=True)
    url = 'https://github.com/davidmuma/EPG_dobleM/raw/master/guiatv_color.xml.gz'
    file_path = os.path.join(EPG_FILES_DIR, 'epg.xml.gz')
    fetch_and_save_epg_file(url, file_path)
    os.system(f'gunzip {file_path}')
    file_path = file_path.rstrip('.gz')  # Remove the .gz extension for further processing
    parse_and_save_daily_files()

if __name__ == "__main__":
    main()



