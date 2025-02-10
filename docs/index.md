---
title: Pacini-typing Documentation & Guide
description: Pacini-typing documentation homepage
hide:
    - navigation
---

Pacini-typing is a YAML-based genotyping application built for the National Institute for Public Health and the Environment (RIVM) in the Netherlands.



The application can be used to detect genetic sequences in bacteria using a configuration schema. Both *^^FASTA^^* and *^^FASTQ^^* files can be used as input. With the genetic sequences, the application can determine whether the sequence is actually present in the bacteria and create a simple (CSV) report of the findings.


!!! block "Focus of Pacini-typing"
    Pacini-typing was mainly build around the detection of genetic sequences in **Vibrio cholerae**, but can be used for a variety of other genomic sequences as well. Two configuration files are present for the pandemic serogroupsa of *Vibrio cholerae*, O1 and O139.

## Quick usage

Pacini-typing can be run very easily from the command line, using the following command:

```bash linenums="1" title="Run Pacini-typing"
pacini_typing \
  --config configuration_schema.yaml \
  --input FASTQ_file1.fastq FASTQ_file2.fastq
```

At least a configuration schema and one FASTA or two FASTQ files are required to run the application.

!!! tip
    *For a detailed description of the configuration schema, explanation of the output and more, please take a look at the subpages of this documentation.*