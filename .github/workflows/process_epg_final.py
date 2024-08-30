import os
import glob
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def load_epg_from_file(filepath):
    """Load EPG data from a file into a dictionary."""
    if not os.path.exists(filepath):
        return {}

    tree = ET.parse(filepath)
    root = tree.getroot()
    epg_data = {}

    for programme in root.findall('programme'):
        start = programme.get('start')
        channel = programme.get('channel')
        if start and channel:
            key = (channel, start)
            epg_data[key] = ET.tostring(programme, encoding='unicode')

    return epg_data

def update_epg_completo(epg_completo_path, epg_data):
    """Update EPGcompleto.xml with new data."""
    # Initialize EPGcompleto.xml if it doesn't exist
    if not os.path.exists(epg_completo_path):
        with open(epg_completo_path, 'w') as file:
            file.write('<tv>\n')

    # Append new data to EPGcompleto.xml
    with open(epg_completo_path, 'a') as file:
        for key, programme_str in sorted(epg_data.items(), key=lambda x: (x[0][0], x[0][1])):
            file.write(programme_str + '\n')
        file.write('</tv>')

def remove_old_files(directory, days_old):
    """Remove files older than the specified number of days."""
    cutoff_date = datetime.now() - timedelta(days=days_old)
    for filename in glob.glob(os.path.join(directory, '*.xml')):
        file_date_str = os.path.basename(filename).replace('.xml', '')
        try:
            file_date = datetime.strptime(file_date_str, '%Y%m%d')
            if file_date < cutoff_date:
                os.remove(filename)
                print(f"Removed old file: {filename}")
        except ValueError:
            continue

def process_final():
    """Main function to process the final EPG file."""
    epg_dir = '/tmp/epg/'
    epg_completo_path = os.path.join(epg_dir, 'EPGcompleto.xml')
    days_old = 15

    # Remove old files
    remove_old_files(epg_dir, days_old)

    # Load EPG data from the initial EPGcompleto.xml
    epg_data = load_epg_from_file(epg_completo_path)

    # Process each previous day's EPG files
    for filename in sorted(glob.glob(os.path.join(epg_dir, '*.xml')), reverse=True):
        if filename == epg_completo_path:
            continue

        new_epg_data = load_epg_from_file(filename)
        for key, programme_str in new_epg_data.items():
            if key not in epg_data:
                epg_data[key] = programme_str

    # Update EPGcompleto.xml
    update_epg_completo(epg_completo_path, epg_data)

if __name__ == "__main__":
    process_final()

