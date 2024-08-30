import os
from datetime import datetime
from lxml import etree

# Definir rutas
epg_dir = '/tmp/epg'
output_dir = 'epg-temporales'
os.makedirs(output_dir, exist_ok=True)

# Fecha actual para el nombre del archivo
current_date = datetime.now().strftime('%Y%m%d')

# Archivo EPGactual.xml
epg_actual_path = os.path.join(epg_dir, 'EPGactual.xml')
daily_epg_filename = f'{current_date}.xml'
daily_epg_path = os.path.join(output_dir, daily_epg_filename)

# Leer EPGactual.xml
with open(epg_actual_path, 'r') as file:
    tree = etree.parse(file)

# Filtrar programas del día actual
root = tree.getroot()
programmes = root.findall(f"./programme[starts-with(@start, '{current_date}')]")

# Crear el nuevo archivo con los programas filtrados
new_root = etree.Element('tv')
for programme in programmes:
    new_root.append(programme)

new_tree = etree.ElementTree(new_root)
new_tree.write(daily_epg_path, pretty_print=True, encoding='utf-8', xml_declaration=True)

# Mover EPGactual.xml a la carpeta epg-temporales
os.replace(epg_actual_path, os.path.join(output_dir, 'EPGactual.xml'))
