# Changelog

## [2.0.2](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v2.0.1...v2.0.2) (2025-06-05)


### Documentation

* pull request [#39](https://github.com/RIVM-bioinformatics/Pacini-typing/issues/39) - Updated the README with clarity, fixed typos, and future ideas ([e67678f](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/e67678fe0db1a7f02614a8a3d9350298dad3e237))
* Updated the README with clarity and fixed typos ([fce48ec](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/fce48ece53b47437b541137338a0a683f6ae77ab))

## [2.0.1](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v2.0.0...v2.0.1) (2025-06-04)


### Documentation

* Improved documentation/commenting across multiple modules for clarity ([dba9185](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/dba9185c837bb45f3e735c7ea18a968341d2ad46))
* Improved documentation/commenting in files ([e5fd8d3](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/e5fd8d3d91f2f6a315517f43a55f1ce34a9cd5dc))

## [2.0.0](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.6.4...v2.0.0) (2025-06-02)


### ⚠ BREAKING CHANGES

* Updated coverage calculation for blastn reports in multiple files (was not fully correct)
* Fixed a bug where the identity threshold was not used correctly.

### Features

* Add search mode argument to main parser ([6c421fe](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/6c421fe2a83ec2ce17796004daa6cb24cb4ee835))
* Added cgecore (2.0.1) dependency to environments configs ([b8eca27](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/b8eca2713ac643229dc76c596cdfe3ebe4d97d65))
* Added the automatic downloading of PointFinder script (if not exists) ([1080834](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/1080834ebbaa50cf0171f761bfef421f00ee1ea1))
* Changed the QueryRunner class into a Template Design Pattern to share same functionality/recipe for SNP expansion ([16ae667](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/16ae667c0132156e32cde8c2b0b6c633d2c91671))
* Created a codon translation enum for translating purposes ([84a0220](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/84a02205bf3aee7ede2d1470c42d7f2ec4e3b1ac))
* Created an additional GENE database check within the SNP database check only for FASTQ ([06a9dd1](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/06a9dd1c7406b4fac29a1b118c4c4b2728a71f6d))
* Created class PointFinderReferenceChecker for the validation of PointFinder reference database and corresponding custom error exceptions ([45044f8](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/45044f87aaf3f9eb81ab39a62fdeaba80d8987fe))
* Created HandleSearchModes class for managing search modes and database validation (still some TODO statements) ([fb14d3a](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/fb14d3a34478393e1e7f02a234e6c926f8a5d2f6))
* Created new validation functionality for the SNP pattern in configuration file ([d176caa](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/d176caa512c3b32122e9b56f0669e370bd662b27))
* Created version tool logging functionality for PointFinder ([e2d624f](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/e2d624f69a00352fa928286260c8ff6d92b7f113))
* Developed the runner Enum for PointFinder with the right command preparation (still with example present) ([6152eb7](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/6152eb7d9dcb10be94f8dde606802249d451d8fe))
* Enhanced ReadConfigPattern and PointFinder for SNP database handling ([9f8bc91](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/9f8bc913e331c3ebbdeba4585ae51dcfadc431d7))
* Enhanced the ParsingManager class to support the search modes SNPs and both ([12904fb](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/12904fb78220f493612414b468e739620ca26e3c))
* Implemented PointFinders database creation functionality ([de1fe4a](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/de1fe4a25bdca78d5e2cc2eb8e4682336459b24f))
* Implemented SNPParser class for parsing PointFinders data and generating output reports ([65e675b](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/65e675b382b63c8b58091603ba3ed8a3f5d79736))
* Introduced a new column in the output reports ("mode") to easily spot if a found hit is a gene or SNP ([1f76fb3](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/1f76fb3384bfc653b9aa64889ee1bf826354ccc3))
* Pull request [#35](https://github.com/RIVM-bioinformatics/Pacini-typing/issues/35) of 'dev' branch with new SNP-functionality, output report, configuration file, README, and more ([0c75e90](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/0c75e903cc304646e23a10699c136df7d6d1e140))
* Pull request of 'dev' branch with new SNP-functionality, output report, configuration file, README, and more ([0c75e90](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/0c75e903cc304646e23a10699c136df7d6d1e140))
* WIP - Prepared the reading config pattern class to better fit SNP-related tasks ([6c6273a](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/6c6273ac5ebb7d50831efafa3ea19617016d3f1f))
* WIP - started implementing the SNP query runner class for SNP-related operations ([aa8d2c4](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/aa8d2c4e6a691a5e5d48f7f4d5a3ea1750aa7c4e))


### Bug Fixes

* Corrected comparison operator to accept same values ([51cab2c](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/51cab2c8b2fdf892b9ae35e503f089b4ea344832))
* Corrected mutation format in SNP hits column of output report ([75bf687](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/75bf687ed4c707e42fb1a4ff095dd59ccb5ac984))
* Fixed a bug in the validation of the pointfinder database where genes where checked in one file but had to be checked for indivudual files ([59b5fab](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/59b5fabb7b9a983829e10f20590ae2142ca6c75a))
* Fixed a bug where it was possible to provide fasta out flag for search mode SNPs ([dffb44a](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/dffb44a3b0f5075559c24fc60f1343688b515123))
* Fixed a bug where the identity threshold was not used correctly. ([ccbda83](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/ccbda83fe1b33d695f636a3d1139d78643ab5198))
* Fixed a bug where the index column in combined reports was wrong ([16ea985](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/16ea985923c181207f05b4be8fe3b9c9020181f8))
* Fixed a bug where the retrieval of non existing reports caused errors ([8ce44a1](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/8ce44a19295e4bef77e50d6a5ceec4ea4d65fc4a))
* Fixed a bug where the SNP directory was saved in wrong search mode ([bc3d6da](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/bc3d6da374e03414e4a694a9d37c8a58238d0596))
* Fixed a bug where unknown mutations where also placed in the output report (wrong flag for this purpose) ([470d27a](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/470d27a135c75fd5580af35800bb5c727d37e3f1))
* Fixed a small error where the logging of the tool version could continue if output was None ([ee76ff1](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/ee76ff134c90d3b868a04e69d7f4ecd88860ff8f))
* Fixed an error that raises an error in the initial SNP database check (before even trying to create it) ([aff4a43](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/aff4a43f3f69cee153c7c489d0246b6967b66153))
* Updated coverage calculation for blastn reports in multiple files (was not fully correct) ([8b95526](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/8b95526d31fab78f53c9ef5d6b63ecbe010d9d2f))
* Updated error messages for better debugging (errors where not displaying the topic or location of error) ([4ba1cca](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/4ba1cca4263c7c5c4b88dff0411cae2c982f4b6e))


### Documentation

* **queries:** Improved the documentation in the queries module to better explain the new PointFinder expansion and introduction of design pattern ([2e4a7db](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/2e4a7db1d7537adacb40d150515c5be1ff0b3f1f))
* Update README to include information about SNP-detection ([48a42bd](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/48a42bd2ab61dd7a608f18b363bcbdc5ae78c0d2))
* Updated class docstring for gene query runner class ([a1364ec](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/a1364ec62645a4849e483d72815f467b0d516e84))

## [1.6.4](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.6.3...v1.6.4) (2025-01-20)


### Documentation

* Added short description about accepted arguments ([d4c195d](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/d4c195dd0d43ece4994dec1f4f53940e22179bc7))

## [1.6.3](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.6.2...v1.6.3) (2025-01-20)


### Bug Fixes

* reverted an error in merge conflict ([bccf9ac](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/bccf9ac72f8bd4444190ed23b40422eab9178c77))

## [1.6.2](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.6.1...v1.6.2) (2025-01-16)


### Documentation

* add markdown badge for bioconda ([211ac55](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/211ac556984c4891cdb8309a046a76732b2c570d))
* Added a new python package to the list of required packages ([6d4be99](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/6d4be99e089bedc6f5a47e520f3a54395172b786))
* New version of the logo ([90c5a86](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/90c5a860d9d66c8232f1b7423389e86dced0eb43))
* update README with new installation instructions and badge updates ([8306a6a](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/8306a6ab07fb79848e4fcd7ddeb88e7730ecdf76))
* update the example config file in readme ([80f5818](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/80f5818a3653a408054a8f2ef0b11560380476a6))
* updated README with better future ideas ([3b22027](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/3b220272ee544db868bda5d537bfec1d82a9b9c5))
* updated README with some information about bugfix ([2c97d75](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/2c97d757fec279f1b25a541e8eace91d17f957ea))

## [1.6.1](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.6.0...v1.6.1) (2024-12-30)

### Bug Fixes

* bug fix where a non-existing path was causing an error in query option ([7ec633d](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/7ec633d34f747a0f29b20345e75ad5249e81a4f2))

## [1.6.0](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.5.1...v1.6.0) (2024-12-18)


### Features

* --fasta-out option for BLAST runs, with small change in the strategy ([8621a86](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/8621a865ee7bea45761054957412e3542188a8d1))
* --fasta-out option that writes sequence hits to output fasta. Only working for FASTQ-reads in this commit ([f86adfc](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/f86adfc70d2214b76644f5fa6ac9b24b18bf5a4a))
* add EmptySequenceError exception and handle empty query sequences in AlignmentExtractor ([ae9b52a](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/ae9b52ac9eefb62c99b5df7f20132603c62238be))
* add new validation tests for determining input type ([34e0b1e](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/34e0b1e89a8f00156cde2a4adc1828d9be14dad3))
* add support for multi-threading in query processing ([7a1b2e0](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/7a1b2e0298337e38af91fb8f71da4b9c9e087f1e))
* add tests for alignment_extractor and update output handling in end-to-end tests ([b002fed](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/b002fedad473f7db17d06fc3277b11808288dfee))
* Full file checking for both fastq and fasta files ([46eed5f](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/46eed5fbd45dca4d2076d6949803153ee606757f))
* implement parsing strategy to split functions of FASTA/FASTQ ([26c2665](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/26c2665e17cbeaba00528edfe39b1f8398e94604))


### Bug Fixes

* correct spelling of "extractor" in fasta_parser and fastq_parser ([5d182f7](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/5d182f7e86c6f39268ff22aa7165fbf229d519ad))
* fixed bug issue [#16](https://github.com/RIVM-bioinformatics/Pacini-typing/issues/16): --save-intermediates options fails ([2ec7e99](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/2ec7e99f4eeadfd84d9424f747a0260ad8f92195))
* fixed bug issue [#17](https://github.com/RIVM-bioinformatics/Pacini-typing/issues/17): always save database dir ([604f7a8](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/604f7a8ec68fc9bd074df90e71dee0d3eca27065))
* normalize database type to uppercase in configuration and argument parsing ([93452ab](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/93452ab14682255db13ec2506842c72df19f685c))
* small fix in de intermediate delete/save option for paths that were custom provided ([2ef3bc4](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/2ef3bc4975f450853c40db7ba604c5e32ea97525))
* swapped the mkdir to makedirs function to handle intermediates folders in paths ([8879e28](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/8879e2841b47476914044d05bb5ea7bacb899605))

## [1.5.1](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.5.0...v1.5.1) (2024-12-02)


### Documentation

* reshuffled the environment section and added more information about the output files ([623d767](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/623d76766c805e6a4eabfa7bb4b5991319feeeae))
* update README with improved YAML configuration details ([88a9f6c](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/88a9f6c0279fd5f81919874c26b34ef73d027c67))

## [1.5.0](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.4.0...v1.5.0) (2024-11-22)


### Features

* usage of the command design pattern for executing commands in Pacini-typing ([f276115](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/f27611567b0401a3292ab6ec2065675fca602f59))

## [1.4.0](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.3.1...v1.4.0) (2024-11-21)


### Features

* add FASTA files for VIB-O1 and VIB-O139 patterns ([e295e28](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/e295e28810bbf1cbf1e7ee642d00d59a9c3a6f42))


### Bug Fixes

* fixed a bug whith package dependenies in the linux env ([a758b6c](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/a758b6cf3d3e937dcfb4e82bff1aa9bd013e90ca))


### Documentation

* add new documentation files for installation, prerequisites, parameters, usage, and example run ([80680cc](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/80680cc2032dfe04ffcdac3e409c4a8af76fa298))
* add sections for Issues, Future Ideas, License, and Contact in README ([bbf1e4f](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/bbf1e4fa44213bc135ef493f63e4f7bc867ce539))
* update README with additional installation instructions, package requirements, and usage commands ([668a725](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/668a725c6108e9d73802c252d2720c8a02a41c75))

## [1.4.0](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.3.1...v1.4.0) (2024-11-21)


### Features

* add FASTA files for VIB-O1 and VIB-O139 patterns ([e295e28](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/e295e28810bbf1cbf1e7ee642d00d59a9c3a6f42))


### Bug Fixes

## [1.3.1](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.3.0...v1.3.1) (2024-11-18)


### Documentation

* update README with corrected prerequisites, required packages, and conda environment setup instructions ([c19841e](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/c19841e1456ea2eee86bcfcfbebcfeca121aafe8))

## [1.3.0](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.2.0...v1.3.0) (2024-11-14)


### Features

* add additional scripts for sample file management and analysis ([b279eb8](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/b279eb88feb578237264d1bf2f42d3ba45c1cdfb))
* update setup.py with author information and enhance package configuration ([6144b60](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/6144b60c74b51d61d1207d5e78318c0659967181))
* WIP - automatic database creation based on config file ([d73c56c](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/d73c56cb979b7b0be0c42439173f4054ae9e388f))
* WIP - implemented the usage of the config option ([6d071f5](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/6d071f5e41237ca71e5620668e6cef963aa16040))
* WIP - initial pattern parsing reading script ([e564a2b](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/e564a2bea40cc4f5276b5c2249974b0006ae0b34))
* WIP - Prepared the pattern parsing module with the implementation of config args ([122f1b1](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/122f1b1ae524e3d9451755f170da76a99cb897ae))
* WIP - prepared the re-use of multiple functions by the config file run option ([ddf1272](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/ddf1272fdda41dd060d3045e3dc68e4f6e136035))


### Bug Fixes

* fixed a bug where the wrong database was created using the configation file run option ([8ae742a](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/8ae742a9060e1b90147d5ccb50efed0b5a18d846))


### Documentation

* updated README with new badges ([3e75e34](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/3e75e34ea6e8dac16056a98fe56d9c379b49be1b))
* updated README with right badges ([bdf4116](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/bdf4116bf7292142fc690fd89789eedb35a4d2b8))

## [1.2.0](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.1.1...v1.2.0) (2024-10-28)


### Features

* implement custom error exceptions for input type validation ([75913b6](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/75913b6b5f2c89627e897c62184603c666181291))


### Bug Fixes

* implemented custom error exceptions for better debugging ([5f0413c](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/5f0413c82f9854431caa21808df4fa61f4039779))

## [1.1.1](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.1.0...v1.1.1) (2024-10-16)


### Bug Fixes

* tried to fix a github actions problem ([68c4d09](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/68c4d0958672c9639817ba923d6dcc5a3c085ac9))

## [1.1.0](https://github.com/RIVM-bioinformatics/Pacini-typing/compare/v1.0.0...v1.1.0) (2024-10-15)


### Features

* fixed auto release github action workflow ([eaedaae](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/eaedaae45dcf6f91fac127c4b336262d8fe5246f))
* implemented auto release github action workflow ([afd4242](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/afd4242185325532e02079a38a97b6d4624ddfc8))
* removed a bug in unit tests ([45f4578](https://github.com/RIVM-bioinformatics/Pacini-typing/commit/45f45780f40a8bb09681180a6e3e791d69b19f85))
