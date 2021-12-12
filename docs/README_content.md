# Canadian COVID-19 Data Archive

The purpose of this repository is to support automated, daily backups of COVID-19 data from Canadian governmental and non-governmental sources. It is composed of a list of datasets (`datasets.json`), as well as the Python code making up the archival tool itself. The Canadian COVID-19 Data Archive is one component of the **[What Happened? COVID-19 in Canada](https://whathappened.coronavirus.icu/)** project.

For information on how to access the datasets in the archive, see [Accessing the data](#accessing-the-data). For a list of available datasets, see the [Data catalogue](#data-catalogue) below.

The easiest way to [contribute to this project](#contributing) is to help add new data (by providing a link to the data or by uploading files you have previously downloaded) using our [data submission form](https://docs.google.com/forms/d/e/1FAIpQLSeiUd415u_qdqNwNHVEeA_6KCEMRJhXJSL9_9i1UvLDN3LGQA/viewform?usp=sf_link) or by opening an issue on GitHub. We're also looking for help making this archive more useful and accessible by building tools to simplify discovering, downloading and working with the data contained within.

File name timestamps are given in ET (America/Toronto) in the following format: %Y-%m-%d_%H-%M. Files are archived nightly around 22:00 ET.

All code in this repository is covered by the [MIT License](https://github.com/ccodwg/Covid19CanadaArchive/blob/master/LICENSE). Archived datasets may be used under the licenses/terms of use assigned to them by the data creators.

This repository is maintained by [Jean-Paul R. Soucy](https://jeanpaulsoucy.com/) on behalf of the [COVID-19 Open Data Working Group](https://opencovid.ca/).

Table of contents:

* [Accessing the data](#accessing-the-data)
* [Contributing](#contributing)
  * [Add a new dataset](#add-a-new-dataset)
  * [Retire an inactive dataset](#retire-an-inactive-dataset)
  * [Contribute historical data](#contribute-historical-data)
* [Recommended citation](#recommended-citation)
* [Running archiver.py](#running-archiverpy)
* [Data catalogue](#data-catalogue)
  * [Alberta](#alberta)
     * [Edmonton](#edmonton)
  * [British Columbia](#british-columbia)
  * [Canada](#canada)
  * [Manitoba](#manitoba)
     * [Winnipeg](#winnipeg)
  * [New Brunswick](#new-brunswick)
  * [Newfoundland and Labrador](#newfoundland-and-labrador)
  * [Northwest Territories](#northwest-territories)
  * [Nova Scotia](#nova-scotia)
  * [Nunavut](#nunavut)
  * [Ontario](#ontario)
     * [Ontario universities](#ontario-universities)
     * [Ottawa](#ottawa)
     * [Public Health Ontario](#public-health-ontario)
     * [Public Health Units](#public-health-units)
     * [Toronto](#toronto)
  * [Prince Edward Island](#prince-edward-island)
  * [Quebec](#quebec)
     * [Montreal](#montreal)
  * [Saskatchewan](#saskatchewan)
  * [Yukon](#yukon)
  * [Other: Non-governmental sources](#other-non-governmental-sources)
     * [Canada](#canada-1)
     * [Quebec](#quebec-1)
* [Notes about the data archive](#notes-about-the-data-archive)
* [Acknowledgements](#acknowledgements)

## Accessing the data

The easiest way to explore the data in the archive and download individual files is with the interactive file explorer: [http://data.opencovid.ca/archive/index.html#archive/](http://data.opencovid.ca/archive/index.html#archive/).

The files in the archive are hosted at the following URL: [https://data.opencovid.ca.s3.amazonaws.com/archive/](https://data.opencovid.ca.s3.amazonaws.com/archive/)

For example, the PHAC Epidemiology Update from November 4, 2020 may be downloaded at the following URL: [https://data.opencovid.ca.s3.amazonaws.com/archive/can/epidemiology-update-2/covid19-download_2020-11-04_23-38.csv](https://data.opencovid.ca.s3.amazonaws.com/archive/can/epidemiology-update-2/covid19-download_2020-11-04_23-38.csv)

A complete index of files in the archive, including flags for duplicated files and corrected file dates, is available at the following URL: [https://data.opencovid.ca.s3.amazonaws.com/archive/file_index.csv](https://data.opencovid.ca.s3.amazonaws.com/archive/file_index.csv). This index is refreshed nightly around 23:00 ET.

Alternatively, software such as Python or R may be used to explore and download files from specific directories. Examples are provided below.

All files in a particular directory may be listed in Python using the following code (change `Prefix` as desired):

```
# load modules
from boto3 import client

# get list of files in directory
cli = client('s3')
files = [key['Key'] for key in cli.list_objects(Bucket='data.opencovid.ca', Prefix='archive/can/epidemiology-update-2')['Contents']]

# (optional) filter out supplementary material from list of files in the directory
import re
pat = re.compile('^.*/supplementary/') # match files in supplementary folder
files = [s for s in files if not pat.match(s)]

# print list of files
print(files)
```

These files could then be downloaded by appending the base URL to the above file list.

In R, the above may be achieved using the following code:

```
# load packages
library(aws.s3)

# get list of files in directory
files <- aws.s3::get_bucket(bucket = "data.opencovid.ca" , prefix = "archive/can/epidemiology-update-2/", region = "us-east-2")
files <- unlist(lapply(files, function(x) x[["Key"]]), use.names = FALSE)

# (optional) filter out supplementary material from list of files in the directory
files <- files[!grepl("^.*/supplementary/", files)]

# print list of files
print(files)
```

Please note that the data in this archive were previously hosted on Google Drive. This product has been discontinued and all further data updates will occur on the [data.opencovid.ca](http://data.opencovid.ca/archive/index.html#archive/) site.

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

## Running archiver.py

*archiver.py* can run in two modes:
* `python archiver.py -m prod`: Download files and upload them to the archive.
* `python archiver.py -m test`: Don't upload files to the archive, just test that they can be successfully downloaded. Sends a notification email if a URL cannot be reached.

The script relies on setting environmental variables to function properly. See *archiver.py* for more details.

## Data catalogue

A list of datasets available in the archive is given below, sorted by province (and city, if applicable). Supplementary data (e.g., codebooks, data dictionaries) are available for some datasets in `supplementary` subdirectories. Full details for each dataset, including any notes pertaining to them, are given in [`datasets.json`](https://github.com/ccodwg/Covid19CanadaArchive/blob/master/datasets.json).

A note about data from Quebec: when both French and English data files are available, French files should generally be considered definitive (and in many cases, these files have been captured in the archive for a longer duration). The English versions of files available in both languages have "-en" appended to their directory names.

[INSERT DATA CATALOGUE HERE]

## Notes about the data archive

On several occasions, the nightly archival script has failed to run. Depending on when the failure was identified, this may have resulted in a partial or total loss of archival data for that day. A list of these days is provided below:

* Wednesday, October 21, 2020
* Thursday, November 19, 2020

In the future, a package will be provided to more easily access the data provided in this archive and to document missing or incomplete data.

## Acknowledgements

Shannon Fiedler created the banner image for the Canadian COVID-19 Data Archive.

Many people are to thank for contributing archived data and code to this repository.
 
* [Jens von Bergmann](https://github.com/mountainMath)
* [Simon Coulombe](https://github.com/simoncoulombe)
* [James E. Wright](https://twitter.com/JWright159)
* [Farbod Abolhassani](https://github.com/farbodab)
* [Shelby L. Sturrock](https://twitter.com/shelbysturrock)
* [Safa Ahmad](https://twitter.com/birdseye47)
* [Jacques Marcoux](https://twitter.com/jacquesmarcoux)
* [Shraddha Pai](https://twitter.com/spaiglass)
* [Matti Aleve](https://twitter.com/maleve)
* [Scott van Millingen](https://github.com/svmillin)
* [Robson Fletcher](https://twitter.com/CBCFletch)
* [Les Perreaux](https://twitter.com/perreaux)
* Allen Kwan ([Twitter](https://twitter.com/allenkwan)/[LinkedIn](https://www.linkedin.com/in/allen-kwan/))
* Christine Hagyard ([Twitter](https://twitter.com/ChrisHagyard)/[LinkedIn](https://www.linkedin.com/in/christine-hagyard/))
* Amy Bihari ([Twitter](https://twitter.com/AmyBihari)/[LinkedIn](https://www.linkedin.com/in/amy-bihari/))
* Razieh Faraji ([Twitter](https://twitter.com/raziehfaraji)/[LinkedIn](https://www.linkedin.com/in/raziehfaraji/))
* [David Lussier](https://twitter.com/LussiD)
* [Matthias Schoettle](https://github.com/mschoettle)
* [Jeremy Moreau](https://github.com/jeremymoreau)
