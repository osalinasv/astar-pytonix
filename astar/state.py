

class State(object):

	def __init__(self, positions: [tuple]):
		self.positions = positions
		self.cost      = 0
		self.heuristic = 0
		self.f_cost    = 0
		self.prev_state: State = None

	def set_cost(self, cost: int, heuristic: int) -> int:
		self.cost = cost
		self.heuristic = heuristic
		self.f_cost = self.cost + self.heuristic

		return self.f_cost

	def __eq__(self, value) -> bool:
		return False if value is None else self.positions == value.positions

	def __lt__(self, value):
	 return True if value is None else self.f_cost < value.f_cost and self.cost < value.cost

	def __hash__(self) -> int:
		return sum([hash(p) for p in self.positions])

	def __str__(self):
		return 'S{}'.format(self.positions)
