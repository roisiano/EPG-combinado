import os
import re
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

# Directorios y archivos
output_dir = '/tmp/epg'
combined_file = f'{output_dir}/EPGcompleto.xml'
epg_actual_file = f'{output_dir}/epg.xml'

def parse_programmes(file_path):
    programmes = []
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    for programme in root.findall('programme'):
        start = programme.get('start')
        stop = programme.get('stop')
        channel = programme.get('channel')
        data = ET.tostring(programme, encoding='unicode')
        programmes.append((start, stop, channel, data))
    
    return programmes

def is_overlap(prog1, prog2):
    start1, stop1 = datetime.strptime(prog1[0], '%Y%m%d%H%M%S %z'), datetime.strptime(prog1[1], '%Y%m%d%H%M%S %z')
    start2, stop2 = datetime.strptime(prog2[0], '%Y%m%d%H%M%S %z'), datetime.strptime(prog2[1], '%Y%m%d%H%M%S %z')
    return not (stop1 <= start2 or stop2 <= start1)

def combine_epgs(output_dir, combined_file, epg_actual_file):
    programmes = []
    
    # Añadir el archivo actual completo
    programmes.extend(parse_programmes(epg_actual_file))
    
    # Eliminar archivos antiguos de más de 15 días
    cutoff_date = datetime.now() - timedelta(days=15)
    for file in os.listdir(output_dir):
        if file.endswith('.xml') and file != os.path.basename(epg_actual_file):
            file_path = os.path.join(output_dir, file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_mtime < cutoff_date:
                os.remove(file_path)
                print(f'Removido archivo antiguo: {file_path}')
    
    # Listar y procesar archivos de días anteriores
    files = sorted([f for f in os.listdir(output_dir) if f.endswith('.xml') and f != os.path.basename(epg_actual_file)],
                   key=lambda x: os.path.getmtime(os.path.join(output_dir, x)),
                   reverse=True)

    for epg_file in files:
        file_path = os.path.join(output_dir, epg_file)
        previous_programmes = parse_programmes(file_path)
        
        # Filtrar programas no solapados
        for prog in previous_programmes:
            if all(not is_overlap(prog, p) for p in programmes):
                programmes.append(prog)

    # Escribir el archivo combinado
    with open(combined_file, 'w') as outfile:
        outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        outfile.write('<tv>\n')
        for prog in programmes:
            outfile.write(prog[3])
        outfile.write('</tv>\n')

combine_epgs(output_dir, combined_file, epg_actual_file)
