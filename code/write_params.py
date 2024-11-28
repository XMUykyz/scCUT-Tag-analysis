#Build a profile of single-cell Af-CUT-Tag data for running CUT-Tag workflows

import os

# Define the folder path to process
base_dir = 'split_data/barcode-trimmed'
# Generate a list of folders from b1 to b96
folders = [f'b{i}' for i in range(1, 97) ]

print(folders)

# Open a new configuration file for writing
with open('cut_tag_config.ymal', 'w') as config_file:
    # Writes to the header of the configuration file
    config_file.write('sample\tfastq1\tfastq2\n')

    # Walk through each folder
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        # Get all the files in the folder and sort them
        files = sorted(os.listdir(folder_path))

        # Assume that the file is saved in a standard naming format (e.g. A1_1.fq.gz, A1_2.fq.gz, etc.)
        for i in range(0, len(files), 2):
            # Get the paired file
            fastq1 = files[i]
            fastq2 = files[i + 1]

            # Make sure the files are paired correctly
            if fastq1.endswith('_1.fq.gz') and fastq2.endswith('_2.fq.gz'):
                # Extract sample name (e.g. A1)
                sample_name = fastq1.split('_')[0]
                # Generates a sample name that starts with the folder name
                full_sample_name = f"{folder}_{sample_name}"
                # Write to profile
                config_file.write(f'{full_sample_name}\t{os.path.join(folder_path, fastq1)}\t{os.path.join(folder_path, fastq2)}\n')

print("The configuration file cut_tag_config.txt is generated")
