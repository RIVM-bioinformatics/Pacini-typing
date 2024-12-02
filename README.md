![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)
[![git](https://badgen.net/badge/icon/git?icon=git&label)](https://git-scm.com)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/RIVM-bioinformatics/Pacini-typing?include_prereleases)](https://github.com/RIVM-bioinformatics/Pacini-typing/releases/latest)
[![GitHub](https://img.shields.io/github/license/RIVM-bioinformatics/Pacini-typing)](https://github.com/RIVM-bioinformatics/Pacini-typing/blob/main/LICENSE)
[![GitHub latest commit](https://badgen.net/github/last-commit/RIVM-bioinformatics/Pacini-typing)](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/main)
![Unit tests](https://github.com/RIVM-bioinformatics/Pacini-typing/actions/workflows/run_unit_tests.yaml/badge.svg)

<!-- [![CodeFactor](https://www.codefactor.io/repository/github/rivm-bioinformatics/Pacini-typing/badge)](https://www.codefactor.io/repository/github/rivm-bioinformatics/Pacini-typing)   -->

Pylint output: Your code has been rated at 9.91/10 (previous run: 7.68/10, +2.23)

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

*Based on these variants, the application can calculate the change of pathogenicity of the given bacteria. (This is still under development...)*

## Table of Contents

* [Application information](#application-information)
* [About this project](#about-this-project)
* [Table of Contents](#table-of-contents)
* [Prerequisites](#prerequisites)
* [Complete list of required packages](#complete-list-of-required-packages)
* [Installation](#installation)
* [(very) Brief Overview of Pacini-typing](#very-brief-overview-of-pacini-typing)
* [Getting Started](#getting-started)
* [Parameters \& Usage](#parameters--usage)
* [Example Run of Pacini-typing](#example-run-of-pacini-typing)
* [Issues](#issues)
* [Future Ideas](#future-ideas)
* [License](#license)
* [Contact](#contact)

## Prerequisites

>All of the above packages are available in a pre-defined conda environment. Steps to install this environment can be found in the [Automatic installation of the required packages](#automatic-installation-of-the-required-packages) section.

* Linux-like environment with (mini) conda installed
* Python 3.10 or higher (developed on 3.12)

The following Python packages are required:

1. pip=>24.2
2. pyyaml=>6.0.2
3. setuptools=>75.1.0

The following Tools are required:

1. blast=>2.16.0
   1. The makeblastdb subcommand of BLAST must be available as well
2. kma=>1.4.15
   1. The kma_index subcommand of KMA must be available as well

## Complete list of required packages

| Package    | Version |
|------------|---------|
| pip        | >=24.2  |
| pyyaml     | >=6.0.2 |
| setuptools | >=75.1.0|
| pandas     | >=2.2.3 |
| blast      | >=2.16.0|
| kma        | >=1.4.15|

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

1. Install the package.

```bash
pip install .
```

Pacini-typing is now installed on your system. After installation, the application can be run by calling `pacini_typing` or `Pacini-typing` in every directory.

Additionally, the application can be run by calling the original `pacini_typing.py` script in the `pacini_typing` directory with the following command:

```bash
python3 directory_to_pacini_typing_clone/pacini_typing.py --help
```

### Automatic installation of the required packages

For both macOS and Linux users, a complete conda environment, containing all the required packages, can be found in the root of the repository.

To install the environment, run the following command:

```bash
# For Linux users:
conda env create -f linux-environment.yaml -n pacini-typing
# or for macOS users:
conda env create -f mac-environment.yaml -n pacini-typing
```

After the environment is installed, activate the environment by running:

```bash
conda activate pacini-typing
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
# The metadata must always be present, exactly as shown below.
# The fields are used in the final output reports.
metadata:
  id: "VIB-O139"
  name: "O139 Gene group"
  description: "Genetic pattern run config file for Vibrio cholerae O139 serogroup"
  date_created: "2024-11-06"

# The database section is used to define the database to be used in the run.
# You can specify a matching sequence file to be used in the run.
# The matching sequence file should contain the sequences of the genes you want to detect.
# Format in Multi-FASTA format.
# The run_output field is used to specify the output directory for the intermediate files.
database:
  name: "VIB-O139"
  path: "databases"
  matching_seq_file: "patterns/VIB-O139.fasta"
  run_output: "output/"

# This section is most important in creating filters for the genes.
# The perc_ident and perc_cov fields are used for all genes in the 'genes' section.
pattern:
  perc_ident: 95.0
  perc_cov: 90.0
  e_value: 0
  p_value: 0.05
  genes:
    - gene_name: "wbfZ"
    - gene_name: "ctxB"
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
pacini_typing -h
usage: pacini_typing [-h] [-v] [-V] [-c File] [-i File [File ...]] [--save-intermediates] [--log-file]
              {makedatabase,query} ...

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
  --save-intermediates  Save intermediate files of the run
  --log-file            Save log file of the run

operations:
  For more information on a specific command, type: Pacini.py <command> -h

  {makedatabase,query}
    makedatabase        Create a new reference database
    query               Run query against reference database

See github.com/RIVM-Bioinformatics for more information
```

### Required parameters

Pacini-typing can be used at two different ways. This could either be:

>* Using a pre-defined configuration file to run the application

>* Manually running Pacini-typing, this consists of running `pacini_typing` with an additional subcommands `makedatabase` or `query`.

One of these two methods must be used to run the application.

#### Pre-defined configuration file required parameters

* ```-c, --config``` path to the configuration file

* ```-i, --input``` path to the input file(s). It can accept 1 or 2 files. If providing 2 files, separate them with a space:

```bash
pacini_typing --input file_1.ext file_2.ext
```

#### Manually creating database required parameters

* ```-h, --help``` Shows the help for the makedatabase command
* ```-db_path, --database_path``` path to the database directory
* ```-db_name, --database_name``` name of the database
* ```-I, --input_file``` path to the database file
* ```-db_type, --database_type``` type of the database, choose between `fasta` or `fastq`

To run the above options, don't forget to add the `makedatabase` subcommand at the beginning of the command:

```bash
pacini_typing makedatabase -db_path [path_to_database_directory] -db_name [name_of_database] -I [path_to_input_file.ext] -db_type [fasta/fastq]
```

#### Manually running query required parameters

* ```query -h``` Shows the help for the query command
* ```-db_path, --database_path``` path to the database directory
* ```-db_name, --database_name``` name of the database
* ```-p, --paired``` path to the paired FASTQ files, seperate with a space
* ```-s, --single``` path to the single FASTQ files
* ```-o, --output``` path to the output directory and prefix of the output files

**Note:** The `-p` and `-s` parameters are mutually exclusive. Only one of these parameters can be used at a time.

To run the above options, don't forget to add the `query` subcommand at the beginning of the command:

```bash
pacini_typing query -db_path [path_to_database_directory] -db_name [name_of_database] -p [path_to_paired_files.ext] -o [path_to_output_directory]
```

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
pacini_typing \
  --i input_file.ext \ # 1 FASTA file OR 2 FASTQ files
  --config path_to_config_file.yaml
```

### Output

*This section is still in development...*

But, the output of the application consists of three files:

1. `{prefix}_report.csv`: CSV file containing the report

Example:

```csv
ID,Input,Schema,Type/Gene,Hits
1,ERR976461,O1-scheme.yaml,V. cholerae O1 related genes,rfbV
2,ERR976461,O1-scheme.yaml,V. cholerae O1 related genes,ctxA
```

2. `{prefix}_hits_report.csv`: CSV file containing information about the hits

Example:

```csv
ID,hit,percentage identity,percentage coverage,p-value
1,rfbV_O1,100.0,100.0,1e-26
2,ctxA,100.0,100.0,1e-26
```

3. (optional with --log-file) `pacini_typing.log`: Log file containing information about the run

*Further output is still in development...*

[Back to top](#pacini-typing)

## Issues

If encoutering any issues:

* Any issues can be reported in the [Issues](https://github.com/RIVM-bioinformatics/Pacini-typing/issues) section of this repository
* Contact the author(s) of the application

## Future Ideas

* Add more optional parameters
* Negatively search for genetic variants; search for the absence of genes

## License

This pipeline is licensed with a AGPL3 license. Detailed information can be found inside the 'LICENSE' file in this repository.

## Contact

* **Contact person:**       Mark van de Streek
* **Email**                 <mark.van.de.streek@rivm.nl> or <m.van.de.streek@st.hanze.nl>

[Back to top](#pacini-typing)
