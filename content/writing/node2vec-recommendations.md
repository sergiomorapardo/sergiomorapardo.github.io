---
title: "From co-likes to candidates with Node2Vec"
description: "A practical route from MovieLens interactions to graph embeddings, along with the evidence and limits needed before calling the result a recommender."
date: 2026-09-06T00:00:00-05:00
translationKey: "node2vec-recommendations"
weight: 1
level: "Intermediate"
topic: "Recommendation systems"
repository: "AdvancedTopicsAnalytics"
repository_url: "https://github.com/sergiomorapardo/AdvancedTopicsAnalytics"
notebook: "L25-Node2Vec-RecSys.ipynb"
notebook_url: "https://github.com/sergiomorapardo/AdvancedTopicsAnalytics/blob/main/notebooks/L25-Node2Vec-RecSys.ipynb"
tags: ["Node2Vec", "Graph ML", "Recommendation"]
---

A catalog can become a graph before it becomes a recommender. In the source notebook, two movies are connected when the same users rate both of them highly. Node2Vec then turns the resulting neighborhoods into vectors, so nearby movies can be retrieved with a cosine-similarity lookup.

That is a useful candidate-generation pattern. It is not, by itself, a complete recommendation system. This note separates what the notebook demonstrates from the evaluation and serving work that a production system would still need.

## Frame the signal

The notebook uses the MovieLens 100K data loaded from GroupLens. The raw table contains **100,000 ratings** and 1,682 movie records. The first editorial decision is to treat only ratings of four or five as positive preference. That leaves **55,375 positive interactions** in the executed output.

```python
ratings = pd.read_csv(
    "ml-100k/u.data",
    sep="\t",
    names=["user_id", "movie_id", "rating", "unix_timestamp"],
)

positive = ratings[ratings.rating >= 4]
```

This threshold makes the graph easier to explain: an edge now represents repeated co-liking, not merely co-rating. It also discards information. A rating of one and a missing rating both become an absent positive edge, even though they mean different things. That tradeoff is acceptable for a compact teaching example, but it should be explicit.

## Build a movie graph

For every user, the notebook enumerates pairs among that user's positively rated movies. Each pair receives a count equal to the number of users who liked both titles. Only pairs observed at least 20 times become edges.

```python
from collections import defaultdict

pairs = defaultdict(int)
for _, user_ratings in positive.groupby("user_id"):
    user_movies = list(user_ratings["movie_id"])
    for i in range(len(user_movies)):
        for j in range(i + 1, len(user_movies)):
            pairs[(user_movies[i], user_movies[j])] += 1

graph = nx.Graph()
for (movie_a, movie_b), count in pairs.items():
    if count >= 20:
        graph.add_edge(movie_a, movie_b, weight=count)
```

The executed notebook reports **410 nodes and 14,936 edges** after filtering. The edge threshold reduces noise and computation, but it also favors popular titles. Long-tail movies that do not collect 20 shared positive raters disappear before Node2Vec starts.

There is another scaling issue hidden in the simple loop: generating every pair for every user grows quadratically with the number of liked items per user. For a larger event stream, the same idea would need sparse matrix operations, bounded histories, sampling, or distributed aggregation.

## Learn local neighborhoods

Node2Vec creates biased random walks through the graph and trains a Word2Vec-style model on those walks. Movies that occur in similar graph contexts receive similar vectors. The notebook uses 64 dimensions, walks of length 20, 200 walks per node, and a context window of 10.

```python
from node2vec import Node2Vec

walker = Node2Vec(
    graph,
    dimensions=64,
    walk_length=20,
    num_walks=200,
    p=2,
    q=1,
    workers=1,
)
model = walker.fit(window=10, min_count=1, batch_words=4)
```

The parameters `p` and `q` control how the walks balance revisiting a node against exploring farther neighborhoods. Here, `p=2` makes an immediate return less likely than it would be at `p=1`, while `q=1` keeps the outward exploration neutral. They are modeling choices, not universal defaults. Their value should ultimately be judged by retrieval quality, not by how tidy a two-dimensional plot looks.

## Retrieve candidates

Recommendation is a nearest-neighbor query in the learned vector space. For a seed movie, the notebook finds the five most similar embeddings and maps their IDs back to titles.

```python
def recommend(title, top_n=5):
    movie_id = str(movies.loc[movies.title == title, "movie_id"].iloc[0])
    neighbors = model.wv.most_similar(movie_id, topn=top_n)
    return [
        (movies.loc[movies.movie_id == int(node_id), "title"].iloc[0], score)
        for node_id, score in neighbors
    ]
```

For **Star Wars (1977)**, the saved output begins with *Raiders of the Lost Ark* at 0.59 and *Return of the Jedi* at 0.55. For **Toy Story (1995)**, it begins with *Return of the Jedi* at 0.77 and *Twelve Monkeys* at 0.75. Those examples show that the pipeline produces inspectable neighbors. They do not establish that users prefer these lists over a popularity baseline or another collaborative method.

The notebook also projects the 64-dimensional embeddings with t-SNE. That view can help inspect local clusters, but t-SNE distorts global distances. It should be treated as a diagnostic visualization, not as evidence that recommendation quality is high.

## Turn the lesson into a system

A production version would separate retrieval, ranking, evaluation, and serving:

1. **Retrieval:** use the graph embedding to generate a few hundred candidates from recent positive interactions.
2. **Filtering:** remove unavailable, already consumed, unsafe, or otherwise ineligible items.
3. **Ranking:** combine user, item, context, and freshness features in a model aligned with the product objective.
4. **Offline evaluation:** split interactions by time and report recall@K, precision@K, coverage, novelty, and popularity bias against clear baselines.
5. **Online evaluation:** test the complete experience with guardrails, not just clicks on the recommendation module.
6. **Serving:** version embeddings, define cold-start fallbacks, and monitor catalog coverage plus neighborhood drift.

The source notebook earns its place as a technical note because the central abstraction is strong: co-preference becomes graph structure, and graph structure becomes a reusable retrieval space. The next engineering step is to keep that elegant idea while adding honest evaluation and operational constraints.

> Source boundary: all dataset counts, graph dimensions, hyperparameters, and example neighbors above come from the saved notebook output. The production extensions are proposed next steps, not results claimed by the notebook.
