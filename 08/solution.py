import pandas as pd


def interpret_instruction(instruction, parameter):
    """ Interprets an instruction and returns offset to next command and accumulator value.

    :param instruction: acc, jmp or nop
    :param parameter: signed integer
    :return: (jump_offset, accumulator_offset)
    """
    if instruction == 'acc':
        return 1, parameter
    elif instruction == 'jmp':
        return parameter, 0
    else:
        return 1, 0


def execute_code(code):
    """ Executes code until an instruction is called the second time (until it enters the infinite loop)

    :param code: pandas dataframe with columns ['instruction', 'parameter']
    :return: accumulator value (int), success (boolean)
    """
    # idea: add all line indexes to this list and check if already executed
    lines_executed = []
    accumulator = 0
    current_line = 0

    while current_line not in lines_executed:
        lines_executed.append(current_line)
        # interpret the instruction
        jump_offset, accumulator_offset = interpret_instruction(code.iloc[current_line][0], code.iloc[current_line][1])
        print('Line {}: jmp: {}, acc: {}'.format(current_line, jump_offset, accumulator_offset))
        current_line += jump_offset
        accumulator += accumulator_offset
        # if end reached return successfully
        if current_line == len(code):
            print('Code terminated successfully!')
            return accumulator, True

    # return unsuccessfully if loop ended
    return accumulator, False


def fix_code(code):
    """ Tries out to switch nop to jmp or jmp to nop one by one to see if code can finish successfully

    :param code: pandas dataframe with columns ['instruction', 'parameter']
    :return: accumulator value, line index
    """
    current_line = 0
    success = False

    while not success and current_line < len(code):
        print('-----------------------------------')
        print('Current line: {}'.format(current_line))
        # if current instruction is nop --> swap with jmp and check if it works
        if code.iloc[current_line][0] == 'nop':
            code._set_value(current_line, 'instruction', 'jmp')
            accumulator, success = execute_code(code)
            if success:
                return accumulator, current_line
            code._set_value(current_line, 'instruction', 'nop')
        # if current instruction is jmp --> swap with nop and check if it works
        elif code.iloc[current_line][0] == 'jmp':
            code._set_value(current_line, 'instruction', 'nop')
            accumulator, success = execute_code(code)
            if success:
                return accumulator, current_line
            code._set_value(current_line, 'instruction', 'jmp')

        current_line += 1

    return -1, -1


def main():
    file_path = 'input'
    code = pd.read_csv(file_path, delimiter=' ', names=['instruction', 'parameter'])
    print('Accumulator: {}'.format(execute_code(code)[0]))
    acc, line = fix_code(code)
    print('Accumulator: {}, Line that needs to be changed: {}'.format(acc, line+1))


if __name__ == '__main__':
    main()
