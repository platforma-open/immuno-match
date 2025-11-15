# Overview

Predicts cognate pairing of heavy and light immunoglobulin chains from single-cell B-cell receptor sequencing data using the ImmunoMatch machine learning framework. The block processes VH-VL sequence pairs from single-cell clonotype data (e.g., from MiXCR Clonotyping) and uses fine-tuned antibody-specific language models (AntiBERTA2) to distinguish authentic cognate H-L pairs from randomly paired sequences, enabling accurate reconstruction of complete antibody molecules from single-cell sequencing data.

The block implements the ImmunoMatch framework created by Fraternalilab, which learns molecular rules governing antibody chain pairing from paired H and L sequences from single human B cells. The integration uses separate models for κ (kappa) and λ (lambda) light chains, allowing accurate pairing prediction for both light chain types. For each VH-VL sequence pair, the block calculates pairing scores that quantify the likelihood of cognate pairing, enabling identification of authentic antibody pairs and filtering of spurious pairings that may arise from sequencing or analysis artifacts. This analysis is essential for downstream applications such as antibody discovery, functional characterization, and understanding antibody-antigen interactions.

The block uses ImmunoMatch models from the [Fraternalilab repository](https://github.com/Fraternalilab/ImmunoMatch). When using this block in your research, cite the ImmunoMatch publication (Guo et al. 2025) listed below.

The following publication describes the methodology used:

> Guo, D., Dunn-Walters, D. K., Fraternali, F., & Ng, J. C. F. (2025). ImmunoMatch learns and predicts cognate pairing of heavy and light immunoglobulin chains. _bioRxiv_ 2025.02.11.637677 (2025). [https://doi.org/10.1101/2025.02.11.637677](https://doi.org/10.1101/2025.02.11.637677)
