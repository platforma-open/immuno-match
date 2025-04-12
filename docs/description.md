# Overview

This block implements the ImmunoMatch framework created by Fraternalilab (https://github.com/Fraternalilab/ImmunoMatch). ImmunoMatch is a machine learning framework for deciphering the molecular rules governing the pairing of antibody chains. Fine-tuned on an antibody-specific language model (AntiBERTA2), ImmunoMatch learns from paired H and L sequences from single human B cells to distinguish cognate H-L pairs and randomly paired sequences.

This integration specifically uses the κ (kappa) and λ (lambda) models from the Fraternalilab ImmunoMatch repository:
- **ImmunoMatch-κ**: Trained on antibodies with κ light chains
- **ImmunoMatch-λ**: Trained on antibodies with λ light chains

The original `Run_ImmunoMatch.ipynb` notebook from the Fraternalilab repository has been modified into a parametrized Python script for use in this block, enabling the tool to obtain H-L pairing scores for given VH-VL sequence pairs or to annotate sequences in batch.

The block takes the output of "MiXCR Clonotyping 2" block as input.

Please cite:
- *doi: [10.1101/2025.02.11.637677](https://doi.org/10.1101/2025.02.11.637677)*

```
@article {Guo2025.02.11.637677,
	author = {Guo, Dongjun and Dunn-Walters, Deborah K and Fraternali, Franca and Ng, Joseph CF},
	title = {ImmunoMatch learns and predicts cognate pairing of heavy and light immunoglobulin chains},
	elocation-id = {2025.02.11.637677},
	year = {2025},
	doi = {10.1101/2025.02.11.637677},
	publisher = {Cold Spring Harbor Laboratory},
	URL = {https://www.biorxiv.org/content/early/2025/02/15/2025.02.11.637677},
	journal = {bioRxiv}
}
```

