![](https://anaconda.org/bioconda/pacini_typing/badges/version.svg)
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/pacini_typing/README.html)
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/RIVM-bioinformatics/Pacini-typing?include_prereleases)](https://github.com/RIVM-bioinformatics/Pacini-typing/releases/latest)
![Unit tests](https://github.com/RIVM-bioinformatics/Pacini-typing/actions/workflows/run_unit_tests.yaml/badge.svg)
[![GitHub latest commit](https://badgen.net/github/last-commit/RIVM-bioinformatics/Pacini-typing)](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/main)
![](https://anaconda.org/bioconda/pacini_typing/badges/downloads.svg
)
[![GitHub](https://img.shields.io/github/license/RIVM-bioinformatics/Pacini-typing)](https://github.com/RIVM-bioinformatics/Pacini-typing/blob/main/LICENSE)

<!-- [![CodeFactor](https://www.codefactor.io/repository/github/rivm-bioinformatics/Pacini-typing/badge)](https://www.codefactor.io/repository/github/rivm-bioinformatics/Pacini-typing)   -->

Pylint output: Your code has been rated at 9.34/10

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
* **Commissioned by:**      Roxanne Wolthuis & Boas van der Putten & Sohana Singh

## About this project

Pacini-typing is a user-friendly application for the detection of **DNA sequences** and **SNPs** in both FASTA and FASTQ files. The application is designed to be used in a Linux-like environment and is easily executable via a YAML-based configuration scheme.

> Pacini-typing is not limited to bacterial genomes, although is was primarily developed with **Yersinia pestis** and **Vibrio cholerae** as first real use cases. Performance in other species is not yet validated, but the application is designed to be flexible.

**Quick start command of the application:**

```bash
pacini_typing --config path_to_config_file.yaml --input file_1.fastq file_2.fastq --search_mode SNPs
```

The structure of configuration file is explained [here](#configuration-file) and the search modes are explained [here](#modes-of-pacini-typing).

## Table of Contents

* [Application information](#application-information)
* [About this project](#about-this-project)
* [Table of Contents](#table-of-contents)
* [Prerequisites](#prerequisites)
* [Complete list of required packages](#complete-list-of-required-packages)
* [Installation](#installation)
* [Modes of Pacini-typing](#modes-of-pacini-typing)
* [Configuration file](#configuration-file)
* [Approach](#approach)
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
| cgecore    | >=2.0.1 |

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

## Modes of Pacini-typing

Pacini-typing accepts both assembled FASTA contigs and paired-end FASTQ files as input. The application can be executed using the following three search modes:

1. `genes`: Search for genes in the input genome(s)
2. `SNPs`: Search for SNPs in the input genome(s)
3. `both`: Search for both genes and SNPs in the input genome(s)

In addition, Pacini-typing does have two subcommands which can be used manually to (1) create a gene reference database and (2) run a query against the gene reference database. These subcommands are `makedatabase` and `query`, respectively. More information about these subcommands can be found in the [Parameters & Usage](#parameters--usage) section.

## Configuration file

The configuration file of Pacini-typing delivers the required information to run in a easy-to-use manner. The configuration file is a YAML-based file with paths to the input files, database location and the genetic threshold values to use for a specific run.

> There two pre-defined genetic patterns for _Vibrio cholerae_ available in the `config` directory of the repository. These patterns can be used detect the pandemic serotypes O1 and O139 of _Vibrio cholerae_.
>

There are three pre-defined configuration schemes available in the `config` directory of the repository:

1. `O1-scheme.yaml`: Configuration file for the O1 serotype of _Vibrio cholerae_
2. `O139-scheme.yaml`: Configuration file for the O139 serotype of _Vibrio cholerae_
3. `Yersinia-pestis-scheme.yaml`: **EXAMPLE** Configuration file for _Yersinia pestis_ (since sharing pandemic-related genes is not allowed at the time of writing, this file is only an example and does not contain any real genes)

The schemes for _Vibrio cholerae_ are based on the real genetic patterns of the pandemic serotypes O1 and O139. The scheme for _Yersinia pestis_ is an example of how a configuration file can be structured.

Example configuration file for the O139 serotype of _Vibrio cholerae_:

```yaml
%YAML 1.2

# TODO: explain the SNPs fields very briefly
```

[Back to top](#pacini-typing)

## Approach

Global steps of the application are:

1. **Validating the input**: Check if the input files are valid and if the configuration file is valid.
2. **Checking the availability of the required database**: Check if the database (gene, SNPs or both databses) are available in the specified path. This checking also includes the database structure.
3. **Creating the database**: If the database is not available, Pacini-typing will try to create the database.
4. **Check again if the database is available**: If any of the required databases are not available, the application will exit with an error.
5. **Running the query**: If the database is available, the application will prepare the query and execute it against the correct reference database.
6. **Parsing the results**: The application will parse the results of the query. For genes, this process includes filtering according to the threshold values in the configuration file (coverage and identity).
7. **Creating the output**: Pacini-typing will create a (CSV) output report and, based on the user input, a FASTA file with the found sequences, a log file or a zip containing all intermediate files of a run will be created as well.

### Parsing operations

The main logic for the parsing operation is present in the `parsing` module of the application. Additionally, this folder contains the usage of two design patterns:

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
usage: Pacini-typing [-h] [-v] [-V] [-c File] [-i File [File ...]]
                     [--save-intermediates] [--log-file] [-t Threads] [-f]
                     [-m {SNPs,genes,both}]
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
  -m {SNPs,genes,both}, --search_mode {SNPs,genes,both}
                        Search mode to use. SNPs, genes or both.
                        Default is genes.

operations:
  For more information on a specific command, type: pacini_typing <command> -h

  {makedatabase,query}
    makedatabase        Create a new reference database
    query               Run query against reference database

See github.com/RIVM-Bioinformatics for more information
```

### Required parameters

Pacini-typing can be used at two different ways. This could either be:

>* Using a pre-defined configuration file to run the application

>* Manually creating a (gene) reference database and manually search for genes, this consists of running `pacini_typing` with an additional subcommands `makedatabase` or `query`.

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

* ```-m, --search_mode``` Search mode to use. Choose between `SNPs`, `genes` or `both`. Default is `genes`.
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

The output of Pacini-typing consists of four possible files, depending on the parameters used:

1. `{prefix}_report.csv`: report of found genetic variations

> This report is created if Pacini-typing founds a hit that is above the defined threshold values in the configuration file.

Example (for `--search_mode genes`):

```csv
ID,Input,Configuration,Type/Genes,Mode,Hits,Percentage Identity,Percentage Coverage,e-value
1,ERR976461,O1-scheme.yaml,V. cholerae O1 related genes,Gene,rfbV,100.0,100.0,1e-26
1,ERR976461,O1-scheme.yaml,V. cholerae O1 related genes,Gene,ctxA,100.0,100.0,1e-26
```

Example (for `--search_mode SNPs`):

```csv
ID,Input,Configuration,Type/Genes,Mode,Hits,Reference nucleotide,Alternative nucleotide,Position,Amino acid change
1,SAMN00115171,Yersinia.yaml,Y. pestis related variants,SNP,group_1234 p.V1I,CCC,CTC,1,V1I
2,SAMN00115171,Yersinia.yaml,Y. pestis related variants,SNP,group_5678 p.E7K,AAA,AAG,7,E7K
```

> The above report does not contain any real hits, but is an example of how the report looks like. `Position` refers to the position of the **CODON** in the sequence, not the position of the nucleotide. `Amino acid change` is formatted as `p.<original amino acid><position><new amino acid>`, e.g. `p.V1I` means that the original amino acid is `V` at position `1` and the new amino acid is `I`.

2. (optional with --log-file) `pacini_typing.log`: Log file containing information about the run

This optional log file contains the output of the application. This file can be used to debug the application.

3. (optional with --fasta-out) `{prefix}_sequences.fasta`: FASTA file containing the found sequences

This file contains the found sequences of the (gene) hits in the input file. Not the sequence of search, but the actual sequence that was found in the input file. The sequences are written in FASTA format.

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

4. (optional with --save-intermediates) `{prefix}_intermediates_<SNP/gene>.tar.gz`: Tarball containing all intermediate files of the run.

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

* Implement biological typing based on the configuration file

## License

This pipeline is licensed with a AGPL3 license. Detailed information can be found inside the 'LICENSE' file in this repository.

## Contact

* **Contact person:**       Mark van de Streek
* **Email**                 <mark.van.de.streek@rivm.nl> or <m.van.de.streek@st.hanze.nl>

[Back to top](#pacini-typing)
