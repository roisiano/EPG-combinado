import os
import re
from datetime import datetime, timedelta

EPG_FILES_DIR = '/tmp/epg'
DAYS_TO_KEEP = 15

def parse_programmes_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    programmes = re.findall(r'<programme start="[^"]*" stop="[^"]*" channel="[^"]*">.*?</programme>', content, re.DOTALL)
    return programmes

def delete_old_files():
    now = datetime.now()
    for file_name in os.listdir(EPG_FILES_DIR):
        if file_name.endswith('.xml') and file_name != 'EPGactual.xml':
            file_path = os.path.join(EPG_FILES_DIR, file_name)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if now - file_mtime > timedelta(days=DAYS_TO_KEEP):
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")

def process_epg_files():
    delete_old_files()  # Eliminar archivos antiguos

    epg_files = sorted(
        [f for f in os.listdir(EPG_FILES_DIR) if f.endswith('.xml') and f != 'EPGactual.xml'],
        reverse=True
    )
    epg_files.insert(0, 'EPGactual.xml')  # Insertar primero el archivo actual

    print(f"Processing files: {epg_files}")

    programmes_dict = {}

    for file_name in epg_files:
        file_path = os.path.join(EPG_FILES_DIR, file_name)
        programmes = parse_programmes_from_file(file_path)
        
        for programme in programmes:
            start_time = re.search(r'start="([^"]*)"', programme).group(1)
            channel = re.search(r'channel="([^"]*)"', programme).group(1)
            key = f'{start_time}_{channel}'
            if key not in programmes_dict:
                programmes_dict[key] = programme
            else:
                existing_start_time = re.search(r'start="([^"]*)"', programmes_dict[key]).group(1)
                existing_date = datetime.strptime(existing_start_time[:-6], '%Y%m%d%H%M%S')  # Comparar sin desfase horario
                new_date = datetime.strptime(start_time[:-6], '%Y%m%d%H%M%S')  # Comparar sin desfase horario
                if new_date > existing_date:
                    programmes_dict[key] = programme

    output_file = os.path.join(EPG_FILES_DIR, 'EPGcompleto.xml')
    with open(output_file, 'w') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n')
        for programme in programmes_dict.values():
            file.write(programme + '\n')
        file.write('</tv>\n')
    print(f"EPGcompleto.xml generated: {output_file}")

def main():
    process_epg_files()

if __name__ == "__main__":
    main()




