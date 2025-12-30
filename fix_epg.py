import sys
from lxml import etree

input_file = sys.argv[1]
output_file = sys.argv[2]

print("Cargando XML...")
parser = etree.XMLParser(recover=True, huge_tree=True)

tree = etree.parse(input_file, parser)
root = tree.getroot()

print("Analizando programas...")

clean_programmes = []
removed = 0

for programme in root.findall("programme"):
    try:
        etree.tostring(programme)
        clean_programmes.append(programme)
    except Exception as e:
        removed += 1
        print(f"Eliminado <programme> corrupto: {e}")

print(f"Programas eliminados: {removed}")

print("Reconstruyendo XML limpio...")

new_root = etree.Element("tv")

# Copiar canales
for child in root:
    if child.tag != "programme":
        new_root.append(child)

# Copiar programas válidos
for p in clean_programmes:
    new_root.append(p)

tree = etree.ElementTree(new_root)
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print("EPG reparado generado:", output_file)
