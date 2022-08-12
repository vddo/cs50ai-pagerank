from pagerank import *

corpus = crawl(
    "/Users/duc/Desktop/CS50AI_code/P2_Uncertainty/pagerank/corpus0")
P3 = "3.html"


distribution_0 = sample_pagerank(corpus, 0.85, 10)
d0 = DiscreteDistribution(distribution_0)

pagerank = sample_pagerank(corpus, 0.85, 10)
sample_pagerank(corpus, 0.85, 10000)
