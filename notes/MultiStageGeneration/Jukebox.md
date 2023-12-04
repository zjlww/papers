---
corpus_id: 218470180
title: "Jukebox: A Generative Model for Music"
stars: 4
topics: [cascaded generation, music generation]
---

How was the hierarchical codebook obtained?

Apparently there are some problems in automatically constructing a hierarchy of code:

> When using the hierarchical VQ-VAE from (Razavi et al., 2019) for raw audio, we observed that the bottlenecked top level is utilized very little and sometimes experiences a com- plete collapse, as the model decides to pass all information through the less bottlenecked lower levels. To maximize the amount of information stored at each level, we simply train separate autoencoders with varying hop lengths. Dis- crete codes from each level can be treated as independent encodings of the input at different levels of compression.
