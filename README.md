# Canadian COVID-19 Data Archive

The purpose of this repository is to support automated, daily backups of COVID-19 data from Canadian governmental and non-governmental sources. It is composed of a list of datasets (`datasets.json`), as well as the Python code making up the archival tool itself. The Canadian COVID-19 Data Archive is one component of the **[What Happened? COVID-19 in Canada](https://whathappened.coronavirus.icu/)** project.

For a list of available datasets, see the [Data catalogue](#data-catalogue) below. For information on how to access the datasets in the archive, see [Accessing the data](#accessing-the-data).

The easiest way to [contribute to this project](#contributing) is to help add new data (by providing a link to the data or by uploading files you have previously downloaded) using our [data submission form](https://docs.google.com/forms/d/e/1FAIpQLSeiUd415u_qdqNwNHVEeA_6KCEMRJhXJSL9_9i1UvLDN3LGQA/viewform?usp=sf_link) or by opening an issue on GitHub. We're also looking for help making this archive more useful and accessible by building tools to simplify discovering, downloading and working with the data contained within.

File name timestamps are given in ET (America/Toronto) in the following format: %Y-%m-%d_%H-%M. Files are archived nightly beginning around 22:00 ET.

All code in this repository is covered by the [MIT License](https://github.com/ccodwg/Covid19CanadaArchive/blob/master/LICENSE). Archived datasets may be used under the licenses/terms of use assigned to them by the data creators.

This repository is maintained by [Jean-Paul R. Soucy](https://jeanpaulsoucy.com/) on behalf of the [COVID-19 Open Data Working Group](https://opencovid.ca/).

Table of contents:

* [Data catalogue](#data-catalogue)
* [Accessing the data](#accessing-the-data)
* [Contributing](#contributing)
  * [Add a new dataset](#add-a-new-dataset)
  * [Retire an inactive dataset](#retire-an-inactive-dataset)
  * [Contribute historical data](#contribute-historical-data)
* [Recommended citation](#recommended-citation)
* [Notes about the data archive](#notes-about-the-data-archive)
* [Notes about the archival tool](#notes-about-the-archival-tool)
* [Acknowledgements](#acknowledgements)

## Data catalogue

A searchable catalogue of datasets, sorted by province/territory (and city/organization, if applicable), is available in the [Data Explorer](https://ccodwg.github.io/Covid19CanadaArchive-data-explorer/) [**note: the Data Explorer is temporarily unavailable**]. Full details for each dataset, including any notes pertaining to them, are available in the **Search list of datasets** section of the [Data Explorer](https://ccodwg.github.io/Covid19CanadaArchive-data-explorer/). Feature requests and bug reports for the Data Explorer should be made in its [dedicated GitHub repository](https://github.com/ccodwg/Covid19CanadaArchive-data-explorer).

A note about data from Quebec: when both French and English data files are available, the French dataset should usually be considered definitive (and in most cases, these files have been captured in the archive for a longer duration).

## Accessing the data

The easiest way to explore the data in the archive and download individual files is the aforementioned [Data Explorer](https://ccodwg.github.io/Covid19CanadaArchive-data-explorer/) [**note: the Data Explorer is temporarily unavailable**].

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

## Contributing

You may contribute to the project in several ways. In the future, more ways of contributing will be added (e.g., adding metadata).

### Add a new dataset

New datasets may be added in the following ways:

* **New!** Use our [data submission form](https://docs.google.com/forms/d/e/1FAIpQLSeiUd415u_qdqNwNHVEeA_6KCEMRJhXJSL9_9i1UvLDN3LGQA/viewform?usp=sf_link).
* Create a pull request on GitHub adding the dataset to the appropriate location in the "active" section of `data/datasets.json`. See other entries for examples.
* Create an issue on GitHub requesting the new dataset be added.
* Email [the maintainer](https://jeanpaulsoucy.com/) requesting the new dataset be added.

If you have archived versions of the dataset you are adding (e.g., you previously downloaded the dataset daily), see "Contributing historical data" below.

### Contribute historical data

Historical data (e.g., archived versions of a dataset newly added to the archival tool) may be contributed in the following ways:

* **New!** Use our [data submission form](https://docs.google.com/forms/d/e/1FAIpQLSeiUd415u_qdqNwNHVEeA_6KCEMRJhXJSL9_9i1UvLDN3LGQA/viewform?usp=sf_link).
* Create an issue on GitHub regarding the historical data.
* Email [the maintainer](https://jeanpaulsoucy.com/) regarding the historical data.

### Retire an inactive dataset

Some datasets continue to exist at a URL but are no longer updated. These datasets should be removed from the nightly update. This may be achieved in the following ways:

* Create a pull request on GitHub moving the dataset's entry from the "active" section of `data/datsets.json` to the appropriate location in the "inactive" section. Also, change the dataset's "active" flag from "True" to "False". See other entries for examples.
* Email [the maintainer](https://jeanpaulsoucy.com/) with the historical data (for a dataset you've downloaded previously but is no longer updated).

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

 Last but not least, thank you to the [Internet Archive](https://archive.org/) for being a resource and an inspiration to amateur archivists everywhere. They even gave the Canadian COVID-19 Data Archive a [shoutout on Twitter](https://twitter.com/internetarchive/status/1420041682125426691)!
