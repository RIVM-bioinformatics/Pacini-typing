<div align="center">
    <h1>pacini_typing</h1>
    <br />
    <h2>Bacterial typing application</h2>
    <br />
    <img src="https://via.placeholder.com/150" alt="pipeline logo">
</div>

## Application information

* **Author(s):**            Mark van de Streek
* **Organization:**         Rijksinstituut voor Volksgezondheid en Milieu (RIVM)
* **Department:**           Infectieziekteonderzoek, Diagnostiek en Laboratorium Surveillance (IDS)
* **Start date:**           02 - 09 - 2024
* **Commissioned by:**      Name

## About this project

Pacini-typing is a software application which can be used to determine genetic variants in bacteria. These variants are:

1. Presence or absence of certain genes
2. Single nucleotide polymorphisms (SNPs)

*Based on these variants, the application can estimate the pathogenicity of the given bacteria/organism. The pathongenicity patterns are defined in a set of rules in a configuration file.*

## Prerequisities

* Linux-like environment with (mini) conda installed
* Python 3.7.6

## Installation

1. Clone the repository.

```
git clone [link]
```

2. Go to [name] directory.

```
cd [directory name]
```

3. Continue steps

```
continue example code
```

## Parameters & Usage

### Command for help

* ```-h, --help``` Shows the help of the pipeline

### Required parameters

* ```-p, --parameter``` exaplanation of the parameter

### Optional parameters

* ```-o --optional_parameter``` exaplanation of the parameter

### The base command to run this program

```
python3 juno-amr.py -s [species] -i [dir/to/fasta_or_fastq_files]
```

### An example on how to run the pipeline

```
[insert command here]
```

Detailed information about the pipeline can be found in the [documentation](link to other docs). This documentation is only suitable for users that have access to the RIVM Linux environment.

## Explanation of the output

* **log:** Log with output and error file from the cluster for each Snakemake rule/step that is performed
* **output_dir_1** Explanation of the output in this directory

## Issues

* For now this only works on the RIVM cluster.
* Place to store the issues that are not resolved yet.

## Future ideas for this pipeline

* Make this pipeline available and user friendly for users outside RIVM.
* Place to store future ideas.

## License

This pipeline is licensed with a AGPL3 license. Detailed information can be found inside the 'LICENSE' file in this repository.

## Contact

* **Contact person:**       Mark van de Streek
* **Email**                 <mark.van.de.streek@rivm.nl>;<m.van.de.streek@st.hanze.nl>  

## Acknowledgements
