import re


def separate_input_data(data):
    """ Separates input data in segments with different masks.

    :param data: input data
    :return: list
    """
    segments = []
    while len(data) > 0:
        # get memory address line
        segment = [data.pop(0).split(' = ')[1]]
        # get memory value lines
        while len(data) > 0 and 'mem' in data[0]:
            mem_val = data.pop(0).split(' = ')
            mem_val[0] = re.search(r"\[([0-9]+)\]", mem_val[0]).group(1)
            mem_val[1] = int(mem_val[1])
            segment.append(mem_val)
        segments.append(segment)

    return segments


def calculate_value(mask, value):
    """ Calculates value with mask applied.

    :param mask: mask string
    :param value: int value
    :return: int value
    """
    # get binary value as string
    bin_value = '{0:036b}'.format(value)

    # replace all values except X
    for i in range(len(mask)):
        if mask[i] != 'X':
            bin_value = bin_value[:i] + mask[i] + bin_value[i+1:]

    return int(str(bin_value), 2)


def replace_floating_bit(address):
    """ Replaces floating bit with 0 and 1. Return a list of addresses.

    :param address: 36 Bit string
    :return: list of addresses
    """
    queue = [address]
    addresses = []

    # append addresses to queue while X in address
    while len(queue) > 0:
        # add to address list if no X left
        a = queue.pop(0)
        if 'X' not in a:
            addresses.append(a)
        else:
            for i in range(len(a)):
                # make 2 addresses and add to queue
                if a[i] == 'X':
                    a0 = a
                    a1 = a
                    a0 = a0[:i] + '0' + a0[i+1:]
                    a1 = a1[:i] + '1' + a1[i+1:]
                    queue.append(a0)
                    queue.append(a1)
                    break

    return addresses


def calculate_address(mask, value):
    """ Calculates memory address with applied mask. Due to floating bits there can be multiple addresses

    :param mask: mask string
    :param value: int value
    :return: list with addresses
    """
    bin_value = '{0:036b}'.format(int(value))

    # apply mask on address
    for i in range(len(mask)):
        if mask[i] == '1':
            bin_value = bin_value[:i] + '1' + bin_value[i+1:]
        elif mask[i] == 'X':
            bin_value = bin_value[:i] + 'X' + bin_value[i+1:]

    return replace_floating_bit(bin_value)


def update_memory(segments):
    """ Updates the memory dictionary.

    :param segments: list of segments with mask and new values
    :return: mem_dict
    """
    mem_dict = {}

    # iterate over segments
    for segment in segments:
        for i in range(1, len(segment)):
            mem_dict[segment[i][0]] = calculate_value(segment[0], segment[i][1])

    return mem_dict


def update_memory_v2(segments):
    """ Calculates sum of values stored in memory with the v2 chip.

    :param segments: list of segments with mask and new values
    :return: mem_dict
    """
    mem_dict = {}

    # iterate over segments
    for segment in segments:
        for i in range(1, len(segment)):
            addresses = calculate_address(segment[0], segment[i][0])
            for address in addresses:
                mem_dict[address] = segment[i][1]

    return mem_dict


def calc_sum_mem_dict(mem_dict):
    """ Calculates sum of values stored in memory.

    :param mem_dict: dictionary with memory address as key and stored value as value
    :return: int
    """
    return sum(mem_dict.values())


def main():
    # load data
    file_path = 'input'
    with open(file_path, 'r') as f:
        data = [line.split('\n')[0] for line in f.readlines()]
    f.close()

    segments = separate_input_data(data)

    # task 1
    mem_dict = update_memory(segments)
    print(calc_sum_mem_dict(mem_dict))

    # task 2
    mem_dict2 = update_memory_v2(segments)
    print(calc_sum_mem_dict(mem_dict2))


if __name__ == '__main__':
    main()
