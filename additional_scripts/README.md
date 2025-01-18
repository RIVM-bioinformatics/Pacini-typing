# Internally used scripts

For this project, I created a few scripts that helped downloading/running/analyzing Pacini-typing data. These scripts are not meant to be used by the end-user, but rather to gain insights into the Pacini-typing project.

A main goal of Pacini-typing was validating the methods used by the application, to ensure that the results were consistent with the expected results.

The validation was done using internal RIVM samples and external samples from public available databases.

## Internal Data

The internal data comes from the RIVM own laboratory. The samples were sequenced and simple software was called to generate insides before running the Pacini-typing application.

For Vibrio cholerae, a main upside of the internal data was the availability of agglutination results. This allowed us to compare the results of Pacini-typing with the results of the agglutination tests.

## External Data

The external data comes from public available databases. All samples were downloaded from the Enterobase database.

Additionally, some samples were downloaded from published literature. These samples were used to validate the Pacini-typing application.

The literature-based validation was mainly focused on O139 serogroup Virbio cholerae samples, because these strains were not present within the RIVM. Because of the uncommonness of these strains, it was important to validate the Pacini-typing application with these samples.

Publications used for the literature-based validation were:

1. https://www.nature.com/articles/s41588-018-0150-8
2. https://www.nature.com/articles/s41467-022-31391-4

Together, these two studies provided a total of 75+ samples that were used for the validation of the O139 serogroup of Vibrio cholerae.

## Scripts

A very short description of the scripts:

1. `IRODS_path_collector.sh`: Collects the paths of the files in the IRODS system.
2. `IRODS_path_downloader.sh`: Downloads the files from the IRODS system.
3. `sorter.py`: Creates folders for the samples and moves the files to the correct folders. Also creates metadata files for the samples.
4. `run_pacini_on_external_samples.py`: Runs the Pacini-typing application on the external samples.
5. `run_pacini_on_internal_samples.py`: Runs the Pacini-typing application on the internal samples.
6. `create_report.py`: Creates a basic report of the results of the Pacini-typing application.
7. `downloader.py`: Downloads the accession numbers using multiple threads.

For specific information about the scripts, please take a look at the scripts themselves.
