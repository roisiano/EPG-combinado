import sys
from lxml import etree

if len(sys.argv) < 3:
    print("Uso: python3 fix_epg.py <entrada.xml> <salida.xml>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

print("Cargando XML original...")
parser = etree.XMLParser(recover=True, huge_tree=True)

try:
    tree = etree.parse(input_file, parser)
except Exception as e:
    print("❌ Error cargando el XML:", e)
    sys.exit(1)

root = tree.getroot()

print("Analizando <programme> uno por uno...")

clean_programmes = []
removed = 0

for programme in root.findall("programme"):
    try:
        # Intentar serializar el nodo para detectar errores internos
        etree.tostring(programme)
        clean_programmes.append(programme)
    except Exception as e:
        removed += 1
        print(f"⚠️ Eliminado <programme> corrupto: {e}")

print(f"Programas eliminados: {removed}")

print("Reconstruyendo XML limpio...")

# Crear nuevo root <tv>
new_root = etree.Element("tv")

# Copiar todos los nodos que NO son <programme> (ej: <channel>)
for child in root:
    if child.tag != "programme":
        new_root.append(child)

# Añadir solo los programas válidos
for p in clean_programmes:
    new_root.append(p)

# Guardar XML limpio
tree = etree.ElementTree(new_root)
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print("Archivo reparado generado:", output_file)

# Validación final
print("Validando XML final...")

try:
    etree.parse(output_file)
    print("✔️ XML válido")
except Exception as e:
    print("❌ XML inválido:", e)
    sys.exit(1)
