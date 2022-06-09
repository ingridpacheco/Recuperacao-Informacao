import math
import sys

sys.path.insert(0, '../Examples')
#from example2 import M, stopwords, q, separadores
from example3 import M, stopwords, q, separadores

words = []

def pre_processing(entry):
    # Tokenizacao
    for s in separadores:
        entry = entry.replace(s, ' ')

    entry = entry.split()

    result = []
    for word in entry:
        # Normalizacao
        word = word.lower()
        # Remocao de stop words
        if word not in stopwords:
            if word not in words:
                words.append(word)
            result.append(word)

    return result

def create_matrixes(phrases):
    qty = len(phrases)
    freq = {}
    docs = {}

    for word in words:
        freq[word] = [0]*qty
        docs[word] = 0

    for word in words:
        for i, phrase in enumerate(phrases):
            if word in phrase:
                rep = phrase.count(word)
                freq[word][i] = 1 + math.log2(rep)
                docs[word] += 1

    return freq, docs

def calculate_tf_idf(freq, docs, qty_docs):

    tf_idf = {}

    for (k,v) in freq.items():
        tf_idf[k] = [0]*len(v)
        for i,doc in enumerate(v):
            tf_idf[k][i] = doc * (math.log2(qty_docs/docs[k]))

    return tf_idf

if __name__ == "__main__":
    phrases = []
    print('Phrases:')
    for phrase in M:
        print(phrase)
        phrases.append(pre_processing(phrase[0]))

    freq,docs = create_matrixes(phrases)

    qty_docs = len(phrases)

    tf_idf = calculate_tf_idf(freq,docs,qty_docs)

    print('TF-IDF: ', tf_idf)