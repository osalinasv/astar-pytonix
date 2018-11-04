import copy

from astar.state import State
from astar.tuples import tuple_sum
from colorama import Fore
from typing import Optional


class Node(object):

	def __init__(self, position: tuple = (0, 0), walkable: bool = True):
		self.position = position
		self.walkable = walkable

	def __str__(self):
		return 'N{}{}'.format('!' if not self.walkable else '', self.position)


class Grid(object):

	directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

	def __init__(self, grid_size: tuple, nodes: [Node]):
		self.width  = grid_size[0]
		self.height = grid_size[1]
		self.nodes  = nodes

		self.cached_states = []

	
	def expand_state(self, current_state: State) -> [State]:
		neighbour_states = []

		for i, position in enumerate(current_state.positions):
			for neighbour in self.get_neighbour_positions(position, current_state):
				positions_copy = copy.deepcopy(current_state.positions)
				positions_copy[i] = neighbour

				neighbour_state = State(positions_copy)

				if neighbour_state in self.cached_states:
					neighbour_state = self.cached_states[self.cached_states.index(neighbour_state)]
				else:
					self.cached_states.append(neighbour_state)

				neighbour_states.append(neighbour_state)

		return neighbour_states


	def get_neighbour_positions(self, position: tuple, current_state: State) -> [tuple]:
		neighbour_positions = []

		for direction in self.directions:
			neighbour_node = self.get_neighbour_in_direction(position, direction, current_state)

			if neighbour_node is not None:
				neighbour_positions.append(neighbour_node.position)

		return neighbour_positions


	def get_neighbour_in_direction(self, position: tuple, direction: tuple, current_state: State) -> Optional[tuple]:
		new_position = tuple_sum(position, direction)

		if not self.is_position_in_bounds(new_position):
			return None

		new_neighbour  = None
		next_neighbour = self.nodes[self.position_to_index(new_position)]

		while self.is_position_in_bounds(new_position) and next_neighbour.walkable and next_neighbour.position not in current_state.positions:
			new_neighbour  = next_neighbour
			next_neighbour = self.nodes[self.position_to_index(new_position)]

			new_position = tuple_sum(new_position, direction)

		return new_neighbour


	def is_position_in_bounds(self, position: tuple) -> bool:
		return position[0] > -1 and position[0] < self.width and position[1] > -1 and position[1] < self.height


	def draw_grid(self, current_atoms: [tuple]):
		print('  ', end='')
		for i in range(self.width):
			print('{}{}'.format(i, ' ' if len(str(i)) < 2 else ''), end='')
		print()

		for row in range(self.height):
			print('{}{}'.format(row, ' ' if len(str(row)) < 2 else ''), end='')

			for col in range(self.width):
				node = self.nodes[self.position_to_index((col, row))]

				if not node.walkable:
					print('# ', end='')
				elif (col, row) in current_atoms:
					if (col, row) == current_atoms[0]:
						print(Fore.CYAN + 'C ' + Fore.RESET, end='')
					else:
						print(Fore.YELLOW + 'H ' + Fore.RESET, end='')
				else:
					print('  ', end='')

			print()

		print()

	def position_to_index(self, position) -> int:
		return self.width * position[1] + position[0]
