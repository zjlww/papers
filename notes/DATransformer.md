---
corpus_id: 248811033
title: "Directed Acyclic Transformer for Non-Autoregressive Machine Translation"
topics: [machine translation, NAR, NLP]
stars: 5
---

This seems to be a fairly original idea.

Finite-state method + neural network. Their source code contains special CUDA kernels. Can this be replaced with k2, which is a universal differentiable FSA implementation?

Yep, the training loss is the sum of all possible paths.

The author mentioned a training trick called "glancing training", basically BERT like training? I think this has appeared in other places with the same name?

The transition model's parameterization seems to be too simple, may be room for improvement?