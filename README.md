![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
[![git](https://badgen.net/badge/icon/git?icon=git&label)](https://git-scm.com)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/RIVM-bioinformatics/Pacini-typing?include_prereleases)](https://github.com/RIVM-bioinformatics/Pacini-typing/releases/latest)
[![GitHub](https://img.shields.io/github/license/RIVM-bioinformatics/Pacini-typing)](https://github.com/RIVM-bioinformatics/Pacini-typing/blob/main/LICENSE)
[![GitHub latest commit](https://badgen.net/github/last-commit/RIVM-bioinformatics/Pacini-typing)](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/main)
![Unit tests](https://github.com/RIVM-bioinformatics/Pacini-typing/actions/workflows/run_unit_tests.yaml/badge.svg)

<!-- [![CodeFactor](https://www.codefactor.io/repository/github/rivm-bioinformatics/Pacini-typing/badge)](https://www.codefactor.io/repository/github/rivm-bioinformatics/Pacini-typing)   -->

Pylint output: Your code has been rated at 9.44/10 (previous run: 9.44/10, +0.00)

<div align="center">
    <h1>Pacini-typing</h1>
    <br />
    <img src="https://via.placeholder.com/150" alt="pipeline logo">
    <h3>Directly go to <a href="#installation">Installation</a> or <a href="#getting-started">Getting Started</a></h2>
</div>

## Application information

* **Author(s):**            Mark van de Streek
* **Organization:**         Rijksinstituut voor Volksgezondheid en Milieu (RIVM)
* **Department:**           Infectieziekteonderzoek, Diagnostiek en Laboratorium Surveillance (IDS)
* **Start date:**           02 - 09 - 2024
* **Commissioned by:**      Roxanne Wolthuis & Boas van der Putten

## About this project

The Pacini project is a software application which can be used to determine genetic variants in bacteria. These variants are:

1. Presence or absence of certain genes
2. Single nucleotide polymorphisms (SNPs)

*Based on these variants, the application can calculate the change of pathogenicity of the given bacteria.*

## Table of Contents

- [Application information](#application-information)
- [About this project](#about-this-project)
- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [(very) Brief Overview of Pacini-typing](#very-brief-overview-of-pacini-typing)
- [Getting Started](#getting-started)
- [Parameters \& Usage](#parameters--usage)
- [Example Run of Pacini-typing](#example-run-of-pacini-typing)

## Prerequisites

* Linux-like environment with (mini) conda installed
* Python 3.10 or higher (developed on 3.12)

The following Python packages are required:

1. pip=>24.2
2. PyYAML=>6.0.2
3. setuptools=>75.1.0

The following Tools are required:

1. blast=>2.5.0
   1. The makeblastdb must be available as well
2. kma=>1.4.15
   1. The kma_index must be available as well

A complete conda environment, containing all the required packages, can be found in the `environment.yaml` file. It is very advised to use this environment to run the application. The environment can be installed by running the following command:

```bash
conda env create -f environment.yaml -n pacini-typing
```

And activated by running:

```bash
conda activate pacini-typing
```

## Installation

Installation of the application can be done by cloning the repository and installing the requirements. The following steps can be followed:

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

Pacini-typing is now installed on your system. After installation, the application can be run by calling `pacini_typing` or `Pacini-typing` in every directory.

Additionally, the application can be run by calling the original `pacini_typing.py` script in the `pacini_typing` directory with the following command:

```bash
python3 directory_to_pacini_typing_clone/pacini_typing.py --help
```

[Back to top](#pacini-typing)

## (very) Brief Overview of Pacini-typing

Based on:

* Genetic Patterns
* Methods of Detection
* Parsing and Calculation of Pathogenicity

We hope to provide a brief overview of the Pacini-typing application.

The methods are shortly described in the following sections.

> **Full documentation can be found at https://...**

### Genetic Patterns

This application stands out from a series of similar applications because genetic detection is defined in a set of rules in a configuration file. This allows the user to define their own rules for genetic detection.

The application if therefore well suited for the detection of genetic variants in bacteria for which no other software is available.

> **Important note**: The application was build around two bacterial species: *Vibrio cholerae* and *Bordetella pertussis*. The application is not limited to these species, but the application is mainly focused on these species.

The genetic patterns are split up in gene groups. Each gene group has certain criteria which must be met in order to be considered a pathogen. The overarching criteria are:

1. Presence or Absence of complete genes
2. Presence or Absence of Single Nucleotide Polymorphisms (SNPs)
3. Percentage identity of the gene
4. Percentage coverage of the gene
5. Statistical significance values (different values used for different application methods)

Example of a YAML configuration file with gene group, this file defines the genetic pattern for the O139 serogroup of *Vibrio cholerae*:

```yaml
%YAML 1.2
---
metadata:
  id: "VIB-O139"
  name: "O139 Gene group"
  description: "Genetic pattern run config file for Vibrio cholerae O139 serogroup"
  date_created: "2024-11-06"

database:
  name: "VIB-O139"
  path: "databases"
  matching_seq_file: "patterns/VIB-O139.fasta"
  run_output: "output/"

pattern:
  perc_ident: 95.0
  perc_cov: 90.0
  e_value: 0
  p_value: 0.05
  genes:
    - gene_name: "wbfZ"
      presence: true
      pident: 98.0
      pcoverage: 95.0
    - gene_name: "wbfY"
      presence: true
      pident: 98.0
      pcoverage: null
```

[Back to top](#pacini-typing)

### Methods of Detection

Pacini-typing can accept different types of input data. This data can be used to determine the genetic variants of the bacteria. The following data is supported:

1. **Assembled FASTA files**
2. **Raw paired FASTQ files**

Assembled FASTA files can directly be used by *BLAST* to determine given genes. Paired FASTQ files are processed by a tool called *K-mer Alignment (KMA)*. These tool generate almost the same output, but via different names and formats. Both tool require different calls to the application as well.

Method for detecting SNP's still have to be filled in here...

[Back to top](#pacini-typing)

### Parsing and Calculation of Pathogenicity

With all hits and results from the detection methods, the application can calculate the pathogenicity of the bacteria. This is done by parsing the results together with the patterns of the gene groups `config` files.

This parsing is done in the parsing module of the application.

## Getting Started

To get started with the application, you can run the following command to see the help of the application:

```bash
python pacini_typing.py --help
```

See the [Parameters & Usage](#parameters--usage) section for more information on how to run the application.

[Back to top](#pacini-typing)

## Parameters & Usage

### Command for help

* ```-h, --help``` Shows the help of the pipeline.

```bash
usage: Pacini [-h] [-v] {makedatabase,query} ...

Bacterial Genotyping Tool for RIVM IDS-Bioinformatics

options:
  -h, --help            show this help message and exit
  -v, --verbose         Increase output verbosity

operations:
  For more information on a specific command, type: Pacini.py <command> -h

  {makedatabase,query}
    makedatabase        Create a new reference database
    query               Run query against reference database

See github.com/RIVM-Bioinformatics for more information
```

### Required parameters

Pacini-typing can be used at two different ways. This could either be:

>* Manually running Pacini-typing, this consists of running `pacini_typing` with an additional subcommand
>* Using a pre-defined configuration file to run the application

One of these two methods must be used to run the application.

#### Pre-defined configuration file required parameters

* ```-c, --config``` path to the configuration file

* ```-i, --input``` path to the input file(s). It can accept 1 or 2 files. If providing 2 files, separate them with a space:

```bash
pacini_typing --input file_1.ext file_2.ext
```

#### Manually creating database required parameters

* ```makedatabase -h``` Shows the help for the makedatabase command
* ```-db_path, --database_path``` path to the database directory
* ```-db_name, --database_name``` name of the database
* ```-i, --input``` path to the database file
* ```-db_type, --database_type``` type of the database, choose between `fasta` or `fastq`

#### Manually running query required parameters

* ```query -h``` Shows the help for the query command
* ```-db_path, --database_path``` path to the database directory
* ```-db_name, --database_name``` name of the database
* ```-p, --paired``` path to the paired FASTQ files, seperate with a space
* ```-s, --single``` path to the single FASTQ files
* ```-o, --output``` path to the output directory and prefix of the output files

**Note:** The `-p` and `-s` parameters are mutually exclusive. Only one of these parameters can be used at a time.

### Optional parameters

* ```-v, --verbose``` Increase output verbosity
* Add more optional parameters here...

### The base command to run this program

```
pacini_typing --config [path_to_config_file.yaml] --input [path_to_input_file.ext]
```

## Example Run of Pacini-typing

* Input
* Run
* Output

### Input

Input is **either** *1* Assembled FASTA file **OR** *2* Paired FASTQ files.

Example of an Assembled FASTA file containing the `rfbV` gene of the O1 serotype of *Vibrio cholerae*:

```fasta
>rfbV_O1:1:AE003852
ATGCCATGGAAGACCTACTCACGGAACTTGATGTATGCTGTCATAACTTTGATGTTGAATGTATTAAGCG
AATTTTACTTGATGCACCTACGGGTTATTCGCCACAAAAATGAGAATAAAATGAAAGTATTGCATGTATA
```

Example of a *1* Paired FASTQ file *Vibrio cholerae*:

```fastq
@ERR976461.1 1 length=100
CTACTATTAAGGAGCAGGATCTTTGTGGATAAGTGAAAAATGATCAACAAGATCATGCGATTCAGAAGGA
+ERR976461.1 1 length=100
CCCFFFFFHHHGHJJJJJJIJJJJJHIJJJJJC1:FHIIIIIJJIIJFIJGHIJJJJJJJIGIJJJJIJJ
```

### Run

```bash
pacini_typing \\
  --i input_file.ext \\ # 1 FASTA file OR 2 FASTQ files
  --config path_to_config_file.yaml
```

### Output

Output consists of three files:

1. `{prefix}.csv`: CSV file containing the results of the genetic detection

Example:

```csv
gene_group,genes,identity_percentage,coverage_percentage,snps
O139,wbfZ,98.0,95.0,150:C>T
O139,rfbV,0.0,0.0,
```

2. Still have to fill in here...

[Back to top](#pacini-typing)
