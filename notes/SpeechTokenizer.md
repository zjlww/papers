---
corpus_id: 261394297
title: "SpeechTokenizer: Unified Speech Tokenizer for Speech Large Language Models"
stars: 2
topics: [ICLR 2024, speech codec, TTS]
---

A combination of many trivial contributions...

This paper poposed a new benchmark (SLMTokBench) for tokenizers? What is it about?

> To build powerful speech language models, discrete speech representations should possess the following two key characteristics:
> i) Strong alignment with text;
> ii) Effective preservation of speech information.

For (i) train a phoneme classifier.
For (ii) convert speech tokens back to speech and evaluate resynthesized speech by automatic metrics on content and timbre.

This paper proposed a new tokenizer (SpeechTokenizer). What is it about?
- Regularize the first level RVQ such that it only contains content information.
- A HUBERT model's L9 representation is used to regularize the first layer VQ vectors.
