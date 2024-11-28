# Remove the barcode sequence from all.fq.gz suffix files in a folder
# python remove_barcode.py -i /path/to/input_directory -o /path/to/output_directory

import os
import subprocess
import argparse

# Define a fixed sequence and barcode list
fixed_sequence = 'AGATGTGTATAAGAGACAG'
barcodes_5 = [
    'CATTGGT', 'CCGTAGT', 'GAAGCCTT', 'TGACGCTTA',
    'ACCTTGTCGG', 'GGTACTTCTTC', 'TACAGGCCTCCT', 'TTCGTCAAGGTCC','ATCCGTTCTCCTCC',
    'GTGCGAAT','ACACCAAGA','GCTGCTCAAC','AGTGACCTACT','CCGATCTTAGCC','CATAAGGATCCTC','TGGCGATCCAATGC'
]
barcodes_3 = [
    'CGTAATAGGAG', 'GTGACCGCAAGAAC', 'CGGAGACTT', 'ACTCGGAATGC','AGAGAG','TTACTGGCATCC','ACGATGCACTTAAC','GCGTATCTCTTGCG','TCTTCTCGCTC','TACCTCGCACTCGA','GAAGCACTAGACC','CACACGCTT'
]

# Generate cutadapt parameters
cutadapt_params_5 = ' '.join([f'-g {barcode}{fixed_sequence}' for barcode in barcodes_5])
cutadapt_params_3 = ' '.join([f'-g {barcode}{fixed_sequence}' for barcode in barcodes_3])

def process_files(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through all FASTQ files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.fq.gz'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # Determine whether it is 1 end or 2 end
            if '_1.fq.gz' in filename:
                cutadapt_params = cutadapt_params_5
            elif '_2.fq.gz' in filename:
                cutadapt_params = cutadapt_params_3
            else:
                continue

            # Build the cutadapt command
            cmd = f'cutadapt {cutadapt_params} -o {output_path} {input_path} --cores 12'
            print(f'Processing {input_path} with command: {cmd}')
            subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process FASTQ files to remove barcodes and fixed sequences.')
    parser.add_argument('-i', '--input_dir', required=True, help='Directory containing input FASTQ files.')
    parser.add_argument('-o', '--output_dir', required=True, help='Directory to save processed FASTQ files.')
    args = parser.parse_args()

    process_files(args.input_dir, args.output_dir)
