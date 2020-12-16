import pandas as pd
import numpy as np


def read_inputs():
    """ Reads input files and returns a dictionary with the rules and dataframes with the tickets.

    :return: rules_dict, my_ticket df, nearby_tickets df
    """
    # file paths
    rules_path = 'rules'
    my_ticket_path = 'my_ticket'
    nearby_tickets_path = 'nearby_tickets'

    # get rules
    rules = {}
    with open(rules_path, 'r') as f:
        for line in f.readlines():
            # get label and rules values
            rule = line.split(': ')
            # transform rule values to [(a, b), (c, d)]
            rule[1] = rule[1].split('\n')[0].split(' or ')
            tuples = []
            for values in rule[1]:
                values = values.split('-')
                tuples.append(tuple(int(value) for value in values))
            # add to rules
            rules[rule[0]] = tuples
        f.close()

    # load tickets in dataframes
    my_ticket = pd.read_csv(my_ticket_path, names=None, header=None, dtype=np.int64)
    nearby_tickets = pd.read_csv(nearby_tickets_path, names=None, header=None, dtype=np.int64)

    return rules, my_ticket, nearby_tickets


def value_in_range(rule, value):
    """ Checks if a value is in range of a given tuple.

    :param rule: [(a, b), (c, d)]
    :param value: value
    :return: boolean
    """
    return value in range(rule[0][0], rule[0][1] + 1) or \
           value in range(rule[1][0], rule[1][1] + 1)


def value_in_rules(rules, value):
    """ Checks if value is valid for any rule in rules.

    :param rules: Rules dictionary
    :param value: value
    :return: boolean
    """
    for rule in rules.keys():
        if value_in_range(rules[rule], value):
            return True

    return False


def column_valid(rule, data):
    """ Checks if a rule is valid on each value of a column

    :param rule: rule
    :param data: df
    :return: boolean
    """
    for value in data:
        if not value_in_range(rule, value):
            return False

    return True


def find_field_labels(rules, tickets):
    """ Iterate validation over columns to determine the right field names.

    :param rules: Rules dictionary
    :param tickets: df
    :return: column label list
    """
    # create label dictionary with label as key and list of valid column indices as values
    label_dict = {}
    for label in rules.keys():
        label_list = []
        for i in range(tickets.shape[1]):
            if column_valid(rules[label], tickets[i]):
                label_list.append(i)
        label_dict[label] = label_list

    # sort labels ascending by length
    sorted_labels = sorted(label_dict, key=lambda k: len(label_dict[k]))
    # initialize empty column array
    columns = [None]*20

    # assign each label to valid unassigned column
    for label in sorted_labels:
        for i in range(len(label_dict[label])):
            if columns[label_dict[label][i]] is not None:
                continue
            else:
                columns[label_dict[label][i]] = label
                break

    return columns


def find_invalid_values(rules, tickets):
    """ Finds all invalid values in tickets and returns a list of them. Discards all invalid tickets.

    :param rules: Rules dictionary
    :param tickets: df
    :return: list
    """
    # list with values to sum up later
    invalid_values = []
    # list with row indices to drop from the dataframe
    invalid_tickets = []

    # iterate over values
    for i in range(tickets.shape[0]):
        for j in range(tickets.shape[1]):
            # if invalid add to lists
            if not value_in_rules(rules, tickets.iloc[i][j]):
                invalid_values.append(tickets.iloc[i][j])
                if i not in invalid_tickets:
                    invalid_tickets.append(i)

    # drop invalid tickets
    tickets = tickets.drop(invalid_tickets)

    return invalid_values, tickets


def multiply_my_ticket_values(columns, my_ticket):
    """ Adds columns to my_ticket and returns product of values with departure columns.

    :param columns: list of labels
    :param my_ticket: df
    :return: int
    """
    product = 1
    # set columns
    my_ticket.columns = columns
    # iterate over columns and multiply if departure in column name
    for column in columns:
        if 'departure' in column:
            product *= my_ticket[column]

    return product


def main():
    # read input
    rules, my_ticket, nearby_tickets = read_inputs()

    # task 1
    invalid_values, tickets = find_invalid_values(rules, nearby_tickets)
    print('Task 1: {}'.format(sum(invalid_values)))

    # task 2
    columns = find_field_labels(rules, tickets)
    print('Task 2: {}'.format(multiply_my_ticket_values(columns, my_ticket)))


if __name__ == '__main__':
    main()
