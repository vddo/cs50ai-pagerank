from pagerank import *
from pomegranate import *
a = {
    'one': 1, 'two': 2, 'three': 3
}

a

a['one'] += 5

a

# Test Crawler funciton

corpus = crawl(
    "/Users/duc/Desktop/CS50AI_code/P2_Uncertainty/pagerank/corpus0")
corpus

P2 = "2.html"
corpus[P2]
len(corpus[P2])

list(corpus)
len(list(corpus))

'1.html' in corpus[P2]

for i in corpus:
    if i in corpus[P2]:
        print(i)

out = {}
out
type(out)

out["P1"] = 0.2
out

out["P2"] = 0.7
out

out["P3"] = 0.1
out

type(out)


# Testing transition model
P3 = "3.html"
transition_model(corpus, P3, 0.85)

0.4625 + 0.4625 + 2*0.037500000000000006

# Test first sample
sample_pagerank(corpus, 1, 1)
n = 10000
n -= 1
n

T1 = sample_pagerank(corpus, 0.85, 10)
T1[-1]

transition_model(corpus, P3, 0.85)
DiscreteDistribution(transition_model(corpus, P3, 0.85))
