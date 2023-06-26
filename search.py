
import os
from utils import *
from string import punctuation

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

def linear_search(collection_name, search_term):
    results = []
    collection = read_collection(collection_name)
    for filename, document in collection.items():
        for word in document:
            if search_term.lower() in word.lower():
                results.append(filename)
                break
    return results

def inverted_search(collection_name, search_terms):
    results = []
    collection = read_collection(collection_name)
    inverted_index = build_inverted_index(collection_name)
    matching_docs = []
    for term in search_terms:
        if term.lower() in inverted_index:
            matching_docs.append(inverted_index[term.lower()])
    return matching_docs

def build_inverted_index(collection_name):
    inverted_index = {}
    collection = read_collection(collection_name)
    for filename, document in collection.items():
        for word in document:
            lower_word = word.lower()
            if lower_word not in inverted_index:
                inverted_index[lower_word] = [filename]
            elif filename not in inverted_index[lower_word]:
                inverted_index[lower_word].append(filename)
    return inverted_index
