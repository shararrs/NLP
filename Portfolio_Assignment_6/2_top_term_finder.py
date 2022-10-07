import nltk
from nltk import word_tokenize, sent_tokenize
from collections import defaultdict
from nltk.corpus import reuters
from nltk.corpus import stopwords
import math
import os

stopwords = stopwords.words('english')

def file_clean(file_num):
    sentences = []
    with open(f'sent_tokenized/{file_num}_sent.txt', 'w', encoding='utf8') as writeFile:

        with open(f'websites/{file_num}.txt', 'r', encoding='utf8') as read_file:
            file_text = read_file.read()
            file_text = file_text.replace('\n', ' ')  # remove new lines
            file_text = file_text.replace('\r', ' ')  # remove carriage return
            file_text = file_text.replace('\t', ' ')  # remove tabs
            file_text = file_text.replace('\u00A0', ' ')  # remove  
            file_text = file_text.replace('\u200B', ' ')  # remove ​
            for sent in sent_tokenize(file_text):
                if len(word_tokenize(sent)) > 3 and not any((substr in sent for substr in ('?',))):
                    sentences.append(sent)

        writeFile.write('\n'.join(sentences))

    return sentences


def filter_words(words):
    return ((w.lower() for w in words if w.isalpha() and w not in stopwords))


def create_tf_dict(doc):
    # returns a normalized term frequency dict
    # doc is a set of processed tokens
    tf_dict = {}
    tokens = word_tokenize(doc)
    tokens = list(filter_words(tokens))
    # get term frequencies
    for t in tokens:
        if t in tf_dict:
            tf_dict[t] += 1
        else:
            tf_dict[t] = 1
    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)
    return tf_dict


def get_per_word_doc_count(documents):
    doc_counter = defaultdict(lambda: 0)
    for doc in documents:
        vocab_set = list(filter_words(word_tokenize(doc)))
        for word in vocab_set:
            doc_counter[word]+=1
    return doc_counter


def extract_top_terms(target_document, general_documents, n):
    per_word_doc_count = get_per_word_doc_count(general_documents)
    tf_dict = create_tf_dict(target_document)
    idf_dict = {}
    target_vocab = set((filter_words(word_tokenize(target_document))))
    for vocab_word in target_vocab:
        idf_dict[vocab_word] = math.log((1+len(general_documents))/(1+per_word_doc_count[vocab_word]))

    tf_idf = {}
    for term in tf_dict.keys():
        tf_idf[term] = tf_dict[term]*idf_dict[term]

    top_n_words = sorted(list(tf_idf.items()), key=lambda x: x[1], reverse=True)[:n]
    return top_n_words


def get_general_documents():
    return [
        str(reuters.raw(filename))
        for filename in reuters.fileids()
    ]


if __name__ == '__main__':
    if not os.path.exists('sent_tokenized'):
        os.makedirs('sent_tokenized')

    all_sentences = []
    for x in range(1, 21):
        all_sentences.extend(file_clean(x))

    target_string = ' '.join(all_sentences)
    general_documents = get_general_documents()
    top_terms = extract_top_terms(target_string, general_documents, 15)
    print(top_terms)




