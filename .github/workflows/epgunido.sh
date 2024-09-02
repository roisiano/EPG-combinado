#!/bin/bash

# Almacenar el tiempo de inicio
start_time=$(date +%s)

# Descargar la guía y descomprimirla
curl -L -o guiatv_color.xml.gz "https://github.com/davidmuma/EPG_dobleM/raw/master/guiatv_color.xml.gz"
gunzip -c guiatv_color.xml.gz > EPGactual.xml

# Crear el archivo cabecera.xml
sed -n '1,/<programme start=/p' EPGactual.xml | head -n -1 > cabecera.xml

# Descargar los archivos previos desde GitHub
for i in {10..0}; do
  curl -L -o "$i.xml" "https://raw.githubusercontent.com/roisiano/EPG-combinado/main/$i.xml" || true
done

# Renombrar los archivos de días anteriores
for i in {9..0}; do
  if [ -f "$i.xml" ]; then
    mv "$i.xml" "$((i+1)).xml"
  fi
done

# Leer las fechas desde el archivo fechas.txt
source fechas.txt

# Crear un único archivo Futuro.xml basado en las fechas del archivo fechas.txt
> Futuro.xml
for j in {1..7}; do
  eval future_date=\$futuro$j
  sed -n "/<programme start=\"$future_date/,/<\/programme>/p; /<programme start=\"/ {/<programme start=\"$future_date/! {N; /<\/programme>/d;}}" EPGactual.xml >> Futuro.xml
done

# Crear el archivo 0.xml con la fecha actual
current_date=$(date +%Y%m%d)
output_file="0.xml"
sed -n "/<programme start=\"$current_date/,/<\/programme>/p; /<programme start=\"/ {/<programme start=\"$current_date/! {N; /<\/programme>/d;}}" EPGactual.xml > "$output_file"

# Crear el archivo EPGunido.xml comenzando con cabecera.xml
cat cabecera.xml > EPGunido.xml

# Añadir los contenidos de 10.xml a 0.xml en orden inverso
for i in {10..0}; do
    if [ -f "$i.xml" ]; then
        cat "$i.xml" >> EPGunido.xml
    fi
done

# Añadir el contenido de Futuro.xml
if [ -f Futuro.xml ]; then
    cat Futuro.xml >> EPGunido.xml
fi

# Añadir la línea final </tv> al archivo de salida
echo "</tv>" >> EPGunido.xml

# Subir todos los archivos generados a GitHub
git add .
git commit -m "Actualización diaria de EPG"
git push
