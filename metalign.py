import argparse, math, os, random, subprocess, sys, time
from operator import mul
from functools import reduce
# Import metalign modules
import map_and_profile
import select_db


__location__ = os.path.realpath(os.path.join(os.getcwd(),
								os.path.dirname(__file__))) + '/'


def metalign_parseargs():  # handle user arguments
	parser = argparse.ArgumentParser(
		description='Runs full metalign pipeline on input reads file(s).')
	parser.add_argument('reads', help='Path to reads file.')
	parser.add_argument('--cutoff', type=float, default=-1.0,
		help='CMash cutoff value. Default is 1/(log10(reads file bytes)**2).')
	parser.add_argument('--db_dir', default = 'AUTO',
		help='Directory with all organism files in the full database.')
	parser.add_argument('--dbinfo_in', default='AUTO',
		help = 'Location of db_info file. Default: data/db_info.txt')
	parser.add_argument('--keep_temp_files', action = 'store_true',
		help='Keep temporary files instead of deleting after this script finishes.')
	parser.add_argument('--min_abundance', type=float, default=10**-4,
		help='Minimum abundance for a taxa to be included in the results.')
	parser.add_argument('--min_map', type=int, default=-1,
		help='Minimum bases mapped to count a hit.')
	parser.add_argument('--max_ed', type=int, default=999999999,
		help='Maximum edit distance from a reference to count a hit.')
	parser.add_argument('--no_len_normalization', action='store_true',
		help='Do not normalize abundances by genome length.')
	parser.add_argument('--no_rank_renormalization', action='store_true',
		help='Do not renormalize abundances to 100 percent at each rank,\
				for instance if an organism has a species but not genus label.')
	parser.add_argument('--output', default='abundances.tsv',
		help='Output abundances file. Default: abundances.txt')
	parser.add_argument('--pct_id', type=float, default=-1,
		help='Minimum percent identity from reference to count a hit.')
	parser.add_argument('--quantify_unmapped', action='store_true',
		help='Factor in unmapped reads in abundance estimation.')
	parser.add_argument('--read_cutoff', type=int, default=-1,
		help='Number of reads to count an organism as present.')
	parser.add_argument('--sampleID', default='NONE',
		help='Sample ID for output. Defaults to input file name(s).')
	parser.add_argument('--strain_level', action='store_true',
		help='Use this flag to profile strains (off by default).')
	parser.add_argument('--temp_dir', default = 'TEMP_metalign',
		help='Directory to write temporary files to.')
	parser.add_argument('--verbose', action='store_true',
		help='Print verbose output.')
	args = parser.parse_args()
	return args


def main():
	args = metalign_parseargs()
	# Set arguments that default to AUTO
	if args.dbinfo_in == 'AUTO':
		__location__ + 'data/db_info.txt'
	if args.db_dir == 'AUTO':
		__location__ + 'data/database/'

	# Ensure that arguments agree between scripts
	if not args.temp_dir.endswith('/'):
		args.temp_dir += '/'
	args.db = args.temp_dir + 'cmashed_db.fna'
	args.dbinfo = args.temp_dir + 'subset_db_info.txt'
	args.dbinfo_out = args.dbinfo
	args.infiles = args.reads
	args.assingment = 'proportional'
	args.cmash_results = 'NONE'

	# Run the database selection and map/profile routines
	select_main()  # runs select_db routine
	map_main()  # runs map_and_profile routine


if __name__ == '__main__':
	main()
#
