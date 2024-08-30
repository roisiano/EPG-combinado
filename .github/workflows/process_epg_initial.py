import shutil

def process_initial_epg():
    source_file = '/tmp/epg/epg.xml'
    dest_file = '/tmp/epg/EPGactual.xml'
    shutil.copy(source_file, dest_file)
    print(f"EPGactual.xml generated: {dest_file}")

def main():
    process_initial_epg()

if __name__ == "__main__":
    main()




