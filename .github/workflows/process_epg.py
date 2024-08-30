import os
from datetime import datetime

# Directorios y archivos
output_dir = '/tmp/epg'
combined_file = f'{output_dir}/EPGcompleto.xml'
epg_actual_file = f'{output_dir}/epg.xml'

# Asegurarse de que el directorio existe
os.makedirs(output_dir, exist_ok=True)

# Verificar la existencia del archivo EPG actual
if not os.path.isfile(epg_actual_file):
    raise FileNotFoundError(f"El archivo EPG actual {epg_actual_file} no existe.")

# Filtrar por día
def filter_epg_by_day(target_date, input_file, output_file):
    date_filter = datetime.strptime(target_date, '%d.%m.%Y').strftime('%Y%m%d')
    print(f"Filtrando archivo: {input_file} para la fecha: {target_date}")
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        inside_programme = False
        for line in infile:
            if '<programme start=' in line:
                inside_programme = True
            if inside_programme:
                outfile.write(line)
            if '</tv>' in line:
                inside_programme = False

# Filtrar por fecha actual
today = datetime.now().strftime('%d.%m.%Y')
today_file = f'{output_dir}/{today}.xml'
filter_epg_by_day(today, epg_actual_file, today_file)

# Combinar EPGs
def combine_epgs(output_dir, combined_file, epg_actual_file):
    # Listar y combinar archivos EPG
    files = sorted([f for f in os.listdir(output_dir) if f.endswith('.xml')])

    if not files:
        print("No se encontraron archivos EPG previos.")
        # Si no hay archivos previos, el archivo combinado es solo el actual
        os.rename(epg_actual_file, combined_file)
        return

    # Primer archivo (el más antiguo)
    first_file = os.path.join(output_dir, files[0])
    with open(first_file, 'r') as infile, open(combined_file, 'w') as outfile:
        # Copiar el contenido del primer archivo sin la última línea </tv>
        lines = infile.readlines()
        outfile.writelines(lines[:-1])

    # Añadir archivos subsiguientes
    for epg_file in files[1:]:
        with open(os.path.join(output_dir, epg_file), 'r') as infile, open(combined_file, 'a') as outfile:
            lines = infile.readlines()
            inside_programme = False
            for line in lines:
                if '<programme start=' in line:
                    inside_programme = True
                if inside_programme:
                    outfile.write(line)

    # Añadir el archivo actual
    if os.path.isfile(epg_actual_file):
        with open(epg_actual_file, 'r') as infile, open(combined_file, 'a') as outfile:
            lines = infile.readlines()
            inside_programme = False
            for line in lines:
                if '<programme start=' in line:
                    inside_programme = True
                if inside_programme:
                    outfile.write(line)
        
        # Añadir la etiqueta de cierre </tv>
        with open(combined_file, 'a') as outfile:
            outfile.write('</tv>\n')

combine_epgs(output_dir, combined_file, epg_actual_file)

