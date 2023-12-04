---
corpus_id: 254854389
title: "Scalable Diffusion Models with Transformers"
topics: [dark magic, diffusion, transformer]
stars: 3
---

Related: UViT

Some results from this paper are contradicting those in U-ViT.
- DiT claims that U-Net architecture is not important.
- DiT claims that conditioning with adaLN is better than as tokens.
- DiT claims that their model scales well, but U-ViT has some scaling issues.

They proposed to initialize a transformer to identity. Is this choice experimented before? I suspect that this is extremely important for transformer + diffusion models.
