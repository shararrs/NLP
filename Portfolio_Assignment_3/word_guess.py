import sys
from collections import Counter

import nltk
from nltk import word_tokenize, WordNetLemmatizer, pos_tag, FreqDist
from nltk.corpus import stopwords


def process_text(tokenized_inp):
    # readin file like this to keep entire text in memory as 1 line
    # easier to word tokenize

    # filtered stop, <5 and is alpha
    game_file_filtered = [t for t in tokenized_inp if t.isalpha() and
                          t not in stopwords.words('english') and len(t) > 5]
    step_a = len(game_file_filtered)
    # print("all words - stop 11043")
    # lemmatizing and finding unique set of words
    # print(f'filtered stop, <5 and is alpha {len(game_file)}')
    # lemmatizing
    wnl = WordNetLemmatizer()
    game_file = [wnl.lemmatize(t) for t in game_file_filtered]
    # create unique list of words
    game_file = set(game_file)
    all_unique_words = len(game_file)
    # print(f'lemmatized unique set {len(game_file)}')
    # part of speech tagging on unique lemmas
    game_file = pos_tag(game_file)
    print('printing first 20 pos tagged words')
    print(game_file[:20])  # keep

    # List of pos tagged nouns singular and plural (NN and NNS) only
    game_file_nn = [t for t in game_file if (t[1] == "NN" or t[1] == "NNS")]
    # print(game_file_nn)
    # print(f'total words after applying filters isalpha, removing stop words and length > 5 are {step_a}')
    print(len(game_file_nn))

    print(game_file_nn)
    return game_file_nn, game_file_filtered


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

    # lexical diversity
    print("\nLexical diversity before any pre processing: %.2f" % (len(set(tokenized_inp)) / len(tokenized_inp)))
    # returning tw values noun for hte game and the step a filtered list
    nouns_for_game, filtered_list = process_text(tokenized_inp)

    noun_dict = {t[0]: filtered_list.count(t[0]) for t in nouns_for_game}

    # sort from highest to lowest based on the value
    noun_dict = sorted(noun_dict.items(), key=lambda item: item[1], reverse=True)
    #top_50_noun = {noun[0] for noun in noun_dict[:50]}
    counter = Counter(noun_dict)
    all = list(counter.keys())
    top_50_noun = []
    for x in range(50):
        top_50_noun.append(all[x][0])
    print(top_50_noun)
    print(len(top_50_noun))

    # inp_file.close()
