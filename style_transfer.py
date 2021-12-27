#!/usr/bin/env python3

import argparse
from vector_util import *
import sys

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', type=str, default='', dest='vector_file',
                        help='file containing vector data to transfer', required=False)
    parser.add_argument('-e', type=str, default='', dest='extract_from',
                        help='video to extract motion vector data from', required=False)
    parser.add_argument('-t', default='', type=str, dest='transfer_to', help='video to transfer motion vector data to')
    parser.add_argument(default='', type=str, dest='output',
                        help='output file either for the final video, or for the vector data')
    return parser.parse_args().__dict__


if __name__ == '__main__':
    # get args
    args = parse_args()
    vector_file = args['vector_file']
    extract_from = args['extract_from']
    transfer_to = args['transfer_to']
    output = args['output']

    # check that either extract_from or vector_file is given
    if not ((extract_from == '') ^ (vector_file == '')):
        print('Only one of -v or -e must be given')
        sys.exit()

    vectors = []

    if extract_from:
        # step 1a: extract vectors
        vectors = get_vectors(extract_from)

        # if we only have to extract the vectors, write to file and exit
        if transfer_to == '':
            with open(output, 'w') as f:
                json.dump(vectors, f)
            sys.exit()
    elif vector_file:
        # step 1b: read vectors from file
        if not transfer_to:
            print('Please specify file to transfer vectors to using -t')
            sys.exit()

        with open(vector_file, 'r') as f:
            vectors = json.load(f)

    # step 2: transfer vector data to file
    apply_vectors(vectors, transfer_to, output)
