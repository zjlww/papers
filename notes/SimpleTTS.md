---
openreview_id: "m4mwbPjOwb"
title: "Simple-TTS: End-to-End Text-to-Speech Synthesis with Latent Diffusion"
topics: [diffusion, TTS, NAR]
stars: 3
---

The backbone is U-Net + Transformer. And the text embedding is ByT5.

This paper is the first to implement explicit alignment free parallel TTS.

Classifier-free guidance once again is the key to performance. The weight is w = 5.0 in this paper.

Is there is solid mathematic background to this idea?

It is kind of funny such an important trick has no solid background. Similar to reducing the temperature of noise in Glow model...
