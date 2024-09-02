#!/bin/sh

# Obtener la fecha actual en formato YYYY-MM-DD
diaactual_normal=$(date +"%Y-%m-%d")

# Convertir fecha en formato YYYY-MM-DD a componentes numéricos
year=$(echo $diaactual_normal | cut -c1-4)
month=$(echo $diaactual_normal | cut -c6-7)
day=$(echo $diaactual_normal | cut -c9-10)

# Función para sumar días a una fecha
suma_dias() {
    local base_year=$1
    local base_month=$2
    local base_day=$3
    local days_to_add=$4

    # Convertir fecha a segundos desde 1970-01-01
    local base_seconds=$(($(date -d "$base_year-$base_month-$base_day" +%s) + days_to_add * 86400))

    # Convertir segundos a fecha
    local new_date=$(date -d "@$base_seconds" +"%Y-%m-%d")
    echo $new_date
}

# Calcular fechas futuras
futuro1_normal=$(suma_dias $year $month $day 1)
futuro2_normal=$(suma_dias $year $month $day 2)
futuro3_normal=$(suma_dias $year $month $day 3)
futuro4_normal=$(suma_dias $year $month $day 4)
futuro5_normal=$(suma_dias $year $month $day 5)
futuro6_normal=$(suma_dias $year $month $day 6)
futuro7_normal=$(suma_dias $year $month $day 7)

# Guardar las fechas en el archivo fechas.txt
echo "diaactual=$diaactual_normal" > fechas.txt
echo "futuro1=$futuro1_normal" >> fechas.txt
echo "futuro2=$futuro2_normal" >> fechas.txt
echo "futuro3=$futuro3_normal" >> fechas.txt
echo "futuro4=$futuro4_normal" >> fechas.txt
echo "futuro5=$futuro5_normal" >> fechas.txt
echo "futuro6=$futuro6_normal" >> fechas.txt
echo "futuro7=$futuro7_normal" >> fechas.txt

# Eliminar guiones de las fechas en el archivo
sed -i 's/-//g' fechas.txt

echo "Fechas guardadas en fechas.txt sin guiones."
