import os
from datetime import datetime
import xml.etree.ElementTree as ET

# Directorios y archivos
output_dir = '/tmp/epg'
combined_file = f'{output_dir}/EPGcompleto.xml'
epg_actual_file = f'{output_dir}/epg.xml'

def extract_programmes(file_path):
    programmes = []
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    for programme in root.findall('programme'):
        programmes.append(ET.tostring(programme, encoding='unicode'))
    
    return programmes

def sort_and_deduplicate_programmes(programmes):
    programme_dict = {}

    for programme in programmes:
        tree = ET.fromstring(programme)
        start_time = tree.get('start')
        channel = tree.get('channel')
        key = (channel, start_time)
        
        start_time_dt = datetime.strptime(start_time, '%Y%m%d%H%M%S %z')
        
        if key not in programme_dict:
            programme_dict[key] = (programme, start_time_dt)
        else:
            existing_programme, existing_time = programme_dict[key]
            if start_time_dt > existing_time:
                programme_dict[key] = (programme, start_time_dt)

    unique_programmes = [prog[0] for prog in sorted(programme_dict.values(), key=lambda x: (x[1], x[0]))]
    
    return unique_programmes

def combine_epgs(output_dir, combined_file, epg_actual_file):
    files = sorted([f for f in os.listdir(output_dir) if f.endswith('.xml') and f != os.path.basename(epg_actual_file)],
                   key=lambda x: os.path.getmtime(os.path.join(output_dir, x)),
                   reverse=True)

    all_programmes = []

    # Añadir el archivo actual completo
    with open(epg_actual_file, 'r') as infile:
        all_programmes.append(infile.read())
    
    # Añadir programas de archivos previos, ordenando por fecha de archivo (más reciente primero)
    programmes = []
    for epg_file in files:
        file_path = os.path.join(output_dir, epg_file)
        programmes.extend(extract_programmes(file_path))
    
    programmes.extend(extract_programmes(epg_actual_file))
    
    # Ordenar y deduplicar todos los programas
    programmes = sort_and_deduplicate_programmes(programmes)
    
    # Escribir el archivo combinado
    with open(combined_file, 'w') as outfile:
        outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        outfile.write('<tv>\n')
        outfile.write(''.join(programmes))
        outfile.write('</tv>\n')

combine_epgs(output_dir, combined_file, epg_actual_file)

