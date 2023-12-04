---
corpus_id: 253581703
title: "All are Worth Words: A ViT Backbone for Diffusion Models"
topics: [dark magic, diffusion, transformer]
stars: 3
---

Related simultaneous work: DiT

This one adds residual connections in a transformer.

What the hell? Not the larger the better in this model?

A list of takeaways from this paper.
- diffusion time, condition, and noisy image patches can be all viewed as tokens.
    - uniform and simple design.
    - Input time as token is more effective then with AdaLN.
        - This is consistent with my results.
- This paper considers skip-connections as crucial.
    - Is this the common perception? 
    - Reported results shows very poor performance without skip connections.
    - Concat + linear is the most effective skip connection method.
- Adding some last 2D CNN accelerates convergence, but no contribution asymptotically.
    - This is consistent with my experiments.
