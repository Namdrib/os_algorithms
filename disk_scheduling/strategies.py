# This file includes the following disk scheudling strategies:
# - First Come First Serve (FCFS)
# - Shortest Seek Time First (SSTF)
# - Scan (Scan)
# - C-Scan (CScan)
# - Look (Look)
# - C-Look (CLook)
# --- All of these are child classes of SchedulingStrategy

# TODO : Moving left
#      : fix the sorting/splicing part if going left


class SchedulingStrategy:
	# requests is a list of pairs
	def __init__(self, position = 0, disk_size = 0, direction = "right", requests = []):
		self.position  = position
		self.disk_size = disk_size
		self.direction = direction
		self.requests  = requests
		self.pivots    = 0

		self.distance  = 0
		self.idle      = 0

		if direction == "left":
			reverse(self.requests)

	# Pick which request to service next, and return the request
	# If there are no requests left to service, return None
	# Child classes (different strategies) override this method
	def choose_request(self):
		return None if len(self.requests) == 0 else self.requests[0]

	# Calculate the distance between two requests
	# Typically used to find distance between current position and next service
	def calculate_distance(self, old, new):
		# print("going from {} to {}".format(int(old), int(new)))
		return abs(int(new) - int(old))

	# Returns the "next" request in requests in accordance with
	# the appropriate strategy (determined by child's serve_next_request)
	def serve_next_request(self):
		# Get next request
		request = self.choose_request()
		if request in self.requests:
			self.requests.remove(request)
		else:
			return

		# Update information
		delta_distance = self.calculate_distance(self.position, request[1])
		self.distance += delta_distance
		self.position = request[1]
		return request

	def print_results(self):
		print("travel distance: {}".format(self.distance))
		# print("idle time:       {}".format(self.idle_time))
		print("pivots:          {}".format(self.pivots))
		print("final position:  {}".format(self.position))
		print("final direction: {}".format(self.direction))

	def get_essential_stats(self):
		return [self.distance, self.position, self.direction]

# First come first serve
# Process in order of requests
class FCFS(SchedulingStrategy):
	pass

# A subset of SchedulingStrategies where the requests
# should be sorted by their position
class SchedulingStrategySorted(SchedulingStrategy):
	# requests is a list of pairs
	def __init__(self, position = 0, disk_size = 0, direction = "right", requests = []):
		super().__init__(position, disk_size, direction, requests)
		self.requests.sort(key = lambda tup: tup[1]) # sort by position

	def choose_request(self):
		return None if len(self.requests) == 0 else self.requests[0]

# Shortest seek time first
# Process in order of which is closest to current position
# if tie, choose the one in the current direction
# e.g. if current at 2, and requests at position 1 and 3
# choose 1 if moving left, 3 if moving right
class SSTF(SchedulingStrategySorted):
	def choose_request(self):
		# look for the one closest to current position
		temp_position = self.position
		best_dist = self.disk_size
		best_request = None
		for request in self.requests:
			current_distance = abs(temp_position - request[1])
			if current_distance < best_dist:
				best_dist = current_distance
				best_request = request
			# in the case distance is same, choose by direction (avoid pivoting)
			elif current_distance == best_request:
				if (request[1] > temp_position and self.direction == "right"):
					best_request = request

		if best_request:
			temp_position = best_request[1]
		return best_request

# Loop from 0 to disk_size-1 back to 0 (bounce off zero and reverse direction)
# Service any requests "along the way"
class Scan(SchedulingStrategySorted):
	def __init__(self, position = 0, disk_size = 0, direction = "right", requests = []):
		super().__init__(position, disk_size, direction, requests)
		# splice requests into order
		# [current, above current, ..., last, disk_size, 0, beginning, ..., current-1]
		lower_positions  = [x for x in self.requests if x[1] < self.position]
		higher_positions = [x for x in self.requests if x[1] > self.position]
		lower_positions.reverse()

		if self.disk_size-1 not in higher_positions:
			higher_positions.append((1, self.disk_size-1))
		higher_positions.extend(lower_positions)
		self.requests = higher_positions
		if self.direction == "left":
			reverse(self.requests)

