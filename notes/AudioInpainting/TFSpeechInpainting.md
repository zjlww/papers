---
corpus_id: 204800390
title: "Deep Speech Inpainting of Time-Frequency Masks"
stars: 2
topics: [audio inpainting]
---

1. First train a speech feature extractor.
2. Train a U-Net taking STFT complex spectrogram with mask and output reconstructed spectrogram.
3. Training loss is deep feature loss.
