# conda install -c conda-forge exiftool
# !! remember to activate conda ve

import sys
import exiftool

def extractAndPrint(file):
    print("\n", file, "\n")
    with exiftool.ExifToolHelper() as et:
        metadata_list = et.get_metadata(file)
    for metadata in metadata_list:
        print(f'Metadata for file {metadata["SourceFile"]}:')
    for key, value in metadata.items():
        print(f'{key}: {value}')
        
for filespaths in sys.argv[1:]:
    extractAndPrint(filespaths)