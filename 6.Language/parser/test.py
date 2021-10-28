from nltk.tree import Tree

# words = nltk.word_tokenize("I had a little moist red paint in the palm of my hand.")

# print(list(
#         word.lower() for word in words
#         if any(c.isalpha() for c in word)
#     ))

# new_list =[]
# for word in words:
# 	word =word.lower()
# 	for char in word:
# 		if char>='a' and char<= 'z':
# 			new_list.append(word)
# 			break
# print(new_list)


t = Tree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
for s in t.subtrees():
     print(s)