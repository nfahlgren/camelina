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
        IOError: if dir does not exist.
    """

    parser = argparse.ArgumentParser(description="Convert camelina plant barcodes to genotypes.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--dir", help="Input GWAS directory. ", required=True)
    parser.add_argument("-o", "--outfile", help="Output table file", required=True)
    parser.add_argument("-g", "--genotypes", help="Input genotype hapmap file.", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        raise IOError("GWAS directory does not exist: {0}".format(args.dir))
    if not os.path.exists(args.genotypes):
        raise IOError("Genotype hapmap file does not exist")
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
    hapmap=open(args.genotypes,"r")

    snps=[]
    hapmap.readline()
    for row in hapmap:
        cols=row.split("\t")
        snps.append(cols[2]+"."+cols[3])
    hapmap.close()
    out=open(args.outfile,"w")
    times=[]
    time={}
    for (dirpath, dirnames, filenames) in os.walk(args.dir):
        for filename in filenames:
            if filename[-16:]=="GWAS.Results.csv":
                pos={}
                name=filename.split(".")
                day=name[2]+"."+name[3]
                times.append(day)
                result=open(dirpath + "/" + filename,"r")
                result.readline()
                for row in result:
                    row=row.rstrip("\n")
                    cols=row.split(",")
                    pos[cols[1]+"."+cols[2]]=cols[8]
                result.close()
                time[day]=pos
    out.write("time,"+",".join(map(str,snps))+"\n")
    for t in times:
        values=[t]
        for snp in snps:
            values.append(time[t][snp])
        out.write(",".join(map(str,values))+"\n")

    out.close()

if __name__ == '__main__':
    main()
