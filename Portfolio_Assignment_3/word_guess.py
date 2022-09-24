import sys
import nltk
from nltk import word_tokenize, WordNetLemmatizer, pos_tag
from nltk.corpus import stopwords


def process_text(tokenized_inp):
    # readin file like this to keep entire text in memory as 1 line
    # easier to word tokenize

    # filtered stop, <5 and is alpha
    game_file = [t for t in tokenized_inp if t.isalpha() and
                 t not in stopwords.words('english') and len(t) > 5]
    step_a = len(game_file)
    # print("all words - stop 11043")
    # lemmatizing and finding unique set of words
    # print(f'filtered stop, <5 and is alpha {len(game_file)}')
    # lemmatizing
    wnl = WordNetLemmatizer()
    game_file = [wnl.lemmatize(t) for t in game_file]
    # create unique list of words
    game_file = set(game_file)
    all_unique_words = len(game_file)
    # print(f'lemmatized unique set {len(game_file)}')
    # part of speech tagging on unique lemmas
    game_file = pos_tag(game_file)
    print('printing first 20 pos tagged words')
    print(game_file[:20])  # keep

    # List of pos tagged nouns NN only
    game_file_nn = [t for t in game_file if (t[1] == "NN")]
    # print(game_file_nn)
    #print(f'total words after applying filters isalpha, removing stop words and length > 5 are {step_a}')
    print(len(game_file_nn))

    print(game_file_nn)
    return game_file_nn


# ______________________________________________
if __name__ == '__main__':
    # print_hi('Python')
    # inp = input("Please enter the file to use to play the game")
    print(sys.argv.__len__())
    if (sys.argv.__len__() != 2):
        print("please add the file name as a parameter")
        exit(0)

    print(f'You are using the {sys.argv[1]} to play the game')


    inp_file = open(sys.argv[1]).read()
    # tokenizing all words
    tokenized_inp = word_tokenize(inp_file)
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

    # lexical diversity
    print("\nLexical diversity before any pre processing: %.2f" % (len(set(tokenized_inp)) / len(tokenized_inp)))

    text_for_game = process_text(tokenized_inp)
    #print("After process")
    #print(text_for_game)
    #print(len(text_for_game))


    # inp_file.close()
