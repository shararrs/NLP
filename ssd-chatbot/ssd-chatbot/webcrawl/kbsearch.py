#  Blake Oberlander	bho180000
#  Sharar Siddiqui	srs200003

import pickle
import random
from nltk import word_tokenize
from nltk import WordNetLemmatizer


class FactDatabase:
    def __init__(self, db_filename):
        # load the database and identify the key terms
        self.database: dict[str, list[str]] = pickle.load(open(db_filename, 'rb'))
        self.terms = self.database.keys()

    def query_database(self, term):
        """Return a random sentence from the database containing `term`"""
        sent_list = self.database[term]
        return sent_list[random.randint(0, len(sent_list)-1)]

    def extract_term(self, query):
        words = word_tokenize(query)
        lemmatizer = WordNetLemmatizer()
        lemmas = [lemmatizer.lemmatize(word.lower()) for word in words]
        for lemma in lemmas:
            if lemma in self.terms:
                return lemma
        return None
