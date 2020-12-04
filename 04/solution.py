import re


def extract_passport_list(lines):
    """ Gets a list of passports from the input

    :param lines: input
    :return: list of passports
    """
    passports = []
    current_passport = {}
    for line in lines:
        if line == '\n':
            passports.append(current_passport)
            current_passport = {}
        else:
            fields = line.split(' ')
            for field in fields:
                kv = field.split(':')
                current_passport[kv[0]] = kv[1].split('\n')[0]

    return passports


def byr_valid(passport):
    """ Check that byr is valid

    byr (Birth Year) - four digits; at least 1920 and at most 2002.

    :param passport: passport
    :return: boolean
    """
    return len(passport['byr']) == 4 and 1920 <= int(passport['byr']) <= 2002


def iyr_valid(passport):
    """ Check that iyr is valid

    iyr (Issue Year) - four digits; at least 2010 and at most 2020.

    :param passport: passport
    :return: boolean
    """
    return len(passport['iyr']) == 4 and 2010 <= int(passport['iyr']) <= 2020


def eyr_valid(passport):
    """ Check that eyr is valid

    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.

    :param passport: passport
    :return: boolean
    """
    return len(passport['eyr']) == 4 and 2020 <= int(passport['eyr']) <= 2030


def hgt_valid(passport):
    """ Check that hgt is valid

    hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.

    :param passport: passport
    :return: boolean
    """
    return (passport['hgt'][-2:] == 'cm' and 150 <= int(passport['hgt'][:-2]) <= 193) or \
           (passport['hgt'][-2:] == 'in' and 59 <= int(passport['hgt'][:-2]) <= 76)


def hcl_valid(passport):
    """ Check that hcl is valid

    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.

    :param passport: passport
    :return: boolean
    """
    return bool(re.match(r'^#[\da-f]{6}$', passport['hcl']))


def ecl_valid(passport):
    """ Check that ecl is valid

    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.

    :param passport: passport
    :return: boolean
    """
    return any(color == passport['ecl'] for color in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])


def pid_valid(passport):
    """ Check that pid is valid

    pid (Passport ID) - a nine-digit number, including leading zeroes.

    :param passport: passport
    :return: boolean
    """
    return bool(re.match(r'[\d]{9}$', passport['pid']))


def passport_is_valid_1(passport):
    """ Determines whether a passport is valid or not only checking the presence of the fields.

    :param passport: passport
    :return: boolean
    """
    return all(field in passport.keys() for field in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])


def passport_is_valid_2(passport):
    """ Determines whether a passport is valid or not with checking field values.

    :param passport: passport
    :return: boolean
    """
    if not passport_is_valid_1(passport):
        return False

    requirements = [byr_valid(passport), iyr_valid(passport), eyr_valid(passport), hgt_valid(passport),
                    hcl_valid(passport), ecl_valid(passport), pid_valid(passport)]

    return all(requirements)


def count_valid_passports(passports, validation_method):
    """ Count valid passports

    :param passports: List of passports
    :param validation_method: validation method
    :return: int
    """
    counter = 0
    for passport in passports:
        if validation_method(passport):
            counter += 1

    return counter


def main():
    file_path = 'input'
    with open(file_path, 'r') as f:
        lines = f.readlines()
    f.close()

    passports = extract_passport_list(lines)

    print('Task 1: {}'.format(count_valid_passports(passports, passport_is_valid_1)))
    print('Task 2: {}'.format(count_valid_passports(passports, passport_is_valid_2)))


if __name__ == '__main__':
    main()
