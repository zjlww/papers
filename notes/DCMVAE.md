---
openreview_id: "k5THrhXDV3"
title: "Deep Generative Clustering with Multimodal Diffusion Variational Autoencoders"
stars: 1
topics: [ICLR 2024, clustering]
---

By multimodal, they mean the same modality with many distributional modes.
> In particular, we introduce a novel multimodal VAE model, called Clustering Multimodal VAE (CMVAE). An overview of the method is illustrated in Figure 1. The proposed approach divides the latent space into shared and modalityspecific embeddings (Palumbo et al., 2023), and imposes a Gaussian mixture prior to enforce a clustering structure in the shared latent representation of the data (see Figure 1 (a)).

And they dumped a diffusion on their VAE:
> Finally, inspired by the work of Pandey et al. (2022), we propose to integrate DDPMs (Sohl-Dickstein et al., 2015; Ho et al., 2020) into the CMVAE framework, to further improve the generative quality of reconstructed and generated images while retaining the clustered latent space of CMVAE. In particular, we train the diffusion process conditioned on the CMVAE reconstructions, using both the self and the cross-modal reconstructions, thus enhancing the model’s capacity of generalization.
