from random import randint
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

    # lemmatizing and finding unique set of words
    # lemmatizing
    wnl = WordNetLemmatizer()
    game_file = [wnl.lemmatize(t) for t in game_file_filtered]

    # create unique list of words
    game_file = set(game_file)
    all_unique_words = len(game_file)

    # part of speech tagging on unique lemmas
    game_file = pos_tag(game_file)
    print('printing first 20 pos tagged words')
    print(game_file[:20])  # keep

    # List of pos tagged nouns singular and plural (NN and NNS) only
    game_file_nn = [t for t in game_file if (t[1] == "NN" or t[1] == "NNS")]
    print(len(game_file_nn))

    print(game_file_nn)
    return game_file_nn, game_file_filtered


def game_on(list_of_words):
    global inp
    points = 5
    while True:
        # word = random.choice(list_of_words)
        random_num = randint(0, 49)
        print(f'the number selected is {random_num}')
        word = list_of_words[random_num]
        print('Type \'!\' to exit at any time')
        word = list(word)
        blank_word = []
        user_inputs = []
        print(word)
        print(len(word))
        for i in range(len(word)):
            blank_word.append('_')
        print(''.join(blank_word))
        while True:
            # check if the whole word has been guessed
            finished = 0  # signifies if the word has been guessed
            if not blank_word.__contains__('_'):
                finished = 1

            if finished == 1:
                print('You solved it!')
                print(f'Current score: {points}')
                break

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
            count = 0
            guess = 0
            while count < len(word):
                # check if user input this character before
                if word[count] == inp:
                    blank_word[count] = inp
                    word[count] = '_'
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

        #print('Play more? press enter for yes and type n for no')
        #if input().lower() == 'n':
        #    print(f'Final score {points}')
        #    break
        if inp == '!':
            print(f'Final score {points}')
            break

        continue


# ______________________________________________


if __name__ == '__main__':
    # print_hi('Python')
    # inp = input("Please enter the file to use to play the game")
    print(sys.argv.__len__())
    if sys.argv.__len__() != 2:
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
    # top_50_noun = {noun[0] for noun in noun_dict[:50]}
    counter = Counter(noun_dict)
    all_keys = list(counter.keys())
    top_50_noun = []
    for x in range(50):
        top_50_noun.append(all_keys[x][0])
    print(top_50_noun)
    print(len(top_50_noun))

    game_on(top_50_noun)

    # inp_file.close()
