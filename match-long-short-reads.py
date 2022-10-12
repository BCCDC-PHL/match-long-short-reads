#!/usr/bin/env python3

import argparse
import csv
import glob
import json
import os
import sys

def parse_short_reads(short_read_fastq_paths):
    short_reads_by_sample_id = {}
    for short_read_fastq_path in short_read_fastq_paths:
        fastq_filename = os.path.basename(short_read_fastq_path)
        sample_id = fastq_filename.split('_')[0]
        r1_r2 = fastq_filename.split('_')[1].split('.')[0]
        if sample_id in short_reads_by_sample_id:
            short_reads_by_sample_id[sample_id][r1_r2] = short_read_fastq_path
        else:
            short_reads_by_sample_id[sample_id] = {"ID": sample_id}
            short_reads_by_sample_id[sample_id][r1_r2] = short_read_fastq_path

    return short_reads_by_sample_id


def parse_long_reads(long_read_fastq_paths):
    long_reads_by_sample_id = {}
    for long_read_fastq_path in long_read_fastq_paths:
        fastq_filename = os.path.basename(long_read_fastq_path)
        sample_id = fastq_filename.split('_')[0]
        if sample_id in long_reads_by_sample_id:
            long_reads_by_sample_id[sample_id]['LONG'] = long_read_fastq_path
        else:
            long_reads_by_sample_id[sample_id] = {"ID": sample_id}
            long_reads_by_sample_id[sample_id]['LONG'] = long_read_fastq_path

    return long_reads_by_sample_id
    

def match_long_reads_to_short(short_reads_by_sample_id, long_reads_by_sample_id):
    matched_short_long_reads = {}
    for sample_id, reads in short_reads_by_sample_id.items():
        if sample_id in long_reads_by_sample_id:
            reads['LONG'] = long_reads_by_sample_id[sample_id]['LONG']
            matched_short_long_reads[sample_id] = reads

    return matched_short_long_reads


def main(args):
    short_read_fastqs = glob.glob(os.path.join(args.short_read_dir, '*' + args.fastq_suffix))
    short_reads_by_sample_id = parse_short_reads(short_read_fastqs)

    long_read_fastqs = glob.glob(os.path.join(args.all_reads_dir, '*', '*' + args.long_read_suffix))
    long_reads_by_sample_id = parse_long_reads(long_read_fastqs)
    
    matched_short_long_reads = match_long_reads_to_short(short_reads_by_sample_id, long_reads_by_sample_id)

    # print(json.dumps(matched_short_long_reads, indent=2))
    output_fieldnames = [
        'ID',
        'R1',
        'R2',
        'LONG',
    ]
    writer = csv.DictWriter(sys.stdout, fieldnames=output_fieldnames, dialect='unix', quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for sample_id, row in matched_short_long_reads.items():
        writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--short-read-dir')
    parser.add_argument('-a', '--all-reads-dir')
    parser.add_argument('-f', '--fastq-suffix', default= "fastq.gz")
    parser.add_argument('-l', '--long-read-suffix', default= "RL.fastq.gz")
    args = parser.parse_args()
    main(args)
