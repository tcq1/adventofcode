import numpy as np


def find_solution_task_1(data):
    # try out all pairs and return their product if they sum up to 2020
    for i in data:
        for j in data:
            if i + j == 2020:
                return i * j

    return None


def find_solution_task_2(data):
    # try out all 3-tuples and return their product if they sum up to 2020
    for i in data:
        for j in data:
            for k in data:
                if i + j + k == 2020:
                    return i * j * k

    return None


def main():
    """ Task: https://adventofcode.com/2020/day/1
    """
    file_path = 'input'
    data = np.loadtxt(file_path, dtype=int)
    print(find_solution_task_1(data))
    print(find_solution_task_2(data))


if __name__ == '__main__':
    main()
