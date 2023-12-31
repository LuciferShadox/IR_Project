import re
import os
from nltk.tokenize import word_tokenize
# import nltk
# nltk.download('punkt')

def remove_leading_space_and_newline(text):
    return re.sub(r"\n", "", re.sub(r"^\s+", "", text))


def replace_space_with_underscore(text):
    return text.replace(" ", "_")


def get_fable_save_file_name(fable_count, fable_title_line):
    fable_name = remove_leading_space_and_newline(fable_title_line)
    fable_name_with_underscore = replace_space_with_underscore(fable_name)
    return f"{fable_count:02d}_{fable_name_with_underscore.lower()}.txt"

def write_file(filename,text_to_write):
    file =open(filename,'w')
    file.write(text_to_write)
    file.close

def save_fable(original_foldername, fable_name, fable_text):
    # create folder
    if not os.path.exists(original_foldername):
        os.mkdir(original_foldername)
    if fable_text != "":
        fable_name_with_folder_path = os.path.join(original_foldername, fable_name)
        write_file(fable_name_with_folder_path,fable_text)
        # file = open(fable_name_with_folder_path, "w")
        # file.write(fable_text)
        # file.close()
    else:
        print(f"No Fable text for {fable_name}")

def print_documents(documents):
    for document in documents:
        print(document)
    
def get_file_contents(filename):
    file = open(filename,'r')
    contents = file.readlines()
    # for line in contents:
    #     file_contents=file_contents[:-1]+' '+line
    file.close()
    return contents

def remove_extra_spaces(text):
    return ' '.join(text.split())


def remove_stop_words(stopword_foldername,original_foldername, fable_filename,stop_word_list):
    if not os.path.exists(stopword_foldername):
        os.mkdir(stopword_foldername)
    
    fable_name_with_original_folder_path = os.path.join(original_foldername, fable_filename)
    fable_name_with_stopword_folder_path = os.path.join(stopword_foldername, fable_filename)
    fable_text_original = get_file_contents(fable_name_with_original_folder_path)
    fable_text_copy = fable_text_original.copy()
    fable_text_copy = [sentence.replace('\n','') for sentence in fable_text_copy]
    punctuations = ['!','\(',')','-','[',']','{','}',';',':',"\'",'\"','\\','<','>','.','\/','\?','@','#','$','%',
                    '^','&','\*','_','~','\n','\t']
    punctuation_pattern = re.compile(r'[^\s\w]')
    
    tokens = word_tokenize(" ".join(fable_text_copy).lower())
    text = punctuation_pattern.sub(' ', " ".join(tokens).lower())
    tokens_wo_stopwords = [t for t in text.split() if t not in stop_word_list]
    stop_word_text =" ".join(tokens_wo_stopwords)
    write_file(fable_name_with_stopword_folder_path,stop_word_text)


def check_operation(query):
    operation = ""
    if "&" in query:
        operation="&"
        queries=query.split("&")
        return queries,operation
    elif "|" in query:
        operation="|"
        queries=query.split("|")
        return queries,operation
    elif "~" in query:    
        return query.split("~")[1:],"~"
    
    return query,None

def load_ground_truth(filename):
    ground_truth = {}
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            line = line.strip()
            if line:
                parts = line.split('-')
                if len(parts) == 2:
                    term, doc_ids = parts
                    doc_ids = doc_ids.split(',')
                    doc_ids_stripped = [idx.strip() for idx in doc_ids]
                    ground_truth[term.strip()] = doc_ids_stripped
                else:
                    print(f"Ignoring invalid line in ground_truth.txt: {line}")
    return ground_truth

def calculate_precision_recall(documents, ground_truth,query):
    retrieved_documents = []
    #get index of documents
    for document_name in documents:
        retrieved_documents.append(document_name.split("_")[0])
    retrieved_documents=set(retrieved_documents)
    try:
        relevant_documents = set(ground_truth[query])
        common_documents = retrieved_documents.intersection(relevant_documents)
        precision = len(common_documents) / len(retrieved_documents) if retrieved_documents else 0
        recall = len(common_documents) / len(relevant_documents) if relevant_documents else 0
        return precision, recall
    except Exception as e:
        return None,None





def get_all_document_names(folder_path):
    return os.listdir(folder_path)


    
