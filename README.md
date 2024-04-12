# Canadian COVID-19 Data Archive

The Canadian COVID-19 Data Archive is a collection of datasets, documents and webpages related to the COVID-19 pandemic in Canada, with files spanning March 2020 to January 2024. This project supported automated, daily snapshots of Canadian COVID-19 data from governmental and non-governmental sources beginning August 25, 2020 and concluding January 31, 2024. The Archive is maintained by [Jean-Paul R. Soucy](https://jeanpaulsoucy.com/) on behalf of the [COVID-19 Open Data Working Group](https://opencovid.ca/). It is a sister project to the [Timeline of COVID-19 in Canada](https://github.com/ccodwg/CovidTimelineCanada), a definitive dataset for COVID-19 in Canada.

For a list of available datasets, see the [Data catalogue](#data-catalogue) below. For information on how to access the datasets in the archive, see [Accessing the data](#accessing-the-data).

File name timestamps are given in ET (America/Toronto) in the following format: %Y-%m-%d_%H-%M. Files were archived nightly beginning around 22:00 ET.

All code in this repository is covered by the [MIT License](https://github.com/ccodwg/Covid19CanadaArchive/blob/master/LICENSE). Archived datasets may be used under the licenses/terms of use assigned to them by the data creators.

Table of contents:

* [Data catalogue](#data-catalogue)
* [Accessing the data](#accessing-the-data)
* [Recommended citation](#recommended-citation)
* [Notes about the data archive](#notes-about-the-data-archive)
* [Notes about the archival tool](#notes-about-the-archival-tool)
* [Acknowledgements](#acknowledgements)

## Data catalogue

A searchable catalogue of datasets, sorted by province/territory (and city/organization, if applicable), is available in the [Data Explorer](https://ccodwg.github.io/Covid19CanadaArchive-data-explorer/). Full details for each dataset, including any notes pertaining to them, are available in the **Search list of datasets** section of the [Data Explorer](https://ccodwg.github.io/Covid19CanadaArchive-data-explorer/). Feature requests and bug reports for the Data Explorer should be made in its [dedicated GitHub repository](https://github.com/ccodwg/Covid19CanadaArchive-data-explorer).

A note about data from Quebec: when both French and English data files are available, the French dataset should usually be considered definitive (and in most cases, these files have been captured in the archive for a longer duration).

## Accessing the data

The easiest way to explore the data in the archive and download individual files is the aforementioned [Data Explorer](https://ccodwg.github.io/Covid19CanadaArchive-data-explorer/).

The files in the archive are hosted under the following domain under the domain `https://data.opencovid.ca/archive`. For example, the PHAC Epidemiology Update from November 4, 2020 may be downloaded at the following URL:

```
https://data.opencovid.ca/archive/can/epidemiology-update-2/covid19-download_2020-11-04_23-38.csv
```

Additionally, a complete copy of the index is available as a SQLite database at the following URL:

```
https://data.opencovid.ca/archive/index.db
```

This database can easily be queried using a programming language and used to download a list of files.

Previously, a [JSON API](https://api.opencovid.ca/) was available to search the file index, which supported filtering by UUID and date ranges, as well as removing duplicate files. This API was retired in February 2024.

## Recommended citation

COVID-19 Canada Open Data Working Group. Canadian COVID-19 Data Archive. https://github.com/ccodwg/Covid19CanadaArchive. (Access date).

## Notes about the data archive

On several occasions, the nightly archival script has failed to run. Depending on when the failure was identified, this may have resulted in a partial or total loss of archival data for that day. A list of these days is provided below:

* 2020-10-21
* 2020-11-19

In addition, the method of archiving websites (HTML files) was modified on 2021-12-30. This may have caused a handful of HTML files not to be marked duplicates of the previous day's file when they otherwise would have been. On 2022-03-26, the old method of archiving websites was erroneously used, once again resulting in some HTML files not being marked duplicates when they otherwise would have been.

## Notes about the archival tool

Updates to the Canadian COVID-19 Data Archive are managed by the [`archivist`](https://github.com/jeanpaulrsoucy/archivist) package. Development of `archivist` originally took place in this repository but has since been migrated to its [own repository](https://github.com/jeanpaulrsoucy/archivist).

## Acknowledgements

Shannon Fiedler created the banner image for the Canadian COVID-19 Data Archive.

Many people are to thank for contributing archived data and code to this repository:

[Jens von Bergmann](https://github.com/mountainMath) / [Simon Coulombe](https://github.com/simoncoulombe) / [James E. Wright](https://twitter.com/JWright159) / [Farbod Abolhassani](https://github.com/farbodab) / [Shelby L. Sturrock](https://twitter.com/shelbysturrock) / [Safa Ahmad](https://twitter.com/birdseye47) / [Jacques Marcoux](https://twitter.com/jacquesmarcoux) / [Shraddha Pai](https://twitter.com/spaiglass) / [Matti Aleve](https://twitter.com/maleve) / [Scott van Millingen](https://github.com/svmillin) / [Robson Fletcher](https://twitter.com/CBCFletch) / [Les Perreaux](https://twitter.com/perreaux) / Allen Kwan ([Twitter](https://twitter.com/allenkwan)/[LinkedIn](https://www.linkedin.com/in/allen-kwan/)) / Christine Hagyard ([Twitter](https://twitter.com/ChrisHagyard)/[LinkedIn](https://www.linkedin.com/in/christine-hagyard/))
 / Amy Bihari ([Twitter](https://twitter.com/AmyBihari)/[LinkedIn](https://www.linkedin.com/in/amy-bihari/)) / Razieh Faraji ([Twitter](https://twitter.com/raziehfaraji)/[LinkedIn](https://www.linkedin.com/in/raziehfaraji/)) / [David Lussier](https://twitter.com/LussiD) / [Matthias Schoettle](https://github.com/mschoettle) / [Jeremy Moreau](https://github.com/jeremymoreau)
