def convert_to_decimal(seat_code):
    """ Takes a seat code and converts it to a tuple containing seat row and column in decimal.

    :param seat_code: string with first seven letters: B, F and last 3 letters: L, R
    :return: decimal tuple
    """
    # get row and column information
    row = seat_code[:7]
    column = seat_code[-3:]

    # replace letters with digits
    row = row.replace('F', '0')
    row = row.replace('B', '1')
    column = column.replace('L', '0')
    column = column.replace('R', '1')

    # convert to decimal
    return int(row, 2), int(column, 2)


def get_seat_id(row, column):
    """ Calculates seat id.

    :param row: decimal row number
    :param column: decimal column number
    :return: id
    """
    return 8 * row + column


def initialize_empty_seat_dict():
    """ Initializes all seats in form of a nested dictionary.

    :return: nested dictionary with all entries set to False
    """
    dic = {}
    for i in range(128):
        dic[i] = {}
        for j in range(8):
            dic[i][j] = False

    return dic


def fill_seats(data):
    """ Iterate through the input data and set non empty seats to True

    :param data: input data (already converted to decimal)
    :return: dictionary
    """
    dic = initialize_empty_seat_dict()
    for seat in data:
        dic[seat[0]][seat[1]] = True

    return dic


def find_my_seat(data):
    """ Finds the empty seat where the neighbor seats exist.

    :param data: input data (already converted to decimal
    :return: seat
    """
    dic = fill_seats(data)
    # iterate over all possibilities
    for i in range(128):
        for j in range(8):
            # check if seat already occupied
            if dic[i][j] is False:
                try:
                    # check if neighbors exist
                    if dic[i][j-1] and dic[i][j+1]:
                        return i, j
                except KeyError:
                    continue


def main():
    # get data
    data = []
    file_path = 'input'
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data.append(line.split('\n')[0])

    # convert data
    for i in range(len(data)):
        data[i] = convert_to_decimal(data[i])

    # task 1
    highest_id = max(data, key=lambda x: get_seat_id(x[0], x[1]))
    print(get_seat_id(highest_id[0], highest_id[1]))

    # task 2
    my_seat = find_my_seat(data)
    print(get_seat_id(my_seat[0], my_seat[1]))


if __name__ == '__main__':
    main()
