import sys


def print_hi(name):
    print(f'Hi, {name}')


# ______________________________________________
if __name__ == '__main__':
    # print_hi('Python')
    # inp = input("Please enter the file to use to play the game")
    print(sys.argv.__len__())
    if (sys.argv.__len__() != 2):
        print("please add the file name as a parameter")
        exit(0)

    print(f'You are using the {sys.argv[1]} to play the game')

    inp_file = open(sys.argv[1], 'r')
    #with open(sys.argv[1]) as inp_file:
    #   game_file= inp_file.readlines()
    game_file = [inp_line.lower() for inp_line in inp_file]
    print(len(game_file))
    #print(game_file)
    inp_file.close()

