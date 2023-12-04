---
corpus_id: 256416291
title: "InstructTTS: Modelling Expressive TTS in Discrete Latent Space with Natural Language Style Prompt"
stars: 3
topics: [representation learning, TTS, conditional generation]
---

Complex system is cool, but no key innovation.

Proprietary NLSpeech dataset contains a bunch of (audio, text, style) pairs.

What are the modules?
- ContentEncoder(text: str) -> matrix.
    - Basically text embedding in standard TTS.
- PromptEncoder(text: str) -> vector.
    - Inconsistent naming in the paper? PromptEncoder and ContentEncoder mixed?
- AudioEncoder(audio: matrix) -> vector.
- SpeakerLUT(sid: int) -> vector.
- VQDiffusion(content: matrix, prompt: vector, speaker: vector) -> audio.
    - We ignored the VQEncoder and VQDecoder here.

How are the modules trained?
1. Train PromptEncoder: RoBERTa(text: str) -> vector (basically BERT, extract cls) on Chinese.
    - CLUECorpusSmall, 14G Chinese text.
    - L=12, H=768.
2. Finetune PromptEncoder: RoBERTa with SimCSE loss. 
    - Performance on sentence-similarity is much better than Sentence BERT.
3. Joint train AudioEncoder and PromptEncoder with contrastive loss (InfoNCE) on NLSpeech.
    - InfoNCE brings better retrieval performance.
    - Evaluated on audio-text retrieval task.
4. Joint train VQDiffusion, ContentEncoder, AudioEncoder, PromptEncoder. The loss is complicated.
    - Freeze parameters of PromptEncoder, add trainable last layer (called Adaptor).
    - Minimize VQ Diffusion Loss.
    - Minimize MI of AudioEncoder(audio) and SpeakerLUT(sid).
    - Minimize MI of AudioEncoder(audio) and ContentEncoder(text).
    - Minimize L2 of PromptEncoder(prompt) and AudioEncoder(audio).
    - Variance Adaptor Loss.
