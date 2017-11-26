import sys

import strategies


class Scheduler:
	# This constructor should be used - pass in the result of parser.parse_args()
	def __init__(self, args):
		self.requests = []         # list of pair <time, location> of requests in the file_handle
		self.disk_size = 0         # number of cylinders on the disk

		# Statistical information
		self.travel_distance = 0   # total distance (in cylinders) the head has moved
		self.idle_time = 0         # time spent idling (not servicing requests)
		self.num_pivots = 0        # number of times head has changd direction
		self.current_position = 0  # which cylinder the head is currently at

		# Set arg information
		self.direction = args.direction # either left or right. changes with pivots
		self.verbose = args.verbose

		# Read disk size, current position, and populate requests
		# assuming the file input is correctly sorted, requests stored in FIFO order
		with open(args.file) as file_handle:
			self.disk_size = int(file_handle.readline().rstrip())
			self.current_position = int(file_handle.readline().rstrip())
			for line in file_handle:
				time,position = line.rstrip().split(" ")
				self.requests.append((int(time), int(position)))

		self.algorithm = args.algorithm # which scheduling algorithm to use
		self.scheduling_strategy = strategies.strategy_by_name(self.algorithm)(self.current_position, self.disk_size, self.direction, self.requests)

		print("Algorithm: {}".format(self.algorithm))
		print("Verbose:   {}".format(self.verbose))
		print("Disk size: {}".format(self.disk_size))
		print(self.requests)

	def schedule(self):
		# Keep fetching and serving next request
		while self.serve_next_request():
			pass
		return

	def serve_next_request(self):
		return self.scheduling_strategy.serve_next_request()

	def print_results(self):
		self.scheduling_strategy.print_results()
