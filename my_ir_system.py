import argparse
from utils import *
from search import linear_search,inverted_search
from stemming import PorterStemmer
import time

ORIGINAL_FOLDER_NAME = "collection_original"
STOPWORD_FOLDER_NAME = "collection_no_stopwords"
STOP_WORD_FILENAME = "englishST.txt"


def extract_collection(filename):
    file_handler = open(filename, "r+")
    count_blank_lines = 0
    fable_count = 0
    fable_save_filename = None
    fable_text = ""
    
    stop_word_list = get_file_contents(STOP_WORD_FILENAME)
    stop_word_list = [word[:-1] for word in stop_word_list]
    
    
    for count, line_text in enumerate(file_handler):
        # starting of the Article
        if count < 304:
            continue

        # check blank lines
        if line_text == "\n":
            count_blank_lines += 1
            continue

        # if it is title
        if count_blank_lines == 3:
            if fable_save_filename:
                save_fable(ORIGINAL_FOLDER_NAME, fable_save_filename, fable_text)
                remove_stop_words(STOPWORD_FOLDER_NAME,
                                  ORIGINAL_FOLDER_NAME,
                                  fable_save_filename,
                                  stop_word_list
                                  )
            fable_count += 1
            fable_save_filename = get_fable_save_file_name(fable_count, line_text)

            # reset fable text
            fable_text = ""

        if count_blank_lines == 2 or fable_text != "":
            fable_text += line_text

        count_blank_lines = 0
    save_fable(ORIGINAL_FOLDER_NAME, fable_save_filename, fable_text)
    file_handler.close()


if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--extract-collection",
        help="Write down the filename for document extraction.(Default value is aesopa10.txt)",
    )
    parser.add_argument(
        "--model",
        help="Only \"bool\" is availble for now.",
    )
    parser.add_argument(
        "--search-mode",
        help="Only Linear mode is available \"linear\"(other modes will be implemented in a later task)",
    )
    parser.add_argument(
        "--documents",
        help='specifies the source documents for the search."original" / "no_stopwords"',
    )
    parser.add_argument(
        "--stemming",action="store_true",
        help='When used, specifies that words in query and documents should be stemmed.',
    )
    parser.add_argument(
        "--query",
        help='specifies the query text to search',
    )
    args = parser.parse_args()
    query =args.query
    # print(args.stemming)
    if args.stemming:
        ps = PorterStemmer()
        query = ps.stem(query)
    
    if args.extract_collection:
        filename = args.extract_collection
        extract_collection(filename)
        exit()
        
    elif args.search_mode:
        search_mode = args.search_mode
        if search_mode:
            if args.model:
                model = args.model
                if model=="bool":
                    if args.documents:
                        document = args.documents
                        if document=="original":
                            document_path = ORIGINAL_FOLDER_NAME
                        elif document == "no_stopwords":
                            document_path = STOPWORD_FOLDER_NAME
                        else:
                            print("Invalid document name")
                            exit()
                        if query:
                            queries,operation = check_operation(query)
                            if type(queries) == list:
                                document_query=[]
                                if search_mode=="linear":
                                    for search_query in queries:
                                        documents = linear_search(document_path,search_query)
                                        document_query.append(documents)
                                elif search_mode=="inverted":
                                    document_query = inverted_search(document_path,queries)
                                if operation=="&":
                                    documents =set(document_query[0]).intersection(*document_query)
                                elif operation=="|":
                                    documents =set().union(*document_query)
                                elif operation=="~":
                                    #get all documents
                                    all_document_names =get_all_document_names(ORIGINAL_FOLDER_NAME)
                                    documents = zip(*document_query)
                                    documents = list(set(all_document_names)-set(documents))

                            else:
                                if search_mode=="linear":
                                    documents = linear_search(document_path,query)
                                elif search_mode=="inverted":
                                    documents = inverted_search(document_path,[query])
                            
                            print_documents(documents)
                        else:
                            print("No query.Please enter query")
                            exit()
                    else:
                        print("No Document specified")
                        exit()

                else:
                    print("No model specified / Invalid Model Specified")
                    exit()

        else:
            print("No Search Mode specified / Invalid Search Mode Specified")

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    print(f"T:{execution_time} ms")



