---
title: Installation
description: Installation of the Pacini-typing package
hide:
    - navigation
---

Before installating the package, make sure you meet the requirements. All requirements can be found [prerequisites](prerequisites.md). The [prerequisites](prerequisites.md#automatic-installation) also explains how to automatically install the prerequisites.

---

## Preparation

If you did not install the prerequisites automatically, it is still very recommended to use a conda environment. This can be done by running the following command:

```bash
conda create -n your_environment_name python=3.10 && conda activate your_environment_name
```

## Installation

1. Clone the repository.

```bash
git clone https://github.com/RIVM-bioinformatics/Pacini-typing.git
```

2. Go to the Pacini-typing directory.

```bash
cd Pacini-typing
```

3. Install the package.

```bash
pip install .
```

The package is now installed and can be used in your Python environment. 

## Calling for help

Call the help function to see the available commands.

```bash
Pacini-typing --help
```

additionally, you can use a lowered case version of the command:

```bash
pacini-typing --help
```

Finally, you can call the original script to run the pipeline.

```bash
python3 pacini-typing.py --help
```

## Help output

The help output will show the following:

```bash
usage: Pacini [-h] [-v] [-V] [-c File] [-i File [File ...]] {makedatabase,query} ...

Bacterial Genotyping Tool for RIVM IDS-Bioinformatics

Either pick a subcommand to manually run the tool or
provide a predefined configuration file and your input file(s) (FASTA/FASTQ)
and let Pacini-typing do the work for you.

If using a configuration file, both the
--config and --input arguments are required.

options:
  -h, --help            show this help message and exit
  -v, --verbose         Increase output verbosity
  -V, --version         show program's version number and exit
  -c File, --config File
                        Path to predefined configuration file
  -i File [File ...], --input File [File ...]
                        Path to input file(s). Accepts 1 fasta file or 2 fastq files

operations:
  For more information on a specific command, type: Pacini.py <command> -h

  {makedatabase,query}
    makedatabase        Create a new reference database
    query               Run query against reference database

See github.com/RIVM-Bioinformatics for more information
```
