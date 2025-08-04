# RAVE Latent Space Explorer

This project builds upon the original RAVE latent space explorer, extending its functionality to support a dual-input workflow and more flexible latent space manipulations. Unlike the forked version, which was limited to single-file encodings, this implementation allows users to:

- Encode and compare two separate audio inputs simultaneously.
- Perform interpolations and structured traversals between latent representations.
- Adjust key parameters (temperature, duration, steps) directly from a Streamlit-based interface.

These improvements make the system more suitable for creative exploration and real-time audio generation, offering a more interactive and user-friendly experience compared to the original fork.

## Notes

- The script assumes a target sample rate of 48 kHz.
- If the input file is not mono, it will be converted to mono.
- Resampling is handled automatically if needed.


