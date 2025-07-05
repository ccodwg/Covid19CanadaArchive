# Canadian COVID-19 Data Archive

The Canadian COVID-19 Data Archive is a collection of datasets, documents and webpages related to the COVID-19 pandemic in Canada, with files spanning March 2020 to January 2024. This project supported automated, daily snapshots of Canadian COVID-19 data from governmental and non-governmental sources beginning August 25, 2020 and concluding January 31, 2024. The Archive is maintained by [Jean-Paul R. Soucy](https://jeanpaulsoucy.com/) on behalf of the [COVID-19 Open Data Working Group](https://opencovid.ca/). It is a sister project to the [Timeline of COVID-19 in Canada](https://github.com/ccodwg/CovidTimelineCanada), a definitive dataset for COVID-19 in Canada.

For a list of available datasets and information on how to access the datasets in the archive, see [Accessing the data](#accessing-the-data).

File name timestamps are given in ET (America/Toronto) in the following format: %Y-%m-%d_%H-%M. Files were archived nightly beginning around 22:00 ET.

All code in this repository is covered by the [MIT License](https://github.com/ccodwg/Covid19CanadaArchive/blob/master/LICENSE). Archived datasets may be used under the licenses/terms of use assigned to them by the data creators.

Table of contents:

* [Accessing the data](#accessing-the-data)
* [Recommended citation](#recommended-citation)
* [Notes about the data archive](#notes-about-the-data-archive)
* [Notes about the archival tool](#notes-about-the-archival-tool)
* [Acknowledgements](#acknowledgements)

## Accessing the data

A searchable catalogue of datasets, sorted by province/territory (and city/organization, if applicable), is available in the [Data Explorer](https://ccodwg.github.io/Covid19CanadaArchive-data-explorer/). Full details for each dataset, including any notes pertaining to them, are available in the **Search list of datasets** section of the [Data Explorer](https://ccodwg.github.io/Covid19CanadaArchive-data-explorer/). All data are stored in the Internet Archive's [Canadian COVID-19 Data Archive collection](https://archive.org/details/canadian-covid-19-data-archive). 

The `dl_archive` function of the R package [`Covid19CanadaData`](https://github.com/ccodwg/Covid19CanadaData) is available for automatically downloading datasets by UUID, filtering by date ranges, and removing duplicate files. See the package's [`README.md`](https://github.com/ccodwg/Covid19CanadaData?tab=readme-ov-file#archived-canadian-covid-19-datasets) for usage examples. Until January 2024, a [JSON API](https://api.opencovid.ca/) was also available with similar functionality.

Additionally, a complete copy of the the file index is available as a [SQLite database](https://archive.org/download/cc19da_ops/index.db). This database can easily be queried using a programming language and used to download a list of files using the following URL pattern:

```
https://archive.org/download/cc19da_{uuid}/cc19da_{uuid}.zip/{file_name}
```

## Recommended citation

COVID-19 Canada Open Data Working Group. Canadian COVID-19 Data Archive. https://github.com/ccodwg/Covid19CanadaArchive. (Access date).

## Notes about the data archive

- **Data from Quebec**: When both French and English data files are available, the French dataset should usually be considered definitive (and in most cases, these files have been captured in the archive for a longer duration).
- **Missing data**: On two occasions, the nightly archival script has failed to run. Depending on when the failure was identified, this may have resulted in a partial or total loss of archival data for that day. These days were 2020-10-21 and 2020-11-19.
- **Files improperly marked as not being duplicates of previous files**: The method of archiving websites (HTML files) was modified on 2021-12-30. This may have caused a handful of HTML files not to be marked duplicates of the previous day's file when they otherwise would have been. On 2022-03-26, the old method of archiving websites was erroneously used, once again resulting in some HTML files not being marked duplicates when they otherwise would have been.

## Notes about the archival tool

Updates to the Canadian COVID-19 Data Archive were managed by the [`archivist`](https://github.com/jeanpaulrsoucy/archivist) package.

## Acknowledgements

Shannon Fiedler created the banner image for the Canadian COVID-19 Data Archive.

Many people are to thank for contributing archived data and code to this repository:

[Jens von Bergmann](https://github.com/mountainMath) / [Simon Coulombe](https://github.com/simoncoulombe) / [James E. Wright](https://twitter.com/JWright159) / [Farbod Abolhassani](https://github.com/farbodab) / [Shelby L. Sturrock](https://twitter.com/shelbysturrock) / [Safa Ahmad](https://twitter.com/birdseye47) / [Jacques Marcoux](https://twitter.com/jacquesmarcoux) / [Shraddha Pai](https://twitter.com/spaiglass) / [Matti Aleve](https://twitter.com/maleve) / [Scott van Millingen](https://github.com/svmillin) / [Robson Fletcher](https://twitter.com/CBCFletch) / [Les Perreaux](https://twitter.com/perreaux) / Allen Kwan ([Twitter](https://twitter.com/allenkwan)/[LinkedIn](https://www.linkedin.com/in/allen-kwan/)) / Christine Hagyard ([Twitter](https://twitter.com/ChrisHagyard)/[LinkedIn](https://www.linkedin.com/in/christine-hagyard/))
 / Amy Bihari ([Twitter](https://twitter.com/AmyBihari)/[LinkedIn](https://www.linkedin.com/in/amy-bihari/)) / Razieh Faraji ([Twitter](https://twitter.com/raziehfaraji)/[LinkedIn](https://www.linkedin.com/in/raziehfaraji/)) / [David Lussier](https://twitter.com/LussiD) / [Matthias Schoettle](https://github.com/mschoettle) / [Jeremy Moreau](https://github.com/jeremymoreau) / [Sarah Otto](https://biodiversity.ubc.ca/people/faculty/sarah-otto)
