import os
import xml.etree.ElementTree as ET
from datetime import datetime

def download_and_process_epg():
    # Define paths
    epg_actual_path = '/tmp/epg/epg.xml'
    epg_completo_path = '/tmp/epg/EPGcompleto.xml'

    # Create EPGcompleto.xml with the content of EPGactual.xml
    if not os.path.exists(epg_actual_path):
        print(f"El archivo {epg_actual_path} no existe.")
        return

    # Copy the entire content of EPGactual.xml to EPGcompleto.xml
    with open(epg_actual_path, 'r') as src_file:
        epg_actual_content = src_file.read()

    # Write the content to EPGcompleto.xml
    with open(epg_completo_path, 'w') as dest_file:
        dest_file.write(epg_actual_content)

if __name__ == "__main__":
    download_and_process_epg()
