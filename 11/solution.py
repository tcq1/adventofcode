import copy
import itertools


def get_adjacent_positions(data, row, column, only_adjacent):
    """ Gets adjacent coordinates.

    :param data: seat map (2d array)
    :param row: row index
    :param column: column index
    :param only_adjacent: boolean, if True only check directly adjacent, if not find first seat in direction
    :return: list of coordinates
    """
    coordinates = []

    # get directions
    direction = [[x, y] for x, y in itertools.product([-1, 0, 1], [-1, 0, 1]) if not (x == 0 and y == 0)]

    # iterate over directions
    for dr, dc in direction:
        # calc coordinate
        coordinate = [row + dr, column + dc]

        # do this if first seat in all directions should be found
        if not only_adjacent:
            # while not out of bounds and not a seat adjust coordinate
            while 0 <= coordinate[0] < len(data) and \
                    0 <= coordinate[1] < len(data[0]) and \
                    data[coordinate[0]][coordinate[1]] == '.':
                coordinate = [coordinate[0] + dr, coordinate[1] + dc]

        # if in bounds and it is a seat append to list
        if 0 <= coordinate[0] < len(data) and 0 <= coordinate[1] < len(data[0]) and \
                data[coordinate[0]][coordinate[1]] != '.':
            coordinates.append(coordinate)

    return coordinates


def count_adjacent_occupied(data, row, column, only_adjacent):
    """ Counts the occupied adjacent seats of a seat.

    :param data: seat map (2d array)
    :param row: row index
    :param column: column index
    :param only_adjacent: boolean, if True only check directly adjacent, if not find first seat in direction
    :return: int
    """
    return [data[row][column] for row, column in get_adjacent_positions(data, row, column, only_adjacent)].count('#')


def count_occupied_seats(data):
    """ Counts all occupied seats.

    :param data: seat map (2d array)
    :return: int
    """
    return sum(row.count('#') for row in data)


def occupy_seats(data, seat_tolerance, only_adjacent):
    """ Occupies seats according to rules.

    :param data: seat map (2d array)
    :param seat_tolerance: number of discovered seats that can be occupied to still make the person occupy the seat
    :param only_adjacent: boolean, if True only check directly adjacent, if not find first seat in direction
    :return: new seat map
    """
    tmp = []
    while data != tmp:
        # copy to tmp
        tmp = copy.deepcopy(data)
        # iterate over data
        for row in range(len(data)):
            for column in range(len(data[0])):
                # if it is a seat then occupy if conditions satisfied
                if tmp[row][column] != '.':
                    if tmp[row][column] == 'L' and count_adjacent_occupied(tmp, row, column, only_adjacent) == 0:
                        data[row][column] = '#'
                    if tmp[row][column] == '#' and count_adjacent_occupied(tmp, row, column,
                                                                           only_adjacent) >= seat_tolerance:
                        data[row][column] = 'L'

    return data


def main():
    # get seat map
    file_path = 'input'
    data = [list(line.strip()) for line in open(file_path, 'r').readlines()]
    # task 1
    print(count_occupied_seats(occupy_seats(copy.deepcopy(data), 4, only_adjacent=True)))
    # task 2
    print(count_occupied_seats(occupy_seats(copy.deepcopy(data), 5, only_adjacent=False)))


if __name__ == '__main__':
    main()
