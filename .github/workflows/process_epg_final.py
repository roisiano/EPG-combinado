import os
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

def remove_old_files(directory, days_old):
    now = datetime.now()
    cutoff_date = now - timedelta(days=days_old)
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_date_str = filename.split('.')[0]
            try:
                file_date = datetime.strptime(file_date_str, '%Y%m%d')
                if file_date < cutoff_date:
                    os.remove(file_path)
            except ValueError:
                continue

def get_programme_entries(filename):
    entries = []
    tree = ET.parse(filename)
    root = tree.getroot()
    for programme in root.findall('programme'):
        entries.append(ET.tostring(programme, encoding='unicode'))
    return entries

def write_combined_epg(filename, entries):
    with open(filename, 'w') as file:
        file.write('<tv>\n')
        for entry in entries:
            file.write(entry + '\n')
        file.write('</tv>')

# Crear el directorio epg_files si no existe
os.makedirs('epg_files', exist_ok=True)

# Inicializar la lista de entradas
all_entries = []

# Procesar el archivo actual (EPGactual.xml)
with open('epg_files/20240830.xml', 'r') as file:  # Ajusta la fecha según el día actual
    root = ET.parse(file).getroot()
    for programme in root.findall('programme'):
        all_entries.append(ET.tostring(programme, encoding='unicode'))

# Procesar archivos históricos
for days in range(1, 6):  # Ajustar según el número de días a considerar
    date = datetime.now() - timedelta(days=days)
    file_date_str = date.strftime('%Y%m%d')
    file_path = f'epg_files/{file_date_str}.xml'
    if os.path.exists(file_path):
        new_entries = get_programme_entries(file_path)
        # Añadir solo las entradas que no se solapan
        for entry in new_entries:
            start_time = entry.split('start="')[1].split('"')[0]
            if not any(start_time in e for e in all_entries):
                all_entries.append(entry)

# Escribir el archivo EPGcompleto.xml
write_combined_epg('epg_files/EPGcompleto.xml', all_entries)
