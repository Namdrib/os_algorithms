import argparse

# my files
from scheduler import Scheduler

def argparse_setup():
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="Running a disk scheduling algorithm on a given input file"
	)

	parser.add_argument(
		"-f", "--file",
		required = True,
		help = "the input file to read"
	)

	parser.add_argument(
		"-a", "--algorithm",
		default = "scan",
		choices = ["fcfs", "sstf", "scan", "cscan", "look", "clook"],
		help = "which disk scheduling algorithm to use"
	)

	parser.add_argument(
		"-d", "--direction",
		default = "right",
		choices = ["left", "right"],
		help = "initial direction of disk head"
	)

	parser.add_argument(
		"-v", "--verbose",
		action = "count",
		help = "increase the verbosity"
	)

	return parser

def main():
	parser = argparse_setup()
	args = parser.parse_args()
	# print(parser)

	scheduler = Scheduler(args)
	scheduler.schedule()
	scheduler.print_results()


if __name__ == "__main__":
	main()
