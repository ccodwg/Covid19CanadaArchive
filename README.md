# Archive of Canadian COVID-19 Data

## THE DATA IN THIS ARCHIVE HAVE MOVED TO A NEW SERVER. To locate data, please use the file explorer: [http://data.opencovid.ca/archive/index.html#archive/](http://data.opencovid.ca/archive/index.html#archive/).

###### The root directory of the file server is: http://data.opencovid.ca/archive/. For example, the PHAC Epidemiology Update from November 4, 2020 may be downloaded at the following URL: [http://data.opencovid.ca/archive/can/epidemiology-update-2/covid19-download_2020-11-04_23-38.csv](http://data.opencovid.ca/archive/can/epidemiology-update-2/covid19-download_2020-11-04_23-38.csv).
###### From now on, this archive will be used only to store and collorate on archival scripts and metadata. Links to the data have been updated. Other options to explore and download the data will be available soon.

This repository provides automated, daily backups of COVID-19 data from Canadian governmental and non-governmental sources.

**File name timestamps are given in ET (America/Toronto) in the following format: %Y-%m-%d_%H-%M.** The script is run nightly around 23:00 ET.

All code in this repository is covered by the [MIT License](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/blob/master/LICENSE). Licenses and terms of use for each archived dataset are given below.

This repository is maintained by [Jean-Paul R. Soucy](https://jeanpaulsoucy.com/) on behalf of the [COVID-19 Open Data Working Group](https://opencovid.ca/).

Table of contents:

* [Contribution guide](#contribution-guide)
  * [Add a new dataset](#add-a-new-dataset)
  * [Retire an inactive dataset](#retire-an-inactive-dataset)
  * [Contribute historical data](#contribute-historical-data)
* [Recommended citation](#recommended-citation)
* [Running archiver.py](#running-archiverpy)
* [Data sources/terms of use/supplementary material](#data-sourcesterms-of-usesupplementary-material)
  * [Alberta](#alberta)
     * [Edmonton](#edmonton)
  * [British Columbia](#british-columbia)
  * [Canada](#canada)
  * [Manitoba](#manitoba)
     * [Winnipeg](#winnipeg)
  * [New Brunswick](#new-brunswick)
  * [Northwest Territories](#northwest-territories)
  * [Nova Scotia](#nova-scotia)
  * [Nunavut](#nunavut)
  * [Ontario](#ontario)
     * [Toronto](#toronto)
     * [Ottawa](#ottawa)
  * [Quebec](#quebec)
     * [Montreal](#montreal)
  * [Prince Edward Island](#prince-edward-island)
  * [Saskatchewan](#saskatchewan)
  * [Yukon](#yukon)
  * [Other: Non-governmental sources](#other-non-governmental-sources)
     * [Canada](#canada-1)
     * [Quebec](#quebec-1)
  * [COVID-19 Canada Open Data Working Group](#covid-19-canada-open-data-working-group)
* [Data notes](#data-notes)
* [Acknowledgements](#acknowledgements)

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

COVID-19 Canada Open Data Working Group. Archive of Canadian COVID-19 Data. https://github.com/ccodwg/Covid19CanadaArchive. (Access date).

## Running archiver.py

*archiver.py* can run in two modes:
* `python archiver.py prod`: Download files and upload them to the server.
* `python archiver.py test`: Don't upload files to the server, just test that they can be successfully downloaded.

The script relies on setting environmental variables to function properly. See *archiver.py* for more details.

## Data sources/terms of use/supplementary material

The sources and terms of use for each included dataset are linked below. Supplementary material such as data dictionaries and codebooks are also included in the list below, if available. These files are included with the relevant datasets in a directory named `supplementary`.

### Alberta

* [COVID-19 Alberta statistics](https://www.alberta.ca/stats/covid-19-alberta-statistics.htm)
    * [ab/cases/covid19dataexport.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence); see also the disclaimer in the "data notes" tab of the [website](https://www.alberta.ca/stats/covid-19-alberta-statistics.htm)
* [COVID-19 relaunch status map](https://www.alberta.ca/maps/covid-19-status-map.htm)
    * [ab/active-cases-by-region/covid19dataexport-relaunch.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence)
* [COVID-19 school status map](https://www.alberta.ca/schools/covid-19-school-status-map.htm)
    * [ab/school-status-by-region/covid19dataexport-schools.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence)
* [Cases in Alberta](https://www.alberta.ca/covid-19-alberta-data.aspx)
    * Webpage: [ab/ab-cases-webpage/ab-cases-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence)
* [COVID-19 vaccine distribution](https://www.alberta.ca/covid19-vaccine.aspx)
    * Webpage: [ab/ab-vaccine-distribution-webpage](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence)

#### Edmonton

* [COVID-19 in Alberta: Current cases by local geographic area (Edmonton)](https://data.edmonton.ca/Community-Services/COVID-19-in-Alberta-Current-cases-by-local-geograp/ix8f-s9xp)
    * [ab/edmonton-cases-by-area/COVID-19_in_Alberta__Current_cases_by_local_geographic_area.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: Assumed to be [City of Edmonton Open Data Terms of Use](https://data.edmonton.ca/stories/s/City-of-Edmonton-Open-Data-Terms-of-Use/msh8-if28/)

### British Columbia

* [BC COVID-19 Data](http://www.bccdc.ca/health-info/diseases-conditions/covid-19/data)
    * Case data: [bc/case-data/BCCDC_COVID19_Dashboard_Case_Details.csv](http://data.opencovid.ca/archive/index.html#archive/)
        * The format of the column "Reported_Date" is %Y-%m-%d except for 2020-08-24 to 2020-08-26 where it is %m/%d/%Y.
        * Due to Excel's aggressive date conversion, the column "Age_Group" may occasionally contain "19-Oct" rather than "10-19" (e.g., see this [Twitter thread](https://twitter.com/vb_jens/status/1298661723876909056)). This archive may not represent a perfect record of the appearance of "19-Oct" as some files may have been processed in Excel prior to upload, either removing or introducing the anomalous value.
        * Data parsing advice for the above issues in R:
        ```
        library(dplyr)
        dat <- read.csv("http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv") %>%
          mutate(
            Reported_Date = coalesce(as.Date(Reported_Date, "%Y-%m-%d"), as.Date(Reported_Date, "%m/%d/%Y")),
            Age_Group = recode(Age_Group, "19-Oct" = "10-19")
          )
        ```     
        * On 2020-11-16 (a Monday), BCCDC retracted their daily datasets from their website and replaced them with datasets from the previous Friday (2020-11-13). These datasets have been saved as "BCCDC_COVID19_Dashboard_Case_Details_2020-11-16_23-05.csv" and "BCCDC_COVID19_Dashboard_Lab_Information_2020-11-16_23-05", whereas the retracted datasets have been preserved as "BCCDC_COVID19_Dashboard_Case_Details_2020-11-16_19-27" and "BCCDC_COVID19_Dashboard_Lab_Information_2020-11-16_19-27".   
    * Laboratory data: [bc/laboratory-data/BCCDC_COVID19_Dashboard_Lab_Information.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Regional data: [bc/regional-case-summary/BCCDC_COVID19_Regional_Summary_Data.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Disclaimer and data notes](http://www.bccdc.ca/Health-Info-Site/Documents/BC_COVID-19_Disclaimer_Data_Notes.pdf)
* [British Columbia COVID-19 Dashboard](https://experience.arcgis.com/experience/a6f23959a8b14bfa989e3cda29297ded)
    * Dashboard BC and Canada cumulative testing rate: [bc/bc-canada-cumulative-testing-rate/BC_COVID19__BC_Canadian_Testing_Rates_View.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard case demographics by Regional Health Authority: [bc/case-demographics-by-rha/BC_COVID19_Dashboard_Case_Details_Production.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard testing time series by Regional Health Authority: [bc/testing-timeseries-by-rha/BC_COVID19_Lab_Information.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard Vaccine Doses by Regional Health Authority: [bc/vaccine-doses-by-rha/BC_COVID19Dashboard_Vaccine_Counts.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard case time series by Health Service Delivery Area: [bc/case-time-series-by-hsda/BCCOVID19_Dashboard_Regional_Summary_Data.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard cumulative case, death, recovered, hospitalization, ICU data by Regional Health Authority: [bc/cumulative-case-death-recover-hosp-icu-by-rha/COVID19_Cases_by_BC_Health_Authority.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Dashboard Regional Health Authority labels: [bc/rha-labels/HA_Labels.json](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Public Exposures](http://www.bccdc.ca/health-info/diseases-conditions/covid-19/public-exposures)
    * Public exposures webpage screenshot: [bc/public-exposures-webpage/public-exposures-screenshot.png](http://data.opencovid.ca/archive/index.html#archive/)
    * Public exposures - flights: [bc/public-exposures-flights/public-exposures-flights-tables-Current.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * [Public exposures - cruises, long distance bus, train, work sites, public events](http://www.bccdc.ca/Health-Info-Site/Documents/Archived_COVID-19_Exposures.pdf): [bc/public-exposures-cruises-bus-train-work-public/Archived_COVID-19_Exposures.pdf](http://data.opencovid.ca/archive/index.html#archive/) (Not included as part of the nightly update, as it is archived)
    * Public exposures Fraser webpage: [bc/regional-exposure-events-fraser-webpage/regional-exposure-events-fraser-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) (warning: some early files are .png screenshots and named differently)
    * Public exposures Interior webpage: [bc/regional-exposure-events-interior-webpage/regional-exposure-events-interior-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) (warning: some early files are .png screenshots and named differently)
    * Public exposures Island webpage: [bc/regional-exposure-events-island-webpage/regional-exposure-events-island-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) (warning: some early files are .png screenshots and named differently)
    * Public exposures Northern webpage: [bc/regional-exposure-events-northern-webpage/regional-exposure-events-northern-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) (warning: some early files are .png screenshots and named differently)
    * Public exposures Vancouver Coastal webpage: [bc/regional-exposure-events-vancouver-coastal-webpage/regional-exposure-events-vancouver-coastal-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) (warning: some early files are .png screenshots or .pdf files and named differently and/or formatted differently)
    * School exposures Fraser webpage: [bc/school-exposures-fraser-webpage/school-exposures-fraser-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) (warning: some early files are .png screenshots and named differently)
    * School exposures Interior webpage: [bc/school-exposures-interior-webpage/school-exposures-interior-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) (warning: some early files are .png screenshots and named differently)
    * School exposures Island webpage: [bc/school-exposures-island-webpage/school-exposures-island-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) (warning: some early files are .png screenshots and named differently; due to an error, this webpage was not captured during a portion of Janaury to March of 2021)
    * School exposures Northern webpage: [bc/school-exposures-northern-webpage/school-exposures-northern-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) (warning: some early files are .png screenshots and named differently)
    * School exposures Vancouver Coastal webpage: [bc/school-exposures-vancouver-coastal-webpage/school-exposures-vancouver-coastal-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) (warning: some early files are .png screenshots and named differently)
    * Vancouver Coastal reported its first school outbreak on 2020-09-22. However, due to a change in the page format, the first day these data were captured in the dataset was 2020-10-05. Screenshots prior to this date ommit the list of schools. However, it is unlikely that any schools were removed from the list prior to it first being captured on 2020-10-05.
    * Terms of use: TBD

### Canada

* [Epidemiological summary of COVID-19 cases in Canada](https://health-infobase.canada.ca/covid-19/epidemiological-summary-covid-19-cases.html) / [COVID-19 Situational Awareness Dashboard](https://health-infobase.canada.ca/covid-19/dashboard/)
    * Epidemiology update / [Data on COVID-19 in Canada](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc): [can/epidemiology-update/covid19.csv](http://data.opencovid.ca/archive/index.html#archive/)
    	* Includes supplementary material: [Data dictionary (English)](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc) and [data dictionary (French)](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc)
* [Epidemiological summary of COVID-19 cases in Canada](https://health-infobase.canada.ca/covid-19/epidemiological-summary-covid-19-cases.html) / [COVID-19 Situational Awareness Dashboard](https://health-infobase.canada.ca/covid-19/dashboard/)
    * Epidemiology update / [Data on COVID-19 in Canada](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc): [can/epidemiology-update/covid19-download.csv](http://data.opencovid.ca/archive/index.html#archive/)
    	* Identical to the above dataset but the date column is in YYYY-MM-DD format instead of DD-MM-YYYY
    	* Includes supplementary material: [Data dictionary (English)](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc) and [data dictionary (French)](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc)
    * Epidemiology summary statements: [can/epidemiology-summary-statements/covid19-epiSummary-statements.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * NML summary: [can/nml-summary/covid19-epiSummary-NML.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * NML weekly testing: [can/nml-weekly-testing/NML_weekly_testing.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Number of cases with detailed case report data: [can/detailed-case-report-n/covid19-nTotal.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases and deaths by health region time series: [can/cases-and-deaths-by-hr-time-series/file_out_v5.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Health region UID table: [can/health-region-uid/covid19-healthregions-hruid.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by exposure setting time series: [can/cases-by-exposure-time-series/covid19-epiSummary-casesovertime.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Epidemic curve by date of illness onset by age group: [can/epidemic-curve-by-age/covid19-epiSummary-epiCurveByAge.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Severity by age group and sex: [can/severity-by-age-and-sex/covid19-epiSummary-severityUpdate.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by severity: [can/cases-by-severity/covid19-epiSummary-severity.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by age group and sex: [can/cases-by-age-and-sex/covid19-epiSummary-agegroups2.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by probable exposure setting: [can/cases-by-probable-exposure-setting/covid19-epiSummary-probableexposure2.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by probable exposure setting and province: [can/cases-by-probable-exposure-setting-and-province/covid19-epiSummary-exposureByPT.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Symptoms summary: [can/symptoms-summary/covid19-epiSummary-symptoms.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Hospitalizaiton, intensive care (ICU), mechanical ventilation: [can/hospitalizations-icu-mechanical-ventilation/covid19-epiSummary-hospVentICU.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases on First Nations reserves: [can/covid-time-series-first-nations-reserves/covid19-isc.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cumulative variants of concern by province: [can/cumulative-variants-of-concern-by-province/covid19-epiSummary-voc.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Situational awareness dashboard update time: [can/situational-awareness-dashboard-update-time/covid19-updateTime.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * PHAC provincial data update notes: [can/provincial-data-update-notes/covid19-epiSummary-exceptions.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada)
* [Testing for COVID-19: Increasing testing supply](https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection/symptoms/testing/increased-supply.html)
    * Webpage: [can/testing-supply-webpage/testing-supply-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada)
* [COVIDTrends](https://health-infobase.canada.ca/covid-19/covidtrends/)
    * Mobility: [can/covidtrends-mobility/mobility.csv](https://drive.google.com/drive/folders/1rywSZlhHQzv7L9r8dIo7_hWgquTG7U45) [dataset is updated only on Thursdays]
    * FluWatchers: [can/covidtrends-fluwatchers/fluwatchers.csv](https://drive.google.com/drive/folders/1l9C7WppFIIc-hSxKRLd8i0dAon6YfbAs) [dataset is updated only on Thursdays]
    * Terms of use: [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada)
* [Vaccines and treatments for COVID-19: Vaccine rollout](https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection/prevention-risks/covid-19-vaccine-treatment/vaccine-rollout.html)
    * [can/vaccine-rollout-webpage/vaccine-rollout-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada)
* [COVID-19 vaccination in Canada - Vaccines administered](https://health-infobase.canada.ca/covid-19/vaccine-administration/)
    * Vaccination administration: [can/vaccination-administration/vaccination-administration.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination administration update date: [can/vaccination-administration-update-date/vaccination-administration-updateDate.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada)
* COVID 19 vaccination in Canada - Vaccines distributed
    * Vaccination distribution: [can/vaccination-distribution/vaccination-distribution.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada)
* [COVID-19 vaccination in Canada - Vaccination coverage](https://health-infobase.canada.ca/covid-19/vaccination-coverage/)
    * Vaccination coverage overall: [can/vaccination-coverage-overall/vaccination-coverage-overall.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage for key populations: [can/vaccination-coverage-keypops/vaccination-coverage-keypops.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by age and sex: [can/vaccination-coverage-by-age-sex/vaccination-coverage-byAgeAndSex.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by age and sex with denominators: [can/vaccination-coverage-by-age-sex-denominators/vaccination-coverage-byAgeAndSexDenominators.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by vaccine type: [can/vaccination-coverage-by-vaccine-type/vaccination-coverage-byVaccineType.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage by province: [can/vaccination-coverage-by-prov/vaccination-coverage-map.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination notes: [can/vaccination-notes/vaccination-notes.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada)
* [COVID-19 vaccination in Canada - Technical notes](https://health-infobase.canada.ca/covid-19/vaccination-coverage/technical-notes.html)
    * Webpage: [can/vaccination-technical-notes-webpage/vaccination-technical-notes-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination coverage data availability by week: [can/vaccination-coverage-data-availability-by-week/vaccination-coverage-dataAvailability.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada)
* [Detailed preliminary information on cases of COVID-19: 6 Dimensions (Aggregated data)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310077401)
    * [can/detailed-preliminary-case-info-aggregated-6-dimensions/13100774.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Includes supplementary material: Footnotes, metadata
    * Terms of use: [Statistics Canada Open Licence](https://www.statcan.gc.ca/eng/reference/licence)
* [Detailed preliminary information on cases of COVID-19: 4 Dimensions (Aggregated data)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310077501)
    * [can/detailed-preliminary-case-info-aggregated-4-dimensions/13100775.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Includes supplementary material: Footnotes, metadata
    * Terms of use: [Statistics Canada Open Licence](https://www.statcan.gc.ca/eng/reference/licence)
* [Detailed preliminary information on confirmed cases of COVID-19 (Revised)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310078101)
    * [can/detailed-preliminary-confirmed-case-info-revised/13100781.csv](http://data.opencovid.ca/archive/index.html#archive/) (Archived as of 2020-12-10, no longer part of the nightly update)
    * Variable value definitions are given in footnotes (see supplementary material).
    * **This file has been processed to avoid the 100mb file limit on GitHub.** (Base file size is > 400mb)
        * Dataset has been pivoted from long to wide (names from: 'Case information', values from: 'VALUE').
        * Columns containing no information have been dropped (GEO, DGUID, UOM, UOM_ID, SCALAR_FACTOR, SCALAR_ID, VECTOR, COORDINATE, STATUS, SYMBOL, TERMINATED, DECIMALS).
        * Example of original data format is preserved (see supplementary material).
    * Includes supplementary material: Footnotes, example of original data format, metadata
    * Terms of use: [Statistics Canada Open Licence](https://www.statcan.gc.ca/eng/reference/licence)
* [Preliminary dataset on confirmed cases of COVID-19, Public Health Agency of Canada](https://www150.statcan.gc.ca/n1/pub/13-26-0003/132600032020001-eng.htm)
    * [can/preliminary-dataset-on-confirmed-cases/COVID19-eng.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Includes supplementary material: user guide and data dictionary, metadata
    * Terms of use: [Statistics Canada Open Licence](https://www.statcan.gc.ca/eng/reference/licence)

### Manitoba

* [Province of Manitoba - COVID-19](https://www.gov.mb.ca/covid19/updates/index.html)
    * Webpage: [mb/manitoba-webpage/manitoba-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [Manitoba COVID-19](https://experience.arcgis.com/experience/f55693e56018406ebbd08b3492e99771)
    * COVID-19 data by RHA and district: [mb/covid-data-by-rha-and-district/covid-data-by-rha-and-district.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by demographics and RHA: [mb/cases-demographics-by-rha/cases-demographics-by-rha.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by status and RHA: [mb/cases-by-status-and-rha/cases-by-status-and-rha.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Manitoba five-day test positivity rate: [mb/five-day-test-positivity/five-day-test-positivity.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Summary statistics by area: [mb/summary-stats-by-area/summary-stats-by-area.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Current status by area: [mb/current-status-by-area/current-status-by-area.json](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 data by RHA and district (JSON to CSV): [mb/covid-data-by-rha-and-district-csv/covid-data-by-rha-and-district.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by demographics and RHA (JSON to CSV): [mb/cases-demographics-by-rha-csv/cases-demographics-by-rha.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by status and RHA (Regional Health Authority) (JSON to CSV): [mb/cases-by-status-and-rha-csv/cases-by-status-and-rha.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Manitoba five-day test positivity rate (JSON to CSV): [mb/five-day-test-positivity-csv/five-day-test-positivity.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
  * [COVID-19 Dashboard: K-12 Schools in Manitoba](https://experience.arcgis.com/experience/6e7af13b3ffb447a99734b0119b169d3/)
    * COVID education statistics summary: [mb/covid-education-summary/covid-education-summary.json](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID educations cases last 2 weeks: [mb/covid-education-cases-last-2-weeks/covid-education-cases-last-2-weeks.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Manitoba school divisions: [mb/school-divisions/school-divisions.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Supplementary: Definitions
    * Terms of use: TBD

#### Winnipeg

* [COVID-19 By-law Enforcement (Winnipeg)](https://data.winnipeg.ca/Neighbourhood-Liveability-Property-Standards-Licen/COVID-19-By-law-Enforcement/ndr6-96vi)
    * [mb/winnipeg-by-law-enforcement/COVID-19_By-law_Enforcement.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence - Winnipeg](https://data.winnipeg.ca/open-data-licence)
    Not included as part of the nightly update, as it does not seem to be receiving regular updates (last new data: June 5, 2020)
* [COVID-19 Designated Active Transportation Route Counts (Winnipeg)](https://data.winnipeg.ca/Transportation-Planning-Traffic-Management/COVID-19-Designated-Active-Transportation-Route-Co/aqka-nz2g)
    * [mb/winnipeg-active-transportation/COVID-19_Designated_Active_Transportation_Route_Counts.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence - Winnipeg](https://data.winnipeg.ca/open-data-licence)
    * Not included as part of the nightly update, as it does not seem to be receiving regular updates (last updated: June 29, 2020)

### New Brunswick

* [New Brunswick COVID-19 Dashboard](https://experience.arcgis.com/experience/8eeb9a2052d641c996dba5de8f25a8aa)
    * Adult residential facilities: : [nb/adult-residential-facilities/adult-residential-facilities.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Airports: [nb/airports/airports.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Counties: [nb/counties/counties.json](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 assessment sites: [nb/covid-assessment-sites/covid-assessment-sites.json](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 compliance by health zone: [nb/covid-compliance-by-health-zone/covid-compliance-by-health-zone.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Provincial case, death, recovered time series: [nb/provincial-case-death-recovered-time-series/provincial-case-death-recovered-time-series.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Provincial cumulative test statistics by age and sex: [nb/provincial-cumulative-test-statistics-by-age-sex/provincial-cumulative-test-statistics-by-age-sex.json](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 vaccine data: [nb/vaccine-data/vaccine-data.json](http://data.opencovid.ca/archive/index.html#archive/)
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
    * Terms of use: TBD
* [Potential Public Exposures](https://www2.gnb.ca/content/gnb/en/corporate/promo/covid-19/potential_public_exposure.html.html)
    * Webpage: [nb/potential-public-exposures-webpage/potential-public-exposures-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD

### Northwest Territories

* [https://www.gov.nt.ca/covid-19/](https://www.gov.nt.ca/covid-19/)
    * Webpage: [nt/nwt-webpage/nwt-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD

### Nova Scotia

* [Coronavirus (COVID-19): case data](https://novascotia.ca/coronavirus/data/)
    * Webpage: [ns/ns-webpage/ns-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases data: [ns/case-data/ns-covid19-data.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: Assumed to be [Open Government Licence – Nova Scotia](https://novascotia.ca/opendata/licence.asp)
* [Nova Scotia COVID-19 Dashboard](https://experience.arcgis.com/experience/204d6ed723244dfbb763ca3f913c5cad)
    * Cases by zone: [ns/cases-by-zone/cases-by-zone.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Zone summary: [ns/zone-summary/zone-summary.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Zone summary cases: [ns/zone-summary-cases/zone-summary-cases.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Community health network summary cases: [ns/chn-summary-cases/chn-summary-cases.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Serious outcomes: [ns/serious-outcomes/serious-outcomes.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Lab testing: [ns/lab-testing/lab-testing.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Lab testing, hospitalization, ICU summary: [ns/lab-testing-summary/lab-testing-summary.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Demographics summary: [ns/demographics-summary/demographics-summary.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Immunizations: [ns/immunizations/immunizations.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Health boundaries: [ns/health-boundaries/health-boundaries.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: Assumed to be [Open Government Licence – Nova Scotia](https://novascotia.ca/opendata/licence.asp)

### Nunavut

* [COVID-19 (Novel Coronavirus)](https://gov.nu.ca/health/information/covid-19-novel-coronavirus)
    * Webpage: [nu/nunavut-webpage/nunavut-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD

### Ontario

* [How Ontario is responding to COVID-19](https://www.ontario.ca/page/how-ontario-is-responding-covid-19)
    * Webpage: [on/ontario-webpage/ontario-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) (warning: some early files are .png screenshots and named differently)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Confirmed positive cases of COVID19 in Ontario](https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario/resource/455fd63b-603d-4608-8216-7d8647f43350)
    * [on/confirmed-positive-cases/conposcovidloc.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Includes supplementary material: [Data dictionary (English and French)](https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario/resource/a2ea0536-1eae-4a17-aa04-e5a1ab89ca9a)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Status of COVID-19 cases in Ontario](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11)
    * [on/status-of-cases/covidtesting.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Includes supplementary material: [Data dictionary (English and French)](https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario/resource/7be0a14c-bf50-4340-9304-2b189d507541)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Status of COVID-19 cases in Ontario by Public Health Unit (PHU)](https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario-by-public-health-unit-phu)
    * [on/status-of-cases-by-phu/cases_by_status_and_phu.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Ontario COVID-19 testing metrics by Public Health Unit (PHU)](https://data.ontario.ca/dataset/ontario-covid-19-testing-metrics-by-public-health-unit-phu)
    * [on/testing-metrics-by-phu/testing_metrics_by_phu.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Ontario COVID-19 testing percent positive by age group](https://data.ontario.ca/dataset/ontario-covid-19-testing-percent-positive-by-age-group)
    * [on/percent-positive-by-age-group/percent_positive_by_agegrp.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [COVID-19 hospital metrics in Ontario by Local Health Integration Network (LHIN) regions](https://data.ontario.ca/dataset/covid-19-hospital-metrics-in-ontario-by-local-health-integration-network-lhin-regions)
    * [on/hosp-icu-by-lhin/lhin_hospital_icu_covid_data.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Effective reproduction number (Re) for COVID-19 in Ontario](https://data.ontario.ca/dataset/effective-reproduction-number-re-for-covid-19-in-ontario)
    * [on/effective_reproduction_number_ontario/effective_reproduction_number_ontario.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [COVID Alert Impact Data](https://data.ontario.ca/dataset/covid-alert-impact-data)
    * [on/covid_alert_downloads_canada/covid_alert_downloads_canada.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * [on/covid-alert-uploads-ontario/covid_alert_positive_uploads_ontario.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [COVID-19 testing locations](https://data.ontario.ca/dataset/covid-19-assessment-centre-locations)
    * [on/testing-locations/locations.json](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Ontario COVID-19 outbreaks data](https://data.ontario.ca/dataset/ontario-covid-19-outbreaks-data)
    * Ongoing outbreaks: [on/ongoing-outbreaks/ongoing_outbreaks.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Summary of cases associated with outbreaks: [on/summary-outbreak-cases/outbreak_cases.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [COVID-19 testing of inmates in Ontario’s Provincial Correctional Institutions](https://data.ontario.ca/dataset/covid-19-testing-of-inmates-in-ontario-s-correctional-institutions)
    * [on/correctional-institutions-inmates-testing/inmatetesting.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Includes supplementary material: [Technical documentation (English and French)](https://data.ontario.ca/dataset/covid-19-testing-of-inmates-in-ontario-s-correctional-institutions/resource/6e2868ab-a242-48d6-9f73-235d19a6668e)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Status of COVID-19 cases in Ontario’s Provincial Correctional Institutions](https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario-s-correctional-institutions)
    * [on/correctional-institutions-status/correctionsinmatecases.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Long-Term Care Home COVID-19 Data](https://data.ontario.ca/dataset/long-term-care-home-covid-19-data)
    * Summary data: [on/long-term-care-home-summary/ltccovidsummary.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Active outbreaks: [on/long-term-care-home-active/activeltcoutbreak.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Resolved outbreaks: [on/long-term-care-home-resolved/resolvedltc.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Includes supplementary material: [Data dictionary (English and French)](https://data.ontario.ca/dataset/long-term-care-home-covid-19-data/resource/adbcf9f8-e473-4f27-b85f-0f05f686067b)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [COVID-19 cases in schools and child care centres](https://www.ontario.ca/page/covid-19-cases-schools-and-child-care-centres)
    * Webpage: [on/cases-schools-and-child-care-centres-webpage/cases-schools-and-child-care-centres-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) (warning: some early files are .png screenshots and named differently)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Schools COVID-19 data](https://data.ontario.ca/dataset/summary-of-cases-in-schools)
    * Summary of cases in schools: [on/schools-summary/schoolcovidsummary.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Schools with active COVID-19 cases: [on/schools-active/schoolsactivecovid.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases in school board partners: [on/school-board-partners/schoolpartnersactivecovid.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Licensed child care settings COVID-19 data](https://data.ontario.ca/dataset/summary-of-cases-in-licensed-child-care-settings)
    * Summary of cases in licensed child care settings: [on/licensed-child-care-settings-summary/lccovidsummary.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Licensed child care centres and agencies with active COVID-19 cases: [on/licensed-child-care-settings-active/lccactivecovid.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [COVID-19 Vaccine Data in Ontario](https://data.ontario.ca/dataset/covid-19-vaccine-data-in-ontario)
    * [on/vaccine-data/vaccine_doses.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [ICES COVID-19 Dashboard](https://www.ices.on.ca/DAS/AHRQ/COVID-19-Dashboard)
    * ICES dashboard percent positivity by FSA: [on/ices-percent-positivity-by-fsa/ICES-COVID19-Testing-Data-FSA-percent-positivity.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * ICES dashboard percent positivity by age group and Public Health Unit (PHU): [on/ices-percent-positivity-by-age-group-and-phu/ICES-COVID19-Testing-Data_PHUxAge-Groups-percent-positivity.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD

#### Toronto

* [City of Toronto Daily Status of COVID-19 Cases](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-daily-status/CityofToronto_COVID-19_Daily_Public_Reporting.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto COVID-19 Summary](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-covid-summary/CityofToronto_COVID-19_Data.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto COVID-19 Neighbourhood Case Data](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-neighbourhood-data/CityofToronto_COVID-19_NeighbourhoodData.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto COVID-19 Neighbourhood Testing Data](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-neighbourhood-test-data/CityofToronto_COVID-19_Testing.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto COVID-19 Monitoring Dashboard](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-monitoring-dashboard/CityofToronto_COVID-19_RecoveryData.xlsx](http://data.opencovid.ca/archive/index.html#archive/)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto COVID-19 Active Outbreaks](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-active-outbreaks/CityofToronto_COVID-19_OutbreakData.xlsx](https://drive.google.com/drive/folders/1Hhnpqrh8AnfIhH80Ss0kY1WWkkxuLeh0
)
    * Include supplementary material: Technical notes - COVID-19 Active Outbreaks - Community and Workplace Settings
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto Ethno-Racial Group, Income, & Infection](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-ethno-racial-income/Ethno-Racial_Group,_Income,_and_COVID-19_Infection.xlsx](http://data.opencovid.ca/archive/index.html#archive/) (original file name is Ethno-Racial Group, Income, and COVID-19 Infection.xlsx, renamed to avoid spaces in file name)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
    * Not included as part of the nightly update, as it does not seem to be receiving regular updates (data as of September 30, 2020)
* [COVID-19 Cases in Toronto](https://open.toronto.ca/dataset/covid-19-cases-in-toronto/)
    * [on/toronto-cases/COVID19_cases.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Data are extracted at 3 PM on the Monday of a given week and posted by Wednesday [dataset is updated only on Wednesdays]
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [University of Toronto COVID-19 tracking](https://www.utoronto.ca/utogether2020/covid19-dashboard)
    * [on/u-of-t-covid-tracking-webpage/u-of-t-covid-tracking-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) (warning: some early files are .png screenshots and named differently)
    * Data are reported every Monday with cumulative cases through the previous Friday [screenshots will be take every day in case the update frequency increases]
    * Terms of use: TBD

#### Ottawa

* [Daily COVID-19 Dashboard (Ottawa)](https://www.ottawapublichealth.ca/en/reports-research-and-statistics/daily-covid19-dashboard.aspx)
    * [Demographics and Source of Infection for Cases, Deaths, and Hospitalizations](https://www.arcgis.com/home/item.html?id=6bfe7832017546e5b30c5cc6a201091b): [on/ottawa-cases-deaths-hosp-demographics-source-of-infection/COVID-19_Cases_and_Deaths_Ottawa_EN.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * [Outbreaks in Healthcare Institutions, Childcare, Summer Camps, and Educational Establishments](https://www.arcgis.com/home/item.html?id=5b24f70482fe4cf1824331d89483d3d3): [on/ottawa-outbreaks-healthcare-childcare-camps-schools/COVID-19_Institutional_Outbreaks.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * [Community Outbreaks](https://open.ottawa.ca/datasets/0df365456c254fbc942fe3d85c3dbf83): [on/ottawa-community-outbreaks/COVID-19_Community_Outbreaks_in_Ottawa.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * [Weekly Rates](https://www.arcgis.com/home/item.html?id=734a327141b14a55b666953c9141abf3): [on/ottawa-weekly-rates/COVID-19_Weekly_Cases_and_Rates_by_Age_in_Ottawa_EN.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * [Estimated Reproduction Number in Ottawa](https://www.arcgis.com/home/item.html?id=d010a848b6e54f4990d60a202f2f2f99): [on/ottawa-estimated-rt/EN_-_Covid-19_Reproduction_Number,_R(t).csv](http://data.opencovid.ca/archive/index.html#archive/)
    * [Testing - Ottawa Residents](https://www.arcgis.com/home/item.html?id=26c902bf1da44d3d90b099392b544b81): [on/ottawa-residents-tested/COVID-19_Ottawa_Residents_Tested_EN.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Ottawa cases and deaths: [on/ottawa-cases-and-deaths/COVID-19_Cases_and_Deaths_in_Ottawa_EN.csv](http://data.opencovid.ca/archive/index.html#archive/) (Archived as of 2020-09-21, no longer part of the nightly update)
    * Ottawa outbreaks in healthcare institutions: [on/ottawa-outbreaks-in-healthcare-institutions/COVID-19_Outbreaks_in_Ottawa_Healthcare_Institutions_EN.csv](http://data.opencovid.ca/archive/index.html#archive/) (Archived as of 2020-09-21, no longer part of the nightly update)
    * Ottawa hospitalization data: [on/ottawa-hospitalization/Hospitalizations_of_Ottawa_residents_with_confirmed_COVID-19.csv](http://data.opencovid.ca/archive/index.html#archive/) (Archived as of 2020-09-21, no longer part of the nightly update)
    * Include supplementary material: User guide, technical guide, overall status assessment
    * Terms of use: [Open Government Licence – City of Ottawa](https://ottawa.ca/en/city-hall/get-know-your-city/open-data#open-data-licence-version-2-0)

### Quebec

When both French and English data files are available, French files should generally be considered definitive (and in many cases, these files have been captured in the archive for a longer duration). The English versions of files avaiable in both languages will always have their directories marked with "-en" at the end.

* [Data on COVID-19 in Québec (province)](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    * [Webpage EN](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/): [qc/qc-webpage-en/qc-webpage-en.html](http://data.opencovid.ca/archive/index.html#archive/)
    * [Webpage FR](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/): [qc/qc-webpage-fr/qc-webpage-fr.html](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 Dashboard: [qc/qc-covid-dashboard/20-210-382W_infographie_sommaire-executif.jpeg](http://data.opencovid.ca/archive/index.html#archive/)
    * Situation in Quebec: [qc/situation-in-quebec/situation-au-quebec.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Correctional facilities - cases among employees (FR): [qc/correctional-cases-employees/donnees_covid_detention_employes_FR.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Correctional facilities - cases among employees (EN): [qc/correctional-cases-employees-en/donnees_covid_detention_employes_EN.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Correctional facilities - cases among detainees (FR): [qc/correctional-cases-detainees/](http://data.opencovid.ca/archive/index.html#archive/)
    * Correctional facilities - cases among detainees (EN): [qc/correctional-cases-detainees/donnees_covid_detention_personnes_incarcerees_EN.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Outbreaks by setting (FR): [qc/outbreaks-by-setting/eclosions-par-milieu.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Outbreaks by setting (EN): [qc/outbreaks-by-setting-en/eclosions-par-milieu-en.csv](https://drive.google.com/drive/folders/1p4EFQ_r4x4wjp76zOwlW9gD7-3sKX4z4) [archived: no longer updated]
    * Cases percentage by age group (FR): [qc/cases-percentage-by-age-group/pourcentage-cas-age.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases percentage by age group (EN): [qc/cases-percentage-by-age-group-en/pourcentage-cas-age-en.csv](https://drive.google.com/drive/folders/1tIW1eONhV1tvhYbappJ44zfvzTpb2RSA) [archived: no longer updated]
    * Deaths percentage by age group (FR): [qc/deaths-percentage-by-age-group/pourcentage-deces-age.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Deaths percentage by age group (EN): [qc/deaths-percentage-by-age-group-en/pourcentage-deces-age-en.csv](https://drive.google.com/drive/folders/1CPP_HMuwljqcktPUgM8TaZK3DF7fRJP9) [archived: no longer updated]
    * Cumulative deaths by region (FR): [qc/cumulative-deaths-by-region/deces-region.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cumulative deaths by region (EN): [qc/cumulative-deaths-by-region-en/deces-region-en.csv](https://drive.google.com/drive/folders/1uL2HHOqEDTl3GoBJDo2EAxkzl2OFw34F) [archived: no longer updated]
    * Recent daily cases by region (FR): [qc/recent-daily-cases-by-region/cas-region.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Recent daily cases by region (EN): [qc/recent-daily-cases-by-region-en/cas-region-en.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 daily data 7 days (FR): [qc/covid-data-daily-7-days/synthese-7jours.csv](http://data.opencovid.ca/archive/index.html#archive/) (Renamed to synthese-7joursV2.csv from synthese-7jours.csv after 2020-11-09; later renamed again to synthese-7jours.csv - a substantial number of files from November and December are missing due to this change)
    * COVID-19 daily data 7 days (EN): [qc/covid-data-daily-7-days-en/synthese-7jours-en.csv](https://drive.google.com/drive/folders/1hiLaw3OLYZK9FIHs68iBheGdJXGRy-9E) [archived: no longer updated]
    * Cases by region 7 days (FR): [qc/cases-by-region-7-days/cas-region-7jours.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Cases by region 7 days (EN): [qc/cases-by-region-7-days-en/cas-region-7jours-en.csv](http://data.opencovid.ca/archive/index.html#archive/)
* [Données de vaccination contre la COVID-19 au Québec](https://www.inspq.qc.ca/covid-19/donnees/vaccination)
    * Vaccination by RSS time series: [qc/vaccination-by-rss-time-series/vaccination.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [COVID-19 vaccination data](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/covid-19-vaccination-data/)
    * [Webpage EN](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/covid-19-vaccination-data/): [qc/qc-vaccination-webpage-en/qc-vaccination-webpage-en.html](http://data.opencovid.ca/archive/index.html#archive/)
    * [Webpage FR](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/donnees-sur-la-vaccination-covid-19/): [qc/qc-vaccination-webpage-fr/qc-vaccination-webpage-fr.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination situation (FR): [qc/vaccination-situation/situation-vaccination.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccination situation (EN): [qc/vaccination-situation-en/situation-vaccination-en.csv](https://drive.google.com/drive/folders/1R3JYs4NT1k2ESctWNN6JfcfimnDkmmsq) [archived: no longer updated]
    * Vaccine doses administered by RSS (FR): [qc/vaccine-doses-admin-by-rss/doses-vaccins.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Vaccine doses administered by RSS (EN): [qc/vaccine-doses-admin-by-rss-en/doses-vaccins-en.csv](http://data.opencovid.ca/archive/index.html#archive/) (note: the first file in this dataset is only available as a screenshot; archived as of 2021-01-14, no longer part of the nightly update)
    * Vaccine doses received (FR): [qc/vaccine-doses-received-7-days/doses-vaccins-7jours.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [Variants de SRAS-CoV-2 sous surveillance rehaussée](https://inspq.qc.ca/covid-19/donnees/variants)
    * [qc/variants/variants.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [Données COVID-19 au Québec (INSPQ)](https://www.inspq.qc.ca/covid-19/donnees)
    * COVID-19 time series by region and demographics: [qc/covid-time-series-by-region-and-demographics/covid19-hist.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 data (charts - summary, time series, and hospitalization by age): [qc/covid-data-charts-summary-time-series-hosp-by-age/manual-data.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Summary by region: [qc/summary-by-region/regions.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Deaths by RSS (health region) and living environment: [qc/deaths-by-rss-and-living-environment/tableau-rpa-new.csv](http://data.opencovid.ca/archive/index.html#archive/) (Renamed from tableau-rpa.csv after 2020-09-16)
    * Cases by RSS (health region) and RLS (local service network): [qc/cases-by-rss-and-rls/tableau-rls-new.csv](http://data.opencovid.ca/archive/index.html#archive/) (Renamed from tableau-rls.csv after 2020-09-16)
    * Comparisons (provinces): [qc/comparisons-provinces/comparaisons_prov.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Comparisons (countries): [qc/comparisons-countries/comparaisons_pays.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Deaths by RSS (health region) and number of pre-existing conditions: [qc/deaths-by-rss-and-pre-existing-conditions](http://data.opencovid.ca/archive/index.html#archive/)
    * COVID-19 time series by region: [qc/covid-time-series-by-region/PL_DATE.csv](http://data.opencovid.ca/archive/index.html#archive/) (Archived as of 2020-10-15, no longer part of the nightly update)
        * [Advice for data process by Simon Coulombe](https://gist.github.com/SimonCoulombe/9a329052ac4cefd421febd8650ed84e2)
    * COVID-19 data: [qc/covid-data/combine.csv](http://data.opencovid.ca/archive/index.html#archive/) (Archived as of 2020-09-16, no longer part of the nightly update)
    * COVID-19 data (charts): [qc/covid-data-charts/combine2.csv](http://data.opencovid.ca/archive/index.html#archive/) (Archived as of 2020-09-16, no longer part of the nightly update)
    * Terms of use: TBD
* [Données COVID-19 par âge et sexe au Québec](https://www.inspq.qc.ca/covid-19/donnees/age-sexe)
    * COVID-19 data by age group and sex: [qc/covid-data-by-age-and-sex/PL_AGE_SEXE.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [Données sur la COVID-19 au Québec](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    * Deaths time series by living environment: [qc/deaths-time-series-by-living-environment/decesquotidien.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [Situation dans les milieux de vie pour personnes aînées et vulnérables](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    * Status report on confirmed cases and deaths by RPA (private residences for seniors): [qc/status-report-cases-and-deaths-by-rpa/etat_situation_rpa.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Status report on confirmed cases and deaths by CHSLD (residential and long-term care centres): [qc/status-report-cases-and-deaths-by-chsld/etat_situation_chsld.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Supplementary material: [Canadian Armed Forces report on their presence in CHSLDs](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec)
    * Terms of use: TBD
* [Liste des écoles comptant des cas de COVID-19](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/liste-des-cas-de-covid-19-dans-les-ecoles/)
    * Webpage (FR): [qc/schools-list-of-schools-webpage/schools-list-of-schools-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * List of schools (CSV): [qc/schools-list-of-schools-csv/Liste_ecole_DCOM.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * List of schools - public and private school system (PDF FR): [qc/schools-list-of-schools/reseauScolaire_listeEcoles.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [List of schools reporting COVID-19 cases](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/list-schools-reporting-covid-19-cases/)
    * Webpage (EN): [qc/schools-list-of-schools-webpage-en/schools-list-of-schools-webpage-en.html](http://data.opencovid.ca/archive/index.html#archive/)
    * PDF list of schools - public and private school system (PDF EN): [qc/schools-list-of-schools-en/reseauScolaire_listeEcoles_ANG.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [Faits saillants des cas de COVID-19 dans les écoles du Québec](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/faits-saillants-covid-ecoles/)
    * Webpage (FR): [qc/schools-highlights-webpage/schools-highlights-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [Highlights - Public and Private School Systems](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/highlights-public-private-school-systems/)
    * Webpage (EN): [qc/schools-highlights-webpage-en/schools-highlights-webpage-en.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [Situation dans les établissements scolaires](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    * Highlights - public and private school system (FR): [qc/schools-highlights/reseauScolaire_faitsSaillants.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Highlights - public and private school system (EN): [qc/schools-highlights-en/reseauScolaire_faitsSaillants_ANG.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Formerly [Situation dans les établissements scolaires relative à la COVID-19](https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/etat_situation_ecole.pdf): qc/schools-list-of-schools/etat_situation_ecole_2020-09-04_2020-09-06/etat_situation_ecole.pdf
    * Formerly [Liste des écoles ayant au moins un cas rapporté de la COVID-19 depuis le 1er septembre 2020](https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/liste-ecole-cas-rapportes.pdf): qc/schools-list-of-schools/liste-ecole-cas-rapportes_2020-09-08_2020-09-09/liste-ecole-cas-rapportes.pdf
    * Terms of use: TBD
* [Portrait quotidien des hospitalisations](https://www.donneesquebec.ca/recherche/dataset/covid-19-portrait-quotidien-des-hospitalisations)
    * Daily hospitalizations by RSS (health region) and care unit: [qc/daily-hosp-by-rss-and-care-unit/COVID19_Qc_HistoHospit.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Daily hospitalizations by age group: [qc/daily-hosp-by-age-group/COVID19_Qc_HospitCatAge.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Supplementary material: List of variables/methodological notes
    * Terms of use: CC-BY-4.0
* Active hospitalizations per hospital (FR)
    * [qc/active-hospitalizations-per-hosp/tableau-hospitalisations.pdf](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* Vaccination of priority groups
    * FR: [vaccination-of-priority-groups](https://drive.google.com/drive/folders/14gHszA6zjkXDPfL7-RT0rfMxhVW8vbDx) [archived: no longer updated]
    * EN: [vaccination-of-priority-groups-en](https://drive.google.com/drive/folders/1ZFdH_8UD1YgpZnF0YLJ0y2AC1mPbIqbZ) [archived: no longer updated]
    * Terms of use: TBD

#### Montreal

* [Situation du coronavirus (COVID-19) à Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/situation-du-coronavirus-covid-19-a-montreal/)
    * **Note that these files are actually semicolon-separated since they use a comma as the decimal marker (rather than a period) and are encoded as ISO 8859-15 (rather than UTF-8)**
    * Montréal cases and deaths by CIUSSS (integrated health and social services centres): [qc/montreal-cases-and-deaths-by-ciusss/ciusss.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Montréal cases by area: [qc/montreal-cases-by-area/municipal.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Montréal cases and deaths by age group: [qc/montreal-cases-and-deaths-by-age-group/grage.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Montréal cases and deaths by sex: [qc/montreal-cases-and-deaths-by-sex/sexe.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Montréal epidemic curve: [qc/montreal-epidemic-curve/courbe.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD

### Prince Edward Island

* [PEI COVID-19 Case Data](https://www.princeedwardisland.ca/en/information/health-and-wellness/pei-covid-19-case-data)
    * Webpage: [pe/pei-webpage/pei-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [COVID-19 Vaccination Data](https://www.princeedwardisland.ca/en/information/health-and-wellness/covid-19-vaccination-data)
    * Webpage: [pe/pei-vaccination-webpage/pei-vaccination-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
* [Potential COVID-19 Exposures](https://www.princeedwardisland.ca/en/information/health-and-wellness/potential-covid-19-exposures)
    * Webpage: [pe/pei-potential-exposures-webpage/pei-potential-exposures-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)

### Saskatchewan

* [Saskatchewan's Dashboard - Total Cases](https://dashboard.saskatchewan.ca/health-wellness/covid-19/cases)
    * CSV: [sk/cases-by-region/cases.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage: [sk/cases-by-region-webpage/cases-webpage.html](hhttps://drive.google.com/drive/folders/1m7_t1qB0x-yVpOb6e1Rzfk5uUQ6iFmqO) (warning: some early files are .png screenshots and named differently)
    * Terms of use: TBD
* [Saskatchewan's Dashboard - Total Tests](https://dashboard.saskatchewan.ca/health-wellness/covid-19-tests/tests)
    * CSV: [sk/tests-by-region/tests.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage: [sk/tests-by-region-webpage/tests-webpage.html](http://data.opencovid.ca/archive/index.html#archive/) (warning: some early files are .png screenshots and named differently)
    * Terms of use: TBD
* [Saskatchewan's Dashboard - Hospitalized Cases](https://dashboard.saskatchewan.ca/health-wellness/covid-19-cases/hospitalized)
    * CSV: [sk/hosp-icu-by-region/hospitalized.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage: [sk/hosp-icu-by-region-webpage/hospitalized-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [Saskatchewan's Dashboard - Seven-day Average of Daily New Cases](https://dashboard.saskatchewan.ca/health-wellness/covid-19/seven-day-average-of-new-covid-cases)
    * CSV: [sk/seven-day-avg-cases-by-region/seven-day-average-of-new-covid-cases.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Webpage: [sk/seven-day-avg-cases-by-region-webpage/seven-day-average-of-new-covid-cases-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [Cases and Risk of COVID-19 in Saskatchewan](https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/cases-and-risk-of-covid-19-in-saskatchewan)
    * Webpage: [sk/summary-and-variant-webpage/summary-and-variant-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [Vaccine Delivery Update](https://www.saskatchewan.ca/covid19-vaccine-update)
    * Webpage: [sk/vaccine-delivery-webpage/vaccine-delivery-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD

### Yukon

* [Case counts: COVID-19](https://yukon.ca/en/case-counts-covid-19)
    * Webpage: [yt/yukon-case-counts-webpage/yukon-case-counts-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD

* [Current COVID-19 situation](https://yukon.ca/en/health-and-wellness/covid-19-information/latest-updates-covid-19/current-covid-19-situation)
    * Webpage: [yt/yukon-current-situation-webpage/yukon-current-situation-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD

### Other: Non-governmental sources

#### Canada

* [Canada COVID-19 School Case Tracker](https://masks4canada.org/canada-covid-19-school-case-tracker/)
    * [other/can/canada-covid-19-school-case-tracker/Canada_COVID-19_School_Report_Tracker.kml](http://data.opencovid.ca/archive/index.html#archive/) (original file name is Canada COVID-19 School Report Tracker.kml, renamed to avoid spaces in file name; warning: some early files are in .kmz format, which is compressed but handled almost identically to .kml)
    * Terms of use: TBD
* [COVID-19 - Loblaw Companies Ltd.](https://www.loblaw.ca/en/covid-19/)
    * [other/can/loblaw-companies-tracker/loblaw-companies-tracker.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [COVID-19 - McDonald's Tracker](https://news.mcdonalds.ca/covid-19-tracker)
    * [other/can/mcdonalds-tracker/mcdonalds-tracker-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [Unofficial COVID Alert Dashboard](https://github.com/uhengart/covid-alert-dashboard)
    * Estimated infections per day: [other/can/unofficial-covid-alert-dashboard/estimated_infections_per_day.txt](http://data.opencovid.ca/archive/index.html#archive/) (Replaced after 2020-11-14 by unofficial-covid-alert-dashboard-analysis, no longer part of the nightly update)
    * Diagnosis key analysis: [other/can/unofficial-covid-alert-dashboard-analysis/DiagnosisKeysAnalysis.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Upload delay: [other/can/unofficial-covid-alert-dashboard-upload-delay/UploadDelay.csv](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD
* [Tracking variants of the novel coronavirus in Canada](https://www.ctvnews.ca/health/coronavirus/tracking-variants-of-the-novel-coronavirus-in-canada-1.5296141)
    * Webpage: [other/can/ctv-variant-tracker-webpage/ctv-variant-tracker-webpage.html](http://data.opencovid.ca/archive/index.html#archive/)
    * CTV variant tracker: [other/can/ctv-variant-tracker/COVID-Variants.txt](http://data.opencovid.ca/archive/index.html#archive/)
    * Terms of use: TBD

#### Quebec

* [Covid Écoles Québec: Number of schools](https://www.covidecolesquebec.org/liste-alphabtique)
    * [Excel spreadsheet](https://drive.google.com/file/d/1xOl0uhyx9IuHZfJuRH-OR7BcGFuWYUex/view): [other/qc/covid-ecoles-quebec-school-list/COVIDECOLESQUEBEC.xlsx](http://data.opencovid.ca/archive/index.html#archive/) (original file name is COVIDECOLESQUEBEC_20200905.xlsx, renamed to avoid confusion)
    * Terms of use: TBD

### COVID-19 Canada Open Data Working Group

[Data from the COVID-19 Canada Open Data Working Group](https://opencovid.ca/) is being added on an experimental basis. The full catalogue of historical data will be available in the future.

## Data notes

On several occasions, the nightly archival script has failed to run. Depending on when the failure was identified, this may have resulted in a partial or total loss of archival data for that day. A list of these days is provided below:

* Wednesday, October 21, 2020
* Thursday, November 19, 2020

In the future, a package will be provided to more easily access the data provided in this archive and to document missing or incomplete data.

## Acknowledgements

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
