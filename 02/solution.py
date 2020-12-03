import pandas as pd


def process_dataframe(df):
    """ Process data to make it easier to work with

    :param df: dataframe
    :return: processed dataframe
    """
    # iterate over all items
    for i in range(len(df.index)):
        # replace policy with a list of integers
        df.loc[i, 'policy'] = list(map(int, df.loc[i, 'policy'].split('-')))
        # get rid of ':' in letter
        df.loc[i, 'letter'] = df.loc[i, 'letter'].split(':')[0]

    return df


def password_is_valid_task_1(row):
    """ Checks if password is valid.

    :param row: dataframe row
    :return: boolean
    """
    return row['policy'][0] <= row['password'].count(row['letter']) <= row['policy'][1]


def password_is_valid_task_2(row):
    """ Checks if password is valid.

    :param row: dataframe row
    :return: boolean
    """
    # XOR the two positions in the password
    return (row['letter'] == row['password'][row['policy'][0] - 1]) != \
           (row['letter'] == row['password'][row['policy'][1] - 1])


def get_valid_passwords(df, validation_method):
    """ Filters all valid passwords of a list.

    :param df: dataframe
    :param validation_method: function that returns a boolean
    :return: dataframe with only valid passwords
    """
    # list of indices that should be dropped
    drop = []

    # find all invalid passwords
    for i in range(len(df.index)):
        if not validation_method(df.iloc[i]):
            drop.append(i)

    # drop invalid passwords and return dataframe
    return df.drop(drop).reset_index(drop=True)


def main():
    """ Task: https://adventofcode.com/2020/day/2
    """
    file_path = 'input'
    data = pd.read_csv(file_path, sep=' ', names=['policy', 'letter', 'password'])
    data = process_dataframe(data)
    print('Task 1: {} passwords are valid.'.format(len(get_valid_passwords(data, password_is_valid_task_1).index)))
    print('Task 2: {} passwords are valid.'.format(len(get_valid_passwords(data, password_is_valid_task_2).index)))


if __name__ == '__main__':
    main()
