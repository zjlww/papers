---
corpus_id: 263834729
title: "DASpeech: Directed Acyclic Transformer for Fast and High-quality Speech-to-Speech Translation"
topics: [speech translation, NAR]
stars: 3
---

One step forward from DA-Transformer.

The generation process is fully parallel.
```
Source Speech -[Speech to Text DA Transformer]-> Target Phoneme -[FastSpeech]-> Mel Spectrogram
```

I am not so clear about how the DA-Transformer works:

> During training, we consider all possible paths in the DAG by calculating the expected hidden state for each target token via dynamic programming, which are fed to the acoustic decoder to predict the target mel-spectrogram. During inference, we first find the most probable path in DAG and take hidden states on that path as input to the acoustic decoder.

Using the CVSS dataset, is this the state of current speech translation datasets?