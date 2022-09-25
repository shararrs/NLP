import sys
from collections import Counter
from random import randint

from nltk import word_tokenize, WordNetLemmatizer, pos_tag
from nltk.corpus import stopwords


# function takes in tokenized words
# returns a set of nouns and processed non lemmatized words
def process_text(tokenized_input):
    # filtered stopwords, <5 and is alpha
    game_file_filtered = [t for t in tokenized_input if t.isalpha() and
                          t not in stopwords.words('english') and len(t) > 5]

    # lemmatizing and finding unique set of words
    # lemmatizing
    wnl = WordNetLemmatizer()
    game_file = [wnl.lemmatize(t) for t in game_file_filtered]

    # create unique list of words
    game_file = set(game_file)

    # part of speech tagging on unique lemmas
    game_file = pos_tag(game_file)
    print('\nPrinting first 20 pos tagged words')
    print(game_file[:20])

    # List of pos tagged nouns singular and plural (NN and NNS) only
    game_file_nn = [t for t in game_file if (t[1] == "NN" or t[1] == "NNS")]

    print(f'\nTotal tokens after filtering(non lemmatized and non unique): {len(game_file_filtered)}')
    print(f'Total nouns (NN and NNS only) : {len(game_file_nn)}')

    # returning nouns and non lemmatized tokens
    return game_file_nn, game_file_filtered


# this function has the game logic
# takes in list of words tp play the game with
# returns nothing
def game_on(list_of_words):
    global inp
    points = 5
    while True:
        random_num = randint(0, 49)
        word = list_of_words[random_num]
        print('\nType \'!\' to exit at any time')
        word = list(word)
        blank_word = []  # this is displayed and updated when a word
        user_inputs = []  # holds input that was tried by the user

        # enable to get the answer displayed at the start
        # print(word)
        # print(len(word))

        for i in range(len(word)):
            blank_word.append('_')
        print(''.join(blank_word))
        while True:
            # check if the whole word has been guessed
            finished = 0  # signifies if the word has been guessed or not
            if not blank_word.__contains__('_'):
                finished = 1

            if finished == 1:
                print('You solved it!')
                print(f'Current score: {points}')
                break

            # start guessing
            # check if valid input or game should end
            if points < 0:
                break
            inp = input("Guess a letter:")
            inp.lower()

            if inp == '!':
                break

            if not inp.isalpha():
                print('Please enter a letter')
                continue

            if len(inp) != 1:
                print('Please input only 1 character each turn')
                continue

            if inp in user_inputs:
                points = points - 1
                print(f'Sorry, you have tried this character before guess again. Score is {points}')
                continue
            else:
                user_inputs.append(inp)

            # checking/comparing logic
            count = 0  # used to loop through list
            guess = 0  # bool to check if guess is right or wrong
            while count < len(word):
                # check if user had tried this character before
                if word[count] == inp:
                    blank_word[count] = inp
                    word[count] = '*'
                    guess = 1
                count = count + 1

            # whether right or wrong
            if guess == 1:
                points = points + 1
                print(f'Right! Score is {points}')
                print(''.join(blank_word))
            else:
                points = points - 1
                print(f'Sorry, guess again. Score is {points}')
                print(''.join(blank_word))

        if inp == '!':
            print(f'Final score {points}')
            break
        if points < 0:
            print(f'Sorry you lost, nice try though')
            break

        continue


# ______________________________________________________________________________________________________________________


if __name__ == '__main__':
    if sys.argv.__len__() != 2:
        print("Please add the file name as a parameter, \nmake sure it is in the same folder as the game file")
        exit(0)

    print(f'You are using nouns in the \"{sys.argv[1]}\" to play the game')

    inp_file = open(sys.argv[1]).read()
    # tokenizing all words
    tokenized_inp = word_tokenize(inp_file)

    # lexical diversity
    print("\nLexical diversity before any pre processing: %.2f" % (len(set(tokenized_inp)) / len(tokenized_inp)))

    # returning two values noun for hte game and the step a filtered list
    print('Generating file may take a bit, please be patient.')
    print('__________________________________________________________________________________________________________')
    nouns_for_game, filtered_list = process_text(tokenized_inp)

    # make a dict of nouns:count of nouns in tokens
    noun_dict = {t[0]: filtered_list.count(t[0]) for t in nouns_for_game}

    # sort from highest to lowest based on the value
    noun_dict = sorted(noun_dict.items(), key=lambda item: item[1], reverse=True)

    # printing top 50 nouns and saving as a new list
    counter = Counter(noun_dict)
    all_keys = list(counter.keys())
    top_50_noun = []
    for x in range(50):
        top_50_noun.append(all_keys[x][0])
    print(top_50_noun)

    game_on(top_50_noun)
