# Installation

## Pre-Requisites

!!! note

    If you are on a Windows machine, we recommend using the [Windows Subsystem for Linux (WSL)](https://ubuntu.com/wsl) to benefit from all the features of quacc.

1. Install Python, preferably in conjunction with an environment manager. For instance, download and run the [Miniconda installer](https://docs.conda.io/en/latest/miniconda.html)
2. When asked to add Miniconda to your `PATH`, select yes
3. Create a fresh Python environment by running `conda create -n quacc python=3.10`
4. Activate this environment via `conda activate quacc`

## Installing quacc

In your newly activated conda environment, run the following commands to install quacc. Note that you will need to install quacc on all machines where you plan to run calculations.

For the latest PyPI release:

```bash
# Install development version of ASE
pip install --no-cache-dir https://gitlab.com/ase/ase/-/archive/master/ase-master.zip

# Install quacc
pip install quacc
```

For the development version:

```bash
# Install development version of ASE
pip install --no-cache-dir https://gitlab.com/ase/ase/-/archive/master/ase-master.zip

# Install development version of quacc
pip install git+https://github.com/quantum-accelerators/quacc.git
```
