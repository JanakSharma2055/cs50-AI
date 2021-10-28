import nltk
import sys
import itertools

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
S -> S Conj S
NP -> N | Det NP | NP P NP | P NP | Adj NP | NP Conj NP
VP -> V | VP NP | Adv VP | VP Adv | VP Conj VP
 
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    #this part is done
    #converting the given sentences into list of words
    words =nltk.word_tokenize(sentence)
    new_list =[]
    for word in words:
        word =word.lower()
        for char in word:
            if char>='a' and char<= 'z':
                new_list.append(word.lower())
                break
    return new_list
    




def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    trees = []
    #this returns all the subtrees having NP as label
    for subtree in tree.subtrees(lambda t: t.label() == 'NP'):
        trees.append(subtree)

    #filtering of those subtrees whose internal subtrees has label NP
    for tree1, tree2 in itertools.combinations(trees, 2):

        if tree1 in trees and tree2 in tree1.subtrees():
            trees.remove(tree1)
        
        elif tree2 in trees and tree1 in tree2.subtrees():
            trees.remove(tree2)


    return trees



if __name__ == "__main__":
    main()
