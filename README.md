---
title: Beyond Space
emoji: 🎛️
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: cc-by-nc-4.0
---

# Beyond Space

Beyond Space is a browser interface for navigating the latent space of [RAVE](https://github.com/acids-ircam/RAVE) generative audio models. Upload between two and four audio files and the backend encodes each one into a latent trajectory using a pretrained VAE. A 2D board lets you place a point anywhere in the convex hull of those encodings; the system computes a barycentric weighted blend of the latent representations at that position and decodes it back to audio. The result is not a crossfade — it is a new signal synthesised from an interpolated position in the model's learned latent space, shaped by the geometry of all inputs simultaneously.

**Demo:** [beyond-space-kappa.vercel.app](https://beyond-space-kappa.vercel.app)

## How to use

Upload two to four audio files. Once at least two are loaded, a shape appears on the board — a line, triangle, or quadrilateral depending on how many files you have. Click anywhere inside it to set a blend point; the percentages at each node reflect the barycentric weights for that position. Adjust temperature and steps in the left panel to control noise injection and generation length. Select a model from the right panel, then press generate. The output downloads as a WAV file.

## Models

The available models come from the [Intelligent Instruments Lab](https://huggingface.co/Intelligent-Instruments-Lab/rave-models) collection and cover a range of timbres: pipe organ, Bach chorales, guitar, two voice datasets, birdsong, and water recordings. Each model has its own latent geometry, so the same board position will produce very different results depending on which one is active. Models can be switched at any time from the right panel without reloading the page.

## Under the hood

The backend is a FastAPI service running a TorchScript RAVE model loaded via `torch.jit.load`, with models downloaded from Hugging Face Hub on first use and cached. The frontend is React with Vite. All encoding and decoding happens server-side; the browser receives a standard 16-bit PCM WAV.

## Credits

RAVE was developed by [IRCAM/ACIDS](https://github.com/acids-ircam/RAVE). Pretrained models by the [Intelligent Instruments Lab](https://iil.is).
