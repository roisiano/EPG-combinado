import os

def merge_epg_files(complete_file, current_file):
    # Leer el archivo EPGactual.xml
    with open(current_file, 'r') as f:
        current_content = f.read()

    # Leer el archivo EPGcompleto.xml
    with open(complete_file, 'r') as f:
        complete_content = f.read()

    # Encuentra el primer <programme start= en el archivo EPGcompleto.xml
    first_programme_index = complete_content.find('<programme start=')

    if first_programme_index != -1:
        # Conservar solo las entradas después del primer <programme start=
        complete_content = complete_content[first_programme_index:]

    # Encontrar el índice de la última etiqueta </programme>
    last_programme_index = complete_content.rfind('</programme>')
    
    # Añadir la línea </tv> después del último </programme>
    if last_programme_index != -1:
        complete_content = complete_content[:last_programme_index + len('</programme>')] + '\n</tv>'

    # Obtener la parte antes del primer <programme start= de EPGactual.xml
    current_pre_programme_content = current_content.split('<programme start=', 1)[0]

    # Escribir el contenido final en EPGcompleto.xml
    with open(complete_file, 'w') as f:
        f.write(current_pre_programme_content + complete_content)

def main():
    today = '20240830'  # Cambia esto según sea necesario
    current_file = f'/tmp/epg/{today}.xml'
    complete_file = '/tmp/epg/EPGcompleto.xml'

    # Merge EPG files
    merge_epg_files(complete_file, current_file)

if __name__ == "__main__":
    main()
