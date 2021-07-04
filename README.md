# Canadian COVID-19 Data Archive

This repository provides automated, daily backups of COVID-19 data from Canadian governmental and non-governmental sources.

**THE DATA FOR THIS ARCHIVE ARE NO LONGER HOSTED ON GOOGLE DRIVE.** For information on how to access the datasets in the archive, see [Accessing the data](#accessing-the-data). For a list of available datasets, see the [Data catalogue](#data-catalogue) below.

File name timestamps are given in ET (America/Toronto) in the following format: %Y-%m-%d_%H-%M. Files are archived nightly around 22:00 ET.

All code in this repository is covered by the [MIT License](https://github.com/ccodwg/Covid19CanadaArchive/blob/master/LICENSE). Archived datasets may be used under the licenses/terms of use assigned to them by the data creators.

This repository is maintained by [Jean-Paul R. Soucy](https://jeanpaulsoucy.com/) on behalf of the [COVID-19 Open Data Working Group](https://opencovid.ca/).

Table of contents:

* [Accessing the data](#accessing-the-data)
* [Contribution guide](#contribution-guide)
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
     * [Ottawa](#ottawa)
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

## Contribution guide

Community members may contribute to the project in several ways. In the future, more ways of contributing will be added (e.g., adding metadata).

### Add a new dataset

New datasets may be added in the following ways:

* Create a pull request on GitHub adding the dataset to the appropriate location in the "active" section of `data/datasets.json`. See other entries for examples.
* Create an issue on GitHub requesting the new dataset be added.
* Email [the maintainer](https://jeanpaulsoucy.com/) requesting the new dataset be added.

If you have archived versions of the dataset you are adding (e.g., you previously downloaded the dataset daily), see "Contributing historical data" below.

### Retire an inactive dataset

Some datasets continue to exist at a URL but are no longer updated. These datasets should be removed from the nightly update. This may be achieved in the following ways:

* Create a pull request on GitHub moving the dataset's entry from the "active" section of `data/datsets.json` to the appropriate location in the "inactive" section. Also, change the dataset's "active" flag from "True" to "False". See other entries for examples.
* Create an issue on GitHub requesting the dataset be retired.
* Email [the maintainer](https://jeanpaulsoucy.com/) with the historical data.

### Contribute historical data

Historical data (e.g., archived versions of a dataset newly added to the archival tool) may be contributed in the following ways:

* Create an issue on GitHub regarding the historical data.
* Email [the maintainer](https://jeanpaulsoucy.com/) regarding the historical data.

## Recommended citation

COVID-19 Canada Open Data Working Group. Canadian COVID-19 Data Archive. https://github.com/ccodwg/Covid19CanadaArchive. (Access date).

## Running archiver.py

*archiver.py* can run in two modes:
* `python archiver.py prod`: Download files and upload them to the archive.
* `python archiver.py test`: Don't upload files to the archive, just test that they can be successfully downloaded. Sends a notification email if a URL cannot be reached.

The script relies on setting environmental variables to function properly. See *archiver.py* for more details.

## Data catalogue

A list of datasets available in the archive is given below, sorted by province (and city, if applicable). Supplementary data (e.g., codebooks, data dictionaries) are available for some datasets in `supplementary` subdirectories. Full details for each dataset, including any notes pertaining to them, are given in [`datasets.json`](https://github.com/ccodwg/Covid19CanadaArchive/blob/master/datasets.json).

A note about data from Quebec: when both French and English data files are available, French files should generally be considered definitive (and in many cases, these files have been captured in the archive for a longer duration). The English versions of files available in both languages have "-en" appended to their directory names.

### Alberta

* [COVID-19 Alberta statistics](https://www.alberta.ca/stats/covid-19-alberta-statistics.htm)
    * Webpage: [ab/ab-covid-statistics-webpage/ab-covid-statistics-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Case data: [ab/cases/covid19dataexport.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Case time series (Local geographic area): [ab/case-time-series-by-lga/covid-19-alberta-statistics-map-data.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine data (Local geographic area): [ab/vaccine-coverage-by-lga/lga-coverage.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine data (Zone): [ab/vaccine-coverage-by-zone/zone-coverage.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [COVID-19 relaunch status map](https://www.alberta.ca/maps/covid-19-status-map.htm)
    * Active cases by region: [ab/active-cases-by-region/covid19dataexport-relaunch.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 school status map](https://www.alberta.ca/schools/covid-19-school-status-map.htm)
    * School status map: [ab/school-status-by-region/covid19dataexport-schools.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Cases in Alberta](https://www.alberta.ca/covid-19-alberta-data.aspx)
    * Webpage: [ab/ab-cases-webpage/ab-cases-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 vaccine distribution](https://www.alberta.ca/covid19-vaccine.aspx)
    * Webpage: [ab/ab-vaccine-distribution-webpage/ab-vaccine-distribution-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 info for Albertans](https://www.alberta.ca/coronavirus-info-for-albertans.aspx)
    * Webpage: [ab/ab-provincial-summary-webpage/ab-provincial-summary-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
#### Edmonton

* [COVID-19 in Alberta: Current cases by local geographic area (Edmonton)](https://data.edmonton.ca/Community-Services/COVID-19-in-Alberta-Current-cases-by-local-geograp/ix8f-s9xp)
    * Current cases by local geographic area: [ab/edmonton-cases-by-area/COVID-19_in_Alberta__Current_cases_by_local_geographic_area.csv](http://data.opencovid.ca/archive/index.html#archive/)

### British Columbia

* [British Columbia COVID-19 Dashboard](https://experience.arcgis.com/experience/a6f23959a8b14bfa989e3cda29297ded)
    * Dashboard BC and Canada cumulative testing rate: [bc/bc-canada-cumulative-testing-rate/BC_COVID19__BC_Canadian_Testing_Rates_View.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard case demographics by Regional Health Authority: [bc/case-demographics-by-rha/BC_COVID19_Dashboard_Case_Details_Production.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard 7-day and cumulative cases by HSDA: [bc/7-day-and-cumulative-cases-by-hsda/BC_COVID19_Dashboard_Cases_by_Health_Service_Delivery_Areas_HSDA_VIEW.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard testing time series by Regional Health Authority (2): [bc/testing-timeseries-by-rha-2/BC_COVID19_Laboratory_Information.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard testing time series by Regional Health Authority: [bc/testing-timeseries-by-rha/BC_COVID19_Lab_Information.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard Vaccine Doses by Regional Health Authority: [bc/vaccine-doses-by-rha/BC_COVID19Dashboard_Vaccine_Counts.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard case time series by Health Service Delivery Area: [bc/case-time-series-by-hsda/BCCOVID19_Dashboard_Regional_Summary_Data.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard cumulative case, death, recovered, hospitalization, ICU data by Regional Health Authority: [bc/cumulative-case-death-recover-hosp-icu-by-rha/COVID19_Cases_by_BC_Health_Authority.json](http://data.opencovid.ca/archive/index.html#archive/)
    * 7-day and cumulative cases by HSDA (2): [bc/7-day-and-cumulative-cases-by-hsda-2/CumulativeCases.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard Regional Health Authority labels: [bc/rha-labels/HA_Labels.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard Vaccine Doses by Regional Health Authority (2): [bc/vaccine-doses-by-rha-2/BCCOVID19DashboardVaccineCountsVIEWSTAGING.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [COVID-19 Public Exposures](http://www.bccdc.ca/health-info/diseases-conditions/covid-19/public-exposures)
    * Public exposures webpage screenshot: [bc/public-exposures-webpage/public-exposures-screenshot.png](http://data.opencovid.ca/archive/index.html#archive/)
    * Public exposures - flights: [bc/public-exposures-flights/public-exposures-flights-tables-Current.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Public exposures Fraser webpage: [bc/regional-exposure-events-fraser-webpage/regional-exposure-events-fraser-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Public exposures Interior webpage: [bc/regional-exposure-events-interior-webpage/regional-exposure-events-interior-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Public exposures Island webpage: [bc/regional-exposure-events-island-webpage/regional-exposure-events-island-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Public exposures Northern webpage: [bc/regional-exposure-events-northern-webpage/regional-exposure-events-northern-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Public exposures Vancouver Coastal webpage: [bc/regional-exposure-events-vancouver-coastal-webpage/regional-exposure-events-vancouver-coastal-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * School exposures Fraser webpage: [bc/school-exposures-fraser-webpage/school-exposures-fraser-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * School exposures Interior webpage: [bc/school-exposures-interior-webpage/school-exposures-interior-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * School exposures Island webpage: [bc/school-exposures-island-webpage/school-exposures-island-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * School exposures Northern webpage: [bc/school-exposures-northern-webpage/school-exposures-northern-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * School exposures Vancouver Coastal webpage: [bc/school-exposures-vancouver-coastal-webpage/school-exposures-vancouver-coastal-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Public exposures - cruises, long distance bus, train, work sites, public events: [bc/public-exposures-cruises-bus-train-work-public/Archived_COVID-19_Exposures.pdf](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [BC COVID-19 Data](http://www.bccdc.ca/health-info/diseases-conditions/covid-19/data)
    * Webpage: [bc/bc-covid-data-webpage/bc-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * : [bc/case-data/BCCDC_COVID19_Dashboard_Case_Details.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * : [bc/laboratory-data/BCCDC_COVID19_Dashboard_Lab_Information.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * : [bc/regional-case-summary/BCCDC_COVID19_Regional_Summary_Data.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * : [bc/voc-time-series-by-rha-2/Figure1_weeklyreport_data.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * VOC time series by RHA: [bc/voc-time-series-by-rha/COVID19_VoC_data.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]

### Canada

* [Vaccines and treatments for COVID-19: Vaccine rollout](https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection/prevention-risks/covid-19-vaccine-treatment/vaccine-rollout.html)
    * Webpage: [can/vaccine-rollout-webpage/vaccine-rollout-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 international data](https://health-infobase.canada.ca/covid-19/international/)
    * International case and death time series: [can/international-covid-cases-deaths-time-series/InternationalCovid19Cases.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * International case and death time series update date: [can/international-covid-cases-deaths-time-series-update-date/updated.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Preliminary dataset on confirmed cases of COVID-19, Public Health Agency of Canada](https://www150.statcan.gc.ca/n1/pub/13-26-0003/132600032020001-eng.htm)
    * Dataset: [can/preliminary-dataset-on-confirmed-cases/COVID19-eng.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 daily epidemiology update](https://health-infobase.canada.ca/covid-19/epidemiological-summary-covid-19-cases.html)
    * National overview (DD-MM-YYYY): [can/epidemiology-update/covid19.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * National overview (YYYY-MM-DD): [can/epidemiology-update-2/covid19-download.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Epidemiology summary statements: [can/epidemiology-summary-statements/covid19-epiSummary-statements.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * NML summary: [can/nml-summary/covid19-epiSummary-NML.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * NML weekly testing: [can/nml-weekly-testing/NML_weekly_testing.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Lab indicators: [can/lab-testing-time-series/covid19-epiSummary-labIndicators.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Number of cases with detailed case report data: [can/detailed-case-report-n/covid19-nTotal.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases and deaths by health region time series: [can/cases-and-deaths-by-hr-time-series/file_out_v5.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Health region UID table: [can/health-region-uid/covid19-healthregions-hruid.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by exposure setting time series: [can/cases-by-exposure-time-series/covid19-epiSummary-casesovertime.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Epidemic curve by date of illness onset by age group: [can/epidemic-curve-by-age/covid19-epiSummary-epiCurveByAge.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Severity by age group and sex: [can/severity-by-age-and-sex/covid19-epiSummary-severityUpdate.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by severity: [can/cases-by-severity/covid19-epiSummary-severity.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by age group and sex: [can/cases-by-age-and-sex/covid19-epiSummary-agegroups2.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by probable exposure setting: [can/cases-by-probable-exposure-setting/covid19-epiSummary-probableexposure2.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by probable expsoure setting by province: [can/cases-by-probable-exposure-setting-and-province/covid19-epiSummary-exposureByPT.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Symptoms summary: [can/symptoms-summary/covid19-epiSummary-symptoms.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Hospitalizations, intensive care unit (ICU), mechanical ventilation: [can/hospitalizations-icu-mechanical-ventilation/covid19-epiSummary-hospVentICU.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases on First Nations reserves: [can/covid-time-series-first-nations-reserves/covid19-isc.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Variants of concern time series by province: [can/variants-of-concern-time-series-by-province/covid19-epiSummary-voc.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Situational awareness dashboard update time: [can/situational-awareness-dashboard-update-time/covid19-updateTime.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * PHAC provincial data update notes: [can/provincial-data-update-notes/covid19-epiSummary-exceptions.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Coronavirus disease (COVID-19): Locations where you may have been exposed to COVID-19](https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection/latest-travel-health-advice/exposure-flights-cruise-ships-mass-gatherings.html)
    * Webpage: [can/can-potential-exposures-webpage/can-potential-exposures-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Detailed preliminary information on confirmed cases of COVID-19 (Revised)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310078101)
    * Dataset: [can/detailed-preliminary-confirmed-case-info-revised/13100781.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [COVID-19 vaccination in Canada - Vaccines administered](https://health-infobase.canada.ca/covid-19/vaccine-administration/)
    * Vaccination administration: [can/vaccination-administration/vaccination-administration.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination administration update date: [can/vaccination-administration-update-date/vaccination-administration-updateDate.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination distribution: [can/vaccination-distribution/vaccination-distribution.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 vaccination in Canada - Technical notes](https://health-infobase.canada.ca/covid-19/vaccination-coverage/technical-notes.html)
    * Webpage: [can/vaccination-technical-notes-webpage/vaccination-technical-notes-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage data availability by week: [can/vaccination-coverage-data-availability-by-week/vaccination-coverage-dataAvailability.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVIDTrends](https://health-infobase.canada.ca/covid-19/covidtrends/)
    * Mobility: [can/covidtrends-mobility/mobility.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * FluWatchers: [can/covidtrends-fluwatchers/fluwatchers.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Detailed preliminary information on cases of COVID-19: 4 Dimensions (Aggregated data)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310077501)
    * Dataset: [can/detailed-preliminary-case-info-aggregated-4-dimensions/13100775.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Detailed preliminary information on cases of COVID-19: 6 Dimensions (Aggregated data)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310077401)
    * Dataset: [can/detailed-preliminary-case-info-aggregated-6-dimensions/13100774.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Reported side effects following COVID-19 vaccination in Canada](https://health-infobase.canada.ca/covid-19/vaccine-safety/)
    * AEFI weekly reports by event type: [can/aefi-weekly-by-event-type/vaccine-safety-AEFI-figure.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * AEFI weekly reports key updates: [can/aefi-weekly-key-updates/vaccine-safety-keyupdates.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * AEFI summary including vaccination data: [can/aefi-figure-weekly-summary-including-vaccination/vaccine-safety-figure1.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * AEFI weekly summary by vaccine type: [can/aefi-figure-weekly-summary-by-vaccine-type/vaccine-safety-figure2.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * AEFI weekly summary by age and sex: [can/aefi-figure-weekly-summary-by-age-sex/vaccine-safety-figure3.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * AEFI weekly summary by serious events: [can/aefi-figure-weekly-summary-by-serious-events/vaccine-safety-figure4.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Reported side effects following COVID-19 vaccination in Canada: AEFI weekly summary (old): [can/aefi-weekly-summary-old/vaccine-safety-AEFI.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * AEFI weekly summary by serious event type (old): [can/aefi-weekly-summary-by-serious-event-type-old/vaccine-safety-severity.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [COVID-19 vaccination in Canada - Vaccination coverage](https://health-infobase.canada.ca/covid-19/vaccination-coverage/)
    * Vaccination coverage overall: [can/vaccination-coverage-overall/vaccination-coverage-overall.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage for key populations: [can/vaccination-coverage-keypops/vaccination-coverage-keypops.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by age and sex: [can/vaccination-coverage-by-age-sex/vaccination-coverage-byAgeAndSex.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by age and sex (2): [can/vaccination-coverage-by-age-sex-2/vaccination-coverage-byAgeAndSex2.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by age and sex (condensed): [can/vaccination-coverage-by-age-sex-condensed/vaccination-coverage-byAgeAndSexOT.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by age and sex (alternative): [can/vaccination-coverage-by-age-sex-alt/vaccination-coverage-byAgeAndSex-overTime.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by age and sex with denominators: [can/vaccination-coverage-by-age-sex-denominators/vaccination-coverage-byAgeAndSexDenominators.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by vaccine type: [can/vaccination-coverage-by-vaccine-type/vaccination-coverage-byVaccineType.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by province: [can/vaccination-coverage-by-prov/vaccination-coverage-map.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination notes: [can/vaccination-notes/vaccination-notes.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Testing for COVID-19: Increasing testing supply](https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection/symptoms/testing/increased-supply.html)
    * Webpage: [can/testing-supply-webpage/testing-supply-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)

### Manitoba

* [COVID-19 Dashboard: K-12 Schools in Manitoba](https://experience.arcgis.com/experience/6e7af13b3ffb447a99734b0119b169d3/)
    * COVID education statistics summary: [mb/covid-education-summary/covid-education-summary.json](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID educations cases last 2 weeks: [mb/covid-education-cases-last-2-weeks/covid-education-cases-last-2-weeks.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Manitoba school divisions: [mb/school-divisions/school-divisions.json](http://data.opencovid.ca/archive/index.html#archive/)
* [Province of Manitoba - COVID-19](https://www.gov.mb.ca/covid19/updates/index.html)
    * Webpage: [mb/manitoba-webpage/manitoba-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Manitoba COVID-19](https://experience.arcgis.com/experience/f55693e56018406ebbd08b3492e99771)
    * COVID-19 data by RHA and district: [mb/covid-data-by-rha-and-district/covid-data-by-rha-and-district.json](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 data by RHA and district (JSON to CSV): [mb/covid-data-by-rha-and-district-csv/covid-data-by-rha-and-district.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by demographics and RHA: [mb/cases-demographics-by-rha/cases-demographics-by-rha.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by demographics and RHA (JSON to CSV): [mb/cases-demographics-by-rha-csv/cases-demographics-by-rha.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by status and RHA: [mb/cases-by-status-and-rha/cases-by-status-and-rha.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by status and RHA (JSON to CSV): [mb/cases-by-status-and-rha-csv/cases-by-status-and-rha.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Manitoba five-day test positivity rate: [mb/five-day-test-positivity/five-day-test-positivity.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Manitoba five-day test positivity rate (JSON to CSV): [mb/five-day-test-positivity-csv/five-day-test-positivity.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Summary statistics by area: [mb/summary-stats-by-area/summary-stats-by-area.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Current status by area: [mb/current-status-by-area/current-status-by-area.json](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Variant of Concern Cases in Manitoba](https://geoportal.gov.mb.ca/app/95badc9cb5c3408ca2eb562ab61af51b)
    * Dataset: [mb/cumulative-variants-by-rha/mb_covid_variants.json](http://data.opencovid.ca/archive/index.html#archive/)
* [Manitoba COVID-19 Vaccinations](https://www.gov.mb.ca/covid19/vaccine/reports.html)
    * Vaccination coverage by Regional Health Authority: [mb/vaccination-coverage-by-rha/mb_covid_vaccinations_18_coverage.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination time series: [mb/vaccination-time-series/mb_covid_vaccinations_daily_cumulative.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination by age group and sex: [mb/vaccination-by-age-sex/mb_covid_vaccinations_demographics.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination by manufacturer: [mb/vaccination-by-manufacturer/mb_covid_vaccinations_manufacturers.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Projected vaccine doses: [mb/projected-vaccine-doses/mb_covid_vaccinations_projected_doses.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination summary by Regional Health Authority: [mb/vaccination-summary-by-rha/mb_covid_vaccinations_summary_stats.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage: [mb/vaccination-coverage/mb_covid_vaccinations_coverage.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Uptake by RHA, age, sex: [mb/vaccine-uptake-by-rha-age-sex/mb_covid_vaccine_uptake_demographics.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Uptake by Health District: [mb/vaccine-uptake-by-district/mb_covid_vaccine_uptake_district.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Inventory, delivered, administered, scheduled: [mb/vaccination-inventory-delivered-admin-scheduled/mb_covid_vaccinations_inventory_stats.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Regional Health Authorities: [mb/regional-health-authorities/Manitoba_Regional_Health_Authorities.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Health Districts: [mb/health-districts/Health_Districts.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Winnipeg Community Areas: [mb/winnipeg-community-areas/bdy_wha_community_areas_py_shp.json](http://data.opencovid.ca/archive/index.html#archive/)
    * First Nations vaccination time series: [mb/first-nations-vaccination-time-series/mbfn_covid_vaccinations_daily_cumulative.json](http://data.opencovid.ca/archive/index.html#archive/)
    * First Nations vaccination by age group and sex: [mb/first-nations-vaccination-by-age-sex/mbfn_covid_vaccinations_demographics.json](http://data.opencovid.ca/archive/index.html#archive/)
    * First Nations vaccination by provider: [mb/first-nations-vaccination-by-provider/mbfn_covid_vaccinations_provider_summary.json](http://data.opencovid.ca/archive/index.html#archive/)
    * First Nations vaccination by Regional Health Authority: [mb/first-nations-vaccination-by-rha/mbfn_covid_vaccinations_rha_summary.json](http://data.opencovid.ca/archive/index.html#archive/)
    * First Nations vaccination summary on reserve and off reserve: [mb/first-nations-vaccination-summary-on-reserve-off-reserve/mbfn_covid_vaccinations_summary_statistics.json](http://data.opencovid.ca/archive/index.html#archive/)
    * First nations vaccination by Tribal Council Region: [mb/first-nations-vaccination-by-tribal-council-region/mbfn_covid_vaccinations_tribal_council_summary.json](http://data.opencovid.ca/archive/index.html#archive/)
#### Winnipeg

* [COVID-19 By-law Enforcement](https://data.winnipeg.ca/Neighbourhood-Liveability-Property-Standards-Licen/COVID-19-By-law-Enforcement/ndr6-96vi)
    * Dataset: [mb/winnipeg-by-law-enforcement/COVID-19_By-law_Enforcement.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Designated Active Transportation Route Counts](https://data.winnipeg.ca/Transportation-Planning-Traffic-Management/COVID-19-Designated-Active-Transportation-Route-Co/aqka-nz2g)
    * Dataset: [mb/winnipeg-active-transportation/COVID-19_Designated_Active_Transportation_Route_Counts.csv](http://data.opencovid.ca/archive/index.html#archive/)

### New Brunswick

* [Potential Public Exposures](https://www2.gnb.ca/content/gnb/en/corporate/promo/covid-19/potential_public_exposure.html)
    * Webpage: [nb/potential-public-exposures-webpage/potential-public-exposures-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [New Brunswick COVID-19 Dashboard](https://experience.arcgis.com/experience/8eeb9a2052d641c996dba5de8f25a8aa)
    * Adult residential facilities: [nb/adult-residential-facilities/adult-residential-facilities.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Airports: [nb/airports/airports.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Counties: [nb/counties/counties.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Assessment sites: [nb/covid-assessment-sites/covid-assessment-sites.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Compliance by health zone: [nb/covid-compliance-by-health-zone/covid-compliance-by-health-zone.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Provincial case, death, recovered time series: [nb/provincial-case-death-recovered-time-series/provincial-case-death-recovered-time-series.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Provincial cumulative test statistics by age and sex: [nb/provincial-cumulative-test-statistics-by-age-sex/provincial-cumulative-test-statistics-by-age-sex.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine data: [nb/vaccine-data/vaccine-data.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine coverage by age groups: [nb/vaccine-coverage-by-age/Covid19VaccineAge.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine time series: [nb/vaccine-time-series/Covid19VaccineTimeline.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Ferries: [nb/ferries/ferries.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Health zone cumulative stats: [nb/health-zone-cumulative-stats/health-zone-cumulative-stats.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Hospitals: [nb/hospitals/hospitals.json](http://data.opencovid.ca/archive/index.html#archive/)
    * International border: [nb/international-border/international-border.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Communities: [nb/communities/communities.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Neighbour region cumulative stats: [nb/neighbour-regions-cumulative-stats/neighbour-regions-cumulative-stats.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Neighbour state/province cumulative stats: [nb/neighbour-state-prov-cumulative-stats/neighbour-state-prov-cumulative-stats.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Nursing homes: [nb/nursing-homes/nursing-homes.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Health zone and community recovery phases: [nb/health-zone-community-recovery-phases/health-zone-community-recovery-phases.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Traffic control points: [nb/traffic-control-points/traffic-control-points.json](http://data.opencovid.ca/archive/index.html#archive/)

### Newfoundland and Labrador

* [Newfoundland and Labrador COVID-19 Pandemic Update Hub](https://covid-19-newfoundland-and-labrador-gnl.hub.arcgis.com/)
    * Webpage: [nl/nl-pandemic-hub-webpage/nl-pandemic-hub-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Province summary: [nl/nl-summary/ProvCovidDailyStats.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Province time series: [nl/nl-summary-time-series/Prov_Covid_Daily_Stats_v2_Public_View.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Regional Health Authority summary: [nl/rha-summary/RHA_CurrentStats2_Public2.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cumulative cases by Primary Health Care Zone: [nl/cumulative-cases-by-phcz/PHZ_Zone_Public.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by likely exposure setting: [nl/cases-by-likely-exposure-setting/Exposure_New_Public.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by age and sex: [nl/cases-by-age-and-sex/Covid_AgeLayerPublic2.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cumulative vaccination (3): [nl/cumulative-vaccination-3/DailyVaccineUpdatePublic.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine doses received and expected this week: [nl/vaccine-doses-received-and-expected/WeeklyDoses_Public.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cumulative vaccination: [nl/cumulative-vaccination/Vaccine_LatestPublic_v2.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Cumulative vaccination (2): [nl/cumulative-vaccination-2/DailyVaccination_Public.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Primary Health Care Zone populations: [nl/phcz-populations/PHC_Zones_Combined_Public.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]

### Northwest Territories

* [Northwest Territories COVID-19 dashboard](https://nwt-covid.shinyapps.io/Testing-and-Cases/?lang=1)
    * Cases webpage: [nt/nwt-dashboard-cases-webpage/nwt-dashboard-cases-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [GNWT's Response to COVID-19](https://www.gov.nt.ca/covid-19/)
    * Webpage: [nt/nwt-webpage/nwt-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)

### Nova Scotia

* [Coronavirus (COVID-19): case data](https://novascotia.ca/coronavirus/data/)
    * Webpage: [ns/ns-webpage/ns-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Case data: [ns/case-data/ns-covid19-data.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Nova Scotia COVID-19 Dashboard](https://experience.arcgis.com/experience/204d6ed723244dfbb763ca3f913c5cad)
    * Cases by zone: [ns/cases-by-zone/cases-by-zone.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Zone summary: [ns/zone-summary/zone-summary.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Zone summary cases: [ns/zone-summary-cases/zone-summary-cases.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Community health network summary cases: [ns/chn-summary-cases/chn-summary-cases.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Serious outcomes: [ns/serious-outcomes/serious-outcomes.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Lab testing: [ns/lab-testing/lab-testing.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Lab testing, hospitalization, ICU summary: [ns/lab-testing-hos-icu-summary/lab-testing-hos-icu-summary.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Demographics summary: [ns/demographics-summary/demographics-summary.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Health boundaries: [ns/health-boundaries/health-boundaries.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Immunizations (3): [ns/immunizations-3/Immunizations_V4_PROD.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Immunizations: [ns/immunizations/immunizations.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Immunizations (2): [ns/immunizations-2/Immunizations_3_PROD.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Potential COVID Exposures](http://www.nshealth.ca/covid-exposures)
    * Webpage: [ns/ns-potential-covid-exposures-webpage/ns-potential-covid-exposures-webpage.json](http://data.opencovid.ca/archive/index.html#archive/)

### Nunavut

* [COVID-19 (Novel Coronavirus)](https://gov.nu.ca/health/information/covid-19-novel-coronavirus)
    * Webpage: [nu/nunavut-webpage/nunavut-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Vaccination](https://www.gov.nu.ca/health/information/covid-19-vaccination)
    * Webpage: [nu/nunavut-vaccination-webpage/nunavut-vaccination-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Table (image): [nu/nunavut-vaccination-table/vaccine_table.jpg](http://data.opencovid.ca/archive/index.html#archive/)

### Ontario

* [Schools COVID-19 data](https://data.ontario.ca/dataset/summary-of-cases-in-schools)
    * Summary of cases in schools: [on/schools-summary/schoolcovidsummary.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Schools with active COVID-19 cases: [on/schools-active/schoolsactivecovid.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases in school board partners: [on/school-board-partners/schoolpartnersactivecovid.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Long-Term Care Home COVID-19 Data](https://data.ontario.ca/dataset/long-term-care-home-covid-19-data)
    * Summary data: [on/long-term-care-home-summary/ltccovidsummary.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Active outbreaks: [on/long-term-care-home-active/activeltcoutbreak.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Resolved outbreaks: [on/long-term-care-home-resolved/resolvedltc.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Licensed child care settings COVID-19 data](https://data.ontario.ca/dataset/summary-of-cases-in-licensed-child-care-settings)
    * Summary of cases in licensed child care settings: [on/licensed-child-care-settings-summary/lccovidsummary.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Licensed child care centres and agencies with active COVID-19 cases: [on/licensed-child-care-settings-active/lccactivecovid.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Confirmed positive cases of COVID19 in Ontario](https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario/resource/455fd63b-603d-4608-8216-7d8647f43350)
    * Dataset: [on/confirmed-positive-cases/conposcovidloc.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [How Ontario is responding to COVID-19](https://www.ontario.ca/page/how-ontario-is-responding-covid-19)
    * Webpage: [on/ontario-webpage/ontario-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Effective reproduction number (Re) for COVID-19 in Ontario](https://data.ontario.ca/dataset/effective-reproduction-number-re-for-covid-19-in-ontario)
    * Dataset: [on/effective-reproduction-number/effective_reproduction_number_ontario.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Ontario COVID-19 testing metrics by Public Health Unit (PHU)](https://data.ontario.ca/dataset/ontario-covid-19-testing-metrics-by-public-health-unit-phu)
    * Dataset: [on/testing-metrics-by-phu/testing_metrics_by_phu.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Ontario COVID-19 testing percent positive by age group](https://data.ontario.ca/dataset/ontario-covid-19-testing-percent-positive-by-age-group)
    * Dataset: [on/percent-positive-by-age-group/percent_positive_by_agegrp.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID Alert Impact Data](https://data.ontario.ca/dataset/covid-alert-impact-data)
    * COVID Alert downloads - Canada: [on/covid_alert_downloads_canada/covid_alert_downloads_canada.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Uploads of COVID-19 diagnosis to COVID Alert - Ontario: [on/covid-alert-uploads-ontario/covid_alert_positive_uploads_ontario.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 testing of inmates in Ontario’s Provincial Correctional Institutions](https://data.ontario.ca/dataset/covid-19-testing-of-inmates-in-ontario-s-correctional-institutions)
    * Dataset: [on/correctional-institutions-inmates-testing/inmatetesting.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Status of COVID-19 cases in Ontario’s Provincial Correctional Institutions](https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario-s-correctional-institutions)
    * Dataset: [on/correctional-institutions-status/correctionsinmatecases.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 pharmacy vaccine locations](https://covid-19.ontario.ca/vaccine-locations/)
    * Webpage: [on/vaccine-pharmacy-locations-webpage/vaccine-pharmacy-locations-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 hospital metrics in Ontario by Local Health Integration Network (LHIN) regions](https://data.ontario.ca/dataset/covid-19-hospital-metrics-in-ontario-by-local-health-integration-network-lhin-regions)
    * Dataset: [on/hosp-icu-by-lhin/lhin_hospital_icu_covid_data.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Status of COVID-19 cases in Ontario by Public Health Unit (PHU)](https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario-by-public-health-unit-phu)
    * Dataset: [on/status-of-cases-by-phu/cases_by_status_and_phu.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 cases in schools and child care centres](https://www.ontario.ca/page/covid-19-cases-schools-and-child-care-centres)
    * Webpage: [on/cases-schools-and-child-care-centres-webpage/cases-schools-and-child-care-centres-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [All Ontario: Case numbers and spread](https://covid-19.ontario.ca/data)
    * Webpage: [on/on-data-webpage/on-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [ICES COVID-19 Dashboard](https://www.ices.on.ca/DAS/AHRQ/COVID-19-Dashboard)
    * Percent positivity by FSA: [on/ices-percent-positivity-by-fsa/ICES-COVID19-Testing-Data-FSA-percent-positivity.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Percent positivity by age group and Public Health Unit (PHU): [on/ices-percent-positivity-by-age-group-and-phu/ICES-COVID19-Testing-Data_PHUxAge-Groups-percent-positivity.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine coverage estimates for selected age groups by FSA: [on/ices-vaccine-coverage-by-age-group-and-fsa/ICES-COVID19-Vaccination-Data-by-FSA.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Vaccine Data in Ontario](https://data.ontario.ca/dataset/covid-19-vaccine-data-in-ontario)
    * Vaccine Data in Ontario: [on/vaccine-data/vaccine_doses.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine Data by Age: [on/vaccine-data-by-age/vaccines_by_age.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Ontario COVID-19 outbreaks data](https://data.ontario.ca/dataset/ontario-covid-19-outbreaks-data)
    * Ongoing outbreaks: [on/ongoing-outbreaks/ongoing_outbreaks.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Summary of cases associated with outbreaks: [on/summary-outbreak-cases/outbreak_cases.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Status of COVID-19 cases in Ontario](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11)
    * Dataset: [on/status-of-cases/covidtesting.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 testing locations](https://data.ontario.ca/dataset/covid-19-assessment-centre-locations)
    * Dataset: [on/testing-locations/locations.json](http://data.opencovid.ca/archive/index.html#archive/)
#### Ottawa

* [Daily COVID-19 Dashboard](https://www.ottawapublichealth.ca/en/reports-research-and-statistics/daily-covid19-dashboard.aspx)
    * Demographics and Source of Infection for Cases, Deaths, and Hospitalizations: [on/ottawa-cases-deaths-hosp-demographics-source-of-infection/COVID-19_Cases_and_Deaths_Ottawa_EN.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Outbreaks in Healthcare Institutions, Childcare, Summer Camps, and Educational Establishments: [on/ottawa-outbreaks-healthcare-childcare-camps-schools/COVID-19_Institutional_Outbreaks.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Community Outbreaks: [on/ottawa-community-outbreaks/COVID-19_Community_Outbreaks_in_Ottawa.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Ottawa Community Outbreaks (JSON): [on/ottawa-community-outbreaks-json/COVID-19_Community_Outbreaks_in_Ottawa.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Ottawa Weekly Rates: [on/ottawa-weekly-rates/COVID-19_Weekly_Cases_and_Rates_by_Age_in_Ottawa_EN.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Estimated Reproduction Number in Ottawa: [on/ottawa-estimated-rt/EN_-_Covid-19_Reproduction_Number,_R(t).csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Ottawa Residents: [on/ottawa-residents-tested/COVID-19_Ottawa_Residents_Tested_EN.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Data tables for Public COVID-19 Maps: [on/ottawa-wards-cases-cumulative/COVID19_MapPublic_DataTables_EN.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases and deaths: [on/ottawa-cases-and-deaths/COVID-19_Cases_and_Deaths_in_Ottawa_EN.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Outbreaks in healthcare institutions: [on/ottawa-outbreaks-in-healthcare-institutions/COVID-19_Outbreaks_in_Ottawa_Healthcare_Institutions_EN.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Hospitalization data: [on/ottawa-hospitalization/Hospitalizations_of_Ottawa_residents_with_confirmed_COVID-19.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [COVID-19 Vaccination Dashboard](https://www.ottawapublichealth.ca/en/reports-research-and-statistics/COVID-19_Vaccination_Dashboard.aspx)
    * Vaccinations by Day by Vaccine Type - Ottawa Residents: [on/ottawa-vaccinations-by-day-and-type-ottawa-residents/ottawa-vaccinations-by-day-and-type-ottawa-residents.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccinations by Day by Vaccine Type - Vaccinated in Ottawa: [on/ottawa-vaccinations-by-day-and-type-vaccinated-in-ottawa/ottawa-vaccinations-by-day-and-type-vaccinated-in-ottawa.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine Doses Received by Date - Ottawa Less Pharmacies: [on/ottawa-vaccine-doses-received-dy-date-ottawa-less-pharmacies/ottawa-vaccine-doses-received-dy-date-ottawa-less-pharmacies.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccinations by Day by Vaccine Type - Non-Residents Vaccinated in Ottawa: [on/ottawa-vaccinations-by-day-and-type-non-residents-vaccinated-in-Ottawa/.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccinations by Day by Vaccine Type - Residents of Ottawa Vaccinated Outside of Ottawa: [on/ottawa-vaccinations-by-day-and-type-ottawa-residents-vaccinated-outside-ottawa/ottawa-vaccinations-by-day-and-type-ottawa-residents-vaccinated-outside-ottawa.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination Coverage by Age for Ottawa Residents with at Least 1 Dose: [on/ottawa-vaccination-coverage-by-age-ottawa-residents/ottawa-vaccination-coverage-by-age-ottawa-residents.json](http://data.opencovid.ca/archive/index.html#archive/)
#### Toronto

* [University of Toronto COVID-19 tracking](https://www.utoronto.ca/utogether/covid19-dashboard)
    * Webpage: [on/u-of-t-covid-tracking-webpage/u-of-t-covid-tracking-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Cases in Toronto](https://open.toronto.ca/dataset/covid-19-cases-in-toronto/)
    * Dataset: [on/toronto-cases/COVID19_cases.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19: Epidemiological Summary of Cases](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-pandemic-data/covid-19-epidemiological-summary-of-cases-data/)
    * Dataset: [on/toronto-covid-summary/CityofToronto_COVID-19_Data.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19: Neighbourhood Maps](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-pandemic-data/covid-19-neighbourhood-maps-data/)
    * Case Data: [on/toronto-neighbourhood-data/CityofToronto_COVID-19_NeighbourhoodData.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Testing Data: [on/toronto-neighbourhood-test-data/CityofToronto_COVID-19_Testing.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19: Active Outbreaks](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-pandemic-data/covid-19-active-outbreaks-data/)
    * Dataset: [on/toronto-active-outbreaks/CityofToronto_COVID-19_OutbreakData.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19: Case Counts](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-pandemic-data/covid-19-weekday-status-of-cases-data/)
    * Dataset: [on/toronto-daily-status/CityofToronto_COVID-19_Daily_Public_Reporting.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID 19: Ethno-Racial Identity & Income](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-pandemic-data/covid-19-ethno-racial-group-income-infection-data/)
    * Dataset: [on/toronto-ethno-racial-income/Ethno-Racial_Group,_Income,_and_COVID-19_Infection.xlsx](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [COVID-19: Monitoring Dashboard](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-pandemic-data/covid-19-monitoring-dashboard-data/)
    * Dataset: [on/toronto-monitoring-dashboard/CityofToronto_COVID-19_RecoveryData.xlsx](http://data.opencovid.ca/archive/index.html#archive/)

### Prince Edward Island

* [Potential COVID-19 Exposures](https://www.princeedwardisland.ca/en/information/health-and-wellness/potential-covid-19-exposures)
    * Webpage: [pe/pei-potential-exposures-webpage/pei-potential-exposures-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [PEI COVID-19 Case Data](https://www.princeedwardisland.ca/en/information/health-and-wellness/pei-covid-19-case-data)
    * Webpage: [pe/pei-webpage/pei-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Possible Air Travel Exposures](https://www.princeedwardisland.ca/en/information/health-and-wellness/possible-air-travel-exposures)
    * Webpage: [pe/pei-possible-air-travel-exposures-webpage/pei-possible-air-travel-exposures-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Vaccination Data](https://www.princeedwardisland.ca/en/information/health-and-wellness/covid-19-vaccination-data)
    * Webpage: [pe/pei-vaccination-webpage/pei-vaccination-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Dataset: [pe/vaccine-data-cumulative/Vaccine_Rollout.xlsx](http://data.opencovid.ca/archive/index.html#archive/)

### Quebec

* []()
    * Highlights - public and private school system (FR): [qc/schools-highlights/reseauScolaire_faitsSaillants.pdf](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Highlights - public and private school system (EN): [qc/schools-highlights-en/reseauScolaire_faitsSaillants_ANG.pdf](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Variants de SRAS-CoV-2 sous surveillance rehaussée](https://inspq.qc.ca/covid-19/donnees/variants)
    * Variants under enhanced surveillance: [qc/variants/variants.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Variant screening time series by RSS: [qc/variant-screening-time-series-by-rss/variants-criblage.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Variant screening time series by RSS (expanded): [qc/variant-screening-time-series-by-rss-expanded/variants-criblage-sem.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Variant Rt time series: [qc/variants-rt-time-series/variants-rt.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Projection of variant dominance: [qc/variants-dominance-projection/variants-proj.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Données de vaccination contre la COVID-19 au Québec](https://www.inspq.qc.ca/covid-19/donnees/vaccination)
    * Webpage: [qc/inspq-data-webpage/inspq-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination by RSS time series: [qc/vaccination-by-rss-time-series/vaccination.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cumulative vaccination adverse events by vaccine type: [qc/cumulative-vaccination-adverse-events-by-vaccine-type/vaccination-mci.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Portrait quotidien des hospitalisations](https://www.donneesquebec.ca/recherche/dataset/covid-19-portrait-quotidien-des-hospitalisations)
    * Daily hospitalizations by RSS and care unit: [qc/daily-hosp-by-rss-and-care-unit/COVID19_Qc_HistoHospit.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Daily hospitalizations by age group: [qc/daily-hosp-by-age-group/COVID19_Qc_HospitCatAge.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Liste des écoles comptant des cas de COVID-19](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/liste-des-cas-de-covid-19-dans-les-ecoles/)
    * Webpage (FR): [qc/schools-list-of-schools-webpage/schools-list-of-schools-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage (EN): [qc/schools-list-of-schools-webpage-en/schools-list-of-schools-webpage-en.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Dataset (CSV): [qc/schools-list-of-schools-csv/Liste_ecole_DCOM.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Report (PDF FR): [qc/schools-list-of-schools/reseauScolaire_listeEcoles.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Report (PDF EN): [qc/schools-list-of-schools-en/reseauScolaire_listeEcoles_ANG.pdf](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 - Portrait quotidien des cas confirmés ](https://www.donneesquebec.ca/recherche/dataset/covid-19-portrait-quotidien-des-cas-confirmes)
    * Cumulative time series of confirmed cases and deaths: [qc/cumulative-confirmed-cases-deaths-time-series/COVID19_Qc_RapportINSPQ_HistoVigie.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cumulative snapshot of confirmed cases and deaths by region, age group and sex: [qc/cumulative-confirmed-cases-deaths-by-region-age-sex/COVID19_Qc_RapportINSPQ_VigieCategories.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 - Portrait quotidien de la vaccination](https://www.donneesquebec.ca/recherche/dataset/covid-19-portrait-quotidien-de-la-vaccination)
    * Doses administered by region of administration: [qc/vaccine-doses-admin-by-rss-time-series/COVID19_Qc_Vaccination_RegionAdministration.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Doses administered by region of residence: [qc/vaccine-doses-admin-by-rss-of-residence-time-series/COVID19_Qc_Vaccination_RegionResidence.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Doses administered by age group: [qc/vaccine-doses-admin-by-age-group-time-series/COVID19_Qc_Vaccination_CatAge.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Upcoming first dose appointments by region of administration: [qc/first-vaccine-dose-appointments-by-rss/COVID19_Qc_RDVVaccination_RegionAdministration.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Upcoming 1st dose appointments by age group: [qc/first-vaccine-dose-appointments-by-age-group/COVID19_Qc_RDVVaccination_CatAge.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 vaccination data](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/covid-19-vaccination-data/)
    * Webpage (FR): [qc/qc-vaccination-webpage-fr/qc-vaccination-webpage-fr.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage (EN): [qc/qc-vaccination-webpage-en/qc-vaccination-webpage-en.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination situation (FR): [qc/vaccination-situation/situation-vaccination.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine doses received (FR): [qc/vaccine-doses-received-7-days/doses-vaccins-7jours.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination situation (EN): [qc/vaccination-situation-en/situation-vaccination-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccine doses administered by RSS (FR): [qc/vaccine-doses-admin-by-rss/doses-vaccins.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccine doses administered by RSS (EN): [qc/vaccine-doses-admin-by-rss-en/doses-vaccins-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccination by age group: [qc/vaccination-by-age-group/tableau-suivi-vaccination-groupe-age.jpg](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Éclosions de COVID-19 au Québec](https://www.inspq.qc.ca/covid-19/donnees/eclosions)
    * Dataset: [qc/active-outbreaks-time-series-by-setting/eclosions.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Données COVID-19 au Québec (INSPQ)](https://www.inspq.qc.ca/covid-19/donnees)
    * Time series by region and demographics: [qc/covid-time-series-by-region-and-demographics/covid19-hist.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Charts - summary, time series, and hospitalization by age: [qc/covid-data-charts-summary-time-series-hosp-by-age/manual-data.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Summary by region: [qc/summary-by-region/regions.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Deaths by RSS (health region) and living environment: [qc/deaths-by-rss-and-living-environment/tableau-rpa-new.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by RSS (health region) and RLS (local service network): [qc/cases-by-rss-and-rls/tableau-rls-new.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Comparisons (provinces): [qc/comparisons-provinces/comparaisons_prov.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Comparisons (countries): [qc/comparisons-countries/comparaisons_pays.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Deaths by RSS (health region) and number of pre-existing conditions: [qc/deaths-by-rss-and-pre-existing-conditions/comorbidite.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Time series by region: [qc/covid-time-series-by-region/PL_DATE.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Data (original): [qc/covid-data/combine.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Charts (original): [qc/covid-data-charts/combine2.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Données COVID-19 par âge et sexe au Québec](https://www.inspq.qc.ca/covid-19/donnees/age-sexe)
    * Dataset: [qc/covid-data-by-age-and-sex/PL_AGE_SEXE.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Faits saillants des cas de COVID-19 dans les écoles du Québec](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/faits-saillants-covid-ecoles/)
    * Webpage (FR): [qc/schools-highlights-webpage/schools-highlights-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage (EN): [qc/schools-highlights-webpage-en/schools-highlights-webpage-en.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Données sur la COVID-19 au Québec (province)](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    * Webpage (FR): [qc/qc-webpage-fr/qc-webpage-fr.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage (EN): [qc/qc-webpage-en/qc-webpage-en.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard (image): [qc/qc-covid-dashboard/20-210-382W_infographie_sommaire-executif.jpg](http://data.opencovid.ca/archive/index.html#archive/)
    * Situation in Quebec: [qc/situation-in-quebec/situation-au-quebec.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Correctional facilities - cases among employees (FR): [qc/correctional-cases-employees/donnees_covid_detention_employes_FR.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Correctional facilities - cases among employees (EN): [qc/correctional-cases-employees-en/donnees_covid_detention_employes_EN.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Correctional facilities - cases among detainees (FR): [qc/correctional-cases-detainees/donnees_covid_detention_personnes_incarcerees_FR.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Correctional facilities - cases among detainees (EN): [qc/correctional-cases-detainees-en/donnees_covid_detention_personnes_incarcerees_EN.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Outbreaks by setting (FR): [qc/outbreaks-by-setting/eclosions-par-milieu.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases percentage by age group (FR): [qc/cases-percentage-by-age-group/pourcentage-cas-age.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Deaths percentage by age group (FR): [qc/deaths-percentage-by-age-group/pourcentage-deces-age.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cumulative deaths by region (FR): [qc/cumulative-deaths-by-region/deces-region.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Recent daily cases by region (FR): [qc/recent-daily-cases-by-region/cas-region.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 daily data 7 days (FR): [qc/covid-data-daily-7-days/synthese-7jours.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by region 7 days (FR): [qc/cases-by-region-7-days/cas-region-7jours.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by region 7 days (EN): [qc/cases-by-region-7-days-en/cas-region-7jours-en.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Deaths time series by living environment: [qc/deaths-time-series-by-living-environment/decesquotidien.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Status report on confirmed cases and deaths by RPA: [qc/status-report-cases-and-deaths-by-rpa/etat_situation_rpa.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Status report on confirmed cases and deaths by CHSLD: [qc/status-report-cases-and-deaths-by-chsld/etat_situation_chsld.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Active hospitalizations per hospital: [qc/active-hospitalizations-per-hosp/tableau-hospitalisations.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Outbreaks by setting (EN): [qc/outbreaks-by-setting-en/eclosions-par-milieu-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * COVID-19 daily data 7 days (EN): [qc/covid-data-daily-7-days-en/synthese-7jours-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Cumulative deaths by region (EN): [qc/cumulative-deaths-by-region-en/deces-region-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Cases percentage by age group (EN): [qc/cases-percentage-by-age-group-en/pourcentage-cas-age-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Deaths percentage by age group (EN): [qc/deaths-percentage-by-age-group-en/pourcentage-deces-age-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Recent daily cases by region (EN): [qc/recent-daily-cases-by-region-en/cas-region-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccination of priority groups (FR): [qc/vaccination-of-priority-groups/20-279-07WF_Previsions_vaccination.pdf](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccination of priority groups (EN): [qc/vaccination-of-priority-groups-en/20-279-07WA_Previsions_vaccination-anglais.pdf](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
#### Montreal

* [Situation du coronavirus (COVID-19) à Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/situation-du-coronavirus-covid-19-a-montreal/)
    * Montréal cases and deaths by CIUSSS: [qc/montreal-cases-and-deaths-by-ciusss/ciusss.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Montréal cases by area: [qc/montreal-cases-by-area/municipal.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Montréal cases and deaths by age group: [qc/montreal-cases-and-deaths-by-age-group/grage.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Montréal cases and deaths by sex: [qc/montreal-cases-and-deaths-by-sex/sexe.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Montréal epidemic curve: [qc/montreal-epidemic-curve/courbe.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Données sur la vaccination COVID-19 à Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/vaccination/donnees/)
    * Vaccine coverage by neighbourhood: [qc/montreal-vaccine-coverage-by-neighbourhood/VAXarrondissementsMTL.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine coverage by age group: [qc/montreal-vaccine-coverage-by-age-group/VAXparGrpAGE_CSVupload.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine administration time series (2): [qc/montreal-vaccine-administration-time-series-v2/VAXparJOUR_CSVuploadv2.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine administration time series: [qc/montreal-vaccine-administration-time-series/VAXparJOUR_googledrive.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Neighbourhoods: [qc/montreal-vaccine-dashboard-neighbourhoods/Arrondissements_et_municipalites.json](http://data.opencovid.ca/archive/index.html#archive/)

### Saskatchewan

* [Saskatchewan's Dashboard - Hospitalized Cases](https://dashboard.saskatchewan.ca/health-wellness/covid-19-cases/hospitalized)
    * Dataset: [sk/hosp-icu-by-region/hospitalized.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage: [sk/hosp-icu-by-region-webpage/hospitalized-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables: [sk/hosp-icu-by-region-highlights-charts-tables/health-wellness-covid-19-cases-hospitalized.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables (legacy): [sk/hosp-icu-by-region-highlights-charts-tables-legacy/health-wellness-covid-19-cases-hospitalized.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Saskatchewan's Dashboard - Total Cases](https://dashboard.saskatchewan.ca/health-wellness/covid-19/cases)
    * Dataset: [sk/cases-by-region/cases.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage: [sk/cases-by-region-webpage/cases-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables: [sk/cases-by-region-highlights-charts-tables/health-wellness-covid-19-cases.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables (legacy): [sk/cases-by-region-highlights-charts-tables-legacy/health-wellness-covid-19-cases.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Saskatchewan's Dashboard - Total Tests](https://dashboard.saskatchewan.ca/health-wellness/covid-19-tests/tests)
    * Dataset: [sk/tests-by-region/tests.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage: [sk/tests-by-region-webpage/tests-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables: [sk/tests-by-region-highlights-charts-tables/health-wellness-covid-19-tests-tests.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables (legacy): [sk/tests-by-region-highlights-charts-tables-legacy/health-wellness-covid-19-tests-tests.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Saskatchewan's Dashboard - Total Doses](https://dashboard.saskatchewan.ca/health-wellness/covid-19-vaccines/vaccines)
    * Dataset: [sk/vaccination-by-region/vaccines.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage: [sk/vaccine-delivery-webpage/vaccine-delivery-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables: [sk/vaccination-by-region-highlights-charts-tables/health-wellness-covid-19-vaccines-vaccines.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables (legacy): [sk/vaccination-by-region-highlights-charts-tables-legacy/health-wellness-covid-19-vaccines-vaccines.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Saskatchewan's Dashboard - Seven-day Average of Daily New Cases](https://dashboard.saskatchewan.ca/health-wellness/covid-19/seven-day-average-of-new-covid-cases)
    * Dataset: [sk/seven-day-avg-cases-by-region/seven-day-average-of-new-covid-cases.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage: [sk/seven-day-avg-cases-by-region-webpage/seven-day-average-of-new-covid-cases-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables: [sk/seven-day-avg-cases-by-region-highlights-charts-tables/health-wellness-covid-19-seven-day-average-of-new-covid-cases.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables (legacy): [sk/seven-day-avg-cases-by-region-highlights-charts-tables-legacy/health-wellness-covid-19-seven-day-average-of-new-covid-cases.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Cases and Risk of COVID-19 in Saskatchewan](https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/cases-and-risk-of-covid-19-in-saskatchewan)
    * Webpage: [sk/summary-and-variant-webpage/summary-and-variant-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)

### Yukon

* [Current COVID-19 situation](https://yukon.ca/en/health-and-wellness/covid-19-information/latest-updates-covid-19/current-covid-19-situation)
    * Webpage: [yt/yukon-current-situation-webpage/yukon-current-situation-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Case and vaccine counts: COVID-19](https://yukon.ca/en/case-counts-covid-19)
    * Webpage: [yt/yukon-case-counts-webpage/yukon-case-counts-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Vaccine tracker](https://yukon.ca/this-is-our-shot)
    * Webpage: [yt/yukon-vaccine-tracker-webpage/yukon-vaccine-tracker-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)

### Other: Non-governmental sources

#### Canada

* [Unofficial COVID Alert Dashboard](https://github.com/uhengart/covid-alert-dashboard)
    * Diagnosis Keys Analysis: [other/can/unofficial-covid-alert-dashboard-analysis/DiagnosisKeysAnalysis.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Upload Delay: [other/can/unofficial-covid-alert-dashboard-upload-delay/UploadDelay.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 - Loblaw Companies Ltd.](https://www.loblaw.ca/en/covid-19/)
    * Webpage: [other/can/loblaw-companies-tracker/loblaw-companies-tracker.html](http://data.opencovid.ca/archive/index.html#archive/)
* [CTV: Tracking variants of the novel coronavirus in Canada](https://www.ctvnews.ca/health/coronavirus/tracking-variants-of-the-novel-coronavirus-in-canada-1.5296141)
    * Webpage: [other/can/ctv-variant-tracker-webpage/ctv-variant-tracker-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Dataset: [other/can/ctv-variant-tracker/COVID-Variants.txt](http://data.opencovid.ca/archive/index.html#archive/)
* [Canada COVID-19 School Case Tracker](https://masks4canada.org/canada-covid-19-school-case-tracker/)
    * Dataset: [other/can/canada-covid-19-school-case-tracker/Canada_COVID-19_School_Report_Tracker.kml](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [COVID-19 - McDonald's Tracker](https://news.mcdonalds.ca/covid-19-tracker)
    * Webpage: [other/can/mcdonalds-tracker/mcdonalds-tracker-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
#### Quebec

* [Covid Écoles Québec: Number of schools](https://www.covidecolesquebec.org/liste-alphabtique)
    * Dataset: [other/qc/covid-ecoles-quebec-school-list/COVIDECOLESQUEBEC.xlsx](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]



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
