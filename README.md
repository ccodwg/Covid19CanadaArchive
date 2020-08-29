# Archive of COVID-19 Data from Canadian Government Sources

This repository provides automated, daily backups of COVID-19 data from various Canadian government sources.

**File name timestamps are given in ET (America/Toronto) in the following format: %Y%-m-%d_%H-%M.** The script is run nightly around 23:00 ET.

All code in this repository is covered by the [MIT License](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/blob/master/LICENSE). Licenses and terms of use for each archived dataset are given below.

This repository is maintained by [Jean-Paul R. Soucy](https://jeanpaulsoucy.com/) on behalf of the [COVID-19 Open Data Working Group](https://opencovid.ca/).

## Contributing

Community members may contribute to this repository in three ways:

* Create an issue to request a dataset be added to the archive.
* Create a pull request for *archiver.py* adding the ability to automatically archive a requested or not-yet-implemented dataset.
* Submit archived versions of an existing, requested, or not-yet-implemented dataset. If possible, please use the original file name plus timestamp in the format described above.

## Recommended citation

COVID-19 Canada Open Data Working Group. Archive of COVID-19 Data from Canadian Government Sources. https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data. (Access date).

## Data sources/terms of use

The sources and terms of use for each included dataset are linked below.

### Alberta

* [COVID-19 Alberta statistics](https://www.alberta.ca/stats/covid-19-alberta-statistics.htm)
    * ab/cases/covid19dataexport.csv
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence); see also the disclaimer in the "data notes" tab of the [website](https://www.alberta.ca/stats/covid-19-alberta-statistics.htm)
* [COVID-19 relaunch status map](https://www.alberta.ca/maps/covid-19-status-map.htm)
    * ab/active-cases-by-region/covid19dataexport-relaunch.csv
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence)
* [COVID-19 in Alberta: Current cases by local geographic area (Edmonton)](https://data.edmonton.ca/Community-Services/COVID-19-in-Alberta-Current-cases-by-local-geograp/ix8f-s9xp)
    * ab/edmonton-cases-by-area/COVID-19_in_Alberta__Current_cases_by_local_geographic_area.csv
    * Terms of use: Assumed to be [City of Edmonton Open Data Terms of Use](https://data.edmonton.ca/stories/s/City-of-Edmonton-Open-Data-Terms-of-Use/msh8-if28/)

### British Columbia

* [BC COVID-19 Data](http://www.bccdc.ca/health-info/diseases-conditions/covid-19/data)
    * Case data: bc/case-data/BCCDC_COVID19_Dashboard_Case_Details.csv
        * The format of the column "Reported_Date" is %Y-%m-%d except for 2020-08-24 to 2020-08-26 where it is %m/%d/%Y.
        * Due to Excel's aggressive date conversion, the column "Age_Group" may occasionally contain "19-Oct" rather than "10-19" (e.g., see this [Twitter thread](https://twitter.com/vb_jens/status/1298661723876909056)). This archive may not represent a perfect record of the appearance of "19-Oct" as some files may have been processed in Excel prior to upload, either removing or introducing the anomalous value.
        * Data parsing advice for the above issues in R:
        ```
        library(dplyr)
        dat <- read.csv("http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv") %>%
          mutate(
            Reported_Date = coalesce(as.Date(Reported_Date), as.Date(Reported_Date, "%m/%d/%Y")),
            Age_Group = recode(Age_Group, "19-Oct" = "10-19")
          )
        ```        
    * Laboratory data: bc/laboratory-data/BCCDC_COVID19_Dashboard_Lab_Information.csv
    * Terms of use: [Disclaimer and data notes](http://www.bccdc.ca/Health-Info-Site/Documents/BC_COVID-19_Disclaimer_Data_Notes.pdf)

### Canada

* [Epidemiological summary of COVID-19 cases in Canada](https://health-infobase.canada.ca/covid-19/epidemiological-summary-covid-19-cases.html) / [COVID-19 Situational Awareness Dashboard](https://health-infobase.canada.ca/covid-19/dashboard/)
    * Epidemiology update: can/epidemiology-update/covid19.csv
    * Epidemiology summary statements: can/epidemiology-summary-statements/covid19-epiSummary-statements.csv
    * NML summary: can/nml-summary/covid19-epiSummary-NML.csv
    * NML weekly testing: can/nml-weekly-testing/NML_weekly_testing.csv
    * Number of cases with detailed case report data: can/detailed-case-report-n/covid19-nTotal.csv
    * Cases and deaths by health region time series: can/cases-and-deaths-by-hr-time-series/file_out_v5.csv
    * Health region UID table: can/health-region-uid/covid19-healthregions-hruid.csv
    * Cases by exposure setting time series: can/cases-by-exposure-time-series/covid19-epiSummary-casesovertime.csv
    * Epidemic curve by date of illness onset by age group: can/epidemic-curve-by-age/covid19-epiSummary-epiCurveByAge.csv
    * Severity by age group and sex: can/severity-by-age-and-sex/covid19-epiSummary-severityUpdate.csv
    * Cases by severity: can/cases-by-severity/covid19-epiSummary-severity.csv
    * Cases by age group and sex: can/cases-by-age-and-sex/covid19-epiSummary-agegroups2.csv
    * Cases by probable exposure setting: can/cases-by-probable-exposure-setting/covid19-epiSummary-probableexposure2.csv
    * Symptoms summary: can/symptoms-summary/covid19-epiSummary-symptoms.csv
    * Situational awareness dashboard update time: can/situational-awareness-dashboard-update-time/covid19-updateTime.csv
    * Terms of use: Assumed to be [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada)

### Ontario

* [Confirmed positive cases of COVID19 in Ontario](https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario/resource/455fd63b-603d-4608-8216-7d8647f43350)
    * on/confirmed-positive-cases/conposcovidloc.csv
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Status of COVID-19 cases in Ontario](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11)
    * on/status-of-cases/covidtesting.csv
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [City of Toronto COVID-19 Summary](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * on/toronto-covid-summary/CityofToronto_COVID-19_Data.xlsx
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [COVID-19 Cases in Toronto](https://open.toronto.ca/dataset/covid-19-cases-in-toronto/)
    * Data are extracted at 3 PM on the Monday of a given week and posted by Wednesday [dataset is updated only on Wednesdays]
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)

### Quebec

* [Données COVID-19 au Québec](https://www.inspq.qc.ca/covid-19/donnees)
    * COVID-19 data: qc/covid-data/combine.csv
    * COVID-19 data (charts): qc/covid-data-charts/combine2.csv
    * Deaths by RSS (health region) and living environment: qc/deaths-by-rss-and-living-environment/tableau-rpa.csv
    * Cases by RSS (health region) and RLS (local service network): Cases qc/cases-by-rss-and-rls/tableau-rls.csv
    * Terms of use: TBD
* [Situation du coronavirus (COVID-19) à Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/situation-du-coronavirus-covid-19-a-montreal/)
    * **Note that these files are actually semicolon-separated since they use a comma as the decimal marker (rather than a period) and are encoded as ISO 8859-15 (rather than UTF-8)**
    * Montréal cases and deaths by CIUSSS (integrated health and social services centres): qc/montreal-cases-and-deaths-by-ciusss/ciusss.csv
    * Montréal cases by area: qc/montreal-cases-by-area/municipal.csv
    * Montréal cases and deaths by age group: qc/montreal-cases-and-deaths-by-age-group/grage.csv
    * Montréal cases and deaths by sex: qc/montreal-cases-and-deaths-by-sex/sexe.csv
    * Montréal epidemic curve: qc/montreal-epidemic-curve/courbe.csv
    * Terms of use: TBD

## Acknowledgements

Many people are to thank for contributing archived data and code to this repository.
 
* [Jens von Bergmann](https://github.com/mountainMath)
* [Simon Coulombe](https://github.com/simoncoulombe)
* [James E. Wright](https://twitter.com/JWright159)
* [Farbod Abolhassani](https://github.com/farbodab)
* [Shelby L. Sturrock](https://twitter.com/shelbysturrock)
* [Safa Ahmad](https://twitter.com/birdseye47)
