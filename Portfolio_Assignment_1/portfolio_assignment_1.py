import csv
import pickle
import sys
import re


# ----------------------------------------------------------------------------------------------------------------------
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print(f'Employee id: {self.id}')
        print(f'\t\t{self.first} {self.mi} {self.last}')
        print(f'\t\t{self.phone}')


# ----------------------------------------------------------------------------------------------------------------------
# Data formatters
def first_name(first):
    return first.capitalize()


def last_name(last):
    return last.capitalize()


def mid_name(mid):  # checks for mid initial
    if mid == '':
        mid = 'X'
        return mid
    else:
        return mid.upper()


def id_format(id_inp):  # check ID format
    if id_format_checker(id_inp):
        return id_inp
    else:
        while True:
            print(f'ID invalid: {id_inp}')
            print('ID is two letters followed by 4 digits')
            id_inp = input('Please enter a valid id: ').upper()
            if id_format_checker(id_inp):
                return id_inp


def id_format_checker(id_inp):  # reg ex for ID
    regex = r'[a-z A-z][a-z A-z]\d\d\d\d'
    return re.fullmatch(regex, id_inp)


def num_format(num_inp):  # check number format
    if num_format_checker(num_inp):
        return num_inp
    else:
        while True:
            print(f'Phone {num_inp} is invalid')
            print('Enter phone number in form 123-456-7890')
            num_inp = input('Enter phone number: ')
            if num_format_checker(num_inp):
                return num_inp


def num_format_checker(num_inp):  # reg ex for number
    regex = r'\d\d\d-\d\d\d-\d\d\d\d'
    return re.fullmatch(regex, num_inp)


# ----------------------------------------------------------------------------------------------------------------------
# main program
if __name__ == '__main__':
    person_dict = {}  # will have the person objects

    if len(sys.argv) != 2:
        print('No data location specified as parameter, Please add relative data location as parameter and try again.')
        exit()
    else:
        data_location = sys.argv[1]
    with open(data_location, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')  # splits data at ','
        line_count = 0
        formatted_data_list = []  # list to hold data to add to dict
        output_txt = []  # list to hold data to write
        for row in csv_reader:
            if line_count == 0 and row[3] == 'ID':
                #print('skipping header')
                line_count += 1
            else:
                # checks data format
                lastName = last_name(row[0])
                firstName = first_name(row[1])
                midName = mid_name(row[2])
                idFormat = id_format(row[3])
                numFormat = num_format(row[4])
                # append to list temporarily
                formatted_data_list.append(
                    f'{lastName},{firstName},{midName},{idFormat},{numFormat}')

                # append to list to write to file
                output_txt.append(
                    f'{lastName},{firstName},{midName},{idFormat},{numFormat}')
                output_txt.append('\n')
                formatted_data_list = formatted_data_list[0].split(',')

                per_obj = Person(formatted_data_list[0], formatted_data_list[1], formatted_data_list[2],
                                 formatted_data_list[3], formatted_data_list[4])
                person_dict[formatted_data_list[3]] = per_obj
                for i in range(5):
                    formatted_data_list.pop()
                line_count += 1

        print(f'Processed {line_count} lines.')
        file1 = open(data_location, 'w')
        file1.writelines(output_txt)
        file1.close()
        csv_file.seek(0)  # goes to the start of file

    # Write dict to Pickle Binary
    pik_inp = person_dict
    pickle.dump(pik_inp, open('pik_data.pickle', 'wb'))

    # Read pickle file
    pik_inp_data = pickle.load(open('pik_data.pickle', 'rb'))

    # show the data from pickle file using keys
    for x in pik_inp_data.keys():
        pik_inp_data[x].display()
