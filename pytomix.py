import os
import re
import sys
import traceback

from astar.astar import run_astar
from astar.grid import Grid
from colorama import init, Fore
from level import get_level_data, get_levels_from_json


init(autoreset=True)

root_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(root_dir, 'data')


def main():
	while True:
		os.system('cls' if os.name == 'nt' else 'clear')

		try:
			levels_json_path = os.path.join(data_dir, 'levels.json')

			levels = get_levels_from_json(levels_json_path)
			ordered_levels = [key for key in levels] + [Fore.RED + 'Exit' + Fore.RESET]
			selected_level = display_menu_and_get_selection(ordered_levels)

			if selected_level == len(ordered_levels) - 1:
				return

			selected_level = levels[ordered_levels[selected_level]]
			level_data = get_level_data(data_dir, selected_level)

			grid = Grid(level_data['grid_size'], level_data['grid'])
			start_state  = level_data['start_state']
			target_state = level_data['target_state']

			print('\nSTARTING STATE:\n')
			grid.draw_grid(start_state)

			print('\nTARGET STATE:\n')
			grid.draw_grid(target_state)
			
			path = run_astar(grid, start_state, target_state)
			display_path(grid, path)
		except Exception as err:
			print_exception(err, False)

		input('\nPress enter to continue...')


def display_menu_and_get_selection(levels: dict) -> int:
	print('''
 _____ __ __ _____ _____ _____ _____ __ __ 
|  _  |  |  |_   _|     |   | |     |  |  |
|   __|_   _| | | |  |  | | | |-   -|-   -|
|__|    |_|   |_| |_____|_|___|_____|__|__|

Level selection\n''')

	for i, level_name in enumerate(levels):
		print('   {:0d}. {}'.format(i + 1, level_name))

	selected_index = int(input(Fore.GREEN + '\n>> ' + Fore.RESET)) - 1

	if selected_index < 0 or selected_index >= len(levels):
		raise Exception("Not a valid level selection")

	return selected_index


def display_path(grid: Grid, path: list):
	if path is not None and len(path) > 0:
		print('\nSolved in ' + Fore.GREEN + '{}'.format(len(path) - 1) + Fore.RESET + ' steps.\n')

		move_counter = 1

		for i in range(len(path) - 1):
			for current_pos, next_pos in zip(path[i].positions, path[i + 1].positions):
				if current_pos != next_pos:
					print('{:02d}. move  {}  to  {}'.format(move_counter, current_pos, next_pos))
					move_counter += 1

		print('\nEND STATE:\n')
		grid.draw_grid(path[-1].positions)
	else:
		print(Fore.RED + '\nNo solution found.' + Fore.RESET)


def print_exception(err: Exception, verbose: bool = False):
	if verbose:
		traceback.print_exc()
	else:
		print(Fore.RED + str(err))


if __name__ == '__main__':
	main()
