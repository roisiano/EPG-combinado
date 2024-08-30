import os
import requests
import gzip
import shutil

def download_and_extract_epg(url, output_dir, output_file):
    """Download and extract EPG file from URL."""
    response = requests.get(url, stream=True)
    gz_file_path = os.path.join(output_dir, 'epg.xml.gz')
    
    # Save the gzipped file
    with open(gz_file_path, 'wb') as f:
        f.write(response.content)
    
    # Decompress the gzipped file
    with gzip.open(gz_file_path, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def main():
    epg_url = 'https://github.com/davidmuma/EPG_dobleM/raw/master/guiatv_color.xml.gz'
    output_dir = '/tmp/epg'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'EPGactual.xml')

    download_and_extract_epg(epg_url, output_dir, output_file)

if __name__ == "__main__":
    main()
