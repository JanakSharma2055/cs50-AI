import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_distribution ={}
    SIZE =len(corpus)

    if corpus[page]:
        #if page has links 
        for item in corpus[page]:
            prob_distribution[item] = damping_factor/SIZE

        for item in corpus:
            prob_distribution[item] = prob_distribution.get(item,0) + (1-damping_factor)/SIZE
    
    else:
        #random selection of those pages that donot have any link
        for item in corpus:
            prob_distribution[item] = 1/SIZE

    return prob_distribution        
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank_list = {page: 0 for page in corpus}

    
    key_list =list(corpus)
    random_choosen_item = random.choice(key_list)

    
    for i in range(n):
        
        rank_list[random_choosen_item] += 1/n

       
        t = transition_model(corpus, random_choosen_item, damping_factor)

        #returns a list with single item and the first item is extracted from
        #the list of items
        random_choosen_item = random.choices(list(t.keys()), weights=list(t.values()), k=1)[0]

    return rank_list
    

    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank_list = {}

    for name in corpus:
        rank_list[name] = 1 / len(corpus)

    while True:
        calculated_ranks = {}
        for name in corpus:
            for page, link in corpus.items():
                #if not link then it is assumed to have a link to all pages
                if name in link:
                    calculated_ranks[name] = calculated_ranks.get(name, 0) + rank_list[page]/len(link)

                if not link:
                    link = set(corpus)

                
        #making deep copy of list items
        previous_rank = rank_list.copy()
        for name in corpus:
            rank_list[name] = (1 - damping_factor)/len(corpus) + damping_factor * calculated_ranks.get(name, 0)

        #calculation of difference of the rank value from previous one as
        #to check for accuracy
        threshold = {name: abs(previous_rank[name] - rank_list[name]) for name in rank_list}
      
      #this is to check for accuracy 
        if all(round(value,3) <= 0.001 for value in threshold.values()):
            break

    return rank_list


if __name__ == "__main__":
    main()
