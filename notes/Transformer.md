---
corpus_id: 13756489
title: "Attention is All you Need"
topics: [dark magic]
stars: 4
---

Self-attention + cross-attention in the decoder?
The order of layers in the decoder block is:
1. Self-attention.
2. Add residual, and Layer Norm.
3. Cross-attention.
4. Add residual, and Layer Norm.
5. Linear+ReLU+Linear.
6. Add residual, and Layer Norm.

What is the order of the layers? I heard debate on post-norm and pre-norm?
So pre-norm is y = x + F(norm(x)). And post-norm is y = norm(x + F(x)).
It describes the order of a group of resudial + norm + transform.

In the popular choice, Conformer, what is the order?
Conformer is using pre-norm.