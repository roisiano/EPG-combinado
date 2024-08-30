import os
import xml.etree.ElementTree as ET

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
    files = ['EPGactual.xml', 'epg.xml']
    all_programmes = []

    for file_path in files:
        file_path = os.path.join('/tmp/epg', file_path)
        programmes = parse_programmes_from_file(file_path)
        all_programmes.extend(programmes)

    # Save combined programmes to EPGcompleto.xml
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


