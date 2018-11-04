import json
import os
import numpy as np

from astar.grid import Node
from matplotlib.image import imread
from typing import Optional


def get_levels_from_json(path: str) -> Optional[dict]:
	with open(path, 'r') as f:
		data = json.load(f)

	if data is None or len(data) < 1:
		raise Exception('No levels were found in \'{}\''.format(path))

	return data


def get_level_data(data_dir: str, level: dict) -> dict:
	black_color = np.array([0.0, 0.0, 0.0])
	atom_colors = [rgb_array_to_numpy(color) for color in level['colors']]

	grid = []

	start_state  = [None] * len(atom_colors)
	target_state = [None] * len(atom_colors)

	diagram_path = os.path.join(data_dir, level['diagram_path'])
	diagram_data = imread(diagram_path)

	grid_size = len(diagram_data[0]), len(diagram_data)

	for y, row in enumerate(diagram_data):
		for x, pixel in enumerate(row):
			node = Node((x, y), not np.array_equal(pixel, black_color))
			grid.append(node)

			atom_index = index_of_color_in_array(pixel, atom_colors)
			if atom_index > -1: start_state[atom_index] = (x, y)

	solution_path = os.path.join(data_dir, level['solution_path'])
	solution_data = imread(solution_path)

	for y, row in enumerate(solution_data):
		for x, pixel in enumerate(row):
			atom_index = index_of_color_in_array(pixel, atom_colors)
			if atom_index > -1: target_state[atom_index] = (x, y)

	return {
		'grid':         grid,
		'grid_size':    grid_size,
		'start_state':  start_state,
		'target_state': target_state
	}


def rgb_array_to_numpy(rgb: [int]) -> np.ndarray:
	return np.array([i / 255 for i in rgb])


def index_of_color_in_array(c: np.ndarray, colors: [np.ndarray]) -> int:
	for i, color in enumerate(colors):
		if np.array_equal(c, color):
			return i
	
	return -1
