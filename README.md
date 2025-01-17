![](https://anaconda.org/bioconda/pacini_typing/badges/version.svg)
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/pacini_typing/README.html)
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/RIVM-bioinformatics/Pacini-typing?include_prereleases)](https://github.com/RIVM-bioinformatics/Pacini-typing/releases/latest)
![Unit tests](https://github.com/RIVM-bioinformatics/Pacini-typing/actions/workflows/run_unit_tests.yaml/badge.svg)
[![GitHub latest commit](https://badgen.net/github/last-commit/RIVM-bioinformatics/Pacini-typing)](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/main)
![](https://anaconda.org/bioconda/pacini_typing/badges/downloads.svg
)
[![GitHub](https://img.shields.io/github/license/RIVM-bioinformatics/Pacini-typing)](https://github.com/RIVM-bioinformatics/Pacini-typing/blob/main/LICENSE)

<!-- [![CodeFactor](https://www.codefactor.io/repository/github/rivm-bioinformatics/Pacini-typing/badge)](https://www.codefactor.io/repository/github/rivm-bioinformatics/Pacini-typing)   -->

Pylint output: Your code has been rated at 9.95/10 (previous run: 7.68/10, +2.27)

<div align="center">
    <h1>Pacini-typing</h1>
    <br />
    <!--<img src="https://via.placeholder.com/150" alt="pipeline logo"> -->
    <img src="docs/pacini_typing_logo.png" alt="pipeline logo">
    <h3>Directly go to <a href="#installation">Installation</a> or <a href="#getting-started">Getting Started</a></h3>
</div>

## Application information

* **Author(s):**            Mark van de Streek
* **Organization:**         Rijksinstituut voor Volksgezondheid en Milieu (RIVM)
* **Department:**           Infectieziekteonderzoek, Diagnostiek en Laboratorium Surveillance (IDS)
* **Start date:**           02 - 09 - 2024
* **Commissioned by:**      Roxanne Wolthuis & Boas van der Putten

## About this project

The Pacini project is a software application which can be used to detect genetic sequences in bacteria using a configuration schema.

With these genetic sequences, the application can determine whether the sequence is actually present in the bacteria and create a simple (CSV) report of the findings

>_Pacini-typing was mainly build around the detection of genetic sequences in **Vibrio cholerae**_

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
* [Output](#output)
* [Example Run of Pacini-typing](#example-run-of-pacini-typing)
* [Testing](#testing)
* [Issues](#issues)
* [Future Ideas](#future-ideas)
* [License](#license)
* [Contact](#contact)

## Prerequisites

>All required packages are available in a pre-defined conda environment. Steps to install this environment can be found in the [Automatic installation of the required packages](#automatic-installation-of-the-required-packages) section.

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
| pytest     | >=8.3.3 |

## Installation

### 🐍 Conda installation

Pacini-typing can be installed using the conda/mamba package manager. The package is available on the bioconda channel, under the name [_pacini_typing_](https://anaconda.org/bioconda/pacini_typing).

```bash
conda install bioconda::pacini_typing
```

### 💻 Other installation methods

Manual installation of the application can be done by cloning the repository and installing the requirements. The following steps can be followed:

1. Clone the repository.

```bash
git clone https://github.com/RIVM-bioinformatics/Pacini-typing.git
```

2. Go to the Pacini-typing directory.

```bash
cd Pacini-typing
```

At this point, the repository is cloned to your system. It is advised to install the required packages. This can be done by following the steps in the section [Installation of the required packages](#installation-of-the-required-packages) or by installing the required packages manually listed in the [Prerequisites](#prerequisites) section.

1. Install the package.

```bash
pip install .
```

Pacini-typing is now installed on your system. After installation, the application can be run by calling `pacini_typing` or `Pacini-typing` in every directory.

Additionally, the application can be run by calling the original `pacini_typing.py` script in the `pacini_typing` directory with the following command:

```bash
python3 directory_of_clone/pacini_typing.py --help
```

#### Installation of the required packages

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
* Parsing and Reporting

### Genetic Patterns

This application stands out from a series of similar applications because genetic detection is defined in a set of rules in a configuration file. This allows the user to define their own rules for genetic detection.

The application if therefore well suited for the detection of genetic variants in bacteria for which no other software is available.

> **Important note**: The application was build around _Vibrio cholerae_. The application is not limited to this bacteria, but the application is mainly focused on this.

> There two pre-defined genetic patterns for _Vibrio cholerae_ available in the `config` directory of the repository. These patterns can be used detect the pandemic serotypes O1 and O139 of _Vibrio cholerae_.
> A user can also create their own genetic pattern by creating a YAML configuration file of the same structure.

Example of a YAML configuration file with gene group, this file defines the genetic pattern for the O139 serogroup of _Vibrio cholerae_:

```yaml
%YAML 1.2
---
# The metadata must always be present, exactly as shown below.
# The fields are used in the final output reports.
metadata:
  id: "VIB-O139"
  name: "O139 Gene group"
  type: "V. cholerae O139 Genes"
  description: "Genetic pattern run config file for Vibrio cholerae O139 serogroup"
  date_created: "2024-11-06"

# The database section is used to define the database to be used in the run.
# You can specify a target genes file to be used in the run.
# The target genes file should contain the sequences of the genes you want to detect.
# Format in Multi-FASTA format.
# The run_output field is used to specify the output directory for the intermediate files.
database:
  name: "VIB-O139"
  path: "databases"
  target_genes_file: "config/VIB-O139.fasta"
  run_output: "output/"

# This section is most important in creating filters for the genes.
# The perc_ident and perc_cov fields are used for all genes in the 'genes' section.
pattern:
  perc_ident: 99.8
  perc_cov: 100.0
  genes:
    - gene_name: "wbfZ"
    - gene_name: "ctxA"
    - gene_name: "ctxB"
```

The usage of a configuration file consists of the following operations:

1. Creating a reference database
2. Running a query against the reference database
3. Parsing the results and creating a report

The first two steps can also be achieved independently by running the application with the `makedatabase` or `query` subcommands. Only the parsing and reporting steps are done by the configuration file, because this requires a genetic pattern.

More information about these subcommands can be found in the [Parameters & Usage](#parameters--usage) section.

[Back to top](#pacini-typing)

### Methods of Detection

Pacini-typing can accept different types of input data. This data can be used to determine the genetic variants of the bacteria. The following data is supported:

1. **Assembled FASTA contigs**
2. **Paired-end FASTQ-files**

This means, Pacini-typing accepts **1** Assembled FASTA file or **2** Paired end FASTQ files.

Assembled FASTA files can directly be used by _BLAST_ to determine given genes. Paired FASTQ files are processed by a tool called _K-mer Alignment (KMA)_. These tool generate almost the same output, but via different names and formats. Both tool require different calls to the application as well.

The output of both tools is placed in a tab separated file. These tsv files are not exactly identical, but the application creates a unified output file from these files.

[Back to top](#pacini-typing)

### Parsing and Calculation of Pathogenicity

With all hits and results from the detection methods, the application parser the results and determines if the hits are actually present in the input file(s).

The main logic for this operation is present in the `parsing` module of the application. Additionally, this folder contains the usage of two design patterns:

1. **Strategy Pattern**
2. **Filter Pattern**

Firstly, the strategy parser consists of a base class `parsing_strategy.py` which is inherited by the `fasta_parser.py` and `fastq_parser.py` files.
The strategy pattern is used define overarching features required for both methods of parsing.

The filter pattern is used to filter the hits based on the values in the configuration file. All specific filters are inheriting from the `filter_pattern.py` base class.

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
usage: pacini_typing [-h] [-v] [-V] [-c File] [-i File [File ...]] [--save-intermediates]
              [--log-file] [-t Threads] [-f]
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
  -t Threads, --threads Threads
                        Number of threads to use (rounded to the nearest integer)
  -f, --fasta-out       Write found sequences to a FASTA output file

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

>* Manually creating a reference database and manually search for genetic variations, this consists of running `pacini_typing` with an additional subcommands `makedatabase` or `query`.

One of these two methods must be used to run the application.

> Note: Manually searching for genetic variations does not result in parsing and creating output reports. This is only possible when using a pre-defined configuration file.

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
* ```-V, --version``` Show program's version number and exit
* ```--save-intermediates``` Save intermediate files of the run
* ```--log-file``` Save log file of the run, named `pacini_typing.log`
* ```-t, --threads``` Number of threads to use
* ```-f, --fasta-out``` Write found sequences (hits) to a FASTA output file, named `{prefix}_sequences.fasta`

> **Note**: The `--save-intermediates` and `--fasta-out` parameters can not be used in combination with the `makedatabase` or `query` subcommands.

In the `accept_arguments.yaml` file in the `config` directory, the accepted extensions for the input files are defined. These can be changed by the user.

### The base command to run this program

```python
pacini_typing --config [path_to_config_file.yaml] --input [path_to_input_file.ext]
```

## Output

The output of Pacini-typing consists of three files:

1. `{prefix}_report.csv`: report of found genetic variations

Example:

```csv
ID,Input,Schema,Type/Gene,Hits
1,ERR976461,O1-scheme.yaml,V. cholerae O1 related genes,rfbV
2,ERR976461,O1-scheme.yaml,V. cholerae O1 related genes,ctxA
```

All hits in this report are filtered based on the values in the configuration file. Every line in the report represents a hit.

2. `{prefix}_hits_report.csv`: CSV file containing information about the hits

Example:

```csv
ID,hit,percentage identity,percentage coverage,p-value
1,rfbV_O1,100.0,100.0,1e-26
2,ctxA,100.0,100.0,1e-26
```

The hits report also contains hits there are filed based on the values in the configuration file. Every line in the main report represents a line in the hits report.

3. (optional with --log-file) `pacini_typing.log`: Log file containing information about the run

This optional log file contains the output of the application. This file can be used to debug the application.

4. (optional with --fasta-out) `{prefix}_sequences.fasta`: FASTA file containing the found sequences

This file contains the found sequences of the hits in the input file. So not the sequence of search, but the actual sequence that was found in the input file. The sequences are written in FASTA format.

Example:

```text
>rfbV
ATGCCATGGAAGACCTACTCACGGAACTTGATGTATGCTGTCATAACTTTGATGTTGAATGTATTAAGCG
AATTTTACTTGATGCACCTACGGGTTATTCGCCACAAAAATGAGAATAAAATGAAAGTATTGCATGTATA
>ctxA
ATGCCATGGAAGACCTACTCACGGAACTTGATGTATGCTGTCATAACTTTGATGTTGAATGTATTAAGCG
AATTTTACTTGATGCACCTACGGGTTATTCGCCACAAAAATGAGAATAAAATGAAAGTATTGCATGTATA
```

> **Note**: The prefix of the output files is the same as the prefix of the input file.

[Back to top](#pacini-typing)

## Example Run of Pacini-typing

* Input
* Run

### Input

Input is **either** _1_ Assembled FASTA file **OR** _2_ Paired FASTQ files.

Example of an Assembled FASTA file containing the `rfbV` gene of the O1 serotype of _Vibrio cholerae_:

```fasta
>rfbV_O1:1:AE003852
ATGCCATGGAAGACCTACTCACGGAACTTGATGTATGCTGTCATAACTTTGATGTTGAATGTATTAAGCG
AATTTTACTTGATGCACCTACGGGTTATTCGCCACAAAAATGAGAATAAAATGAAAGTATTGCATGTATA
```

Example of a _1_ Paired FASTQ file _Vibrio cholerae_:

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

## Testing

Pacini-typing contains a quite broad test suite. Most useful tests are probably the end-to-end (E2E) tests. These tests are located in the `tests/e2e` directory of the repository. The (most) tests are additionally run online by a GitHub action workflow on every push to the repository.

All tests are written in the `pytest` framework. To run the tests, the following command can be used:

```bash
pytest -v tests/
```

Big downside of some good tests is the dependency of bigger data files. These files are not included in the repository, because of their size and the GitHub Organization's policy. Therefore, some tests must be skipped if running through a GitHub action workflow.

This skipping is done by a skip-if condition in the test file:

```python
skip_in_ci = pytest.mark.skipif(
    os.getenv("CI") == "true",
    reason="Test online (GitHub Action) not available due to dependencies",
)

@skip_in_ci
def test_example():
    # Test code
```

When cloning the repository, the tests must be skipped as well. This can be done by running the following command:

```bash
CI=true pytest -v tests/
```

This simply uses the same strategy as the GitHub action workflow by setting the `CI` environment variable to `true`.

## Issues

If encoutering any issues:

* Any issues can be reported in the [Issues](https://github.com/RIVM-bioinformatics/Pacini-typing/issues) section of this repository
* Contact the author(s) of the application

## Future Ideas

* Implement a SNP detection method
* Implement biological typing based on the configuration file

## License

This pipeline is licensed with a AGPL3 license. Detailed information can be found inside the 'LICENSE' file in this repository.

## Contact

* **Contact person:**       Mark van de Streek
* **Email**                 <mark.van.de.streek@rivm.nl> or <m.van.de.streek@st.hanze.nl>

[Back to top](#pacini-typing)
