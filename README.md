# Robotic Active Learning Workflow for Nanoformulation Screening

This repository contains the code for a robotic active learning workflow designed for nanoformulation screening. It includes three main folders:

- `0_helper_functions`
- `1st_round_screening`
- `2nd_round_screening`

## Folder Structure & Description

### `0_helper_functions`

This folder contains two Python files:

- **`calculation.py`**  
  Facilitates the conversion of drug/excipient ratios into volumes used for nanoformulation.

- **`sdlnano.py`**  
  Supports the generation of OT2 protocols using those volumes.  
  Also contains functions for Bayesian optimization, including the initial design space and AX client for generating trials.

### `1st_round_screening`

This folder includes scripts and data for the first round of nanoformulation screening using an automated robotic system and active learning. It features:

- 11 total iterations:
  - 1 initial random iteration
  - 10 subsequent Bayesian optimization iterations
- All experiment data stored in the `ACE` folder, organized by iteration index.
- **`1st_data_analysis.ipynb`**:
  - A Jupyter Notebook used to analyze results from the iterations.
  - Outputs figures and saves combined data as `aggregated_data.csv`.

### `2nd_round_screening`

This folder focuses on manual nanoformulation screening using a DOE (Design of Experiments) strategy.

- **`DOE.ipynb`**:
  - Used to generate the DOE strategy for manual preparation.
- **`2nd_data_analysis.ipynb`**:
  - A Jupyter Notebook used to analyze the manually prepared samples and generate corresponding figures.

## Environment Setup

The project environment is saved as:  
**`sdlnano_environment.yml`**

Use the following command to create the environment:

```bash
conda env create -f sdlnano_environment.yml
