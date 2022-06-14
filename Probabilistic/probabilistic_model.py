# import sys
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

def create_matrixes(phrases, words):
    qty = len(phrases)
    freq = {}
    log_words = {}
    docs = {}

    for word in words:
        freq[word] = [0]*qty
        docs[word] = 0
        log_words[word] = [0]*qty

    for word in words:
        for i, phrase in enumerate(phrases):
            if word in phrase:
                rep = phrase.count(word)
                freq[word][i] = rep
                log_words[word][i] = 1 + math.log2(rep)
                docs[word] += 1

    return freq, log_words, docs

def calculate_tf_idf(freq, docs, qty_docs):

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

def calculate_vectorial_rank(qty_docs, query, tf_idf, tf_idf_query, total_norm, query_norm):
    rank = {}

    for doc in range(qty_docs):
        doc_sum = 0
        for term in query:
            doc_sum += tf_idf[term][doc] * tf_idf_query[term][0]
        rank[doc+1] = doc_sum / (total_norm[doc] * query_norm[0])

    return rank

def calculate_probabilistic_rank(freq, qty_docs, query, docs, len_phrases, avg_len_doc, k1, b):
    rank = {}

    for doc in range(qty_docs):
        doc_sum = 0
        for term in query:
            if freq[term][doc] > 0:
                bij = ((k1 + 1) * freq[term][doc]) / (k1 * ((1-b)+(b*(len_phrases[doc]/avg_len_doc))) + freq[term][doc])
                sim = math.log2((qty_docs - docs[term] + 0.5)/(docs[term] + 0.5))
                doc_sum += bij * sim
        rank[doc+1] = doc_sum

    return rank


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

def main_probabilistic(freq, len_phrases, qty_docs, query, docs):
    k1 = float(input('Qual o valor de K1? '))
    b = float(input('Qual o valor de b? '))

    avg_len_doc = sum(len_phrases)/qty_docs

    print('Len phrases: ', len_phrases)

    print('Avg len: ', avg_len_doc)

    rank = calculate_probabilistic_rank(freq, qty_docs, query, docs, len_phrases, avg_len_doc, k1, b)

    print('Rank: ', rank)

    sorted_ranking = [x[0] for x in sorted(rank.items(),key=lambda x: x[1], reverse=True)]

    print('Final Ranking: ', str(sorted_ranking) + '\n')

    return sorted_ranking

def phrase_processing(M, q, stopwords, separadores, words):
    phrases = []
    len_phrases = [0] * len(M)
    print('Phrases:')
    for i, phrase in enumerate(M):
        print(phrase)
        res = pre_processing(phrase[0], stopwords, separadores, words)
        processed_phrase = res[0]
        words = res[1]
        len_phrases[i] = len(processed_phrase)
        phrases.append(processed_phrase)

    qty_docs = len(phrases)

    query = pre_processing(q, stopwords, separadores, words)[0]

    print('Query: ', query, '\n')

    freq, logs, docs = create_matrixes(phrases, words)

    return phrases, len_phrases, qty_docs, query, freq, logs, docs

if __name__ == "__main__":
    method = int(input("Qual método você quer usar? 1 - Booleano ; 2 - Vetorial ; 3 - Probabilístico "))
    if method < 1 or method > 3:
        print("Método inválido")
    else:
        words = []
        phrases, len_phrases, qty_docs, query, freq, logs, docs = phrase_processing(M, q, stopwords, separadores, words)

        if method == 1:
            and_docs, or_docs = run_query(query, freq)
            
            print('Docs that contain all words: ', and_docs)
            print('Docs that contain at least one of these words: ', or_docs)
            
        elif method == 2:
            freq_query, logs_query, _ = create_matrixes([query],query)

            tf_idf, total_norm = calculate_tf_idf(logs,docs,qty_docs)

            tf_idf_query, query_norm = calculate_tf_idf(logs_query,docs,qty_docs)

            print('Query TF-IDF: ', tf_idf_query, " - Query norm: ", query_norm, '\n')

            print('TF-IDF: ', tf_idf, ' - Total norm: ', total_norm, '\n')

            rank = calculate_vectorial_rank(qty_docs, query, tf_idf, tf_idf_query, total_norm, query_norm)

            print('Rank: ', rank)

            print('Final Ranking: ', [x[0] for x in sorted(rank.items(),key=lambda x: x[1], reverse=True)])
        
        else:
            main_probabilistic(freq, len_phrases, qty_docs, query, docs)

