import numpy as np


def get_distribution(data):
    """ Takes a sorted list of numbers and returns a dictionary with the distance as key and the number of appearances
    as value.

    :param data: sorted np array
    :return: dictionary
    """
    distribution = {1: 0, 2: 0, 3: 0}

    for i in range(1, len(data)):
        try:
            distribution[data[i] - data[i-1]] += 1
        except KeyError:
            print('Invalid arrangement')
            return None

    return distribution


def count_arrangements(data):
    """ Return number of valid arrangements.
    s/o to github.com/cupcakearmy who found this efficient method.
    (see https://github.com/cupcakearmy/adventofcode/tree/master/solutions/10)

    :param data: numpy array
    :return: int
    """
    # get list of differences
    data = np.diff(data)
    i = 0
    slices = []
    # iterate over data
    while i < len(data):
        # if the current difference is not 3 it means that we can try to leave it out to find new arrangements
        if data[i] != 3:
            # index of next 3
            next_3 = data.tolist().index(3, i + 1)
            diff = next_3 - i
            if diff > 1:
                slices.append(diff)
                i = next_3
        i += 1

    # magic
    return int(np.prod([2 ** (s - 1) - np.floor(s / 4) for s in slices]))


def main():
    # prepare data
    file_name = 'input'
    # append 0 to data and sort
    data = np.sort(np.append(np.loadtxt(file_name, dtype=int), 0))
    # append max_value + 3
    data = np.append(data, data[-1] + 3)

    # task 1
    distribution = get_distribution(data)
    print(distribution[1] * distribution[3])

    # task 2
    print(count_arrangements(data))


if __name__ == '__main__':
    main()
