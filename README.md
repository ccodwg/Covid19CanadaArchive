# Canadian COVID-19 Data Archive

The Canadian COVID-19 Data Archive is a collection of datasets, documents and webpages related to the COVID-19 pandemic in Canada, with files spanning March 2020 to January 2024. This project supported automated, daily snapshots of Canadian COVID-19 data from governmental and non-governmental sources beginning August 24, 2020 and concluding January 31, 2024. The Archive is maintained by [Jean-Paul R. Soucy](https://jeanpaulsoucy.com/) on behalf of the [COVID-19 Open Data Working Group](https://opencovid.ca/). It is a sister project to the [Timeline of COVID-19 in Canada](https://github.com/ccodwg/CovidTimelineCanada), a definitive dataset for COVID-19 in Canada.

A searchable catalogue of datasets is available in the [Data Explorer](https://ccodwg.github.io/Covid19CanadaArchive-data-explorer/). See [Accessing the data](#accessing-the-data) for more information.

File name timestamps are given in ET (America/Toronto) in the following format: %Y-%m-%d_%H-%M. Files were archived nightly beginning around 22:00 ET.

All code in this repository is covered by the [MIT License](https://github.com/ccodwg/Covid19CanadaArchive/blob/master/LICENSE). Archived datasets may be used under the licenses/terms of use assigned to them by the data creators.

Table of contents:

* [Accessing the data](#accessing-the-data)
* [Extra datasets](#extra-datasets)
* [Recommended citation](#recommended-citation)
* [Notes about the archive](#notes-about-the-archive)
* [Notes about the archival tool](#notes-about-the-archival-tool)
* [Acknowledgements](#acknowledgements)

## Accessing the data

A searchable catalogue of datasets, sorted by province/territory (and city/organization, if applicable), is available in the [Data Explorer](https://ccodwg.github.io/Covid19CanadaArchive-data-explorer/). Full details for each dataset, including any notes pertaining to them, are available in the **Search list of datasets** section of the [Data Explorer](https://ccodwg.github.io/Covid19CanadaArchive-data-explorer/). All data are stored in the Internet Archive's [Canadian COVID-19 Data Archive collection](https://archive.org/details/canadian-covid-19-data-archive). All metadata is generated from [`datasets.json`](https://github.com/ccodwg/Covid19CanadaArchive/blob/master/datasets.json) in this repository.

The `dl_archive` function of the R package [`Covid19CanadaData`](https://github.com/ccodwg/Covid19CanadaData) is available for automatically downloading datasets by UUID, filtering by date ranges, and removing duplicate files. See the package's [`README.md`](https://github.com/ccodwg/Covid19CanadaData?tab=readme-ov-file#archived-canadian-covid-19-datasets) for usage examples. Until January 2024, a [JSON API](https://api.opencovid.ca/) was also available with similar functionality.

Additionally, a complete copy of the the file index is available as a [SQLite database](https://archive.org/download/cc19da_ops/index.db). This database can easily be queried using a programming language and used to download a list of files using the following URL pattern:

```
https://archive.org/download/cc19da_{uuid}/cc19da_{uuid}.zip/{file_name}
```

## Extra datasets

Extra datasets, not included in the main catalogue, are documented in [`extra-datasets`](https://github.com/ccodwg/Covid19CanadaArchive/tree/master/extra-datasets). Unlike the main Canadian COVID-19 Data Archive collection, these files do not have standardized metadata or file naming conventions. This collection includes federal, provincial, and municipal datasets as well as datasets relating to the work of the COVID-19 Canada Open Data Working Group.

## Recommended citation

COVID-19 Canada Open Data Working Group. Canadian COVID-19 Data Archive. https://github.com/ccodwg/Covid19CanadaArchive. (Access date).

## Notes about the archive

- **Data from Quebec**: When both French and English data files are available, the French dataset should usually be considered definitive (and in most cases, these files have been captured in the archive for a longer duration). English versions of datasets are usually identified by the suffix `-en`. French datasets usually have the suffix `-fr` or no suffix.
- **Missing data**: The nightly archival script failed to run on two occasions (2020-10-21 and 2020-11-19), resulting in a significant loss of archival data. In some cases, files were added the following day (hopefully before the time they were updated) and labelled with the date of the previous day and time `23-59` (e.g., the timestamp `2020-10-21_23-59`). Additionally, files supplied to the Archive after they were captured with a known date but unknown time were assigned the time `20-00` (e.g., the timestamp `2020-08-25_20-00`).
- **Files improperly marked as not being duplicates of previous files**: The method of archiving websites (HTML files) was modified on 2021-12-30. This may have caused a handful of HTML files not to be marked duplicates of the previous day's file when they otherwise would have been. On 2022-03-26, the old method of archiving websites was erroneously used, once again resulting in some HTML files not being marked duplicates when they otherwise would have been.

## Notes about the archival tool

Updates to the Canadian COVID-19 Data Archive were managed by the [`archivist`](https://github.com/jeanpaulrsoucy/archivist) package.

## Acknowledgements

Many people contributed to the data archived in the Canadian COVID-19 Data Archive: Jean-Paul R. Soucy / Jens von Bergmann / Simon Coulombe / James E. Wright / Farbod Abolhassani / Shelby L. Sturrock / Safa Ahmad / Jacques Marcoux / Shraddha Pai / Matti Aleve / Scott van Millingen / Robson Fletcher / Les Perreaux / Allen Kwan / Christine Hagyard / Amy Bihari / Razieh Faraji / David Lussier / Matthias Schoettle / Jeremy Moreau / Sarah Otto / Bill Comeau / Alf Whitehead

Shannon Fiedler created the banner image for the Canadian COVID-19 Data Archive.
