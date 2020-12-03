import numpy as np


def count_trees_hit(grid, slope):
    """ Counts the trees that were hit on the way down

    :param grid: the map
    :param slope: [n_rows, n_columns] determines the next position after each iteration
    :return: int
    """
    # [row, column]
    coords = [0, 0]
    counter = 0

    # repeat until bottom is reached
    while coords[0] < len(grid):
        # if landed on a tree increment counter
        if grid[coords[0]][coords[1]] == '#':
            counter += 1
        # update position
        coords = [coords[0] + slope[0], (coords[1] + slope[1]) % len(grid[0])]

    return counter


def multiplied_trees_hit(grid, slopes):
    """ Try out different slopes and multiply the encountered trees

    :param grid: the map
    :param slopes: list of slopes that determine the next positions
    """
    result = 1
    # multiply each result
    for slope in slopes:
        result *= count_trees_hit(grid, slope)

    return result


def main():
    """ Task: https://adventofcode.com/2020/day/3
    """
    file_path = 'input'
    grid = np.loadtxt(file_path, dtype=str, comments=None)
    print('Trees hit in task 1: {}'.format(count_trees_hit(grid, [1, 3])))

    # task 2
    slopes = [[1, 1], [1, 3], [1, 5], [1, 7], [2, 1]]
    print('Result of task 2: {}'.format(multiplied_trees_hit(grid, slopes)))


if __name__ == '__main__':
    main()
