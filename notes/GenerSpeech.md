---
corpus_id: 248811428
title: "GenerSpeech: Towards Style Transfer for Generalizable Out-Of-Domain Text-to-Speech Synthesis"
topics: [TTS, voice cloning, dark magic]
stars: 1
---

What is the definition of style?
> Style transfer for out-of-domain (OOD) speech synthesis aims to generate speech samples with unseen style derived from an acoustic reference.

What is counted as style of speech?
> Everything other than the content. (e.g., speaker identity, emotion, and prosody)

So it is just yet another work on voice cloning? What are the problems solved in this work?
> Generalizability to unseen and out-of-domain speech.
> Generalizability to extremely expressive and dynamic cases.

Well, the generalization problem... good luck with that!

What are the proposed solutions? They tuned the neural network architecture.
1. A freakishly complicated multi-scale style encoder.
2. Layer Normalization to eliminate style information in text representation.
