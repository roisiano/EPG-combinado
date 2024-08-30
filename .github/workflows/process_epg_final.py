import os
import xml.etree.ElementTree as ET
from datetime import datetime

def parse_programmes_from_file(file_path):
    programmes = []
    if os.path.exists(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        for programme in root.findall('programme'):
            programmes.append(programme)
    else:
        print(f"File not found: {file_path}")
    return programmes

def process_epg_files():
    # Order of files to process
    files = sorted(
        ['epg_files/EPGactual.xml', 'epg_files/29.08.2024.xml', 'epg_files/28.08.2024.xml', 'epg_files/27.08.2024.xml', 'epg_files/26.08.2024.xml', 'epg_files/25.08.2024.xml'],
        reverse=True
    )

    all_programmes = []
    existing_programmes = []

    # Read existing programmes from EPGcompleto.xml if it exists
    if os.path.exists('/tmp/epg/EPGcompleto.xml'):
        existing_tree = ET.parse('/tmp/epg/EPGcompleto.xml')
        existing_root = existing_tree.getroot()
        existing_programmes = existing_root.findall('programme')

    for file_path in files:
        programmes = parse_programmes_from_file(file_path)
        for programme in programmes:
            start_time = programme.get('start')
            if start_time:
                # Check if this programme overlaps with existing ones
                if not any(p.get('start') == start_time for p in existing_programmes):
                    all_programmes.append(programme)
                    existing_programmes.append(programme)

    # Save the final combined programmes to EPGcompleto.xml
    if all_programmes:
        root = ET.Element('tv')
        for programme in all_programmes:
            root.append(programme)
        tree = ET.ElementTree(root)
        output_path = '/tmp/epg/EPGcompleto.xml'
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        print(f"EPGcompleto.xml saved to {output_path}")

def main():
    process_epg_files()

if __name__ == "__main__":
    main()


