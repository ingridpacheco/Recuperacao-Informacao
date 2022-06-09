import sys

sys.path.insert(0, '../Examples')
#from example1 import M, stopwords, q, separadores
from example2 import M, stopwords, q, separadores
#from example3 import M, stopwords, q, separadores

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

def create_matrix(phrases):
    qty = len(phrases)
    freq = {}

    for word in words:
        freq[word] = [0]*qty

    for word in words:
        for i, phrase in enumerate(phrases):
            if word in phrase:
                freq[word][i] = phrase.count(word)

    return freq

def run_query(query, df):
    docs = []

    w = query.pop(0)
    for i, v in enumerate(df[w]):
            if v > 0:
                docs.append(i)

    and_docs = docs[:]
    or_docs = docs[:]

    for word in query:
        for i, v in enumerate(df[word]):
            if i in and_docs:
                if df[word][i] == 0:
                    and_docs.remove(i)
            if i not in or_docs:
                if df[word][i] > 0:
                    or_docs.append(i)

    return (and_docs, or_docs)

if __name__ == "__main__":
    phrases = []
    print('Phrases:')
    for phrase in M:
        print(phrase)
        phrases.append(pre_processing(phrase[0]))

    df = create_matrix(phrases)

    query = pre_processing(q)
    print('Query: ', query)

    and_docs, or_docs = run_query(query, df)
    print('Docs that contain all words: ', and_docs)
    print('Docs that contain at least one of these words: ', or_docs)