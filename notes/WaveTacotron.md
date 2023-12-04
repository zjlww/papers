---
corpus_id: 226282382
title: "Wave-Tacotron: Spectrogram-Free End-to-End Text-to-Speech Synthesis"
topics: [AR, TTS]
stars: 3
---

Using normalizing flow as the distribution parameterization of tacotron. So yet another block-wise autoregressive model. Each block is about 3.75 x 256 sampling points.

So WaveGlow? Again, low-temperature sampling is improving the performance of the model. The temperature is set to 0.7 during inference.
