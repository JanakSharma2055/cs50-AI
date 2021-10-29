import nltk
import sys
import os
import string
from math import log


FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_contents = {}

    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                # print(entry.name)

                with open(entry.path, encoding='utf8') as f:
                    file_contents[entry.name] = f.read()
    #print(file_contents)
    return file_contents
    


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    word_list = []

    for word in nltk.word_tokenize(document):
        word = word.lower()
        if word in nltk.corpus.stopwords.words('english'):
            continue
        for letter in word:
            if not letter in string.punctuation:
                word_list.append(word)
                break
            
    #print(word_list)
    return word_list



def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # assign zero value to all words
    idf_dict_for_words = {word: 0 for words in documents.values() for word in words}

    for word in idf_dict_for_words:
        # no of document containing that word
        diff = 0
        for document in documents:
            if word in documents[document]:
                diff += 1

        idf_dict_for_words[word] = log(len(documents) / diff)
    #print(idf_dict_for_words)
    return idf_dict_for_words


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = {}

    for filename, words in files.items():
        tf_idfs[filename] = 0
        for word in query:
            if word in words:
                
                tf_idfs[filename] += words.count(word) * idfs[word]

    # sorting on the basis of value of tf_idfs
    first_n_items =sorted(tf_idfs, key=tf_idfs.get, reverse=True)[:n]
    # print(first_n_items)
    return first_n_items

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    idf = {sentence: [0, 0] for sentence in sentences}

    for sentence, words in sentences.items():
        for word in query:
            if word in words:
                
                idf[sentence][0] += idfs[word]
                # query term density
                idf[sentence][1] += words.count(word) / len(words)

    # returns list of sentences sorted by idf  
    return sorted(idf, key=idf.get, reverse=True)[:n]


if __name__ == "__main__":
    main()
