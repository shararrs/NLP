import pickle
import random


DB_FILENAME = 'demo_database.pickle'


if __name__ == '__main__':
    # load the database and identify the key terms
    database: dict[str, list[str]] = pickle.load(open(DB_FILENAME, 'rb'))
    terms = database.keys()

    def query_database(term):
        """Return a random sentence from the database containing `term`"""
        sent_list = database[term]
        return sent_list[random.randint(0, len(sent_list)-1)]

    # demo code (REPLACE LATER):
    # pick a term, query the db for that term, print it out
    term = next(iter(terms))
    sent = query_database(term)
    print(f'{term}: {sent}')
