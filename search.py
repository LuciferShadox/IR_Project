
import os
from utils import *
from string import punctuation
from tfidf import calculate_corpus_tf_idf
import numpy as np
from collections import defaultdict
import math

def read_collection(collection_name):
    collection={}
    for filename in os.listdir(collection_name):
        # document=[]
        fable_text = get_file_contents(os.path.join(collection_name,filename))
        fable_text = [sentence.replace('\n','') for sentence in fable_text]
        document = " ".join(fable_text).lower().split()
        new_document=[]
        for word in document:
            new_document.append(word.strip(punctuation))
        collection[filename]=new_document
    return collection

def linear_search(collection_name,search_term):
    results = []
    collection = read_collection(collection_name)
    for filename,document in collection.items():
        for word in document:
            if search_term in word:
                results.append(filename)
                break
    return results

def inverted_search(collection_name, search_terms):
    results = []
    collection = read_collection(collection_name)
    inverted_index = build_inverted_index(collection_name)
    matching_docs = []
    for term in search_terms:
        if term in inverted_index:
            matching_docs.append(inverted_index[term])
    # for filename in matching_docs:
    #     document = collection.get(filename, [])
    #     if all(term in document for term in search_terms):
    #         results.append(filename)
    return matching_docs




def build_inverted_index(collection_name):
    inverted_index = {}
    collection = read_collection(collection_name)
    for filename, document in collection.items():
        for word in document:
            if word not in inverted_index:
                inverted_index[word] = [filename]
            elif filename not in inverted_index[word]:
                inverted_index[word].append(filename)
    return inverted_index

def cosine_similarity(query_vector,document_vectors):
    similarity_scores = []

    for idx, doc in enumerate(document_vectors):
        dot_product = sum(query_vector[term] * doc.get(term, 0) for term in query_vector)
        query_norm = math.sqrt(sum(value ** 2 for value in query_vector.values()))
        doc_norm = math.sqrt(sum(value ** 2 for value in doc.values()))
        similarity = dot_product / (query_norm * doc_norm)
        similarity_scores.append((idx, similarity))

    return np.array(similarity_scores)


def search_documents(query_vector, document_vectors, documents, top_k=10):
    # Calculate the cosine similarity between the query vector and document vectors
    similarities = cosine_similarity(query_vector, document_vectors)
    # Get the indices of the top-k most similar documents
    top_indices = similarities.argsort()[0][::-1][:top_k]
    # Retrieve the top-k documents along with their similarity scores
    # results = [(documents[i], similarities[0, i]) for i in top_indices]
    results = [documents[i] for i in top_indices]
    return results

# #vector Space Search
# def vector_space_model(collection_name,search_term):
#     collection = read_collection(collection_name)
#     document_vectors = calculate_corpus_tf_idf(collection)
#     #need to build query vector

   # results = search_documents(query_vector, document_vectors, collection, top_k=10)
def build_document_term_matrix(documents):
    document_term_matrix = []
    vocabulary = set()

    for doc in documents:
        term_freq = defaultdict(int)
        for term in doc:
            term_freq[term] += 1
            vocabulary.add(term)

        document_term_matrix.append(term_freq)

    return document_term_matrix, vocabulary


def calculate_idf(document_term_matrix):
    idf = {}
    total_documents = len(document_term_matrix)

    for doc in document_term_matrix:
        for term in doc:
            idf[term] = idf.get(term, 0) + 1

    for term, freq in idf.items():
        idf[term] = math.log(total_documents / freq)

    return idf

def calculate_tf_idf(document_term_matrix, idf):
    tf_idf = []

    for doc in document_term_matrix:
        doc_tf_idf = {}

        for term, freq in doc.items():
            doc_tf_idf[term] = freq * idf[term]

        tf_idf.append(doc_tf_idf)

    return tf_idf

def build_query_vector(query, vocabulary):
    # Create a query vector using the same vocabulary as the document-term matrix
    query_vector = defaultdict(int)
    for term in query.split():
        if term in vocabulary:
            query_vector[term] += 1

    return query_vector

def vector_space_model(collection_name,search_term):
    
    collection = read_collection(collection_name)
    document_names = list(collection.keys())
    documents = list(collection.values())
    # Step 2: Build the document-term matrix
    document_term_matrix, vocabulary = build_document_term_matrix(documents)
    # Step 3: Calculate IDF
    idf = calculate_idf(document_term_matrix)
    # Step 4: Calculate tf.idf weights for the documents
    tf_idf = calculate_tf_idf(document_term_matrix, idf)
    # Step 6: Preprocess the query and construct the query vector
    query_vector = build_query_vector(search_term, vocabulary)
    top_k = 10
    results = search_documents(query_vector, tf_idf, document_names, top_k)
    # Print the search results
    return results


if __name__=="__main__":
    vector_space_model("collection_original","wolf")