# Loop from 0 to disk_size-1 back to 0 ("wrap" around from disk_size-1 to 0)
# Service any requests "along the way"
class CScan(SchedulingStrategySorted):
	def __init__(self, position = 0, disk_size = 0, direction = "right", requests = []):
		super().__init__(position, disk_size, direction, requests)
		# splice requests into order
		# [current, above current, ..., last, disk_size, 0, beginning, ..., current-1]
		lower_positions  = [x for x in self.requests if x[1] < self.position]
		higher_positions = [x for x in self.requests if x[1] > self.position]

		if 0 not in lower_positions:
			lower_positions.insert(0, (1, 0))
		if self.disk_size-1 not in higher_positions:
			higher_positions.append((1, self.disk_size-1))

		higher_positions.extend(lower_positions)
		self.requests = higher_positions
		if self.direction == "left":
			reverse(self.requests)

	def calculate_distance(self, old, new):
		cost = 0 if (old == self.disk_size-1 and new == 0) else abs(int(new) - int(old))
		print("going from {} to {} costs {}".format(int(old), int(new), cost))
		return cost
		# if self.direction == "right" and new > self.current_position:
		# 	return new - self.current_position
		# elif self.direction == "left" and new < self.current_position:
		# 	return self.current_position - new
		# pass

# Like Scan, but don't go "all the way to the end"
# if position x is the right-most request, turn back
class Look(SchedulingStrategySorted):
	def __init__(self, position = 0, disk_size = 0, direction = "right", requests = []):
		super().__init__(position, disk_size, direction, requests)
		# splice requests into order
		# [current, above current, ..., last, disk_size, 0, beginning, ..., current-1]
		lower_positions  = [x for x in self.requests if x[1] < self.position]
		higher_positions = [x for x in self.requests if x[1] > self.position]
		lower_positions.reverse()

		higher_positions.extend(lower_positions)
		self.requests = higher_positions
		if self.direction == "left":
			reverse(self.requests)

# Like CScan, but don't go "all the way to the end"
# if position x is the right-most request, wrap around to "next" request
class CLook(SchedulingStrategy):
	def __init__(self, position = 0, disk_size = 0, direction = "right", requests = []):
		super().__init__(position, disk_size, direction, requests)
		# splice requests into order
		# [current, above current, ..., last, disk_size, 0, beginning, ..., current-1]
		lower_positions  = sorted([x for x in self.requests if x[1] < self.position])
		higher_positions = sorted([x for x in self.requests if x[1] > self.position])

		higher_positions.extend(lower_positions)
		self.requests = higher_positions
		if self.direction == "left":
			reverse(self.requests)
		print(self.requests)

	def calculate_distance(self, old, new):
		temp = [x[1] for x in sorted(self.requests, key = lambda tup: tup[1])]
		# print("Temp is {}".format(temp))
		cost = abs(int(new) - int(old)) # default
		if (len(temp) == 0):
			return cost
		min_position = min(temp)
		max_position = max(temp)
		if self.direction == "left" and old <= min_position and new >= max_position:
			cost = 0
		elif self.direction == "right" and old >= max_position and new <= min_position:
			cost = 0
		print("Got {}".format(cost))
		return cost


name_to_class = {
	"fcfs":  FCFS,
	"sstf":  SSTF,
	"scan":  Scan,
	"cscan": CScan,
	"look":  Look,
	"clook": CLook
}

# Return a Strategy object based on name according to name_to_class
def strategy_by_name(name):
	return name_to_class[name] if name in name_to_class else None

if __name__ == "__main__":
	print("This module contains the SchedulingStrategy class and subclasses")
	implemented = ["fcfs", "sstf"]
	print(implemented)
