# Team Members:
# Blake Oberlander (bho180000)
# Sharar Siddiqui (srs200003)

import pickle
from nltk import word_tokenize, ngrams


def load(language) -> (dict[tuple, int], dict[tuple, int]):
    """Load the unigrams and bigrams for a language, then return them along with the word count and vocab size """

    unigram_dict = pickle.load(open(f"{language}-unigrams.pickle", 'rb'))
    bigram_dict = pickle.load(open(f"{language}-bigrams.pickle", 'rb'))

    N = sum((x for (x) in unigram_dict.values()))   # word count
    V = len(unigram_dict)                           # vocab size

    return unigram_dict, bigram_dict, N, V


def evaluate(text: str, unigram_dict, bigram_dict, N, V) -> float:
    """Given a sentence, and the unigram and bigram dictionaries from a language, calculate the probability of
    seeing the sentence in the language
    """

    # get bigrams
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    # using the markov assumption, calculate the probability of this sentence appearing in the language
    l = 1
    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        l *= ((n + 1) / (d + V))
    return l


def predict(sent, *languages) -> int:
    """Given a sentence and parameters for a list of languages, return the index of the language that has
    the highest probability"""

    lang_probs = [(i, evaluate(sent, u, b, N, V)) for (i, (u, b, N, V)) in enumerate(languages)]
    return max(lang_probs, key=lambda x: x[1])[0]



if __name__ == '__main__':

    # load all the languages
    english = load('english')
    french = load('french')
    italian = load('italian')

    lang_names = ['English', 'French', 'Italian']


    # write output to this file
    with open('LangId.pred', 'w') as output_file:
        output_lines = []

        correct = 0
        total = 0
        incorrect = []

        # iterate over each sentence and the solution language
        for i, (line, line_sol) in enumerate(
                zip(open('ngram_files/LangId.test').readlines(),
                    open('ngram_files/LangId.sol').readlines()
                    )
        ):

            # predict the best language
            best_index = predict(line, english, french, italian)
            predicted_lang = lang_names[best_index]
            output_lines += f"{i+1} {predicted_lang}\n"

            # get the expected language
            expected_lang = line_sol.strip().split(" ")[1]

            # compare and save metrics
            total += 1
            if predicted_lang == expected_lang:
                correct += 1
            else:
                incorrect.append(i+1)

        accuracy = correct / total
        print(f"Accuracy: {accuracy*100}%")
        print("Incorrect lines:")
        print(incorrect)

        output_file.writelines(output_lines)
