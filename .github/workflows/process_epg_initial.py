import os
import requests
import gzip
import shutil
import datetime

def download_and_extract_epg():
    url = "https://github.com/davidmuma/EPG_dobleM/raw/master/guiatv_color.xml.gz"
    response = requests.get(url)
    with open('/tmp/epg/epg.xml.gz', 'wb') as f:
        f.write(response.content)
    with gzip.open('/tmp/epg/epg.xml.gz', 'rb') as f_in:
        with open('/tmp/epg/epg.xml', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def generate_daily_files():
    with open('/tmp/epg/epg.xml', 'r') as file:
        content = file.read()

    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    output_file = f'/tmp/epg/EPGactual.xml'
    with open(output_file, 'w') as file:
        file.write(content)

    days_to_keep = 5
    for i in range(days_to_keep, 0, -1):
        date_str = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%d.%m.%Y")
        daily_file_path = f'/tmp/epg/{date_str}.xml'
        if os.path.exists(daily_file_path):
            continue
        with open(daily_file_path, 'w') as file:
            file.write(content)

def main():
    download_and_extract_epg()
    generate_daily_files()

if __name__ == "__main__":
    main()


