def get_groups(lines):
    """ Seperates lines in groups of declarations.

    :param lines: lines that were read from a file
    """
    groups = []
    group = []
    for line in lines:
        # if empty line: add current group to groups
        if line == '\n':
            groups.append(group)
            group = []
            continue

        # remove \n from line and add to current group
        group.append(line.split('\n')[0])

    return groups


def get_union_set(group):
    """ Task 1: gets union set of all questions in a group.
    Just add every letter to a set to get the union.

    :param group: list of strings
    """
    question_set = set()
    for declaration in group:
        for letter in declaration:
            question_set.add(letter)

    return question_set


def get_intersection_set(group):
    """ Task 2: gets intersection set of all questions in a group.
    Make a set for every declaration and return the intersection.

    :param group: list of strings
    """
    declarations = []
    for declaration in group:
        questions = set()
        for question in declaration:
            questions.add(question)
        declarations.append(questions)

    return declarations[0].intersection(*declarations)


def count_all_questions(groups, question_set_method):
    """ Adds up length of all question sets and returns the sum.

    :param groups: list of groups
    :param question_set_method: get_union_set or get_intersection_set
    """
    count = 0
    for group in groups:
        count += len(question_set_method(group))

    return count


def main():
    # read file
    file_path = 'input'
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # get groups
    groups = get_groups(lines)

    # task 1
    print(count_all_questions(groups, get_union_set))

    # task 2
    print(count_all_questions(groups, get_intersection_set))


if __name__ == '__main__':
    main()
