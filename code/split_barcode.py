#Usage
#python split_barcode.py -p barcode-rename.txt -1 R1_fq.gz -2 R2_fq.gz

import gzip
import argparse
from Bio import SeqIO
from itertools import product

# Read the barcode file and generate the barcode dictionary
def read_barcode_file(filename):
    barcodes_5 = {}
    barcodes_3 = {}
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('5'):
                parts = line.strip().split()
                barcodes_5[parts[1]] = parts[2]
            elif line.startswith('3'):
                parts = line.strip().split()
                barcodes_3[parts[1]] = parts[2]
    return barcodes_5, barcodes_3

# Matching barcode allows a base mismatch
def match_barcode(seq, barcode):
    mismatches = sum(1 for a, b in zip(seq, barcode) if a != b)
    return mismatches <= 1

# Split raw data according to barcode combination
def split_fastq_by_barcodes(file1, file2, barcodes_5, barcodes_3):
    # Generate all possible barcode combinations
    combinations = list(product(barcodes_5.keys(), barcodes_3.keys()))
    out_files = {comb: (gzip.open(f'{comb[0]}{comb[1]}_1.fq.gz', 'wt'), gzip.open(f'{comb[0]}{comb[1]}_2.fq.gz', 'wt')) for comb in combinations}
    
    with gzip.open(file1, "rt") as handle1, gzip.open(file2, "rt") as handle2:
        records1 = SeqIO.parse(handle1, "fastq")
        records2 = SeqIO.parse(handle2, "fastq")
        
        for record1, record2 in zip(records1, records2):
            seq1 = str(record1.seq)
            seq2 = str(record2.seq)
            
            for barcode_5, sequence_5 in barcodes_5.items():
                if match_barcode(seq1[:len(sequence_5)], sequence_5):
                    for barcode_3, sequence_3 in barcodes_3.items():
                        if match_barcode(seq2[:len(sequence_3)], sequence_3):
                            SeqIO.write(record1, out_files[(barcode_5, barcode_3)][0], "fastq")
                            SeqIO.write(record2, out_files[(barcode_5, barcode_3)][1], "fastq")
                            break
    
    for f1, f2 in out_files.values():
        f1.close()
        f2.close()

# 主程序
def main():
    parser = argparse.ArgumentParser(description='Split FASTQ files by barcodes.')
    parser.add_argument('-p', '--params', required=True, help='Path to params.txt file.')
    parser.add_argument('-1', '--fastq1', required=True, help='Path to 1_fq.gz file.')
    parser.add_argument('-2', '--fastq2', required=True, help='Path to 2_fq.gz file.')
    args = parser.parse_args()

    barcodes_5, barcodes_3 = read_barcode_file(args.params)
    split_fastq_by_barcodes(args.fastq1, args.fastq2, barcodes_5, barcodes_3)

if __name__ == "__main__":
    main()
