import re

#open file
file_handler = open("aesopa10.txt",'r+')
for count,line_text in enumerate(file_handler):
    # to know the starting index 
    if line_text.startswith("Aesop's Fables"):
        print(count+1)

file_handler.close()