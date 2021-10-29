import os
import nltk
import string


# def load_files(directory):
#     """
#     Given a directory name, return a dictionary mapping the filename of each
#     `.txt` file inside that directory to the file's contents as a string.
#     """
#     file_contents = {}

#     with os.scandir(directory) as entries:
#         for entry in entries:
#             if entry.is_file():
				

#                 with open(entry.path, encoding='utf8') as f:
#                     file_contents[entry.name] = f.read()
#                 print(entry.name)

#     return file_contents


# file_contents =load_files('corpus')
# print(file_contents['machine_learning.txt'])

my_str ='''Hello!!!, he said ---and went.'''

word_list = []

for word in nltk.word_tokenize(my_str):
    print(word)
    word = word.lower()
    if word in nltk.corpus.stopwords.words('english'):
        continue
    
    for letter in word:
        if not letter in string.punctuation:
            word_list.append(word)
            break
            

    

print(word_list)