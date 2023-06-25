
import os
from utils import *

def read_collection(collection_name):
    collection={}
    for filename in os.listdir(collection_name):
        # document=[]
        fable_text = get_file_contents(os.path.join(collection_name,filename))
        fable_text = [sentence.replace('\n','') for sentence in fable_text]
        document = " ".join(fable_text).lower().split()
        collection[filename]=document
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