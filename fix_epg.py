import sys
from lxml import etree

if len(sys.argv) < 3:
    print("Uso: python3 fix_epg.py <entrada.xml> <salida.xml>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

print("Reconstruyendo XML con parser tolerante...")

parser = etree.XMLParser(recover=True, huge_tree=True)

# Leer XML como stream
context = etree.iterparse(input_file, events=("end",), recover=True, huge_tree=True)

new_root = etree.Element("tv")
channels = []
programmes = []

for event, elem in context:
    if elem.tag == "channel":
        channels.append(elem)
    elif elem.tag == "programme":
        try:
            etree.tostring(elem)
            programmes.append(elem)
        except:
            print("⚠️ Eliminado programme corrupto")
    elem.clear()

print(f"Canales cargados: {len(channels)}")
print(f"Programas válidos: {len(programmes)}")

# Reconstruir XML limpio
for c in channels:
    new_root.append(c)

for p in programmes:
    new_root.append(p)

tree = etree.ElementTree(new_root)
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print("Validando XML final...")

try:
    etree.parse(output_file)
    print("✔️ XML válido")
except Exception as e:
    print("❌ XML inválido:", e)
    sys.exit(1)

