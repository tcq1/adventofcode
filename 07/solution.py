def extract_rules(lines):
    """ Extracts rules from file. Rules are structured in nested dictionaries.
    The outer dictionary has the color as key with a dictionary as value that contains the bag colors and amounts.
    The inner dictionary has the bag color as key and the amount as value.

    :param lines: Lines from input file
    :return: dictionary
    """
    rules = {}
    # iterate over every line
    for line in lines:
        rule = {}
        # get key and value
        key, value = line.split('contain ')
        key = key.split(' bags')[0]
        # if bag doesn't contain other bags make value None
        if value == 'no other bags.':
            rules[key] = None
        else:
            # add bags to value
            values = value.split(', ')
            for v in values:
                v = v.split(' ')
                rule['{} {}'.format(v[1], v[2])] = int(v[0])

            rules[key] = rule

    return rules


def get_bags_contain_input(rules, color):
    """ Returns a set of bags that contain the bag of the specified color.

    Solved with a stack.
    :param rules: rules
    :param color: color of bag
    :return: set
    """
    bags = set()
    stack = [color]

    # implementation with a stack
    while len(stack) > 0:
        for item in stack:
            # remove item from stack
            stack.remove(item)
            # iterate over all rules to find the right bags
            for key, value in rules.items():
                if value is None:
                    continue
                # if bag contains wanted bag add to stack and output set
                if item in value.keys():
                    bags.add(key)
                    stack.append(key)

    return bags


def get_bags_contained(rules, color):
    """ Counts the bags that are in the specified bag.

    Solved with recursion.
    :param rules: rules
    :param color: color of bag
    :return: int
    """
    counter = 0

    # if no bags contained return 0
    if rules[color] is None:
        return counter

    # iterate over bags that are directly in the current bag
    for bag, count in rules[color].items():
        # add amount of that bag
        counter += count
        # add amount of that bag * bags in that bag
        counter += count * get_bags_contained(rules, bag)

    return counter


def main():
    # read file
    file_path = 'input'
    lines = open(file_path, 'r').read().strip().split('\n')
    # get rules
    rules = extract_rules(lines)

    # task 1
    print(len(get_bags_contain_input(rules, 'shiny gold')))
    # task 2
    print(get_bags_contained(rules, 'shiny gold'))


if __name__ == '__main__':
    main()