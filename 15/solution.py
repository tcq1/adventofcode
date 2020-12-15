import numpy as np


def play(numbers, n):
    """ Play the elves game and get number of index n-1.

    :param numbers: array with starting numbers
    :param n: n-th number
    :return: int
    """
    # dictionary with index of occurrence, smaller than a list that grows bigger with each new value
    occurrences = {numbers[i]: [i] for i in range(0, len(numbers))}

    # stores current number
    current_number = numbers[-1]
    # iterate until n is reached
    for i in range(len(numbers), n):
        # case: only one appearance yet
        if len(occurrences[current_number]) == 1:
            current_number = 0
            # check if 0 already appeared twice, if yes then remove first index
            if len(occurrences[0]) == 2:
                occurrences[0].remove(occurrences[0][0])
            occurrences[0].append(i)
        else:
            # calculate new value by subtracting indices
            new_value = occurrences[current_number][1] - occurrences[current_number][0]
            # same as with the 0
            if new_value in occurrences:
                if len(occurrences[new_value]) == 2:
                    occurrences[new_value].remove(occurrences[new_value][0])
                occurrences[new_value].append(i)
            else:
                occurrences[new_value] = [i]
            current_number = new_value

    return current_number


def main():
    numbers = [13, 16, 0, 12, 15, 1]
    print(play(numbers, 2020))
    print(play(numbers, 30000000))


if __name__ == '__main__':
    main()
