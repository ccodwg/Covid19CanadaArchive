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

## Data sources/terms of use/supplementary material

The sources and terms of use for each included dataset are linked below. Supplementary material such as data dictionaries and codebooks are also included in the list below, if available. These files are included with the relevant datasets in a directory named `supplementary`.

### Alberta

* [COVID-19 Alberta statistics](https://www.alberta.ca/stats/covid-19-alberta-statistics.htm)
    * ab/cases/covid19dataexport.csv
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence); see also the disclaimer in the "data notes" tab of the [website](https://www.alberta.ca/stats/covid-19-alberta-statistics.htm)
* [COVID-19 relaunch status map](https://www.alberta.ca/maps/covid-19-status-map.htm)
    * ab/active-cases-by-region/covid19dataexport-relaunch.csv
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence)
* [COVID-19 school status map](https://www.alberta.ca/schools/covid-19-school-status-map.htm)
    * ab/school-status-by-region/covid19dataexport-schools.csv
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
            Reported_Date = coalesce(as.Date(Reported_Date, "%Y-%m-%d"), as.Date(Reported_Date, "%m/%d/%Y")),
            Age_Group = recode(Age_Group, "19-Oct" = "10-19")
          )
        ```        
    * Laboratory data: bc/laboratory-data/BCCDC_COVID19_Dashboard_Lab_Information.csv
    * Terms of use: [Disclaimer and data notes](http://www.bccdc.ca/Health-Info-Site/Documents/BC_COVID-19_Disclaimer_Data_Notes.pdf)

### Canada

* [Epidemiological summary of COVID-19 cases in Canada](https://health-infobase.canada.ca/covid-19/epidemiological-summary-covid-19-cases.html) / [COVID-19 Situational Awareness Dashboard](https://health-infobase.canada.ca/covid-19/dashboard/)
    * Epidemiology update / [Data on COVID-19 in Canada](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc): can/epidemiology-update/covid19.csv
    	* Includes supplementary material: [Data dictionary (English)](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc) and [data dictionary (French)](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc)
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
    * Terms of use: [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada)

### Manitoba

* [Cases and Risk of COVID-19 in Manitoba]
    * Cases by status and RHA (Regional Health Authority): mb/cases-by-status-and-rha/cases-by-status-and-rha.csv
    * Manitoba Five-Day Test Positivity Rate: mb/five-day-test-positivity/five-day-test-positivity.csv
    * Terms of use: TBD
    * Data have been converted from JSON queries to CSV
* [COVID-19 By-law Enforcement (Winnipeg)](https://data.winnipeg.ca/Neighbourhood-Liveability-Property-Standards-Licen/COVID-19-By-law-Enforcement/ndr6-96vi)
    * mb/winnipeg-by-law-enforcement/COVID-19_By-law_Enforcement.csv
    * Terms of use: [Open Government Licence - Winnipeg](https://data.winnipeg.ca/open-data-licence)
    Not included as part of the nightly update, as it does not seem to be receiving regular updates (last new data: June 5, 2020)
* [COVID-19 Designated Active Transportation Route Counts (Winnipeg)](https://data.winnipeg.ca/Transportation-Planning-Traffic-Management/COVID-19-Designated-Active-Transportation-Route-Co/aqka-nz2g)
    * mb/winnipeg-active-transportation/COVID-19_Designated_Active_Transportation_Route_Counts.csv
    * Terms of use: [Open Government Licence - Winnipeg](https://data.winnipeg.ca/open-data-licence)
    * Not included as part of the nightly update, as it does not seem to be receiving regular updates (last updated: June 29, 2020)

### Nova Scotia

* [Coronavirus (COVID-19): case data](https://novascotia.ca/coronavirus/data/)
    * ns/case-data/ns-covid19-data.csv
    * Terms of use: Assumed to be [Open Government Licence – Nova Scotia](https://novascotia.ca/opendata/licence.asp)

### Ontario

* [Confirmed positive cases of COVID19 in Ontario](https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario/resource/455fd63b-603d-4608-8216-7d8647f43350)
    * on/confirmed-positive-cases/conposcovidloc.csv
    * Includes supplementary material: [Data dictionary (English and French)](https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario/resource/a2ea0536-1eae-4a17-aa04-e5a1ab89ca9a)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Status of COVID-19 cases in Ontario](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11)
    * on/status-of-cases/covidtesting.csv
    * Includes supplementary material: [Data dictionary (English and French)](https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario/resource/7be0a14c-bf50-4340-9304-2b189d507541)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [City of Toronto COVID-19 Summary](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * on/toronto-covid-summary/CityofToronto_COVID-19_Data.xlsx
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [COVID-19 Cases in Toronto](https://open.toronto.ca/dataset/covid-19-cases-in-toronto/)
    * Data are extracted at 3 PM on the Monday of a given week and posted by Wednesday [dataset is updated only on Wednesdays]
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [Daily COVID-19 Dashboard (Ottawa)](https://ottawa.ca/en/city-hall/get-know-your-city/open-data#open-data-licence-version-2-0)
    * Ottawa cases and deaths: on/ottawa-cases-and-deaths/COVID-19_Cases_and_Deaths_in_Ottawa_EN.csv
    * Ottawa outbreaks in healthcare institutions: on/ottawa-outbreaks-in-healthcare-institutions/COVID-19_Outbreaks_in_Ottawa_Healthcare_Institutions_EN.csv
    * Ottawa hospitalization data: on/ottawa-hospitalization/Hospitalizations_of_Ottawa_residents_with_confirmed_COVID-19.csv
    * Terms of use: [Open Government Licence – City of Ottawa](https://ottawa.ca/en/city-hall/get-know-your-city/open-data#open-data-licence-version-2-0)

### Quebec

* [Données COVID-19 au Québec](https://www.inspq.qc.ca/covid-19/donnees)
    * COVID-19 data: qc/covid-data/combine.csv
    * COVID-19 data (charts): qc/covid-data-charts/combine2.csv
    * Deaths by RSS (health region) and living environment: qc/deaths-by-rss-and-living-environment/tableau-rpa.csv
    * Cases by RSS (health region) and RLS (local service network): Cases qc/cases-by-rss-and-rls/tableau-rls.csv
    * Terms of use: TBD
* [Liste des écoles ayant au moins un cas rapporté de la COVID-19 depuis le 1er septembre 2020](https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/liste-ecole-cas-rapportes.pdf)
    * qc/list-of-schools-with-reported-cases/liste-ecole-cas-rapportes.pdf
    * Formerly [Situation dans les établissements scolaires relative à la COVID-19](https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/etat_situation_ecole.pdf): qc/situation-in-schools/etat_situation_ecole.pdf
    * Terms of use: TBD
* [Situation du coronavirus (COVID-19) à Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/situation-du-coronavirus-covid-19-a-montreal/)
    * **Note that these files are actually semicolon-separated since they use a comma as the decimal marker (rather than a period) and are encoded as ISO 8859-15 (rather than UTF-8)**
    * Montréal cases and deaths by CIUSSS (integrated health and social services centres): qc/montreal-cases-and-deaths-by-ciusss/ciusss.csv
    * Montréal cases by area: qc/montreal-cases-by-area/municipal.csv
    * Montréal cases and deaths by age group: qc/montreal-cases-and-deaths-by-age-group/grage.csv
    * Montréal cases and deaths by sex: qc/montreal-cases-and-deaths-by-sex/sexe.csv
    * Montréal epidemic curve: qc/montreal-epidemic-curve/courbe.csv
    * Terms of use: TBD

### Saskatchewan

* [Saskatchewan's Dashboard - Total Cases](https://dashboard.saskatchewan.ca/health-wellness/covid-19/cases)
    * sk/cases-by-region/cases.csv
    * Terms of use: TBD
* [Saskatchewan's Dashboard - Total Tests](https://dashboard.saskatchewan.ca/health-wellness/covid-19/tests)
    * sk/tests-by-region/tests.csv
    * Terms of use: TBD

### Other: Non-governmental sources

#### Quebec

* [Covid Écoles Québec: Number of schools](https://www.covidecolesquebec.org/liste-alphabtique)
    * [Excel spreadsheet](https://drive.google.com/file/d/1xOl0uhyx9IuHZfJuRH-OR7BcGFuWYUex/view): other/qc/covid-ecoles-quebec-school-list/COVIDECOLESQUEBEC.xlsx (original file name is COVIDECOLESQUEBEC_20200905.xlsx, renamed to avoid confusion)
    * Terms of use: TBD

## Acknowledgements

Many people are to thank for contributing archived data and code to this repository.
 
* [Jens von Bergmann](https://github.com/mountainMath)
* [Simon Coulombe](https://github.com/simoncoulombe)
* [James E. Wright](https://twitter.com/JWright159)
* [Farbod Abolhassani](https://github.com/farbodab)
* [Shelby L. Sturrock](https://twitter.com/shelbysturrock)
* [Safa Ahmad](https://twitter.com/birdseye47)
* [Jacques Marcoux](https://twitter.com/jacquesmarcoux)
