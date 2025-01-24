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
    prob_dist = {}

    for key in corpus.keys():
        if key in corpus[page]:
            prob_dist[key] = damping_factor / len(corpus[page]) + (1 - damping_factor)
        else:
            prob_dist[key] = 1 - damping_factor
    
    return prob_dist

def sample_pagerank(corpus: dict, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    from random import choice, choices

    pagerank = {}
    for key in corpus.keys():
        pagerank[key] = 0

    page = choice(list(corpus.keys()))
    for i in range(n):
        distribution = list(transition_model(corpus, page, damping_factor).items())
        page = choices(population=[x[0] for x in distribution], weights=[x[1] for x in distribution], k=1)[0]
        pagerank[page] += 1
    
    for key in pagerank.keys():
        pagerank[key] /= n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    EPSILON = 0.001
    max_diff = 1

    pagerank = {}
    for key in corpus.keys():
        pagerank[key] = 1/len(corpus)
    
    while max_diff > EPSILON:
        max_diff = 0

        for key in pagerank.keys():
            value = (1 - damping_factor)/len(pagerank)
            
            link_to_key = []
            for k in corpus.keys():
                if key in corpus[k]:
                    link_to_key.append(k)
            
            if len(link_to_key) == 0:
                for link in corpus.keys():
                    value += (x := damping_factor * pagerank[link] / len(corpus))
            else:
                for link in link_to_key:
                    value += (x := damping_factor * pagerank[link] / len(corpus[link]))
                
            diff = abs(pagerank[key] - value)

            if diff > max_diff:
                max_diff = diff
            
            pagerank[key] = value
    
    return pagerank


if __name__ == "__main__":
    main()
