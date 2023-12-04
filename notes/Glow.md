---
corpus_id: 49657329
title: "Glow: Generative Flow with Invertible 1x1 Convolutions"
topics: [generative model, normalizing flow, image generation]
stars: 4
---

Quite popular, but seems like a one step forward on Real-NVP.

> Consistent with earlier work on likelihood-based generative models (Parmar et al., 2018), we found that sampling from a reduced-temperature model often results in higher-quality samples. When sampling with temperature T, we sample from the distribution p θ,T (x) ∝ (p θ (x)) T 2 . In case of additive coupling layers, this can be achieved simply by multiplying the standard deviation of p θ (z) by a factor of T.

This is not a very clear description of low-temperature. What did the author mean by additive coupling layers???

The code is available at https://github.com/openai/glow. The code is shitty, and there is no trace of low temperature sampling.