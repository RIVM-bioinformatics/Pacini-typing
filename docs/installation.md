---
title: Installation
description: Installation instructions for Pacini-typing
hide:
    - navigation
---

# Installation Guide

## 🐍 Conda

Pacini-typing can be installed using conda with the following command:

```bash
conda install bioconda::pacini_typing
```

## 💻 Other installation methods

Manual installation of the application can be done by cloning the repository and installing the requirements. The following steps can be followed:

```bash title="1. Clone the repository"
git clone https://github.com/RIVM-bioinformatics/Pacini-typing.git
```

```bash title="2. Go to the Pacini-typing directory."
cd Pacini-typing
```

At this point, the repository is cloned to your system. It is advised to install the required packages. This can be done by following the steps in the section Installation of the required packages or by installing the required packages manually listed in the [Prerequisites](index.md) section.

```bash title="3. Install the package."
pip install .
```