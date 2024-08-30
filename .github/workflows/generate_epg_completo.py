import os
from lxml import etree

# Definir rutas
output_dir = 'epg-temporales'
epg_completo_path = '/tmp/epg/EPGcompleto.xml'
epg_actual_path = os.path.join(output_dir, 'EPGactual.xml')

# Crear un nuevo archivo EPGcompleto.xml
new_root = etree.Element('tv')

# Obtener la lista de archivos diarios
epg_files = sorted(
    [f for f in os.listdir(output_dir) if f.endswith('.xml') and f != 'EPGactual.xml'],
    reverse=True
)

# Agregar los programas de los archivos diarios al EPGcompleto.xml
for epg_file in epg_files:
    with open(os.path.join(output_dir, epg_file), 'r') as file:
        tree = etree.parse(file)
        for programme in tree.getroot():
            new_root.append(programme)

# Finalmente, agregar los programas del EPGactual.xml
with open(epg_actual_path, 'r') as file:
    tree = etree.parse(file)
    for programme in tree.getroot():
        new_root.append(programme)

# Guardar el EPGcompleto.xml
new_tree = etree.ElementTree(new_root)
new_tree.write(epg_completo_path, pretty_print=True, encoding='utf-8', xml_declaration=True)

# Mover EPGcompleto.xml al repositorio
os.replace(epg_completo_path, 'EPGcompleto.xml')
