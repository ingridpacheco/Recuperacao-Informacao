import sys

sys.path.insert(0, '../Vectorial')
from vectorial_model import main_vectorial
sys.path.insert(1, '../Probabilistic')
from probabilistic_model import main_probabilistic, phrase_processing
sys.path.insert(2, '../Examples')
import example1
import example2



def calculate_recall(ranking, relevant):

    relevant_len = len(relevant)
    number_recall = []
    cur_number = 0

    for doc in ranking:
        if doc in relevant:
            cur_number += 1
            number_recall.append(cur_number/relevant_len)

    return number_recall

def calculate_precision(ranking, relevant):

    number_precision = []
    cur_number = 0

    for i, doc in enumerate(ranking):
        if doc in relevant:
            cur_number += 1
            number_precision.append(cur_number/(i + 1))

    return number_precision

def interpolated_precision(recall, precision):

    ip = [0] * 11

    for i in range(len(ip)):
        idx = i / 10
        if idx <= recall[0]:
            ip[i] = max(precision)
        else:
            recall = recall[1:]
            precision = precision[1:]
            if len(recall) == 0:
                break
            else:
                while idx > recall[0]:
                    recall = recall[1:]
                    precision = precision[1:]
                    if len(recall) == 0:
                        break
                ip[i] = max(precision)
    return ip

def calculate_MAP(precisions, relevants):

    maps = []

    for i, prec in enumerate(precisions):
        maps.append(1/len(relevants[i]) * sum(prec))

    return 1/len(maps) * sum(maps)

def calculate_assessment(relevants, rankings):

    precisions = []

    for i, ranking in enumerate(rankings):
        print(f"===> Document {i+1} \n")
        print("Ranking: " + str(ranking))
        print('Relevants: ' + str(relevants[i]))
        recall = calculate_recall(ranking, relevants[i])
        print("Recall: " + str(recall))
        precision = calculate_precision(ranking, relevants[i])
        print("Precision: " + str(precision))
        precisions.append(precision)
        print('IP: ' + str(interpolated_precision(recall, precision)) + '\n')
    print("MAP: " + str(calculate_MAP(precisions, relevants)) + "\n")

if __name__ == "__main__":

    print('Vectorial Model: ')

    relevants = [[1,2], [1,3,5,8]]
    rankings = []

    rankings.append(main_vectorial(example1.M, example1.stopwords, example1.q, example1.separadores))
    rankings.append(main_vectorial(example2.M, example2.stopwords, example2.q, example2.separadores))

    calculate_assessment(relevants, rankings)

    print('Probabilistic Model: ')

    relevants = [[1,2], [1,3,5,8]]
    rankings = []

    # Example 1
    words1 = []
    phrases1, len_phrases1, qty_docs1, query1, freq1, logs1, docs1 = phrase_processing(example1.M, example1.q, example1.stopwords, example1.separadores, words1)
    rankings.append(main_probabilistic(freq1, len_phrases1, qty_docs1, query1, docs1))

    # Example 2
    words2 = []
    phrases2, len_phrases2, qty_docs2, query2, freq2, logs2, docs2 = phrase_processing(example2.M, example2.q, example2.stopwords, example2.separadores, words2)
    rankings.append(main_probabilistic(freq2, len_phrases2, qty_docs2, query2, docs2))

    calculate_assessment(relevants, rankings)