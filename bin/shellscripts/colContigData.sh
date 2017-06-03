#!/bin/bash
# From a M4 it returns a table with contig ID, its number of occurences and its length.
# Input:  stdin in M4 file format
# Output: stout
catContigDataM4.sh $1 | sort | uniq -c | sort -nr | awk '{print $2"	"$1"	"$3}'

