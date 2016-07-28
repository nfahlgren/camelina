#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import argparse


# Parse command-line arguments
###########################################
def options():
    """Parse command line options.

    Args:

    Returns:
        argparse object.
    Raises:
        IOError: if genotypes does not exist.
        IOError: if table does not exist.
    """

    parser = argparse.ArgumentParser(description="Convert camelina plant barcodes to genotypes.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-g", "--genotypes", help="Input file containing the seed stock (genotypes) table. " +
                        "The file should be comma-separated. Columns barcode and genotype should exist.", required=True)
    parser.add_argument("-t", "--table",
                        help="Input file containing the phenotype/genotype table to be converted. " +
                             "First column should contain the ID to be converted. " +
                             "Assumes tab-delimited.", required=True)
    parser.add_argument("-o", "--outfile", help="Output file with converted IDs.", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.genotypes):
        raise IOError("Genotypes table does not exist: {0}".format(args.genotypes))
    if not os.path.exists(args.table):
        raise IOError("Phenotype/genotype table does not exist: {0}".format(args.table))

    return args


# Main
###########################################
def main():
    """Main program.

    Args:

    Returns:

    Raises:

    """

    # Get options
    args = options()

    # Read the genotypes file
    # Initialize genotype and column dictionaries
    genotype = {}
    cols = {}

    # Open genotypes file
    genotype_table = open(args.genotypes, 'r')

    # Read the first line to get the header
    header = genotype_table.readline().rstrip('\n')

    # Split the field names on commas
    fields = header.split(',')

    # Assign the column ID to each field name
    for i, field in enumerate(fields):
        cols[field] = i

    # Read the rest of the file and populate the barcode->genotype index
    for row in genotype_table:
        row = row.rstrip('\n')
        values = row.split(',')
        genotype[values[cols['barcode']]] = values[cols['genotype']]
        # If the plant has an alias barcode, store it also
        if len(values[cols['aliases']]) > 0:
            genotype[values[cols['aliases']]] = values[cols['genotype']]

    genotype_table.close()

    # Open output file
    out = open(args.outfile, 'w')

    # Open the phenotype/genotype table
    table = open(args.table, 'r')

    # Read the first line to get the header
    table_header = table.readline().rstrip('\n')

    # Split the field names on tabs
    table_fields = table_header.split('\t')

    # Append genotype to the table header
    table_fields.append('genotype')

    # Print out the table header
    out.write('\t'.join(map(str, table_fields)) + '\n')

    # Convert IDs for all rows
    for row in table:
        row = row.rstrip('\n')
        values = row.split('\t')
        # If the barcode is in the genotypes table, append it
        if values[0] in genotype:
            values.append(genotype[values[0]])
        else:
            # Otherwise, print an error and append NA
            print("The barcode {0} is not in the genotype table.".format(values[0]), file=sys.stderr)
            values.append('NA')
        out.write('\t'.join(map(str, values)) + '\n')

    table.close()
    out.close()


if __name__ == '__main__':
    main()
