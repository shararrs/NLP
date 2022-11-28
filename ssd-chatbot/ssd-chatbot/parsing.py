from nltk.metrics import edit_distance
from nltk import word_tokenize, WordNetLemmatizer
from nltk import ngrams
import re
import numpy as np
from json import loads

with open('brand-list.txt', 'r') as brand_file:
    BRANDS = [line.strip().lower() for line in brand_file.readlines()]


def correct_brand_name(word: str) -> str:
    """Return a brand (or model) name if the word is similar to a laptop brand/model name. Otherwise return an empty string"""
    max_diff = 0
    if len(word) > 3:
        max_diff = 1
    if len(word) > 6:
        max_diff = 2
    if len(word) > 9:
        max_diff = 3

    for brand in BRANDS:
        if edit_distance(word, brand) <= max_diff:
            return brand
    if len(word) > 2 and any((
            special_character in word
            for special_character in ('-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    )):
        return word

    return ""


LAPTOP_STOP_WORDS = (
    'and',
    'with',
    'that',
    'which',
    'but',
    'so',
    'for',
    'because',
    'although',
)


def parse_laptop_name(line: str) -> str:
    """
    Extract the name of a laptop from a user query

    :param line: Query string containing a laptop name, such as "I have an Acer Aspire 4324 with 8 GB RAM"
    :return: The name of the laptop, which is extracted from the query
    """

    # get a list of lowercase tokens.
    tokens = [token.strip().lower() for token in line.split(" ")]

    # introduce punctuation at certain words to indicate the end of a laptop name
    # For example: "I have an Acer Aspire 43242 with 8 GB RAM"
    #               ->
    #               "I have an Acer Aspire 43232 . 8 GB RAM"
    # Now the "with 8 GB RAM" will not be included in the laptop name
    tokens = [token if token not in LAPTOP_STOP_WORDS else '.'
              for token in tokens if token
              ]

    # Look for a brand name in the laptop.
    # The brand name is always a prefix to the laptop name
    brand_name = None
    for i in range(len(tokens)):
        current_token = tokens[i]
        brand_name = correct_brand_name(current_token)
        if brand_name:
            # Replace the brand name with "BrandName".
            # This is used as a marker for the next step
            tokens[i] = "BrandName"
            break

    if not brand_name:
        return ""


    substituted_name = ' '.join(tokens)
    a = re.search(r"(BrandName)( +[^\.\,\!\?\#\%\^\* \n]+){1,4}", substituted_name)

    # if a result is found:
    if a:
        # return the laptop name, and change BrandName back to the actual brand name
        return a.group(0).replace('BrandName', brand_name)

    # no result -> return ""
    return ""


lemmatizer = WordNetLemmatizer()
punctuation = [',', '.', '?']


def extract_ngrams(query: str) -> list:
    """Return all unigrams and bigrams in a query"""
    lemmas = [
        lemmatizer.lemmatize(word)
        for word in word_tokenize(query.lower())
        if word not in punctuation
    ]
    unigrams = ngrams(lemmas, 1)
    bigrams = ngrams(lemmas, 2, pad_left=True)
    return [*unigrams, *bigrams]


def cosine_similarity(a: np.ndarray, b: np.ndarray):
    """Return the cosine similarity between two vectors"""
    return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b)+0.01)


class IntentExtractor:
    def __init__(self, preprocessor):
        """
        :param preprocessor: A function that takes and returns a string. Will be used on each query
        """
        self.intents_training : dict[str, list[str]] = {}
        self.ngrams = []
        self.ngram_id : dict[tuple, int] = {}
        self.intents_model: dict[str, list[np.ndarray]] = {}
        self.preprocessor = preprocessor

    def add_intent(self, intent_name: str, queries: list[str]):
        """
        Registers an intent.

        :param intent_name: A label for the intent
        :param queries: A list of training examples of what queries of this intent should look like
        :return: nothing
        """
        self.intents_training[intent_name] = [
            self.preprocessor(query)
            for query in queries
        ]

    def vectorize(self, query):
        """
        only call this after training

        :param query: Query string
        :return: A vector representing the query string
        """
        query_vector = np.zeros((len(self.ngrams)))
        for ngram in extract_ngrams(query):
            if ngram in self.ngram_id:
                query_vector[self.ngram_id[ngram]] += 1
        return query_vector

    def train(self):
        # get all the n-grams in the training data
        self.ngrams = list(set((
            ngram
            for intent, queries in self.intents_training.items()
            for query in queries
            for ngram in extract_ngrams(query)
        )))

        # create a ngram -> index map
        self.ngram_id = {ngram: index for index, ngram in enumerate(self.ngrams)}

        # vectorize and remember each training query
        for intent, queries in self.intents_training.items():
            query_vectors = [self.vectorize(query) for query in queries]
            self.intents_model[intent] = query_vectors

    def get_intent(self, query):
        """Given a query, return the predicted intent"""
        query = self.preprocessor(query)
        query_vector = self.vectorize(query)

        # use cosine similarity to get best intent
        return max((
            (intent, cosine_similarity(intent_vector, query_vector))
            for intent, intent_vectors in self.intents_model.items()
            for intent_vector in intent_vectors
        ), key=lambda x: x[1])[0]


with open('synonyms.json', 'r') as f:
    synonyms: dict[str, list[str]] = loads(f.read().lower())

with open('sample-queries.json', 'r') as f:
    sample_queries: dict[str, list[str]] = loads(f.read().lower())


def main_preprocessor(query: str) -> str:
    """This preprocessor lowercases the query and replaces synonyms with the same word to improve accuracy"""
    query = query.lower()
    for word, word_synonyms in synonyms.items():
        for word_synonym in word_synonyms:
            query = query.replace(word_synonym, word)
    return query
