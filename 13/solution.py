import math


def get_multiple_list(bus_id, timestamp):
    """ Gets the 5 next busses from the given timestamp.

    :param bus_id: int
    :param timestamp: int
    :return: int list
    """
    mult_list = []
    k = math.floor(timestamp / bus_id)
    while k * bus_id < timestamp:
        k += 1

    for i in range(5):
        mult_list.append(k * bus_id)
        k += 1

    return mult_list


def get_next_bus(bus_id, timestamp):
    """ Finds the next bus for the given bus_id and returns the timestamp.

    :param bus_id: int
    :param timestamp: int
    :return: difference next bus timestamp - timestamp
    """
    mult_list = get_multiple_list(bus_id, timestamp)
    next_bus = next(i for i in mult_list if i >= timestamp)

    return next_bus


def find_best_bus(bus_ids, timestamp):
    """ Finds the best bus and returns product of difference to timestamp * bus_id.

    :param bus_ids: int list
    :param timestamp: int
    :return: int
    """
    bus_ids = [int(i) for i in bus_ids if i != 'x']
    next_bus_list = [get_next_bus(i, timestamp) - timestamp for i in bus_ids]
    val, index = min((val, index) for (index, val) in enumerate(next_bus_list))

    return bus_ids[index] * val


def egcd(a, b):
    """ Extended Euclidian algorithm

    :param a: int
    :param b: int
    :return:
    """
    if not b:
        return 1, 0, a
    q, r = a // b, a % b
    s, t, g = egcd(b, r)
    return t, s - q * t, g


def crt(r1, q1, r2, q2):
    """ Chinese remainder theorem see https://en.wikipedia.org/wiki/Chinese_remainder_theorem

    :param r1: int
    :param r2: int
    :param q1: int
    :param q2: int
    :return int, int
    """
    q3 = math.lcm(q1, q2)
    t, _, g = egcd(q1 + q2, q3)
    r3 = (r1 * q2 + r2 * q1) * t
    assert not r3 % g
    r3 = r3 // g % q3
    if (r3 < 0) != (q3 < 0):
        r3 += q3
    return r3, q3


def task_2(bus_ids):
    """ Find solution for task 2 using chinese remainder theorem.

    :param bus_ids: list of ints with 'X'
    :return: int
    """
    q, r = 0, 1
    for i, b in enumerate(bus_ids):
        if bus_ids[i] != 'x':
            b = int(b)
            q, r = crt(q, r, (-i) % b, b)

    return q


def main():
    # load data
    file_path = 'input'
    with open(file_path, 'r') as f:
        lines = f.readlines()
        timestamp = int(lines[0])
        bus_ids = lines[1].split(',')
    f.close()

    # task 1
    result1 = find_best_bus(bus_ids, timestamp)
    print(result1)

    # task 2
    result2 = task_2(bus_ids)
    print(result2)


if __name__ == '__main__':
    main()
