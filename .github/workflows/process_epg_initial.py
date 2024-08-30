import os
import requests
import gzip
import shutil
from datetime import datetime

# Configuración
url = "https://github.com/davidmuma/EPG_dobleM/raw/master/guiatv_color.xml.gz"
output_file_path = '/tmp/epg/epg.xml.gz'
today_date = datetime.now().strftime('%Y%m%d')

# Crear el directorio de trabajo
os.makedirs('/tmp/epg', exist_ok=True)

# Descargar el archivo comprimido
response = requests.get(url)
with open(output_file_path, 'wb') as f:
    f.write(response.content)

# Descomprimir el archivo
with gzip.open(output_file_path, 'rb') as f_in:
    with open('/tmp/epg/epg.xml', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

# Leer el archivo XML descomprimido
with open('/tmp/epg/epg.xml', 'r') as file:
    epg_content = file.read()

# Crear la carpeta epg_files si no existe
os.makedirs('epg_files', exist_ok=True)

# Guardar el archivo actual EPGactual.xml
with open(f'epg_files/{today_date}.xml', 'w') as file:
    file.write(epg_content)

