---
corpus_id: 264935149
title: "E3 TTS: Easy End-to-End Diffusion-based Text to Speech"
topics: [diffusion, TTS, NAR]
stars: 4
---

Idea similar to Simple-TTS(ICLR 2024 OpenReview).

How many new metrics are there for evaluating TTS? ==TODO==
- Using SQuId for quality estimation. And Fr´echet Speaker Distance for speaker distribution comparison.

What is the dataset used for training?
- proprietary 400 hours wiht 84 speakers.
- Quality of dataset matters. The model does not perform very well on LibriTTS all.

What is the network architecture? What can be learned from this work?
- Almost the same as a diffusion vocoder, but trained on sentences with cross-attention to BERT.
- I estimate the computation would be quite large.

Why does it work and previous work do not?
- Cheap accessible computation at Google?

