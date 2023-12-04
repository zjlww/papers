---
corpus_id: 252596091
title: "DreamFusion: Text-to-3D using 2D Diffusion"
stars: 3
topics: [3D generation, diffusion]
---

Tutorial videos?
https://www.youtube.com/watch?v=VvLEp3IKIPA

Optimizing a NERF with a frozen diffusion model in the following way.
- The NERF is a trainable MLP.
- Sample a view from NERF (differenable rendering).
- Under text condition, minimize score loss of the frozen diffusion model.
- Gradient descent to optimize the MLP.

This idea seems to be called score distillation. Indeed it is similar to distillation.

Problem? No theoretical guarantee of the distribution of the 3D object generated.