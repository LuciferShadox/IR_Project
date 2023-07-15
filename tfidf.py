
import math
from collections import Counter

def calculate_tf_idf(term, document, corpus):
    # Calculate term frequency (TF)
    tf = document.get(term, 0) / max(document.values())

    # Calculate inverse document frequency (IDF)
    document_frequency = sum(1 for doc in corpus if term in doc)
    idf = math.log(len(corpus) / (document_frequency + 1))

    # Calculate tf-idf score
    tf_idf = tf * idf
    return tf_idf

def calculate_document_tf_idf(document, corpus):
    # Calculate tf-idf scores for each term in the document
    document_tf_idf = {
        term: calculate_tf_idf(term, document, corpus) for term in document
    }
    return document_tf_idf

def get_unique_word_count(corpus):
    corpus_term_matrix=[]
    for document_words in corpus.values():
        document_word_count = Counter(document_words)
        corpus_term_matrix.append(dict(document_word_count))
    return corpus_term_matrix

        

def calculate_corpus_tf_idf(corpus):
    #create corpus term matrix
    corpus_term_matrix = get_unique_word_count(corpus)

    # Create a document-term matrix for the corpus
    document_term_matrix = [Counter(doc) for doc in corpus_term_matrix]

    # Calculate tf-idf scores for each document in the corpus
    corpus_tf_idf = [
        calculate_document_tf_idf(doc, corpus) for doc in document_term_matrix
    ]
    return corpus_tf_idf



