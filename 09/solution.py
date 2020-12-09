import numpy as np


def summable(number, preamble):
    """ Checks if any given pair in the preamble sums up to the specified number.

    :param number: int
    :param preamble: numpy array
    :return: boolean
    """

    for i in range(len(preamble)):
        for j in range(len(preamble)):
            if i != j and preamble[i] + preamble[j] == number:
                return True

    return False


def input_valid(numbers):
    """ Checks if given input is valid. If invalid it returns the number that failed the condition, if not returns None.

    :param numbers: numpy array of numbers
    :return: int
    """
    preamble_index = np.array([0, 25])
    for i in range(preamble_index[1], len(numbers)):
        if not summable(numbers[i], numbers[preamble_index[0]:preamble_index[1]]):
            return numbers[i]
        preamble_index += 1

    return None


def find_contiguous_set(number, numbers):
    """ Finds a contiguous set of numbers that sum up to number.

    :param number: int
    :param numbers: numpy array of all numbers
    :return: set
    """
    for i in range(len(numbers)):
        contiguous_set = np.array([numbers[i]])
        for j in range(i+1, len(numbers)):
            contiguous_set = np.append(contiguous_set, numbers[j])
            if np.sum(contiguous_set) == number:
                return contiguous_set
            if np.sum(contiguous_set) > number:
                break

    return None


def get_encryption_weakness(numbers):
    """ Gets encryption weakness by adding smallest and largest value of a list.

    :param numbers: np array
    :return: int
    """
    return np.sum([np.min(numbers), np.max(numbers)])


def main():
    # load file
    file_name = 'input'
    numbers = np.loadtxt(file_name, dtype=np.int64)

    # task 1: find invalid number
    invalid_number = input_valid(numbers)
    print('Number {} is invalid!'.format(invalid_number))

    # task 2: find contiguous set that sums up to invalid_number and print encryption_weakness
    contiguous_set = find_contiguous_set(invalid_number, numbers)
    print('Contiguous set that fixes the number is {}'.format(contiguous_set))
    encryption_weakness = get_encryption_weakness(contiguous_set)
    print('Encryption weakness is {}'.format(encryption_weakness))


if __name__ == '__main__':
    main()
