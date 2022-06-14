import math
import sys

sys.path.insert(0, '../Examples')
#from example3 import M, stopwords, q, separadores
#from example2 import M, stopwords, q, separadores
from example1 import M, stopwords, q, separadores

def pre_processing(entry, stopwords, separadores, words):
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

    return result, words

def create_matrixes(phrases,words):
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

    print('Words frequencies in docs: ' + str(freq))
    print('Words frequencies: ' + str(docs))
    print('Quantity of documents: ' + str(qty_docs) + '\n')

    tf_idf = {}
    vector_norm = [0] * qty_docs

    for (k,v) in freq.items():
        tf_idf[k] = [0] * qty_docs
        for i,doc in enumerate(v):
            tf_idf[k][i] = doc * math.log2(qty_docs/docs[k])
            vector_norm[i] += tf_idf[k][i] ** 2

    for i,v in enumerate(vector_norm):
        vector_norm[i] = math.sqrt(vector_norm[i])

    return tf_idf, vector_norm

def calculate_rank(qty_docs, query, tf_idf, tf_idf_query, total_norm, query_norm):
    rank = {}

    for doc in range(qty_docs):
        doc_sum = 0
        for term in query:
            doc_sum += tf_idf[term][doc] * tf_idf_query[term][0]
        rank[doc+1] = doc_sum / (total_norm[doc] * query_norm[0])

    return rank

def main_vectorial(M, stopwords, q, separadores):
    phrases = []
    print('Phrases:')
    words = []
    for phrase in M:
        print(phrase)
        res = pre_processing(phrase[0], stopwords, separadores, words)
        phrases.append(res[0])
        words = res[1]

    query = pre_processing(q, stopwords, separadores, words)[0]
    
    print('Query: ', query, '\n')

    freq,docs = create_matrixes(phrases, words)

    freq_query,_ = create_matrixes([query],query)

    qty_docs = len(phrases)

    tf_idf, total_norm = calculate_tf_idf(freq,docs,qty_docs)

    tf_idf_query, query_norm = calculate_tf_idf(freq_query,docs,qty_docs)

    print('Query TF-IDF: ', tf_idf_query, " - Query norm: ", query_norm, '\n')

    print('TF-IDF: ', tf_idf, ' - Total norm: ', total_norm, '\n')

    rank = calculate_rank(qty_docs, query, tf_idf, tf_idf_query, total_norm, query_norm)

    print('Rank: ', rank)

    sorted_ranking = [x[0] for x in sorted(rank.items(),key=lambda x: x[1], reverse=True)]

    print('Final Ranking: ', str(sorted_ranking) + '\n')

    return sorted_ranking

if __name__ == "__main__":
    main_vectorial(M, stopwords, q, separadores)