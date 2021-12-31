# Canadian COVID-19 Data Archive

The purpose of this repository is to support automated, daily backups of COVID-19 data from Canadian governmental and non-governmental sources. It is composed of a list of datasets (`datasets.json`), as well as the Python code making up the archival tool itself. The Canadian COVID-19 Data Archive is one component of the **[What Happened? COVID-19 in Canada](https://whathappened.coronavirus.icu/)** project.

For information on how to access the datasets in the archive, see [Accessing the data](#accessing-the-data). For a list of available datasets, see the [Data catalogue](#data-catalogue) below.

The easiest way to [contribute to this project](#contributing) is to help add new data (by providing a link to the data or by uploading files you have previously downloaded) using our [data submission form](https://docs.google.com/forms/d/e/1FAIpQLSeiUd415u_qdqNwNHVEeA_6KCEMRJhXJSL9_9i1UvLDN3LGQA/viewform?usp=sf_link) or by opening an issue on GitHub. We're also looking for help making this archive more useful and accessible by building tools to simplify discovering, downloading and working with the data contained within.

File name timestamps are given in ET (America/Toronto) in the following format: %Y-%m-%d_%H-%M. Files are archived nightly beginning around 22:00 ET.

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
* [Notes about the data archive](#notes-about-the-data-archive)
* [Notes about the archival tool](#notes-about-the-archival-tool)
* [Acknowledgements](#acknowledgements)

## Accessing the data

The easiest way to explore the data in the archive and download individual files is with the interactive file explorer: [http://data.opencovid.ca/archive/index.html#archive/](http://data.opencovid.ca/archive/index.html#archive/).

The files in the archive are hosted under the following domain: [https://data.opencovid.ca.s3.amazonaws.com/archive/](https://data.opencovid.ca.s3.amazonaws.com/archive/). For example, the PHAC Epidemiology Update from November 4, 2020 may be downloaded at the following URL:

```
https://data.opencovid.ca.s3.amazonaws.com/archive/can/epidemiology-update-2/covid19-download_2020-11-04_23-38.csv
```

A complete index of files in the archive, including flags for duplicated files and corrected file dates (`file_data_true`), is available at the following URL:

```
https://data.opencovid.ca.s3.amazonaws.com/archive/file_index.csv
```

This index is refreshed nightly around 23:00 ET. The file index is a searchable spreadsheet containing the download links to all files in the archive. Any programming language can be used to easily download a list of files.

An experimental [JSON API](https://api.opencovid.ca/archive) is also available to search the file index, although it currently only supports filtering by UUID. For example, the following URL returns the index for the PHAC Epidemiology Update:

```
https://api.opencovid.ca/archive?uuid=f7db31d0-6504-4a55-86f7-608664517bdb
```

The API is not yet documented but will soon be added to [https://opencovid.ca/api/](https://opencovid.ca/api/).

Finally, the entire contents of the archive are accessible via the R package [`Covid19CanadaData`](https://github.com/ccodwg/Covid19CanadaData) using the function `dl_archive`, which interfaces with the API described above. Be aware that this package is undergoing rapid development and may change at any time.

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

## Data catalogue

A list of datasets available in the archive is given below, sorted by province (and city, if applicable). Supplementary data (e.g., codebooks, data dictionaries) are available for some datasets in `supplementary` subdirectories. Full details for each dataset, including any notes pertaining to them, are given in [`datasets.json`](https://github.com/ccodwg/Covid19CanadaArchive/blob/master/datasets.json).

A note about data from Quebec: when both French and English data files are available, French files should generally be considered definitive (and in many cases, these files have been captured in the archive for a longer duration). The English versions of files available in both languages have "-en" appended to their directory names.

<details>
<summary><b>Alberta</b></summary>

* [COVID-19 Alberta statistics](https://www.alberta.ca/stats/covid-19-alberta-statistics.htm)
    * Webpage: [ab/ab-covid-statistics-webpage/ab-covid-statistics-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Case data: [ab/cases/covid19dataexport.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Summary data time series: [ab/covid-summary-time-series/covid-19-alberta-statistics-summary-data.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Case time series (Local geographic area): [ab/case-time-series-by-lga/covid-19-alberta-statistics-map-data.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine data (Local geographic area): [ab/vaccine-coverage-by-lga/lga-coverage.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine data (Zone): [ab/vaccine-coverage-by-zone/zone-coverage.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [COVID-19 relaunch status map](https://www.alberta.ca/maps/covid-19-status-map.htm)
    * Active cases by region: [ab/active-cases-by-region/covid19dataexport-relaunch.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Cases in Alberta](https://www.alberta.ca/covid-19-alberta-data.aspx)
    * Webpage: [ab/ab-cases-webpage/ab-cases-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 info for Albertans](https://www.alberta.ca/coronavirus-info-for-albertans.aspx)
    * Webpage: [ab/ab-provincial-summary-webpage/ab-provincial-summary-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 vaccine distribution](https://www.alberta.ca/covid19-vaccine.aspx)
    * Webpage: [ab/ab-vaccine-distribution-webpage/ab-vaccine-distribution-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Alberta influenza statistics](https://www.alberta.ca/stats/influenza/influenza-statistics.htm)
    * Webpage: [ab/ab-influenza-stats-webpage/ab-influenza-stats-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 school status map](https://www.alberta.ca/schools/covid-19-school-status-map.htm)
    * School status map: [ab/school-status-by-region/covid19dataexport-schools.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]

<details>
<summary><i>Edmonton</i></summary>

* [COVID-19 in Alberta: Current cases by local geographic area (Edmonton)](https://data.edmonton.ca/Community-Services/COVID-19-in-Alberta-Current-cases-by-local-geograp/ix8f-s9xp)
    * Current cases by local geographic area: [ab/edmonton-cases-by-area/COVID-19_in_Alberta__Current_cases_by_local_geographic_area.csv](http://data.opencovid.ca/archive/index.html#archive/)
</details>
</details>
<details>
<summary><b>British Columbia</b></summary>

* [BC COVID-19 Data](http://www.bccdc.ca/health-info/diseases-conditions/covid-19/data)
    * Webpage: [bc/bc-covid-data-webpage/bc-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Case data: [bc/case-data/BCCDC_COVID19_Dashboard_Case_Details.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Laboratory data: [bc/laboratory-data/BCCDC_COVID19_Dashboard_Lab_Information.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Regional data: [bc/regional-case-summary/BCCDC_COVID19_Regional_Summary_Data.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Case, testing, vaccine summary by CHSA and LHA: [bc/case-testing-vaccine-summary-by-CHSA-and-LHA/BCCDC_COVID19_LHA_CHSA_Data.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * VoC Weekly Lineage Frequency Table: [bc/voc-weekly-lineage-frequency-table/Weekly_lineage_table.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * VOC time series by RHA: [bc/voc-time-series-by-rha/COVID19_VoC_data.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * VOC time series by RHA (2): [bc/voc-time-series-by-rha-2/Figure1_weeklyreport_data.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [COVID-19 Public Exposures](http://www.bccdc.ca/health-info/diseases-conditions/covid-19/public-exposures)
    * Public exposures webpage screenshot: [bc/public-exposures-webpage/public-exposures-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
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
    * Public exposures - flights: [bc/public-exposures-flights/public-exposures-flights-tables-Current.pdf](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [British Columbia COVID-19 Dashboard](https://experience.arcgis.com/experience/a6f23959a8b14bfa989e3cda29297ded)
    * Dashboard BC and Canada cumulative testing rate: [bc/bc-canada-cumulative-testing-rate/BC_COVID19__BC_Canadian_Testing_Rates_View.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard case demographics by Regional Health Authority: [bc/case-demographics-by-rha/BC_COVID19_Dashboard_Case_Details_Production.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard 7-day and cumulative cases by HSDA: [bc/7-day-and-cumulative-cases-by-hsda/BC_COVID19_Dashboard_Cases_by_Health_Service_Delivery_Areas_HSDA_VIEW.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard testing time series by Regional Health Authority (2): [bc/testing-timeseries-by-rha-2/BC_COVID19_Laboratory_Information.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard Vaccine Doses by Regional Health Authority: [bc/vaccine-doses-by-rha/BC_COVID19Dashboard_Vaccine_Counts.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard case time series by Health Service Delivery Area: [bc/case-time-series-by-hsda/BCCOVID19_Dashboard_Regional_Summary_Data.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard cumulative case, death, recovered, hospitalization, ICU data by Regional Health Authority: [bc/cumulative-case-death-recover-hosp-icu-by-rha/COVID19_Cases_by_BC_Health_Authority.json](http://data.opencovid.ca/archive/index.html#archive/)
    * 7-day and cumulative cases by HSDA (2): [bc/7-day-and-cumulative-cases-by-hsda-2/CumulativeCases.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard testing time series by Regional Health Authority: [bc/testing-timeseries-by-rha/BC_COVID19_Lab_Information.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Dashboard Regional Health Authority labels: [bc/rha-labels/HA_Labels.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [BCCDC COVID-19 Surveillance Dashboard](https://public.tableau.com/app/profile/bccdc/viz/BCCDCCOVID-19SurveillanceDashboard/Introduction)
    * Introduction: [bc/bccdc-surveillance-dashboard-introduction-webpage/bccdc-surveillance-dashboard-introduction-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Outcomes by Vax 1: [bc/bccdc-surveillance-dashboard-outcomes-by-vax-1-webpage/bccdc-surveillance-dashboard-outcomes-by-vax-1-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Outcomes by Vax 2: [bc/bccdc-surveillance-dashboard-outcomes-by-vax-2-webpage/bccdc-surveillance-dashboard-outcomes-by-vax-2-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Vax Donut Charts: [bc/bccdc-surveillance-dashboard-vax-donut-charts-webpage/bccdc-surveillance-dashboard-vax-donut-charts-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Vax by Age: [bc/bccdc-surveillance-dashboard-vax-by-age-webpage/bccdc-surveillance-dashboard-vax-by-age-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Vax Progress: [bc/bccdc-surveillance-dashboard-vax-progress-webpage/bccdc-surveillance-dashboard-vax-progress-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Map: [bc/bccdc-surveillance-dashboard-map-webpage/bccdc-surveillance-dashboard-map-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Vertical Plots: [bc/bccdc-surveillance-dashboard-vertical-plots-webpage/bccdc-surveillance-dashboard-vertical-plots-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Scatter Plot: [bc/bccdc-surveillance-dashboard-scatter-plot-webpage/bccdc-surveillance-dashboard-scatter-plot-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Case Trends by LHA 1: [bc/bccdc-surveillance-dashboard-case-trends-by-lha-1-webpage/bccdc-surveillance-dashboard-case-trends-by-lha-1-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Case Trends by LHA 2: [bc/bccdc-surveillance-dashboard-case-trends-by-lha-2-webpage/bccdc-surveillance-dashboard-case-trends-by-lha-2-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Weekly Change: [bc/bccdc-surveillance-dashboard-weekly-change-webpage/bccdc-surveillance-dashboard-weekly-change-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Data Notes: [bc/bccdc-surveillance-dashboard-data-notes-webpage/bccdc-surveillance-dashboard-data-notes-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
</details>
<details>
<summary><b>Canada</b></summary>

* [Coronavirus disease (COVID-19)](https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19.html)
    * Webpage: [can/can-covid-summary-webpage/can-covid-summary-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Vaccines and treatments for COVID-19: Vaccine rollout](https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection/prevention-risks/covid-19-vaccine-treatment/vaccine-rollout.html)
    * Webpage: [can/vaccine-rollout-webpage/vaccine-rollout-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Testing for COVID-19: Increasing testing supply](https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection/symptoms/testing/increased-supply.html)
    * Webpage: [can/testing-supply-webpage/testing-supply-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19: Summary data about travellers, testing and compliance](https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19/testing-screening-contact-tracing/summary-data-travellers.html)
    * Webpage: [can/international-traveller-testing-webpage/international-traveller-testing-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Coronavirus disease (COVID-19): Locations where you may have been exposed to COVID-19](https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection/latest-travel-health-advice/exposure-flights-cruise-ships-mass-gatherings.html)
    * Webpage: [can/can-potential-exposures-webpage/can-potential-exposures-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Epidemiological summary of COVID-19 cases in First Nations communities](https://www.sac-isc.gc.ca/eng/1589895506010/1589895527965)
    * Webpage: [can/isc-epi-summary-first-nations-webpage/isc-epi-summary-first-nations-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Detailed preliminary information on cases of COVID-19: 6 Dimensions (Aggregated data)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310077401)
    * Dataset: [can/detailed-preliminary-case-info-aggregated-6-dimensions/13100774.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Detailed preliminary information on cases of COVID-19: 4 Dimensions (Aggregated data)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310077501)
    * Dataset: [can/detailed-preliminary-case-info-aggregated-4-dimensions/13100775.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Preliminary dataset on confirmed cases of COVID-19, Public Health Agency of Canada](https://www150.statcan.gc.ca/n1/pub/13-26-0003/132600032020001-eng.htm)
    * Dataset: [can/preliminary-dataset-on-confirmed-cases/COVID19-eng.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Canada Case Counts (Hospital Vs. ICU)](https://canadiancriticalcare.org/COVID-19-Case-Counts)
    * Canadian Critical Care Society hospital and ICU counts: [can/cccs-hospital-icu-counts/COVID-19_DAILY_TRACKING_STATISTICS.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 data trends](https://www.canada.ca/en/public-health/services/diseases/coronavirus-disease-covid-19/epidemiological-economic-research-data.html)
    * Report (English): [can/phac-weekly-epidemiological-report-english/surv-covid19-weekly-epi-update-en.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Report (French): [can/phac-weekly-epidemiological-report-french/surv-covid19-weekly-epi-update-fr.pdf](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 daily epidemiology update](https://health-infobase.canada.ca/covid-19/epidemiological-summary-covid-19-cases.html)
    * Report (English): [can/phac-daily-epidemiology-update-report-english/Epidemiological-summary-of-COVID-19-cases-in-Canada-Canada.ca.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Report (French): [can/phac-daily-epidemiology-update-report-french/Resume-epidemiologique-des-cas-de-COVID-19-au-Canada.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * National overview (DD-MM-YYYY): [can/epidemiology-update/covid19.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * National overview (YYYY-MM-DD): [can/epidemiology-update-2/covid19-download.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * National overview (YYYY-MM-DD, JSON): [can/epidemiology-update-json/covid19.json](http://data.opencovid.ca/archive/index.html#archive/)
    * National overview (data dictionary): [can/epidemiology-update-data-dictionary/covid19-data-dictionary.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Epidemiology summary statements: [can/epidemiology-summary-statements/covid19-epiSummary-statements.csv](http://data.opencovid.ca/archive/index.html#archive/)
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
    * Hospitalizations, intensive care unit (ICU), mechanical ventilation: [can/hospitalizations-icu-mechanical-ventilation/covid19-epiSummary-hospVentICU.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases on First Nations reserves: [can/covid-time-series-first-nations-reserves/covid19-isc.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Variant prevalence time series: [can/variant-prevalence-time-series/covid19-epiSummary-variants.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Variant sample size time series: [can/variant-sample-size-time-series/covid19-epiSummary-variants-sampleSize.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Detailed variant prevalence time series: [can/variant-prevalence-time-series-detailed/covid19-epiSummary-variants-detailed-download.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Variant contributing labs: [can/variant-contributing-labs/covid19-epiSummary-variants-contributingLabs.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases following vaccination (cases, hospitalizations, deaths by vaccination): [can/cases-following-vaccination-cases-hosp-deaths-by-vaccination-status/covid19-epiSummary-casesAfterVaccination.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases following vaccination (cases by vaccination status and gender): [can/cases-following-vaccination-cases-by-vaccination-status-and-gender/covid19-epiSummary-casesAfterVaccinationGender.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases following vaccination (severe outcomes ratios): [can/cases-following-vaccination-severe-outcomes-ratios/covid19-epiSummary-casesAfterVaccinationSevereOutcome.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases following vaccination (page statements): [can/cases-following-vaccination-page-statements/covid19-epiSummary-casesAfterVaccinationPageStatements.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases following vaccination (update date): [can/cases-following-vaccination-update-date/covid19-epiSummary-casesAfterVaccinationUpdateDate.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Update time: [can/situational-awareness-dashboard-update-time/covid19-updateTime.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * PHAC provincial data update notes: [can/provincial-data-update-notes/covid19-epiSummary-exceptions.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Symptoms summary: [can/symptoms-summary/covid19-epiSummary-symptoms.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * NML weekly testing: [can/nml-weekly-testing/NML_weekly_testing.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * NML summary: [can/nml-summary/covid19-epiSummary-NML.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Variants of concern time series by province: [can/variants-of-concern-time-series-by-province/covid19-epiSummary-voc.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [COVIDTrends](https://health-infobase.canada.ca/covid-19/covidtrends/)
    * Mobility: [can/covidtrends-mobility/mobility.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * FluWatchers: [can/covidtrends-fluwatchers/fluwatchers.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Health region information: [can/health-region-info/hr_websites.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Census district to health region correspondence: [can/census-district-to-health-region-correspondence/censusdistricts.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 vaccination in Canada - Vaccines administered](https://health-infobase.canada.ca/covid-19/vaccine-administration/)
    * Vaccination administration: [can/vaccination-administration/vaccination-administration.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination administration by dose number: [can/vaccination-administration-by-dose-number/vaccination-administration-bydosenumber.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination administration (update date): [can/vaccination-administration-update-date/vaccination-administration-updateDate.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination distribution: [can/vaccination-distribution/vaccination-distribution.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination distribution (update date): [can/vaccination-distribution-update-date/vaccination-distribution-updateDate.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 vaccination in Canada - Vaccination coverage](https://health-infobase.canada.ca/covid-19/vaccination-coverage/)
    * Vaccination coverage overall: [can/vaccination-coverage-overall/vaccination-coverage-overall.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by age and sex: [can/vaccination-coverage-by-age-sex/vaccination-coverage-byAgeAndSex.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by age and sex (3): [can/vaccination-coverage-by-age-sex-3/vaccination-coverage-byAgeAndSexOT1.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by age and sex (current week): [can/vaccination-coverage-by-age-sex-current-week/vaccination-coverage-byAgeAndSex3.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by age and sex (condensed): [can/vaccination-coverage-by-age-sex-condensed/vaccination-coverage-byAgeAndSexOT.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by age and sex (alternative): [can/vaccination-coverage-by-age-sex-alt/vaccination-coverage-byAgeAndSex-overTime.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by age and sex with denominators: [can/vaccination-coverage-by-age-sex-denominators/vaccination-coverage-byAgeAndSexDenominators.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by vaccine type: [can/vaccination-coverage-by-vaccine-type/vaccination-coverage-byVaccineType.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by province: [can/vaccination-coverage-by-prov/vaccination-coverage-map.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by province (update date): [can/vaccination-coverage-by-prov-update-date/vaccination-coverage-updateDate.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination statements: [can/vaccination-statements/vaccination-statements.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination notes: [can/vaccination-notes/vaccination-notes.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Legend buckets: [can/vaccination-coverage-legend-buckets/vaccination-coverage-legendBuckets.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by age and sex (2): [can/vaccination-coverage-by-age-sex-2/vaccination-coverage-byAgeAndSex2.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccination coverage for key populations: [can/vaccination-coverage-keypops/vaccination-coverage-keypops.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [COVID-19 vaccination in Canada - Technical notes](https://health-infobase.canada.ca/covid-19/vaccination-coverage/technical-notes.html)
    * Webpage: [can/vaccination-technical-notes-webpage/vaccination-technical-notes-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage data availability by week: [can/vaccination-coverage-data-availability-by-week/vaccination-coverage-dataAvailability.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 international data](https://health-infobase.canada.ca/covid-19/international/)
    * International case and death time series: [can/international-covid-cases-deaths-time-series/InternationalCovid19Cases.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * International case and death time series update date: [can/international-covid-cases-deaths-time-series-update-date/updated.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Reported side effects following COVID-19 vaccination in Canada](https://health-infobase.canada.ca/covid-19/vaccine-safety/)
    * AEFI weekly reports by event category and vaccine type: [can/aefi-weekly-by-event-type/vaccine-safety-AEFI-figure.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * AESI weekly reports by event category and vaccine type: [can/aesi-weekly-reports-by-category-and-vaccine-type/vaccine-safety-AESIs-table.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * AEFI weekly reports key updates: [can/aefi-weekly-key-updates/vaccine-safety-keyupdates.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * AEFI summary including vaccination data: [can/aefi-figure-weekly-summary-including-vaccination/vaccine-safety-figure1.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * AEFI weekly summary by vaccine type: [can/aefi-figure-weekly-summary-by-vaccine-type/vaccine-safety-figure2.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * AEFI weekly summary by age and sex: [can/aefi-figure-weekly-summary-by-age-sex/vaccine-safety-figure3.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Reported side effects following COVID-19 vaccination in Canada: AEFI weekly summary (old): [can/aefi-weekly-summary-old/vaccine-safety-AEFI.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * AEFI weekly summary by serious event type (old): [can/aefi-weekly-summary-by-serious-event-type-old/vaccine-safety-severity.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * AEFI weekly summary by serious events: [can/aefi-figure-weekly-summary-by-serious-events/vaccine-safety-figure4.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Detailed preliminary information on confirmed cases of COVID-19 (Revised)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310078101)
    * Dataset: [can/detailed-preliminary-confirmed-case-info-revised/13100781.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
</details>
<details>
<summary><b>Manitoba</b></summary>

* [Province of Manitoba - COVID-19](https://www.gov.mb.ca/covid19/updates/index.html)
    * Webpage: [mb/manitoba-webpage/manitoba-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Manitoba COVID-19](https://experience.arcgis.com/experience/f55693e56018406ebbd08b3492e99771)
    * COVID-19 data by RHA and district: [mb/covid-data-by-rha-and-district/covid-data-by-rha-and-district.json](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 data by RHA and district (JSON to CSV): [mb/covid-data-by-rha-and-district-csv/covid-data-by-rha-and-district.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by demographics and RHA: [mb/cases-demographics-by-rha/cases-demographics-by-rha.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by demographics and RHA (JSON to CSV): [mb/cases-demographics-by-rha-csv/cases-demographics-by-rha.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by demographics and RHA (official): [mb/cases-demographics-by-rha-official/cases-demographics-by-rha.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Daily Cases by Status and RHA: [mb/cases-by-status-and-rha/cases-by-status-and-rha.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Daily Cases by Status and RHA (JSON to CSV): [mb/cases-by-status-and-rha-csv/cases-by-status-and-rha.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Daily Cases by Status and RHA (official): [mb/cases-by-status-and-rha-official/mb_covid_cases_by_status_daily_rha.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Manitoba five-day test positivity rate: [mb/five-day-test-positivity/five-day-test-positivity.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Manitoba five-day test positivity rate (JSON to CSV): [mb/five-day-test-positivity-csv/five-day-test-positivity.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Manitoba five-day test positivity rate (official): [mb/five-day-test-positivity-official/mb_covid_5_day_positivity_rate.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Summary Statistics by Geography: [mb/summary-stats-by-area/summary-stats-by-area.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Summary Statistics by Geography (official): [mb/summary-stats-by-area-official/mb_covid_cases_summary_statistics.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Case Status by District: [mb/current-status-by-area/current-status-by-area.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Case Status by District (official): [mb/current-status-by-area-official/Manitoba_COVID19_Case_Status_by_Geography.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Case Status by District (official FGDB): [mb/current-status-by-area-official-fgdb/Manitoba_COVID19_Case_Status_by_Geography.gdb.zip](http://data.opencovid.ca/archive/index.html#archive/)
    * Case Status by RHA (official): [mb/current-status-by-rha-official/Manitoba_COVID19_Case_Status_by_Geography.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Case Status by RHA (official FGDB): [mb/current-status-by-area-rha-fgdb/Manitoba_COVID19_Case_Status_by_Geography.gdb.zip](http://data.opencovid.ca/archive/index.html#archive/)
* [Manitoba COVID-19 Vaccinations](https://www.gov.mb.ca/covid19/vaccine/reports.html)
    * Vaccination time series 2: [mb/vaccination-time-series-2/mb_covid_vaccinations_daily_cumulative_02.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination by age group and sex 2: [mb/vaccination-by-age-sex-2/mb_covid_vaccinations_demographics_02.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination by manufacturer: [mb/vaccination-by-manufacturer/mb_covid_vaccinations_manufacturers.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination summary by Regional Health Authority 2: [mb/vaccination-summary-by-rha-2/mb_covid_vaccinations_summary_stats_02.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage 2: [mb/vaccination-coverage-2/mb_covid_vaccinations_coverage_02.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Uptake by RHA, age, sex: [mb/vaccine-uptake-by-rha-age-sex/mb_covid_vaccine_uptake_demographics.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Uptake by Health District 2: [mb/vaccine-uptake-by-district-2/mb_covid_vaccine_uptake_district_2.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Inventory, delivered, administered, scheduled: [mb/vaccination-inventory-delivered-admin-scheduled-2/mb_covid_vaccinations_inventory_stats_02.json](http://data.opencovid.ca/archive/index.html#archive/)
    * First Nations vaccination time series: [mb/first-nations-vaccination-time-series/mbfn_covid_vaccinations_daily_cumulative.json](http://data.opencovid.ca/archive/index.html#archive/)
    * First Nations vaccination by age group and sex: [mb/first-nations-vaccination-by-age-sex/mbfn_covid_vaccinations_demographics.json](http://data.opencovid.ca/archive/index.html#archive/)
    * First Nations vaccination by provider: [mb/first-nations-vaccination-by-provider/mbfn_covid_vaccinations_provider_summary.json](http://data.opencovid.ca/archive/index.html#archive/)
    * First Nations vaccination by Regional Health Authority: [mb/first-nations-vaccination-by-rha/mbfn_covid_vaccinations_rha_summary.json](http://data.opencovid.ca/archive/index.html#archive/)
    * First Nations vaccination summary on reserve and off reserve: [mb/first-nations-vaccination-summary-on-reserve-off-reserve/mbfn_covid_vaccinations_summary_statistics.json](http://data.opencovid.ca/archive/index.html#archive/)
    * First nations vaccination by Tribal Council Region: [mb/first-nations-vaccination-by-tribal-council-region/mbfn_covid_vaccinations_tribal_council_summary.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by Regional Health Authority: [mb/vaccination-coverage-by-rha/mb_covid_vaccinations_18_coverage.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Projected vaccine doses: [mb/projected-vaccine-doses/mb_covid_vaccinations_projected_doses.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Uptake by Health District: [mb/vaccine-uptake-by-district/mb_covid_vaccine_uptake_district.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccination by age group and sex: [mb/vaccination-by-age-sex/mb_covid_vaccinations_demographics.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccination coverage: [mb/vaccination-coverage/mb_covid_vaccinations_coverage.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccination summary by Regional Health Authority: [mb/vaccination-summary-by-rha/mb_covid_vaccinations_summary_stats.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Inventory, delivered, administered, scheduled: [mb/vaccination-inventory-delivered-admin-scheduled/mb_covid_vaccinations_inventory_stats.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccination time series: [mb/vaccination-time-series/mb_covid_vaccinations_daily_cumulative.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Regional Health Authorities: [mb/regional-health-authorities/Manitoba_Regional_Health_Authorities.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Winnipeg Community Areas: [mb/winnipeg-community-areas/bdy_wha_community_areas_py_shp.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Health Districts: [mb/health-districts/Health_Districts.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [COVID-19 Dashboard: K-12 Schools in Manitoba](https://experience.arcgis.com/experience/6e7af13b3ffb447a99734b0119b169d3/)
    * COVID education statistics summary: [mb/covid-education-summary/covid-education-summary.json](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID educations cases last 2 weeks: [mb/covid-education-cases-last-2-weeks/covid-education-cases-last-2-weeks.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Manitoba school divisions: [mb/school-divisions/school-divisions.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Cases and Risk of COVID-19 in Manitoba](https://www.gov.mb.ca/covid19/updates/cases.html)
    * COVID-19 Variant of Concern Cases in Manitoba: [mb/cumulative-variants-by-rha/mb_covid_variants.json](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 Cases by vaccination status: [mb/daily-cases-by-vaccination-status/mb_covid_cases_by_vaccination_status.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Select COVID-19 Outbreaks in Manitoba: [mb/acive-outbreaks-ltc-institutions-healthcare-schools/Current_MB_COVID_Outbreaks.json](http://data.opencovid.ca/archive/index.html#archive/)

<details>
<summary><i>Winnipeg</i></summary>

* [COVID-19 By-law Enforcement](https://data.winnipeg.ca/Neighbourhood-Liveability-Property-Standards-Licen/COVID-19-By-law-Enforcement/ndr6-96vi)
    * Dataset: [mb/winnipeg-by-law-enforcement/COVID-19_By-law_Enforcement.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Designated Active Transportation Route Counts](https://data.winnipeg.ca/Transportation-Planning-Traffic-Management/COVID-19-Designated-Active-Transportation-Route-Co/aqka-nz2g)
    * Dataset: [mb/winnipeg-active-transportation/COVID-19_Designated_Active_Transportation_Route_Counts.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
</details>
</details>
<details>
<summary><b>New Brunswick</b></summary>

* [New Brunswick COVID-19 Dashboard](https://experience.arcgis.com/experience/8eeb9a2052d641c996dba5de8f25a8aa)
    * Counties: [nb/counties/counties.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Assessment sites: [nb/covid-assessment-sites/covid-assessment-sites.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Provincial case, death, recovered time series: [nb/provincial-case-death-recovered-time-series/provincial-case-death-recovered-time-series.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Provincial case, death, recovered time series 2: [nb/provincial-case-death-recovered-time-series-2/Covid19DailyCaseStats3.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Provincial cumulative test statistics by age and sex: [nb/provincial-cumulative-test-statistics-by-age-sex/provincial-cumulative-test-statistics-by-age-sex.json](http://data.opencovid.ca/archive/index.html#archive/)
    * New cases by age group and Health Zone: [nb/new-cases-by-age-group-and-zone/Covid19NewCaseAgeStats2.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Current COVID-19 statistics by Health Zone: [nb/current-covid-stats-by-zone/WinterPlanLevel.json](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 hospitalization/ICU time series: [nb/hosp-icu-time-series/Covid19HospitalTrends.json](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 travel and enforcement statistics (7-day averages): [nb/covid-travel-enforcement-stats-7-day-avg/Covid19ComplianceEnforcement2.json](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 potential public exposures: [nb/potential-public-exposures/Covid19_Exposures2.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Case/hospitalization/ICU/death rate by vaccination status: [nb/case-hosp-icu-death-rate-by-vaccination-status/Covid19CaseVaccinationRates2.json](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 schools 2021: [nb/covid-schools-2021/Covid19SchoolsData.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Schools: [nb/schools/Covid19NBSchools.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine data 2: [nb/vaccine-data-2/Covid19VaccineData2.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine coverage by age groups: [nb/vaccine-coverage-by-age/Covid19VaccineAge.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine time series 2: [nb/vaccine-time-series-2/Covid19DailyVaccineStats.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Health zone cumulative stats: [nb/health-zone-cumulative-stats/health-zone-cumulative-stats.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Hospitals: [nb/hospitals/hospitals.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine data: [nb/vaccine-data/vaccine-data.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccine time series: [nb/vaccine-time-series/Covid19VaccineTimeline.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Compliance by health zone: [nb/covid-compliance-by-health-zone/covid-compliance-by-health-zone.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Health zone and community recovery phases: [nb/health-zone-community-recovery-phases/health-zone-community-recovery-phases.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Neighbour region cumulative stats: [nb/neighbour-regions-cumulative-stats/neighbour-regions-cumulative-stats.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Neighbour state/province cumulative stats: [nb/neighbour-state-prov-cumulative-stats/neighbour-state-prov-cumulative-stats.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Adult residential facilities: [nb/adult-residential-facilities/adult-residential-facilities.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Communities: [nb/communities/communities.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Nursing homes: [nb/nursing-homes/nursing-homes.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * International border: [nb/international-border/international-border.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Airports: [nb/airports/airports.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Traffic control points: [nb/traffic-control-points/traffic-control-points.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Ferries: [nb/ferries/ferries.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Potential Public Exposures](https://www2.gnb.ca/content/gnb/en/corporate/promo/covid-19/potential_public_exposure.html)
    * Webpage: [nb/potential-public-exposures-webpage/potential-public-exposures-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
</details>
<details>
<summary><b>Newfoundland and Labrador</b></summary>

* [Newfoundland and Labrador COVID-19 Pandemic Update Hub](https://covid-19-newfoundland-and-labrador-gnl.hub.arcgis.com/)
    * Webpage: [nl/nl-pandemic-hub-webpage/nl-pandemic-hub-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Province summary: [nl/nl-summary/ProvCovidDailyStats.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Province time series: [nl/nl-summary-time-series/Prov_Covid_Daily_Stats_v2_Public_View.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Regional Health Authority summary: [nl/rha-summary/RHA_CurrentStats2_Public2.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cumulative cases by Primary Health Care Zone: [nl/cumulative-cases-by-phcz/PHZ_Zone_Public.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by likely exposure setting: [nl/cases-by-likely-exposure-setting/Exposure_New_Public.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by age and sex: [nl/cases-by-age-and-sex/Covid_AgeLayerPublic2.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by vaccination status: [nl/cases-by-vaccination-status/CasesByVaccineStatus_Public.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cumulative vaccination (5): [nl/cumulative-vaccination-5/Daily_Vaccination_Update_v5_Public.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Percent fully vaccinated by Primary Health Care Area (PHC): [nl/fully-vaccinated-by-phc/PHC_FullyVaccinated_LabMerge.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine doses received and expected this week: [nl/vaccine-doses-received-and-expected/WeeklyDoses_Public.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cumulative vaccination: [nl/cumulative-vaccination/Vaccine_LatestPublic_v2.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Cumulative vaccination (2): [nl/cumulative-vaccination-2/DailyVaccination_Public.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Cumulative vaccination (3): [nl/cumulative-vaccination-3/DailyVaccineUpdatePublic.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Cumulative vaccination (4): [nl/cumulative-vaccination-4/DailyVaxUpdatePublicV3.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Primary Health Care Zone populations: [nl/phcz-populations/PHC_Zones_Combined_Public.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
</details>
<details>
<summary><b>Northwest Territories</b></summary>

* [GNWT's Response to COVID-19](https://www.gov.nt.ca/covid-19/)
    * Webpage: [nt/nwt-webpage/nwt-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Northwest Territories COVID-19 dashboard](https://nwt-covid.shinyapps.io/Testing-and-Cases/?lang=1)
    * Cases webpage: [nt/nwt-dashboard-cases-webpage/nwt-dashboard-cases-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Communities webpage: [nt/nwt-dashboard-communities-webpage/nwt-dashboard-communities-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Testing webpage: [nt/nwt-dashboard-testing-webpage/nwt-dashboard-testing-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Wastewater webpage: [nt/nwt-dashboard-wastewater-webpage/nwt-dashboard-wastewater-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccinations coverage webpage: [nt/nwt-dashboard-vaccination-coverage-webpage/nwt-dashboard-vaccination-coverage-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccinations doses webpage: [nt/nwt-dashboard-vaccination-doses-webpage/nwt-dashboard-vaccination-doses-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
</details>
<details>
<summary><b>Nova Scotia</b></summary>

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
    * Immunizations (3): [ns/immunizations-3/Immunizations_V4_PROD.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine coverage by CHN: [ns/vaccine-coverage-by-chn/VaccineCoverageCHN_V4_PROD.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine uptake by age: [ns/vaccine-uptake-by-age/VaccineUptakeAge_V4_PROD.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Breakthough outcomes: [ns/breakthrough-outcomes/Breakthrough_Outcomes_V4_PROD.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Onset zones: [ns/onset-zones/Onset_Zones_V4_PROD.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Immunizations: [ns/immunizations/immunizations.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Immunizations (2): [ns/immunizations-2/Immunizations_3_PROD.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Health boundaries: [ns/health-boundaries/health-boundaries.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Potential COVID Exposures](http://www.nshealth.ca/covid-exposures)
    * Webpage: [ns/ns-potential-covid-exposures-webpage/ns-potential-covid-exposures-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Exposures Connected to Public Schools](https://backtoschool.ednet.ns.ca/school-exposures)
    * Webpage: [ns/ns-public-school-covid-exposures-webpage/ns-public-school-covid-exposures-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 news releases](https://novascotia.ca/news/search/?dept=180)
    * Webpage: [ns/daily-covid-news-release-webpage/daily-covid-news-release-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
</details>
<details>
<summary><b>Nunavut</b></summary>

* [COVID-19 (Novel Coronavirus)](https://gov.nu.ca/health/information/covid-19-novel-coronavirus)
    * Webpage: [nu/nunavut-webpage/nunavut-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Vaccination](https://www.gov.nu.ca/health/information/covid-19-vaccination)
    * Webpage: [nu/nunavut-vaccination-webpage/nunavut-vaccination-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Table (image): [nu/nunavut-vaccination-table/vaccine_table.jpg](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Exposure Notices](https://www.gov.nu.ca/health/information/covid-19-exposure-notices)
    * Webpage: [nu/nunavut-exposure-notices-webpage/nunavut-exposure-notices-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
</details>
<details>
<summary><b>Ontario</b></summary>

* [How Ontario is responding to COVID-19](https://www.ontario.ca/page/how-ontario-is-responding-covid-19)
    * Webpage: [on/ontario-webpage/ontario-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [All Ontario: Case numbers and spread](https://covid-19.ontario.ca/data)
    * Webpage: [on/on-data-webpage/on-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Confirmed positive cases of COVID19 in Ontario](https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario/resource/455fd63b-603d-4608-8216-7d8647f43350)
    * Dataset: [on/confirmed-positive-cases/conposcovidloc.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Status of COVID-19 cases in Ontario](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11)
    * Dataset: [on/status-of-cases/covidtesting.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Status of COVID-19 cases in Ontario by Public Health Unit (PHU)](https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario-by-public-health-unit-phu)
    * Dataset: [on/status-of-cases-by-phu/cases_by_status_and_phu.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Ontario COVID-19 testing metrics by Public Health Unit (PHU)](https://data.ontario.ca/dataset/ontario-covid-19-testing-metrics-by-public-health-unit-phu)
    * Dataset: [on/testing-metrics-by-phu/testing_metrics_by_phu.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Ontario COVID-19 testing percent positive by age group](https://data.ontario.ca/dataset/ontario-covid-19-testing-percent-positive-by-age-group)
    * Dataset: [on/percent-positive-by-age-group/percent_positive_by_agegrp.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 cases in hospital and ICU, by Ontario Health (OH) region](https://data.ontario.ca/dataset/covid-19-cases-in-hospital-and-icu-by-ontario-health-region)
    * Dataset: [on/hosp-icu-by-lhin/lhin_hospital_icu_covid_data.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Effective reproduction number (Re) for COVID-19 in Ontario](https://data.ontario.ca/dataset/effective-reproduction-number-re-for-covid-19-in-ontario)
    * Dataset: [on/effective-reproduction-number/effective_reproduction_number_ontario.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID Alert Impact Data](https://data.ontario.ca/dataset/covid-alert-impact-data)
    * COVID Alert downloads - Canada: [on/covid_alert_downloads_canada/covid_alert_downloads_canada.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Uploads of COVID-19 diagnosis to COVID Alert - Ontario: [on/covid-alert-uploads-ontario/covid_alert_positive_uploads_ontario.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 testing locations](https://data.ontario.ca/dataset/covid-19-assessment-centre-locations)
    * Dataset: [on/testing-locations/locations.json](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 pharmacy vaccine locations](https://covid-19.ontario.ca/vaccine-locations/)
    * Webpage: [on/vaccine-pharmacy-locations-webpage/vaccine-pharmacy-locations-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Ontario COVID-19 outbreaks data](https://data.ontario.ca/dataset/ontario-covid-19-outbreaks-data)
    * Ongoing outbreaks: [on/ongoing-outbreaks/ongoing_outbreaks.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Summary of cases associated with outbreaks: [on/summary-outbreak-cases/outbreak_cases.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 testing of inmates in Ontario’s Provincial Correctional Institutions](https://data.ontario.ca/dataset/covid-19-testing-of-inmates-in-ontario-s-correctional-institutions)
    * Dataset: [on/correctional-institutions-inmates-testing/inmatetesting.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Status of COVID-19 cases in Ontario’s Provincial Correctional Institutions](https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario-s-correctional-institutions)
    * Dataset: [on/correctional-institutions-status/correctionsinmatecases.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Long-Term Care Home COVID-19 Data](https://data.ontario.ca/dataset/long-term-care-home-covid-19-data)
    * Summary data: [on/long-term-care-home-summary/ltccovidsummary.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Active outbreaks: [on/long-term-care-home-active/activeltcoutbreak.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Resolved outbreaks: [on/long-term-care-home-resolved/resolvedltc.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * LTC home COVID-19 staff vaccination rates: [on/long-term-care-home-staff-vaccination-rates/ltc_immunization_data.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 cases in schools](https://www.ontario.ca/page/covid-19-cases-schools)
    * Webpage: [on/cases-schools-webpage/cases-schools-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 cases in child care centres](https://www.ontario.ca/page/covid-19-cases-child-care-centres)
    * Webpage: [on/cases-child-care-centres-webpage/cases-child-care-centres-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Schools COVID-19 data](https://data.ontario.ca/dataset/summary-of-cases-in-schools)
    * 2021-22: Summary of cases in schools: [on/schools-summary-2021-2022/schoolcovidsummary2021_2022.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * 2021-22: Schools with recent COVID-19 cases: [on/schools-recent-2021-2022/schoolrecentcovid2021_2022.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Summary of cases in schools: [on/schools-summary/schoolcovidsummary.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Schools with active COVID-19 cases: [on/schools-active/schoolsactivecovid.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Cases in school board partners: [on/school-board-partners/schoolpartnersactivecovid.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * School Targeted Testing Summary: [on/school-targeted-testing-summary/schoolcovidtesting.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * School Targeted Testing Sites: [on/school-targeted-testing-sites/schooltestingsites.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * School Targeted Testing Partners: [on/school-targeted-testing-partners/schoolcovidtesting_partners.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * School Pharmacy Testing: [on/school-pharmacy-testing/school_pharmacy_covidtesting.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * School Pharmacy Testing Locations: [on/school-pharmacy-testing-locations/school-pharmacy-testing-locations.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Licensed child care settings COVID-19 data](https://data.ontario.ca/dataset/summary-of-cases-in-licensed-child-care-settings)
    * Summary of cases in licensed child care settings: [on/licensed-child-care-settings-summary/lccovidsummary.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Licensed child care centres and agencies with active COVID-19 cases: [on/licensed-child-care-settings-active/lccactivecovid.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Vaccine Data in Ontario](https://data.ontario.ca/dataset/covid-19-vaccine-data-in-ontario)
    * Vaccine data: [on/vaccine-data/vaccine_doses.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine data by age: [on/vaccine-data-by-age/vaccines_by_age.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine data by Public Health Unit and by age: [on/vaccine-data-by-age-and-phu/vaccines_by_age_phu.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Hospitalizations and cases by vaccination status: [on/hospitalizations-and-cases-by-vaccination-status/vac_status.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases and rates by vaccination status: [on/cases-and-rates-by-vaccination-status/cases_by_vac_status.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Hospitalizations by vaccination status: [on/hospitalizations-by-vaccination-status/vac_status_hosp_icu.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Case rates by vaccination status and age group: [on/case-rates-by-vaccination-status-and-age-group/cases_by_age_vac_status.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [ICES COVID-19 Dashboard](https://www.ices.on.ca/DAS/AHRQ/COVID-19-Dashboard)
    * Percent positivity by FSA: [on/ices-percent-positivity-by-fsa/ICES-COVID19-Testing-Data-FSA-percent-positivity.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Percent positivity by age group and Public Health Unit (PHU): [on/ices-percent-positivity-by-age-group-and-phu/ICES-COVID19-Testing-Data_PHUxAge-Groups-percent-positivity.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine coverage estimates for selected age groups by FSA: [on/ices-vaccine-coverage-by-age-group-and-fsa/ICES-COVID19-Vaccination-Data-by-FSA.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine coverage estimates by priority groups: [on/ices-vaccine-coverage-by-priority-group/ICES-COVID19-Vaccine-Coverage-by-Priority-Group.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine coverage estimates for adults with developmental disabilities: [on/ices-vaccine-coverage-for-adults-with-developmental-disabilities/Vaccine-coverage-for-adults-with-developmental-disabilities.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Map and list of Forward Sortation Areas (FSAs) by neighbourhood risk group: [on/ices-fsa-by-neighbourhood-risk-group/ICES-COVID19-Dashboard-Neighbourhood-Risk-Groups-Reference-File.xlsx](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [COVID-19 cases in schools and child care centres](https://www.ontario.ca/page/covid-19-cases-schools-and-child-care-centres)
    * Webpage: [on/cases-schools-and-child-care-centres-webpage/cases-schools-and-child-care-centres-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]

<details>
<summary><i>Ontario universities</i></summary>

* [University of Toronto COVID-19 tracking](https://www.utoronto.ca/utogether/covid19-dashboard)
    * Webpage: [on/u-of-t-covid-tracking-webpage/u-of-t-covid-tracking-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Queen’s University Case Tracker](https://www.queensu.ca/safereturn/health-safety/case-tracker)
    * Webpage: [on/queens-university-case-tracker-webpage/queens-university-case-tracker-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
</details>

<details>
<summary><i>Ottawa</i></summary>

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
</details>

<details>
<summary><i>Public Health Ontario</i></summary>

* [Public Health Ontario: COVID-19 Data and Surveillance](https://www.publichealthontario.ca/en/data-and-analysis/infectious-disease/covid-19-data-surveillance)
    * Daily epidemiologic summary: [on/pho-daily-epi-summary-report/covid-19-daily-epi-summary-report.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Weekly epidemiologic summary: [on/pho-weekly-epi-summary-report/covid-19-weekly-epi-summary-report.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * SARS-CoV-2 Whole Genome Sequencing in Ontario: [on/pho-wgs-summary-report/covid-19-sars-cov2-whole-genome-sequencing-epi-summary.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 in Long-Term Care Homes: [on/pho-ltc-summary-report/covid-19-long-term-care-epi-summary.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 Regional Incidence and Time to Case Notification in Ontario: [on/pho-regional-summary-report/covid-19-regional-epi-summary-report.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 in Children and Education Settings: [on/pho-children-school-outbreak-summary-report/covid-19-children-school-outbreaks-epi-summary.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 Vaccine Uptake and Program Impact in Ontario: [on/pho-vaccine-uptake-summary-report/covid-19-vaccine-uptake-ontario-epi-summary.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Adverse Events Following Immunization (AEFIs) for COVID-19 in Ontario: [on/pho-aefi-report/covid-19-aefi-report.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Trends of COVID-19 Incidence in Ontario: [on/pho-incidence-trends-report/covid-19-epi-trends-incidence-ontario.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Confirmed Cases of COVID-19 Following Vaccination in Ontario: [on/pho-confirmed-cases-post-vaccination-report/covid-19-epi-confirmed-cases-post-vaccination.pdf](http://data.opencovid.ca/archive/index.html#archive/)
</details>

<details>
<summary><i>Public Health Units</i></summary>

* [Algoma (PHU) - Current Status (COVID-19)](https://www.algomapublichealth.com/disease-and-illness/infectious-diseases/novel-coronavirus/current-status-covid-19/)
    * Webpage: [on/on-phu-algoma-covid-data-webpage/on-phu-algoma-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Brant (PHU) - Novel Coronavirus (COVID-19)](https://www.bchu.org/ServicesWeProvide/InfectiousDiseases/Pages/coronavirus.aspx)
    * Webpage: [on/on-phu-brant-covid-data-webpage/on-phu-brant-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Chatham-Kent (PHU) - Current Situation in Chatham-Kent and Surrounding Areas](https://ckphu.com/current-situation-in-chatham-kent/)
    * Epidemiological summary: [on/on-phu-chatham-kent-covid-data-epi-summary-webpage/on-phu-chatham-kent-covid-data-epi-summary-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Durham (PHU) - COVID-19 Update](https://www.durham.ca/en/health-and-wellness/novel-coronavirus-update.aspx)
    * Status of COVID-19 Cases in Durham Region: [on/on-phu-durham-covid-data-status-of-cases-webpage/on-phu-durham-covid-data-status-of-cases-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Eastern (PHU) - Local Status Updates and Statistics](https://eohu.ca/en/covid/covid-19-status-update-for-eohu-region)
    * Webpage: [on/on-phu-eastern-covid-data-webpage/on-phu-eastern-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Grey Bruce (PHU) - Grey Bruce Overview](https://www.publichealthgreybruce.on.ca/)
    * Webpage: [on/on-phu-grey-bruce-covid-data-webpage/on-phu-grey-bruce-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Haldimand-Norfolk (PHU) - Additional daily statistics](https://hnhu.org/additional-daily-statistics/)
    * Vaccinations: [on/on-phu-haldimand-norfolk-covid-data-vaccination-webpage/on-phu-haldimand-norfolk-covid-data-vaccination-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Case status & demography: [on/on-phu-haldimand-norfolk-covid-data-case-status-demography-webpage/on-phu-haldimand-norfolk-covid-data-case-status-demography-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Haliburton Kawartha Pineridge (PHU) - COVID-19](https://www.hkpr.on.ca/covid-19/)
    * Cases and Contacts Table: [on/on-phu-haliburton-kawartha-pineridge-covid-data-cases-contacts-webpage/on-phu-haliburton-kawartha-pineridge-covid-data-cases-contacts-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Halton (PHU) - Status of COVID-19 cases in Halton](https://www.halton.ca/For-Residents/New-Coronavirus/Status-of-COVID-19-Cases-in-Halton)
    * Case counts: [on/on-phu-halton-covid-data-case-counts-webpage/on-phu-halton-covid-data-case-counts-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Hamilton (PHU) - Status of Cases in Hamilton](https://www.hamilton.ca/coronavirus/status-cases-in-hamilton)
    * Cases & Tests: [on/on-phu-hamilton-covid-data-cases-tests-webpage/on-phu-hamilton-covid-data-cases-tests-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Hastings Prince Edward (PHU) - Status of COVID-19 Cases and Vaccinations](https://hpepublichealth.ca/covid-19-cases/)
    * Main: [on/on-phu-hastings-prince-edward-covid-data-main-webpage/on-phu-hastings-prince-edward-covid-data-main-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Kingston Frontenac Lennox & Addington (PHU) - COVID-19 case data for KFL&A Region Dashboard](https://www.kflaph.ca/en/healthy-living/status-of-cases-in-kfla.aspx)
    * Cases: [on/on-phu-kingston-frontenac-lennox-addington-covid-data-cases-webpage/on-phu-kingston-frontenac-lennox-addington-covid-data-cases-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Lambton (PHU) - COVID-19 Report](https://lambtonpublichealth.ca/2019-novel-coronavirus/)
    * Summary: [on/on-phu-lambton-covid-data-summary-webpage/on-phu-lambton-covid-data-summary-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Case details and trends: [on/on-phu-lambton-covid-data-case-details-trends-webpage/on-phu-lambton-covid-data-case-details-trends-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Middlesex-London (PHU) - Summary of COVID-19 Cases in Middlesex-London](https://www.healthunit.com/novel-coronavirus)
    * Case status: [on/on-phu-middlesex-london-covid-data-case-status-webpage/on-phu-middlesex-london-covid-data-case-status-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Niagara (PHU) - COVID-19 Statistics in Niagara](https://www.niagararegion.ca/health/covid-19/statistics/statistics.aspx)
    * Daily & active cases: [on/on-phu-niagara-covid-data-daily-active-cases-webpage/on-phu-niagara-covid-data-daily-active-cases-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [North Bay Parry Sound (PHU) - COVID-19 Status Report](https://www.myhealthunit.ca/en/health-topics/coronavirus.asp)
    * Overview: [on/on-phu-north-bay-parry-sound-covid-data-overview-webpage/on-phu-north-bay-parry-sound-covid-data-overview-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Northwestern (PHU) - COVID-19 Local Data](https://www2.nwhu.on.ca/covid-19/data/)
    * Webpage: [on/on-phu-northwestern-covid-data-webpage/on-phu-northwestern-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Peel (PHU) - COVID-19 in Peel](https://www.peelregion.ca/coronavirus/case-status/)
    * Summary: [on/on-phu-peel-covid-data-summary-webpage/on-phu-peel-covid-data-summary-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Peterborough (PHU) - Local COVID-19 Cases & Status](https://www.peterboroughpublichealth.ca/local-covid-19-status/)
    * Webpage: [on/on-phu-peterborough-covid-data-webpage/on-phu-peterborough-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Porcupine (PHU) - Novel Coronavirus (COVID-19)](https://www.porcupinehu.on.ca/en/your-health/infectious-diseases/novel-coronavirus/)
    * Webpage: [on/on-phu-porcupine-covid-data-webpage/on-phu-porcupine-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Renfrew (PHU) - COVID-19 local cases](https://www.rcdhu.com/novel-coronavirus-covid-19-2/)
    * Webpage: [on/on-phu-renfrew-covid-data-webpage/on-phu-renfrew-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Simcoe Muskoka (PHU) - COVID-19 highlights](https://www.simcoemuskokahealthstats.org/topics/infectious-diseases/a-h/covid-19)
    * Webpage: [on/on-phu-simcoe-muskoka-covid-data-webpage/on-phu-simcoe-muskoka-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Case and Vaccine Summary Table: [on/on-phu-simcoe-muskoka-covid-data-case-vaccine-summary-table-webpage/on-phu-simcoe-muskoka-covid-data-case-vaccine-summary-table-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Sudbury (PHU) - Current status (COVID-19)](https://www.phsd.ca/health-topics-programs/diseases-infections/coronavirus/current-status-covid-19/)
    * Webpage: [on/on-phu-sudbury-covid-data-webpage/on-phu-sudbury-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Thunder Bay (PHU) - Current COVID-19 Data in TBDHU](https://www.tbdhu.com/coviddata)
    * Webpage: [on/on-thunder-bay-covid-data-webpage/on-thunder-bay-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Timiskaming (PHU) - What is the current situation in Timiskaming?](https://www.timiskaminghu.com/90529/What-is-the-current-situation-in-Timiskaming)
    * Webpage: [on/on-phu-timiskaming-covid-data-webpage/on-phu-timiskaming-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Wellington Dufferin Guelph (PHU) - Status of Cases in WDG](https://wdgpublichealth.ca/your-health/covid-19-information-public/status-cases-wdg)
    * Overview: [on/on-phu-wellington-dufferin-guelph-covid-data-overview-webpage/on-phu-wellington-dufferin-guelph-covid-data-overview-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases: [on/on-phu-wellington-dufferin-guelph-covid-data-cases-webpage/on-phu-wellington-dufferin-guelph-covid-data-cases-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Windsor-Essex (PHU) - Local COVID-19 Data](https://www.wechu.org/cv/local-updates)
    * Webpage: [on/on-phu-windsor-essex-covid-data-webpage/on-phu-windsor-essex-covid-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [York (PHU) - COVID-19 in York Region](https://www.york.ca/wps/portal/yorkhome/health/yr/covid-19/covid19inyorkregion/01covid19inyorkregion/!ut/p/z1/tZPbcpswEIafJRdcYi0nS_ROoa6B2NhN4gPcZDAWhxQjBys46dNXJHSm7ThOOylcCGln91_-TwuK0BpFVdwUWSwKXsWlPIfR8M6jY891r8CfmcQBCjPq65jAyNbQ6iUB3ngooOhv6s8kROfllyhC0T4ptijUDYZJYhMVg5WoZpwMVVvbbOVip5Ztp7HdyqEoqcRe5Ch8ru8SXglWCQWeef1NHg6iEI8vgZzvmFxZXIpcgYQ3xVbV7G6n2UXVVtQsk5gUAO1EGPnveZdw9XrqTDPpIBa5WlQpR-ufvbrdH6Lr072kVHH_8BBRaa_19CTQum9_qxbmrw7HN8QEb-ljutRmYHpGl6Dr5tDVHPDBnRHwvuC59Zm4GlzpXcKZ-5UQs5JvXkeRVhuDSFo1S1nN6sFjLcO5EPvDJwUUOB6Pg4zzrGSDhO8UOFWS84NE83smCuUQ4jdv6lpHq6ZgR7SoeL2TX3LzjzPnQtcBE4e6dAxzuF1g-DrCJhlOpvPJtfbBDu8Y6Fne6FUeQ7_yer_y_weO74Gj0fYfM0YGUN1zyKXhkyDol33QL_ugX_ZBv3O__Cic_W6x2BHDKjMibO_eKptJOh0ZZug33y8D9fwru7j4Af7j0Z4!/dz/d5/L2dBISEvZ0FBIS9nQSEh/)
    * Individual-level case dataset: [on/on-phu-york-individual-level-case-data/YR_CaseData.csv](http://data.opencovid.ca/archive/index.html#archive/)
</details>

<details>
<summary><i>Toronto</i></summary>

* [COVID-19: Case Counts](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-pandemic-data/covid-19-weekday-status-of-cases-data/)
    * Dataset: [on/toronto-daily-status/CityofToronto_COVID-19_Daily_Public_Reporting.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19: Epidemiological Summary of Cases](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-pandemic-data/covid-19-epidemiological-summary-of-cases-data/)
    * Dataset: [on/toronto-covid-summary/CityofToronto_COVID-19_Data.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19: Neighbourhood Maps](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-pandemic-data/covid-19-neighbourhood-maps-data/)
    * Case Data: [on/toronto-neighbourhood-data/CityofToronto_COVID-19_NeighbourhoodData.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Testing Data: [on/toronto-neighbourhood-test-data/CityofToronto_COVID-19_Testing.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19: Monitoring Dashboard](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-pandemic-data/covid-19-monitoring-dashboard-data/)
    * Dataset: [on/toronto-monitoring-dashboard/CityofToronto_COVID-19_RecoveryData.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19: Active Outbreaks](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-pandemic-data/covid-19-active-outbreaks-data/)
    * Dataset: [on/toronto-active-outbreaks/CityofToronto_COVID-19_OutbreakData.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Cases in Toronto](https://open.toronto.ca/dataset/covid-19-cases-in-toronto/)
    * Dataset: [on/toronto-cases/COVID19_cases.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID 19: Ethno-Racial Identity & Income](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-pandemic-data/covid-19-ethno-racial-group-income-infection-data/)
    * Dataset: [on/toronto-ethno-racial-income/Ethno-Racial_Group,_Income,_and_COVID-19_Infection.xlsx](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
</details>
</details>
<details>
<summary><b>Prince Edward Island</b></summary>

* [PEI COVID-19 Case Data](https://www.princeedwardisland.ca/en/information/health-and-wellness/pei-covid-19-case-data)
    * Webpage: [pe/pei-webpage/pei-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Vaccination Data](https://www.princeedwardisland.ca/en/information/health-and-wellness/covid-19-vaccination-data)
    * Webpage: [pe/pei-vaccination-webpage/pei-vaccination-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Dataset: [pe/vaccine-data-cumulative/Vaccine_Rollout.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 news releases](https://www.princeedwardisland.ca/en/search/site?f%5B0%5D=type%3Anews&f%5B1%5D=field_news_type%3A22&f%5B2%5D=field_department%3A612)
    * Webpage: [pe/covid-news-release-webpage/covid-news-release-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Potential COVID-19 Exposures](https://www.princeedwardisland.ca/en/information/health-and-wellness/potential-covid-19-exposures)
    * Webpage: [pe/pei-potential-exposures-webpage/pei-potential-exposures-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Possible Air Travel Exposures](https://www.princeedwardisland.ca/en/information/health-and-wellness/possible-air-travel-exposures)
    * Webpage: [pe/pei-possible-air-travel-exposures-webpage/pei-possible-air-travel-exposures-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
</details>
<details>
<summary><b>Quebec</b></summary>

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
    * Deaths time series by living environment: [qc/deaths-time-series-by-living-environment/decesquotidien.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Status report on confirmed cases and deaths by RPA: [qc/status-report-cases-and-deaths-by-rpa/etat_situation_rpa.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Status report on confirmed cases and deaths by CHSLD: [qc/status-report-cases-and-deaths-by-chsld/etat_situation_chsld.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Active hospitalizations per hospital: [qc/active-hospitalizations-per-hosp/tableau-hospitalisations.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Outbreaks by setting (EN): [qc/outbreaks-by-setting-en/eclosions-par-milieu-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * COVID-19 daily data 7 days (FR): [qc/covid-data-daily-7-days/synthese-7jours.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * COVID-19 daily data 7 days (EN): [qc/covid-data-daily-7-days-en/synthese-7jours-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Cases by region 7 days (FR): [qc/cases-by-region-7-days/cas-region-7jours.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Cases by region 7 days (EN): [qc/cases-by-region-7-days-en/cas-region-7jours-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Cumulative deaths by region (EN): [qc/cumulative-deaths-by-region-en/deces-region-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Cases percentage by age group (EN): [qc/cases-percentage-by-age-group-en/pourcentage-cas-age-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Deaths percentage by age group (EN): [qc/deaths-percentage-by-age-group-en/pourcentage-deces-age-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Recent daily cases by region (FR): [qc/recent-daily-cases-by-region/cas-region.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Recent daily cases by region (EN): [qc/recent-daily-cases-by-region-en/cas-region-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccination of priority groups (FR): [qc/vaccination-of-priority-groups/20-279-07WF_Previsions_vaccination.pdf](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccination of priority groups (EN): [qc/vaccination-of-priority-groups-en/20-279-07WA_Previsions_vaccination-anglais.pdf](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Situation in living environments for the elderly and vulnerable (RPA and CHSLD): [qc/status-report-cases-and-deaths-by-rpa-and-chsld/etat_situation_milieux-de-vie.pdf](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Données de vaccination contre la COVID-19 au Québec](https://www.inspq.qc.ca/covid-19/donnees/vaccination)
    * Webpage: [qc/inspq-data-webpage/inspq-data-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination by RSS time series: [qc/vaccination-by-rss-time-series/vaccination.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cumulative vaccination adverse events by vaccine type: [qc/cumulative-vaccination-adverse-events-by-vaccine-type/vaccination-mci.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 - Portrait quotidien des cas confirmés ](https://www.donneesquebec.ca/recherche/dataset/covid-19-portrait-quotidien-des-cas-confirmes)
    * Cumulative time series of confirmed cases and deaths: [qc/cumulative-confirmed-cases-deaths-time-series/COVID19_Qc_RapportINSPQ_HistoVigie.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cumulative snapshot of confirmed cases and deaths by region, age group and sex: [qc/cumulative-confirmed-cases-deaths-by-region-age-sex/COVID19_Qc_RapportINSPQ_VigieCategories.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 - Portrait quotidien de la vaccination](https://www.donneesquebec.ca/recherche/dataset/covid-19-portrait-quotidien-de-la-vaccination)
    * Doses administered by region of administration: [qc/vaccine-doses-admin-by-rss-time-series/COVID19_Qc_Vaccination_RegionAdministration.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Doses administered by region of residence: [qc/vaccine-doses-admin-by-rss-of-residence-time-series/COVID19_Qc_Vaccination_RegionResidence.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Doses administered by age group: [qc/vaccine-doses-admin-by-age-group-time-series/COVID19_Qc_Vaccination_CatAge.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Upcoming first dose appointments by region of administration: [qc/first-vaccine-dose-appointments-by-rss/COVID19_Qc_RDVVaccination_RegionAdministration.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Upcoming 1st dose appointments by age group: [qc/first-vaccine-dose-appointments-by-age-group/COVID19_Qc_RDVVaccination_CatAge.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 - Portrait quotidien du statut vaccinal des nouveaux cas et des nouvelles hospitalisations](https://www.donneesquebec.ca/recherche/dataset/covid-19-portrait-quotidien-du-statut-vaccinal-des-nouveaux-cas-et-des-nouvelles-hospitalisations)
    * New cases by age and vaccination status time series: [qc/new-cases-by-age-and-vaccination-status-timeseries/COVID19_Qc_RapportINSPQ_CasSelonStatutVaccinalEtAge.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * New hospitalizations by age and vaccination status time series: [qc/new-hosp-by-age-and-vaccination-status-timeseries/COVID19_Qc_RapportINSPQ_HospitalisationsSelonStatutVaccinalEtAge.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 vaccination data](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/covid-19-vaccination-data/)
    * Webpage (FR): [qc/qc-vaccination-webpage-fr/qc-vaccination-webpage-fr.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage (EN): [qc/qc-vaccination-webpage-en/qc-vaccination-webpage-en.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination situation (FR): [qc/vaccination-situation/situation-vaccination.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine doses received (FR): [qc/vaccine-doses-received-7-days/doses-vaccins-7jours.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination situation (EN): [qc/vaccination-situation-en/situation-vaccination-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccine doses administered by RSS (FR): [qc/vaccine-doses-admin-by-rss/doses-vaccins.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccine doses administered by RSS (EN): [qc/vaccine-doses-admin-by-rss-en/doses-vaccins-en.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccination by age group: [qc/vaccination-by-age-group/tableau-suivi-vaccination-groupe-age.jpg](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Variants de SRAS-CoV-2 sous surveillance rehaussée](https://inspq.qc.ca/covid-19/donnees/variants)
    * Variants under enhanced surveillance (cumulative) 2: [qc/variants-2/variants-cumul.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Variants under enhanced surveillance (cumulative) 2 (alternative): [qc/vvariants-2-alternative/variants-cumul-v.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Variants under enhanced surveillance (cumulative) 2 (archived): [qc/variants-2-archived/variants-cumul-ARCHIVES.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Variants under enhanced surveillance (cumulative) 2 (last 8 weeks, archived): [qc/variants-2-last-8-weeks-archived/variants-cumul-8s-ARCHIVES.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Variant screening time series by RSS (weekly) 2: [qc/variant-screening-time-series-by-rss-weekly-2/variants-semaines.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Variant screening time series by RSS (weekly) 2 (archived): [qc/variant-screening-time-series-by-rss-weekly-2-archived/variants-semaines-ARCHIVES.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Variants under enhanced surveillance (cumulative): [qc/variants/variants.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Variant screening time series by RSS (cumulative): [qc/variant-screening-time-series-by-rss-cumulative/variants-criblage.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Variant screening time series by RSS (weekly): [qc/variant-screening-time-series-by-rss-weekly/variants-criblage-sem.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Variant Rt time series: [qc/variants-rt-time-series/variants-rt.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Projection of variant dominance: [qc/variants-dominance-projection/variants-proj.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Delta variant screening time series (weekly): [qc/variant-delta-time-series-weekly/variant-delta.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
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
    * Time series by region: [qc/covid-time-series-by-region/PL_DATE.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Data (original): [qc/covid-data/combine.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Charts (original): [qc/covid-data-charts/combine2.csv](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Conditions médicales préexistantes et COVID-19 (INSPQ)](https://www.inspq.qc.ca/covid-19/donnees/conditions-medicales-preexistantes)
    * Deaths by RSS (health region) and number of pre-existing conditions: [qc/deaths-by-rss-and-pre-existing-conditions/comorbidite.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Données COVID-19 par âge et sexe au Québec](https://www.inspq.qc.ca/covid-19/donnees/age-sexe)
    * Dataset: [qc/covid-data-by-age-and-sex/PL_AGE_SEXE.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Faits saillants des cas de COVID-19 dans les écoles du Québec](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/faits-saillants-covid-ecoles/)
    * Webpage (FR): [qc/schools-highlights-webpage/schools-highlights-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage (EN): [qc/schools-highlights-webpage-en/schools-highlights-webpage-en.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Liste des écoles comptant des cas de COVID-19](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/liste-des-cas-de-covid-19-dans-les-ecoles/)
    * Webpage (FR): [qc/schools-list-of-schools-webpage/schools-list-of-schools-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage (EN): [qc/schools-list-of-schools-webpage-en/schools-list-of-schools-webpage-en.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Dataset (CSV): [qc/schools-list-of-schools-csv/Liste_ecole_DCOM.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Report (PDF FR): [qc/schools-list-of-schools/reseauScolaire_listeEcoles.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Report (PDF EN): [qc/schools-list-of-schools-en/reseauScolaire_listeEcoles_ANG.pdf](http://data.opencovid.ca/archive/index.html#archive/)
* [Portrait quotidien des hospitalisations](https://www.donneesquebec.ca/recherche/dataset/covid-19-portrait-quotidien-des-hospitalisations)
    * Daily hospitalizations by RSS and care unit: [qc/daily-hosp-by-rss-and-care-unit/COVID19_Qc_HistoHospit.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Daily hospitalizations by age group: [qc/daily-hosp-by-age-group/COVID19_Qc_HospitCatAge.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Weekly deaths in Quebec](https://statistique.quebec.ca/fr/document/nombre-hebdomadaire-de-deces-au-quebec)
    * Weekly deaths in Quebec by age group: [qc/weekly-deaths-by-age-group/DecesSemaine_QC_GrAge.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Weekly deaths in Quebec by region: [qc/weekly-deaths-by-region/DecesSemaine_QC_Region.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Weekly deaths in Quebec by sex: [qc/weekly-deaths-by-sex/DecesSemaine_QC_Sexe.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
* []()
    * Highlights - public and private school system (FR): [qc/schools-highlights/reseauScolaire_faitsSaillants.pdf](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Highlights - public and private school system (EN): [qc/schools-highlights-en/reseauScolaire_faitsSaillants_ANG.pdf](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]

<details>
<summary><i>Montreal</i></summary>

* [Situation du coronavirus (COVID-19) à Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/situation-du-coronavirus-covid-19-a-montreal/)
    * Montréal cases and deaths by CIUSSS: [qc/montreal-cases-and-deaths-by-ciusss/ciusss.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Montréal cases by area: [qc/montreal-cases-by-area/municipal.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Montréal cases and deaths by age group: [qc/montreal-cases-and-deaths-by-age-group/grage.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Montréal cases and deaths by sex: [qc/montreal-cases-and-deaths-by-sex/sexe.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Montréal epidemic curve: [qc/montreal-epidemic-curve/courbe.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Données sur la vaccination COVID-19 à Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/vaccination/donnees/)
    * Vaccine coverage by neighbourhood (2): [qc/montreal-vaccine-coverage-by-neighbourhood-2/VAXarronMTL_ADEQ.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine coverage by age group (3): [qc/montreal-vaccine-coverage-by-age-group-3/VAXparGrpAGE_CSVuploadv3_ADEQ.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine administration time series (2): [qc/montreal-vaccine-administration-time-series-v2/VAXparJOUR_CSVuploadv2.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine coverage by age group: [qc/montreal-vaccine-coverage-by-age-group/VAXparGrpAGE_CSVupload.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccine coverage by neighbourhood: [qc/montreal-vaccine-coverage-by-neighbourhood/VAXarrondissementsMTL.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccine coverage by age group (2): [qc/montreal-vaccine-coverage-by-age-group-2/VAXparGrpAGE_CSVuploadv2.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Neighbourhoods: [qc/montreal-vaccine-dashboard-neighbourhoods/Arrondissements_et_municipalites.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
    * Vaccine administration time series: [qc/montreal-vaccine-administration-time-series/VAXparJOUR_googledrive.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
</details>
</details>
<details>
<summary><b>Saskatchewan</b></summary>

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
* [Saskatchewan's Dashboard - Hospitalized Cases](https://dashboard.saskatchewan.ca/health-wellness/covid-19-cases/hospitalized)
    * Dataset: [sk/hosp-icu-by-region/hospitalized.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage: [sk/hosp-icu-by-region-webpage/hospitalized-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables: [sk/hosp-icu-by-region-highlights-charts-tables/health-wellness-covid-19-cases-hospitalized.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables (legacy): [sk/hosp-icu-by-region-highlights-charts-tables-legacy/health-wellness-covid-19-cases-hospitalized.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Saskatchewan's Dashboard - Seven-day Average of Daily New Cases](https://dashboard.saskatchewan.ca/health-wellness/covid-19/seven-day-average-of-new-covid-cases)
    * Dataset: [sk/seven-day-avg-cases-by-region/seven-day-average-of-new-covid-cases.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage: [sk/seven-day-avg-cases-by-region-webpage/seven-day-average-of-new-covid-cases-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables: [sk/seven-day-avg-cases-by-region-highlights-charts-tables/health-wellness-covid-19-seven-day-average-of-new-covid-cases.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables (legacy): [sk/seven-day-avg-cases-by-region-highlights-charts-tables-legacy/health-wellness-covid-19-seven-day-average-of-new-covid-cases.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Saskatchewan's Dashboard - Total Doses](https://dashboard.saskatchewan.ca/health-wellness/covid-19-vaccines/vaccines)
    * Dataset: [sk/vaccination-by-region/vaccines.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage: [sk/vaccine-delivery-webpage/vaccine-delivery-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables: [sk/vaccination-by-region-highlights-charts-tables/health-wellness-covid-19-vaccines-vaccines.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights, charts, tables (legacy): [sk/vaccination-by-region-highlights-charts-tables-legacy/health-wellness-covid-19-vaccines-vaccines.json](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [Cases and Risk of COVID-19 in Saskatchewan](https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/cases-and-risk-of-covid-19-in-saskatchewan)
    * Webpage: [sk/summary-and-variant-webpage/summary-and-variant-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
</details>
<details>
<summary><b>Yukon</b></summary>

* [Case and vaccine counts: COVID-19](https://yukon.ca/en/case-counts-covid-19)
    * Webpage: [yt/yukon-case-counts-webpage/yukon-case-counts-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Current COVID-19 situation](https://yukon.ca/en/health-and-wellness/covid-19-information/latest-updates-covid-19/current-covid-19-situation)
    * Webpage: [yt/yukon-current-situation-webpage/yukon-current-situation-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Vaccine tracker](https://yukon.ca/this-is-our-shot)
    * Webpage: [yt/yukon-vaccine-tracker-webpage/yukon-vaccine-tracker-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [News releases: COVID-19 pandemic (2021)](https://yukon.ca/en/health-and-wellness/covid-19/updates-covid-19-pandemic)
    * Webpage: [yt/yukon-covid-updates-2021-webpage/yukon-covid-updates-2021-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Enforcement statistics: COVID-19](https://yukon.ca/en/health-and-wellness/covid-19-information/borders-and-travel-covid-19/find-enforcement-statistics)
    * Webpage: [yt/yukon-covid-enforcement-webpage/yukon-covid-enforcement-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Potential COVID-19 exposure notices](https://yukon.ca/en/health-and-wellness/covid-19-information/your-health-covid-19/potential-covid-19-exposure-notices)
    * Webpage: [yt/yukon-potential-exposures-webpage/yukon-potential-exposures-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [News releases: COVID-19 pandemic (2020)](https://yukon.ca/en/health-and-wellness/covid-19-information/latest-updates-covid-19/2020-news-releases-covid-19)
    * Webpage: [yt/yukon-covid-updates-2020-webpage/yukon-covid-updates-2020-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
</details>
<details>
<summary><b>Other: Non-governmental sources</b></summary>


<details>
<summary><i>Canada</i></summary>

* [Radio-Canada - The latest numbers](https://ici.radio-canada.ca/info/2020/coronavirus-covid-19-pandemie-cas-carte-maladie-symptomes-propagation/index-en.html)
    * Quebec data: [other/can/radio-canada-quebec-data/quebec.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Canada data: [other/can/radio-canada-canada-data/canada.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * USA data: [other/can/radio-canada-usa-data/usa.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * International data: [other/can/radio-canada-international-data/international.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Unofficial COVID Alert Dashboard](https://github.com/uhengart/covid-alert-dashboard)
    * Diagnosis Keys Analysis: [other/can/unofficial-covid-alert-dashboard-analysis/DiagnosisKeysAnalysis.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Upload Delay: [other/can/unofficial-covid-alert-dashboard-upload-delay/UploadDelay.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cumulative cases reported plot: [other/can/unofficial-covid-alert-dashboard-cumulative-cases-reported-plot/Cumulative.png](http://data.opencovid.ca/archive/index.html#archive/)
    * Daily number and percentage of cases reported plot: [other/can/unofficial-covid-alert-dashboard-daily-and-percent-cases-reported-plot/Daily.png](http://data.opencovid.ca/archive/index.html#archive/)
    * Reporting delay plot: [other/can/unofficial-covid-alert-dashboard-reporting-delay-plot/Delay.png](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 - McDonald's Tracker](https://news.mcdonalds.ca/covid-19-tracker)
    * Webpage: [other/can/mcdonalds-tracker/mcdonalds-tracker-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 - Loblaw Companies Ltd.](https://www.loblaw.ca/en/covid-19/)
    * Webpage: [other/can/loblaw-companies-tracker/loblaw-companies-tracker.html](http://data.opencovid.ca/archive/index.html#archive/)
* [CTV: Tracking variants of the novel coronavirus in Canada](https://www.ctvnews.ca/health/coronavirus/tracking-variants-of-the-novel-coronavirus-in-canada-1.5296141)
    * Webpage: [other/can/ctv-variant-tracker-webpage/ctv-variant-tracker-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Dataset: [other/can/ctv-variant-tracker/COVID-Variants.txt](http://data.opencovid.ca/archive/index.html#archive/)
* [Canada COVID-19 School Case Tracker](https://masks4canada.org/canada-covid-19-school-case-tracker/)
    * Dataset: [other/can/canada-covid-19-school-case-tracker/Canada_COVID-19_School_Report_Tracker.kml](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
* [COVID-19 Cases in Canadian Slaughterhouses](https://factoryfarmcollective.ca/covid-19/)
    * Webpage: [other/can/covid-cases-in-canadian-slaughterhouses-webpage/covid-cases-in-canadian-slaughterhouses-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) [inactive, no longer updated]
</details>

<details>
<summary><i>Quebec</i></summary>

* [Covid Écoles Québec: Number of schools](https://www.covidecolesquebec.org/nombre-dcoles-20212022)
    * Dataset: [other/qc/covid-ecoles-quebec-school-list/COVIDECOLESQUEBEC.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
</details>
</details>


## Notes about the data archive

On several occasions, the nightly archival script has failed to run. Depending on when the failure was identified, this may have resulted in a partial or total loss of archival data for that day. A list of these days is provided below:

* 2020-10-21
* 2020-11-19

In addition, the method of archiving websites (HTML files) was modified on 2021-12-30. This may have caused a handful of HTML files not to be marked duplicates of the previous day's file when they otherwise would have been.

## Notes about the archival tool

Updates to the Canadian COVID-19 Data Archive are managed by *archiver.py* via the [`archivist`](https://github.com/jeanpaulrsoucy/archivist) package. Development of `archivist` originally took place in this repository but has since been migrated to its [own repository](https://github.com/jeanpaulrsoucy/archivist).

*archiver.py* can run in two modes:
* `python archiver.py -m prod`: Download datasets and upload them to the archive.
* `python archiver.py -m test`: Don't upload datasets to the archive, just test that they can be successfully downloaded. Send an email summary of datasets that cannot be downloaded, if any.

The archival tool relies on setting environmental variables to function properly. See [*archiver.py*](https://github.com/ccodwg/Covid19CanadaArchive/blob/master/archiver.py) for more details.

## Acknowledgements

Shannon Fiedler created the banner image for the Canadian COVID-19 Data Archive.

Many people are to thank for contributing archived data and code to this repository:

[Jens von Bergmann](https://github.com/mountainMath) / [Simon Coulombe](https://github.com/simoncoulombe) / [James E. Wright](https://twitter.com/JWright159) / [Farbod Abolhassani](https://github.com/farbodab) / [Shelby L. Sturrock](https://twitter.com/shelbysturrock) / [Safa Ahmad](https://twitter.com/birdseye47) / [Jacques Marcoux](https://twitter.com/jacquesmarcoux) / [Shraddha Pai](https://twitter.com/spaiglass) / [Matti Aleve](https://twitter.com/maleve) / [Scott van Millingen](https://github.com/svmillin) / [Robson Fletcher](https://twitter.com/CBCFletch) / [Les Perreaux](https://twitter.com/perreaux) / Allen Kwan ([Twitter](https://twitter.com/allenkwan)/[LinkedIn](https://www.linkedin.com/in/allen-kwan/)) / Christine Hagyard ([Twitter](https://twitter.com/ChrisHagyard)/[LinkedIn](https://www.linkedin.com/in/christine-hagyard/))
 / Amy Bihari ([Twitter](https://twitter.com/AmyBihari)/[LinkedIn](https://www.linkedin.com/in/amy-bihari/)) / Razieh Faraji ([Twitter](https://twitter.com/raziehfaraji)/[LinkedIn](https://www.linkedin.com/in/raziehfaraji/)) / [David Lussier](https://twitter.com/LussiD) / [Matthias Schoettle](https://github.com/mschoettle) / [Jeremy Moreau](https://github.com/jeremymoreau)
