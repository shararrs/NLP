import sys
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords


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
    # readin file like this to keep entire text in memory as 1 line
    # easier to word tokenize
    inp_file = open(sys.argv[1]).read()
    # tokenizing all words
    game_file = word_tokenize(inp_file)
    # -------------------------------------
    # getting unique words using set()
    # game_file = set(game_file)
    # print("total unique words 3096")
    # print(len(game_file))
    # game_file = [t for t in game_file if t.isalpha() and
    #             t not in stopwords.words('english')]
    # print("total unique words - stop words 2819")
    # print(len(game_file))
    # -------------------------------------
    game_file = [t for t in game_file if t.isalpha() and
                 t not in stopwords.words('english') and len(t) > 5]
    print("all words - stop 11043")
    #lemmatizing and finding unique set of words
    #game_file =
    print(len(game_file))
    game_file = set(game_file)
    print(len(game_file))

    # inp_file.close()
