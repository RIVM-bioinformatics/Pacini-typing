---
title: Prerequisites
description: Prerequisites of the Pacini-typing package
hide:
    - navigation
---

In order to use the package, a couple of prerequisites must be met. These will be listed below.

----

## Automatic installation

If you don't want to manually install the prerequisites, you can use the provided conda environment file. This file can be found in the `environment.yaml` file in the root of the repository.

To install the conda environment, use the following command:

```bash
conda env create -f environment.yaml -n pacini_typing
```

Or, if you want to use mamba, use the following command:

```bash
mamba env create -f environment.yaml -n pacini_typing
```

You can provide a different name for the environment by changing the `-n pacini_typing` part of the command.

### Activating the automatically installed environment

You need to activate the conda environment that was just installed. This can be done by running the following command:

```bash
conda activate pacini_typing
```

If using mamba:

```bash
mamba activate pacini_typing
```

## Python

First of all, and most importantly, you need to have Python installed on your system.

> Version 3.10 or higher is needed

The tool was developed using Python 3.12 and it is recommended to use this version or higher.

Because of the use of `typing` annotations, this package is not compatible with Python versions lower than 3.10.

## Python packages

Pip is needed to install certain python dependencies. For installing the package, setuptools is needed. The version of setuptools requires a minimum pip version of 24.3.0.

> Version 24.3.0 or higher is needed

After pip right version is installed, the following packages are needed:

- `setuptools` (version 75.3.0 or higher)
- `pyYAML` (version 6.0.2 or higher)
- `pandas` (version 2.2.3 or higher)

## Tools

Most importantly, you need tools as well. The following tools are needed:

- `blast` (version 2.16.0 or higher)
- `kma` (version 1.4.15 or higher)

## Operating System

Linux-like environment is needed to run the package. The package was developed and tested on both Linux and MacOS. Additionally, conda is very advisable to have installed.

## Full list of prerequisites

The following table shows the total overview of the prerequisites:

| Prerequisite   | Version | Required |
|----------------|---------|----------|
| Python         | 3.10    | Yes      |
| Pip            | 24.3.0  | Yes      |
| Setuptools     | 75.3.0  | Yes      |
| PyYAML         | 6.0.2   | Yes      |
| Pandas         | 2.2.3   | Yes      |
| Blast          | 2.16.0  | Yes      |
| KMA            | 1.4.15  | Yes      |
