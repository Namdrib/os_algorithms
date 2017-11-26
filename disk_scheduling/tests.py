import unittest

import strategies

class TestStrategiesCalculateDistance(unittest.TestCase):
	def setUp(self):
		self.base_strat = strategies.SchedulingStrategy()
	def test_left_to_right_positive(self):
		self.assertEqual(1, self.base_strat.calculate_distance(1, 2))
	def test_left_to_right_zero(self):
		self.assertEqual(2, self.base_strat.calculate_distance(0, 2))
	def test_left_to_right_positive(self):
		self.assertEqual(1, self.base_strat.calculate_distance(1, 2))

class TestStrategyByName(unittest.TestCase):
	def get_class(self, strategy_name):
		return strategies.strategy_by_name(strategy_name)

	def test_fcfs(self):
		self.assertEqual(self.get_class("fcfs"), strategies.FCFS)
	def test_sstf(self):
		self.assertEqual(self.get_class("sstf"), strategies.SSTF)
	def test_scan(self):
		self.assertEqual(self.get_class("scan"), strategies.Scan)
	def test_cscan(self):
		self.assertEqual(self.get_class("cscan"), strategies.CScan)
	def test_look(self):
		self.assertEqual(self.get_class("look"), strategies.Look)
	def test_clook(self):
		self.assertEqual(self.get_class("clook"), strategies.CLook)

	# Sad path: DNE in strategies.name_to_class
	def test_nope(self):
		self.assertEqual(self.get_class("nope"), None)
	def test_fcf(self):
		self.assertEqual(self.get_class("fcf"), None)

# TODO : Direction and pivot
class TestStrategiesInput1(unittest.TestCase):

	def setUp(self):
		self.input1_requests = [(1, 86), (1, 147), (1, 91), (1, 177), (1, 94), (1, 150), (1, 102), (1, 175), (1, 130)]

	def create_and_exhaust(self, strategy_name):
		self.strat = strategies.strategy_by_name(strategy_name)(143, 200, "right", self.input1_requests)
		while self.strat.serve_next_request():
			pass

	def test_fcfs(self):
		self.create_and_exhaust("fcfs")
		self.assertEqual(self.strat.get_essential_stats(), [565, 130, "right"]) # left

	def test_sstf(self):
		self.create_and_exhaust("sstf")
		self.assertEqual(self.strat.get_essential_stats(), [162, 177, "right"])

	def test_scan(self):
		self.create_and_exhaust("scan")
		self.assertEqual(self.strat.get_essential_stats(), [169, 86, "right"]) # left

	def test_cscan(self):
		self.create_and_exhaust("cscan")
		self.assertEqual(self.strat.get_essential_stats(), [186, 130, "right"])

	def test_look(self):
		self.create_and_exhaust("look")
		self.assertEqual(self.strat.get_essential_stats(), [125, 86, "right"]) # left

	def test_clook(self):
		self.create_and_exhaust("clook")
		self.assertEqual(self.strat.get_essential_stats(), [78, 130, "right"]) # left

if __name__ == "__main__":
	unittest.main()
