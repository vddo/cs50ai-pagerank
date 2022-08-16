import os
import random
import re
import sys
from pomegranate import *


DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    # ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    # print(f"PageRank Results from Sampling (n = {SAMPLES})")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")
    # ranks = iterate_pagerank(corpus, DAMPING)
    # print(f"PageRank Results from Iteration")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")
    # Prints output of function crawl
    print({sys.argv[1]})
    print(corpus)


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
    # print(pages)
    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Constant variables
    count_pages = len(corpus)
    count_links = len(corpus[page])

    # Create empty dict for transition model
    dict_tm = dict()

    # Loop over corpus' keys
    for page_i in corpus:
        # If page has no outgoing links then chose any page with equal probab
        if count_links == 0:
            p_i = 1 / count_pages
        else:
            # If page_i is a link in page then probability is a sum
            if page_i in corpus[page]:
                p_i = 1 / count_links * damping_factor + \
                    1 / count_pages * (1 - damping_factor)
            else:
                p_i = 1 / count_pages * (1 - damping_factor)
        dict_tm[page_i] = p_i
    return dict_tm


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Define some constants
    count_pages = len(corpus)
    random_surfer_chain = list()
    pagerank_sample = dict()
    n_bak = n

    # First Sample; chose randomly from every page
    p_0 = 1 / count_pages
    distribution_0 = dict()

    for page_i in corpus:
        distribution_0[page_i] = p_0

    # Generate discrete distribution for randomly picking from all pages
    d0 = DiscreteDistribution(distribution_0)

    # Chose first sample randomly with MarkovChain
    model_0 = MarkovChain([d0])
    # print(model_0.sample(1))
    random_surfer_chain.append(model_0.sample(1)[0])

    # Refresh sample count
    n -= 1
    #
    while n > 0:
        distribution_i = DiscreteDistribution(transition_model(
            corpus, random_surfer_chain[-1], damping_factor))
        model_i = MarkovChain([distribution_i])
        random_surfer_chain.append(model_i.sample(1)[0])
        n -= 1

    # Count page appearences
    for page_i in corpus:
        pagerank_sample[page_i] = random_surfer_chain.count(page_i) / n_bak

    return pagerank_sample


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
