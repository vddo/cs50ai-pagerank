from pagerank_random import *
import random

random.sample(["1.h", "2.h"], counts=[2, 10], k=1)


corpus = crawl(
    "/Users/duc/Desktop/CS50AI_code/P2_Uncertainty/pagerank/corpus0")

sample_pagerank(corpus, 0.85, 10000)
a = sample_pagerank(corpus, 0.85, 10000)
a["4.html"] * 2
# random.sample()


# Some Testing

a = [1, 3, 5]

for i in a:
    b = a.pop(0)
    a.append(b*10000)

a

range(len(a))

for i in range(len(a)):
    print(i)
