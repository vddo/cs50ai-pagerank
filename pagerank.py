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
    # Define variables
    count_pages = len(corpus)
    count_links = len(corpus[page])

    # Create empty dict for transition model
    dict_tm = dict()

    # Loop over corpus keys
    for page_i in corpus:
        # If page has no outgoing links then chose any page with equal
        # probability
        if count_links == 0:
            p_i = 1 / count_pages
        else:
            # If page_i is a link in page then probability is sum of two parts
            if page_i in corpus[page]:
                p_i = 1 / count_links * damping_factor + \
                    1 / count_pages * (1 - damping_factor)
            else:
                p_i = 1 / count_pages * (1 - damping_factor)
        # Add page with probability
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
    # Define variables
    count_pages = len(corpus)
    random_surfer_chain = list()
    pagerank_sample = dict()        # Final dict to return
    n_bak = n                       # Original amount sample; needed for PR

    # First Sample; chose randomly/evenly from every page
    p_0 = 1 / count_pages
    distribution_0 = dict()

    for page_i in corpus:
        distribution_0[page_i] = p_0

    # Preping distribution values
    counts = list(distribution_0.values())
    for i in counts:
        a = counts.pop(0)
        counts.append(int(a*10000))

    # Randomly chosing one sample with distribution_0
    sample0 = random.sample(list(distribution_0),
                            counts=counts, k=1)

    # Append somple to chain
    random_surfer_chain.append(sample0[0])

    # Refresh sample count
    n -= 1
    # Loop n times; last sample new distribution
    while n > 0:
        # call transition model for new distribution i;
        # page is latest sample from chain;
        distribution_i = transition_model(
            corpus, random_surfer_chain[-1], damping_factor)
        # Preping distribution values
        counts = list(distribution_i.values())
        for i in counts:
            a = counts.pop(0)
            counts.append(int(a*10000))
        # Take one sample from latest distribution and append to chain
        random_surfer_chain.append(random.sample(
            list(distribution_i), counts=counts, k=1)[0])
        # Refresh counter
        n -= 1

    # Count page appearances and calculate page rank
    for page_i in corpus:
        pagerank_sample[page_i] = random_surfer_chain.count(page_i) / n_bak

    return pagerank_sample


# Deep copy new dict to old to calculate delta
def copy_dict_PR_iterate(current, backup):
    backup.clear()
    for key_i in current:
        backup[key_i] = current[key_i]


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Define variables
    N = len(corpus)
    pagerank_iterate = dict()       # Later be returned
    pagerank_iterate_0 = dict()

    # Assigning each page same initial PR
    for page_i in corpus:
        pagerank_iterate[page_i] = 1 / N

    # Iteration
    # delta threshold arbitrary value > 0 (int)
    loop_th = 100
    # p-loop
    while loop_th > 0:
        copy_dict_PR_iterate(current=pagerank_iterate,
                             backup=pagerank_iterate_0)
        for p in corpus:
            # Sum over linking pages; initial 0
            PR_pi = 0
            # i-loop
            for i in corpus:
                # Current PR of page i
                PR_i = pagerank_iterate_0[i]
                # Discarding same page; otherwise self linking possible
                if i is not p:
                    # If page without any link at all
                    if len(corpus[i]) == 0:
                        PR_pi += PR_i / N
                    # If page i is linking to p
                    elif p in corpus[i]:
                        N_i = len(corpus[i])
                        PR_pi += PR_i / N_i
                    # Close i-loop
            # Calculate page rank for p with equation from course
            PR_p = (1 - damping_factor) / N + damping_factor * PR_pi
            pagerank_iterate[p] = PR_p
        # Compare to previous
        pr1 = list(pagerank_iterate.values())
        pr0 = list(pagerank_iterate_0.values())
        # Set to fulfill while-condition
        loop_th = 0
        delta_list = list()
        # Extract delta values
        for i in range(len(pr1)):
            delta_list.append(abs(pr1[i] - pr0[i]))
        # Check delta 0.001
        for delta in delta_list:
            print(delta)
            if delta > 0.001:
                loop_th += 100

    return pagerank_iterate


if __name__ == "__main__":
    main()
