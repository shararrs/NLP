from nltk import word_tokenize
import pickle


def tokenize_sent(sentence: str) -> list[str]:
    """Return lowercase tokens in a sentence"""

    return [word.lower() for word in word_tokenize(sentence)]


def load_sentences(filename):
    """Read sentences from a file"""
    with open(filename) as file:
        return [sent.strip() for sent in file.readlines()]


def get_terms(n: int) -> list[str]:
    """Prompt the user to enter 10 terms, then return them"""
    print(f"Enter Top {n} terms:")
    return [
        input(f"Term {i+1}: ").strip().lower()
        for i in range(n)
    ]


SENT_FILENAME = 'demo_sentences.txt'
DB_FILENAME = 'demo_database.pickle'

if __name__ == '__main__':
    sentences = load_sentences(filename="demo_sentences.txt")
    terms = set(get_terms(10))

    sent_database: dict[str, list[str]] = {term: [] for term in terms}

    # Find sentences containing terms, and store them in the database
    for sentence in sentences:
        for token in tokenize_sent(sentence):
            if token in terms:
                sent_database[token].append(sentence)

    pickle.dump(sent_database, open(DB_FILENAME, 'wb'))






