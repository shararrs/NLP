#  Blake Oberlander	bho180000
#  Sharar Siddiqui	srs200003

import pickle
import random


DB_FILENAME = 'database.pickle'


if __name__ == '__main__':
    # load the database and identify the key terms
    database: dict[str, list[str]] = pickle.load(open(DB_FILENAME, 'rb'))
    terms = database.keys()

    def query_database(term):
        """Return a random sentence from the database containing `term`"""
        sent_list = database[term]
        return sent_list[random.randint(0, len(sent_list)-1)]

    # prompt user for terms
    print("KB Searcher")
    while True:
        print("Terms: ")
        for term in terms:
            print(f"- {term}")
        print()
        print("Enter a term to explore, or type ! to quit")
        term = input("Term: ").lower().strip()
        if '!' in term:
            break
        if term not in terms:
            print(f'"{term}" not recognized. Try again')
            continue
        fact = query_database(term)
        print(fact)
        print()

    print("Goodbye")