# This is a sample Python script.
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

def first_name(first):
    return first.capitalize()


def last_name(last):
    return last.capitalize()


def mid_name(mid):
    if mid == '':
        mid = 'X'
        return mid
    else:
        return mid.upper()


def id_format(id_inp):
    if id_format_checker(id_inp):
        return id_inp
    else:
        while True:
            print(f'ID invalid: {id_inp}')
            print('ID is two letters followed by 4 digits')
            id_inp = input('Please enter a valid id: ').upper()
            if id_format_checker(id_inp):
                return id_inp


def id_format_checker(id_inp):
    regex = r'[a-z A-z][a-z A-z]\d\d\d\d'
    return re.fullmatch(regex, id_inp)


def num_format(num_inp):
    if num_format_checker(num_inp):
        return num_inp
    else:
        while True:
            print(f'Phone {num_inp} is invalid')
            print('Enter phone number in form 123-456-7890')
            num_inp = input('Enter phone number: ')
            if num_format_checker(num_inp):
                return num_inp


def num_format_checker(num_inp):
    regex = r'\d\d\d-\d\d\d-\d\d\d\d'
    #regex = re.compile(r'[0-9]{3}-[0-9]{3}-[0-9]{4}')
    return re.fullmatch(regex, num_inp)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print(len(sys.argv))

    person_dict = {}  # will have the person objects

    if len(sys.argv) != 2:
        print('No data location specified as parameter, Please add data location as parameter and try again.')
        exit()
    else:
        print("location exists")
        data_location = sys.argv[1]

    print(f'User input is , {data_location}')
    # ----------------------------------------------------------------------------------------------------------------------
    # show current data
    # opened file as read and write

    # with open(data_location, 'r+') as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    #     line_count = 0
    #     for row in csv_reader:
    #         if line_count == 0:
    #             print(f'Column names are {", ".join(row)}')
    #             line_count += 1
    #             # print(f'\t Last - , First -, Middle initial - , ID - , Office phone - .')
    #         else:
    #             # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
    #             print(
    #                 f'\t Last - {row[0]} || First - {row[1]}, || Middle initial - {row[2]}, || ID - {row[3]}, || '
    #                 f'Office phone - {row[4]}.')
    #             # print(f'\t {row[0]} \t{row[1]} \t {row[2]} \t {row[3]}\t {row[4]}.')
    #             line_count += 1
    #     print(f'Processed {line_count} lines.')
    #     csv_file.seek(0)  # goes to the start

    # ----------------------------------------------------------------------------------------------------------------------
    with open(data_location, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        formatted_data_list = []
        # new_text_counter = 0
        output_txt = []
        for row in csv_reader:
            if line_count == 0 and row[3] == 'ID':
                print('skipping header')
                # print(f' {line_count} - {row}')
                line_count += 1
                # print(f'\t Last - , First -, Middle initial - , ID - , Office phone - .')
            else:
                # print(row)
                # print(f' {line_count} - {row}')
                lastName = last_name(row[0])
                firstName = first_name(row[1])
                midName = mid_name(row[2])
                idFormat = id_format(row[3])
                numFormat = num_format(row[4])

                # formatted_data_list.append(
                #     f'{last_name(row[0])},{first_name(row[1])},{mid_name(row[2])},{id_format(row[3])},{num_format(row[4])}')
                # formatted_data_list.append('\n')

                formatted_data_list.append(
                    f'{lastName},{firstName},{midName},{idFormat},{numFormat}')
                # formatted_data_list.append('\n')
                output_txt.append(
                    f'{lastName},{firstName},{midName},{idFormat},{numFormat}')
                output_txt.append('\n')

                formatted_data_list = formatted_data_list[0].split(',')
                # new_text_counter += 1

                per_obj = Person(formatted_data_list[0], formatted_data_list[1], formatted_data_list[2], formatted_data_list[3], formatted_data_list[4])
                person_dict[formatted_data_list[3]] = per_obj
                for i in range(5):
                    formatted_data_list.pop()

                # print(
                #     f'{line_count} - \t {first_name(row[0])} \t{last_name(row[1])} \t {mid_name(row[2])} \t {id_format(row[3])}\t {num_format(row[4])} \n')

                # print(
                # f'\t Last - {row[0]} || First - {row[1]}, || Middle initial - {row[2]}, || ID - {row[3]}, || '
                # f'Office phone - {row[4]}.')
                # print(f'\t {row[0]} \t{row[1]} \t {row[2]} \t {row[3]}\t {row[4]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')
        file1 = open(data_location, 'w')
        file1.writelines(output_txt)
        file1.close()

        csv_file.seek(0)  # goes to the start of file
        # with open(data_location, 'r+') as csv_file:
        for row in csv_reader:
            print(row)
    pik_inp = person_dict
    pickle.dump(pik_inp, open('pik_inp.pickle', 'wb'))

    pik_inp_data = pickle.load(open('pik_inp.pickle', 'rb'))

    for x in pik_inp_data.keys():
        pik_inp_data[x].display()

    # for x in range(0, line_count-1):
    #     person_dict[x].display()
