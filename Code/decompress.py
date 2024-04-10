import os
import zipfile

folder = '../Outputs/'
compressed_files = []
for file in os.listdir(folder):
    if file[-4:] == '.zip':
        compressed_files.append(file)

for file in compressed_files:

    if file[:7] == 'details':

        out_folder = folder + 'details/'

    elif file[:8] == 'historia':

        out_folder = folder + 'historia/'

    elif file[:10] == 'litigantes':

        out_folder = folder + 'litigantes/'

    with zipfile.ZipFile(folder+file, 'r') as z:
        z.extractall(out_folder)
