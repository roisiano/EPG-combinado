import os
import re
from datetime import datetime

def process_epg_files():
    epg_files = sorted(
        [f for f in os.listdir('/tmp/epg') if f.endswith('.xml') and f != 'EPGactual.xml'],
        reverse=True
    )
    epg_files.insert(0, 'EPGactual.xml')  # Insert the current day file first

    combined_programmes = []
    programmes_dict = {}

    for file_name in epg_files:
        with open(f'/tmp/epg/{file_name}', 'r') as file:
            content = file.read()
        
        programmes = re.findall(r'<programme start="[^"]*" stop="[^"]*" channel="[^"]*">.*?</programme>', content, re.DOTALL)
        
        for programme in programmes:
            start_time = re.search(r'start="([^"]*)"', programme).group(1)
            channel = re.search(r'channel="([^"]*)"', programme).group(1)
            key = f'{start_time}_{channel}'
            if key not in programmes_dict:
                programmes_dict[key] = programme
            else:
                existing_start_time = re.search(r'start="([^"]*)"', programmes_dict[key]).group(1)
                existing_date = datetime.strptime(existing_start_time, '%Y%m%d%H%M%S')
                new_date = datetime.strptime(start_time, '%Y%m%d%H%M%S')
                if new_date > existing_date:
                    programmes_dict[key] = programme

    with open('/tmp/epg/EPGcompleto.xml', 'w') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n')
        for programme in programmes_dict.values():
            file.write(programme + '\n')
        file.write('</tv>\n')

def main():
    process_epg_files()

if __name__ == "__main__":
    main()

