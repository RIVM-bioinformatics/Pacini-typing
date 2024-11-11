![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

![Unit tests](https://github.com/RIVM-bioinformatics/Pacini-typing/actions/workflows/run_unit_tests.yaml/badge.svg)

Pylint output: Your code has been rated at 9.94/10 (previous run: 9.92/10, +0.02)

> **Directly** go to [Installation](#installation) or [Getting Started](#getting-started)

# Pacini-typing

The Pacini project is a software application which can be used to determine genetic variants in bacteria. These variants are:

1. Presence or absence of certain genes
2. Single nucleotide polymorphisms (SNPs)

*Based on these variants, the application can calculate the change of pathogenicity of the given bacteria.*

## (very) Brief Overview of Pacini-typing

Based on:

- Genetic Patterns
- Methods of Detection
- Parsing and Calculation of Pathogenicity

We hope to provide a brief overview of the Pacini-typing application.

The methods are shortly described in the following sections.

> **Full documentation can be found at https://...**

### Genetic Patterns

This application stands out from a series of similar applications because genetic detection is defined in a set of rules in a configuration file. This allows the user to define their own rules for genetic detection.

The application if therefore well suited for the detection of genetic variants in bacteria for which no other software is available.

> **Important note**: The application was build around two bacterial species: _Vibrio cholerae_ and _Bordetella pertussis_. The application is not limited to these species, but the application is mainly focused on these species.

The genetic patterns are split up in gene groups. Each gene group has certain criteria which must be met in order to be considered a pathogen. The overarching criteria are:

1. Presence or Absence of complete genes
2. Presence or Absence of Single Nucleotide Polymorphisms (SNPs)
3. Percentage identity of the gene
4. Percentage coverage of the gene
5. Statistical significance values (different values used for different application methods)

Example of a gene group:

```yaml
gen_groups:
  # Gene group for the O139 serotype of Vibrio cholerae
  - name: "O139"
    # Organism for which the gene group is defined
    organism: "Vibrio cholerae"
    # Genes that are part of the gene group
    genes:
      # O139 specific LPS Gene must be present (wbfZ only present in O139)
      - gene_name: "wbfZ"
        presence: true
        snps:
          - position: 150
            mutation: "C>T"
            confidence: "p-value: 0.01" 
        identity_percentage: 98.0
        coverage_percentage: 95.0
      # O1 LPS gene must no be present (rfbV only present in O1)
      - gene_name: "rfbV"
        presence: false
        identity_percentage: 0.0
        coverage_percentage: 0.0
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

## Installation

Installation of the application can be done by cloning the repository and installing the requirements. The application is written in Python and requires Python 3.6 or higher.

```bash
git clone https://github.com/RIVM-bioinformatics/Pacini-typing.git
```

[Back to top](#pacini-typing)

## Getting Started

To get started with the application, you can run the following command:

```bash
python pacini_typing.py --help
```

[Back to top](#pacini-typing)

## Example Run of Pacini-typing

- Input
- Run
- Output

### Input

Input is **either** *1* Assembled FASTA file **OR** *2* Paired FASTQ files.

Example of an Assembled FASTA file containing the `rfbV` gene of the O1 serotype of _Vibrio cholerae_:

```fasta
>rfbV_O1:1:AE003852
ATGCCATGGAAGACCTACTCACGGAACTTGATGTATGCTGTCATAACTTTGATGTTGAATGTATTAAGCG
AATTTTACTTGATGCACCTACGGGTTATTCGCCACAAAAATGAGAATAAAATGAAAGTATTGCATGTATA
```

Example of a *1* Paired FASTQ file _Vibrio cholerae_:

```fastq
@ERR976461.1 1 length=100
CTACTATTAAGGAGCAGGATCTTTGTGGATAAGTGAAAAATGATCAACAAGATCATGCGATTCAGAAGGA
+ERR976461.1 1 length=100
CCCFFFFFHHHGHJJJJJJIJJJJJHIJJJJJC1:FHIIIIIJJIIJFIJGHIJJJJJJJIGIJJJJIJJ
```

### Run

```bash
python3 pacini_typing.py \\
    --i input_fasta_file.fasta \\
    --setting run_setting.yaml
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