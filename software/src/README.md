# Running independently from the block

## Setup

1. Setup a python virtual env: `python3 -m venv venv`
2. Activate it: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

## Run

Command-line version of the ImmunoMatch tool that uses the Immunomatch-kappa and Immunomatch-lambda models to predict cognate pairing in antibody sequences.

```python
python immuno-match.py \
    --input ./example_input/King_Tonsil_GC_paired.csv \
    --output predictions.csv \
    --hseq_col VH \
    --lseq_col VL \
    --ltype_col=locus \
    --kappa_dir /path/to/immunomatch-kappa \
    --lambda_dir /path/to/immunomatch-lambda
```

# Source Information

This tool is based on ImmunoMatch, a machine learning framework for predicting cognate pairing between immunoglobulin heavy and light chains.

- Original Google Colab notebook: [Run_ImmunoMatch.ipynb](https://colab.research.google.com/github/Fraternalilab/ImmunoMatch/blob/main/Run_ImmunoMatch.ipynb)
- GitHub repository: [Fraternalilab/ImmunoMatch](https://github.com/Fraternalilab/ImmunoMatch)

# Citation

Guo, D., Dunn-Walters, D. K., Fraternali, F., & Ng, J. C. F. (2025). ImmunoMatch learns and predicts cognate pairing of heavy and light immunoglobulin chains. bioRxiv, 2025.02.11.637677. https://doi.org/10.1101/2025.02.11.637677

BibTeX format:
```bibtex
@article{Guo2025ImmunoMatch,
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