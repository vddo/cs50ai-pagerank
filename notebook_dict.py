from pagerank import *

corpus = crawl(
    "/Users/duc/Desktop/CS50AI_code/P2_Uncertainty/pagerank/corpus0")

iter(corpus)
print(iter(corpus))

corpus.items()
corpus.keys()
reversed(corpus)
corpus.get("4.html")

for i in corpus:
    for j in corpus:
        if j is not i:
            print(j)

corpus.get("2.html")
list(corpus.get("2.html"))
list(corpus.get("2.html")).count("1.html")

n = 0
if "1.html" in corpus.get("2.html"):
    n += 1

"1.html" in corpus["2.html"]
len(corpus)

corpus

len(corpus["40.html"])

corpus
corpus_t0 = corpus
corpus["4.html"] = 2
corpus
corpus_t0

list(corpus)
corpus.values()
list(corpus.values())
