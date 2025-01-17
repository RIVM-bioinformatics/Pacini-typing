# Changelog

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
