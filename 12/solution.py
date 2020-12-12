import math
import numpy as np


def move_direction(x, y, direction, amount):
    """ Moves into a direction

    :param x: current x position
    :param y: current y position
    :param direction: facing direction
    :param amount: amount
    :return: x, y
    """
    if direction == 'N':
        y += amount
    elif direction == 'E':
        x += amount
    elif direction == 'S':
        y -= amount
    else:
        x -= amount

    return x, y


def direction_to_degree(direction):
    """ Translates direction to degree

    :param direction: 'N', 'E', 'S', or 'W'
    :return: 0, 90, 180 or 270
    """
    north, east, south, west = 0, 90, 180, 270

    if direction == 'N':
        return north
    elif direction == 'E':
        return east
    elif direction == 'S':
        return south
    else:
        return west


def degree_to_direction(degree):
    """ Translates degree to direction

    :param degree: 0, 90, 180 or 270#
    :return: 'N', 'E', 'S', or 'W'
    """
    if degree == 0:
        return 'N'
    elif degree == 90:
        return 'E'
    elif degree == 180:
        return 'S'
    else:
        return 'W'


def turn(current_direction, direction, degree):
    """ Turns into new direction

    :param current_direction: current direction
    :param direction: left or right
    :param degree: amount
    :return: new direction
    """
    if direction == 'R':
        return degree_to_direction((direction_to_degree(current_direction) + degree) % 360)
    else:
        return degree_to_direction((direction_to_degree(current_direction) - degree) % 360)


def rotate_waypoint(wp_x, wp_y, direction, degree):
    """ Rotates the waypoint around the ship.

    :param wp_x: waypoint x position
    :param wp_y: waypoint y position
    :param direction: left or right
    :param degree: degree
    :return: wp_x, wp_y
    """
    if direction == 'L':
        degree *= -1

    degree = np.deg2rad(degree)

    wp_x_new = wp_x * math.cos(degree) + wp_y * math.sin(degree)
    wp_y_new = -wp_x * math.sin(degree) + wp_y * math.cos(degree)

    return round(wp_x_new), round(wp_y_new)


def move1(instruction, current_x, current_y, current_direction):
    """ Takes an instruction and moves according to it and the rules from task 1.

    :param instruction: [instruction, int]
    :param current_x: current x position
    :param current_y: current y position
    :param current_direction: facing direction
    :return: new_x, new_y, new_direction
    """
    directions = ['N', 'E', 'S', 'W']
    # move to direction
    if instruction[0] in directions:
        current_x, current_y = move_direction(current_x, current_y, instruction[0], instruction[1])
    # move forward
    elif instruction[0] == 'F':
        current_x, current_y = move_direction(current_x, current_y, current_direction, instruction[1])
    # turn
    else:
        current_direction = turn(current_direction, instruction[0], instruction[1])

    return current_x, current_y, current_direction


def move2(instruction, ship_x, ship_y, wp_x, wp_y):
    """ Takes an instruction and moves according to it and the rules from task 2.

    :param instruction: [instruction, int]
    :param ship_x: current ship x position
    :param ship_y: current ship y position
    :param wp_x: current waypoint x position
    :param wp_y: current waypoint y position
    :return: ship_x, ship_y, wp_x, wp_y
    """
    directions = ['N', 'E', 'S', 'W']
    # move waypoint to direction
    if instruction[0] in directions:
        wp_x, wp_y = move_direction(wp_x, wp_y, instruction[0], instruction[1])
    # move ship to waypoint
    elif instruction[0] == 'F':
        ship_x += instruction[1] * wp_x
        ship_y += instruction[1] * wp_y
    # rotate direction
    else:
        wp_x, wp_y = rotate_waypoint(wp_x, wp_y, instruction[0], instruction[1])

    return ship_x, ship_y, wp_x, wp_y


def run_instructions_1(instructions):
    """ Runs through all instructions and returns the final position according to rules from task 1.

    :param instructions: list of [instruction, int]
    :return: final_x, final_x
    """
    # initialize starting parameters
    current_x, current_y = 0, 0
    current_direction = 'E'

    # execute instructions
    for instruction in instructions:
        current_x, current_y, current_direction = move1(instruction, current_x, current_y, current_direction)

    return current_x, current_y


def run_instructions_2(instructions):
    """ Runs through all instructions and returns the final position according to rules from task 2.

    :param instructions: list of [instruction, int]
    :return: final_x, final_x
    """
    # initialize starting parameters
    ship_x, ship_y = 0, 0
    wp_x, wp_y = 10, 1

    # execute instructions
    for instruction in instructions:
        ship_x, ship_y, wp_x, wp_y = move2(instruction, ship_x, ship_y, wp_x, wp_y)

    return ship_x, ship_y


def manhattan_distance(x, y):
    """ Calculates the manhattan distance

    :param x: x position
    :param y: y position
    :return: int
    """
    return abs(x) + abs(y)


def main():
    # read instructions
    file_path = 'input'
    with open(file_path, 'r') as f:
        lines = f.readlines()

    instructions = []
    for line in lines:
        line = line.split('\n')[0]
        instructions.append([line[:1], int(line[1:])])

    # task 1
    x, y = run_instructions_1(instructions)
    print('x = {}, y = {}'.format(x, y))
    print('Manhattan distance = {}'.format(manhattan_distance(x, y)))

    # task 2
    x, y = run_instructions_2(instructions)
    print('x = {}, y = {}'.format(x, y))
    print('Manhattan distance = {}'.format(manhattan_distance(x, y)))


if __name__ == '__main__':
    main()
