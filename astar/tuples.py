

def tuple_sum(a: tuple, b: tuple) -> tuple:
	return tuple([i + j for i, j in zip(a, b)])


def tuple_sub(a: tuple, b: tuple) -> tuple:
	return tuple([i - j for i, j in zip(a, b)])
