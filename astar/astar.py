import datetime
import heapq

from astar.grid import Grid
from astar.state import State
from astar.tuples import tuple_sum, tuple_sub
from time import time


def run_astar(grid: Grid, start_state: [tuple], target_state: [tuple]):
	start_state  = State(start_state)
	target_state = State(target_state)

	open_list   = []
	closed_list = set()

	start_time = time()
	iter_count = 0

	start_state.set_cost(0, state_heuristic(start_state, target_state))
	heapq.heappush(open_list, (start_state.f_cost, start_state))

	while len(open_list) > 0:
		iter_count += 1

		current_state = heapq.heappop(open_list)[1]
		closed_list.add(current_state)

		formatted_time = format_time(time() - start_time)
		print('\rtime: {} | iter: {} | h: {} | f: {}      '.format(formatted_time, iter_count, current_state.heuristic, current_state.f_cost), end='')

		if compare_to_target_state(current_state, target_state):
			print()
			return reconstruct_path(current_state, start_state, target_state)

		neighbour_states = grid.expand_state(current_state)

		for neighbour in neighbour_states:
			if neighbour not in closed_list:
				cost = current_state.cost + state_heuristic(neighbour, current_state)

				is_in_open_list = False

				for _, state in open_list:
					if neighbour == state:
						is_in_open_list = True
						break

				if cost < neighbour.cost or not is_in_open_list:
					neighbour.set_cost(cost, state_heuristic(neighbour, target_state))
					neighbour.prev_state = current_state

					if not is_in_open_list:
						heapq.heappush(open_list, (neighbour.f_cost, neighbour))

	print()
	return None


def reconstruct_path(last_state: State, start_state: State, target_state: State) -> [State]:
	path = []
	current_state = last_state

	if compare_to_target_state(current_state, target_state):
		while current_state is not None:
			path.append(current_state)
			current_state = current_state.prev_state

		if len(path) > 0:
			path.reverse()

	return path


def state_heuristic(current_state: State, target_state: State) -> int:
	heuristic = 0
	first_current = current_state.positions[0]
	first_target  = target_state.positions[0]

	for current, target in zip(current_state.positions[1:], target_state.positions[1:]):
		current_dist = tuple_sub(first_current, current)
		target_dist  = tuple_sub(first_target, target)

		dist_diff = tuple_sub(target_dist, current_dist)
		heuristic += abs(dist_diff[0]) + abs(dist_diff[1])

	return heuristic


def compare_to_target_state(current_state: State, target_state: State) -> bool:
	first_current = current_state.positions[0]
	first_target  = target_state.positions[0]

	for current, target in zip(current_state.positions[1:], target_state.positions[1:]):
		current_dist = tuple_sub(first_current, current)
		target_dist  = tuple_sub(first_target, target)

		if current_dist != target_dist:
			return False

	return True


def format_time(seconds: float) -> str:
	return str(datetime.timedelta(seconds=seconds))
