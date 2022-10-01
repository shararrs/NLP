# Team Members:
# Blake Oberlander (bho180000)
# Sharar Siddiqui (srs200003)

from nltk import word_tokenize, ngrams
from collections import Counter
import pickle


def train(filename):
    """Loads in the training data for a given language
    returns dictionary of unigram and bigram"""

    with open(filename, 'r', encoding='utf8') as f:
        tokens = word_tokenize(f.read().replace('\n', ' '))

    unigrams = [(token,) for token in tokens]
    bigrams = list(ngrams(tokens, 2))

    # count unigrams and bigrams
    unigram_count = dict(Counter((
        unigram
        for
        unigram in unigrams
    )))

    bigram_count = dict(Counter((
        bigram
        for
        bigram in bigrams
    )))

    return unigram_count, bigram_count


def pickle_save(language, unigrams, bigrams):
    """Pickles unigram and bigrams to individual files,
    Uses the language parameter to specify the language"""
    pickle.dump(unigrams, open(f"{language}-unigrams.pickle", 'wb'))
    pickle.dump(bigrams, open(f"{language}-bigrams.pickle", 'wb'))


if __name__ == '__main__':
    # find the unigram and bigram counts for each language
    english_uni, english_bi = train('ngram_files/LangId.train.English')
    french_uni, french_bi = train('ngram_files/LangId.train.French')
    italian_uni, italian_bi = train('ngram_files/LangId.train.Italian')

    # save
    print('Starting to pickle 3 language training data')
    pickle_save('english', english_uni, english_bi)
    pickle_save('french', french_uni, french_bi)
    pickle_save('italian', italian_uni, italian_bi)
    print('Finished pickling output')
    exit(0)
