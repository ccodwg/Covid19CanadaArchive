# Archive of COVID-19 Data from Canadian Government Sources

This repository provides automated, daily backups of COVID-19 data from various Canadian government sources. Selected non-governmental sources are also included.

**File name timestamps are given in ET (America/Toronto) in the following format: %Y%-m-%d_%H-%M.** The script is run nightly around 23:00 ET.

All code in this repository is covered by the [MIT License](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/blob/master/LICENSE). Licenses and terms of use for each archived dataset are given below.

This repository is maintained by [Jean-Paul R. Soucy](https://jeanpaulsoucy.com/) on behalf of the [COVID-19 Open Data Working Group](https://opencovid.ca/).

Table of contents:

* [Contributing](#contributing)
* [Recommended citation](#recommended-citation)
* [Running archiver.py](#running-archiverpy)
* [Data sources/terms of use/supplementary material](#data-sourcesterms-of-usesupplementary-material)
  * [Alberta](#alberta)
     * [Edmonton](#edmonton)
  * [British Columbia](#british-columbia)
  * [Canada](#canada)
  * [Manitoba](#manitoba)
     * [Winnipeg](#winnipeg)
  * [Nova Scotia](#nova-scotia)
  * [Ontario](#ontario)
     * [Toronto](#toronto)
     * [Ottawa](#ottawa)
  * [Quebec](#quebec)
     * [Montreal](#montreal)
  * [Saskatchewan](#saskatchewan)
  * [Other: Non-governmental sources](#other-non-governmental-sources)
     * [Canada](#canada-1)
     * [Quebec](#quebec-1)
* [Acknowledgements](#acknowledgements)

## Contributing

Community members may contribute to this repository in three ways:

* Create an issue to request a dataset be added to the archive.
* Create a pull request for *archiver.py* adding the ability to automatically archive a requested or not-yet-implemented dataset.
* Submit archived versions of an existing, requested, or not-yet-implemented dataset. If possible, please use the original file name plus timestamp in the format described above.

## Recommended citation

COVID-19 Canada Open Data Working Group. Archive of COVID-19 Data from Canadian Government Sources. https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data. (Access date).

## Running archiver.py

*archiver.py* can run in four modes:
* `python archiver.py serverprod`: Download and commit files, running on the Heroku server.
* `python archiver.py localprod`: Download and commit files, running on a local machine.
* `python archiver.py servertest`: Download but do not commit files, running on the Heroku server.
* `python archiver.py localtest`: Download but do not commit files, running on a local machine.

See *archiver.py* for more details.

## Data sources/terms of use/supplementary material

The sources and terms of use for each included dataset are linked below. Supplementary material such as data dictionaries and codebooks are also included in the list below, if available. These files are included with the relevant datasets in a directory named `supplementary`.

### Alberta

* [COVID-19 Alberta statistics](https://www.alberta.ca/stats/covid-19-alberta-statistics.htm)
    * [ab/cases/covid19dataexport.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/ab/cases)
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence); see also the disclaimer in the "data notes" tab of the [website](https://www.alberta.ca/stats/covid-19-alberta-statistics.htm)
* [COVID-19 relaunch status map](https://www.alberta.ca/maps/covid-19-status-map.htm)
    * [ab/active-cases-by-region/covid19dataexport-relaunch.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/ab/active-cases-by-region)
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence)
* [COVID-19 school status map](https://www.alberta.ca/schools/covid-19-school-status-map.htm)
    * [ab/school-status-by-region/covid19dataexport-schools.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/ab/school-status-by-region)
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence)

#### Edmonton

* [COVID-19 in Alberta: Current cases by local geographic area (Edmonton)](https://data.edmonton.ca/Community-Services/COVID-19-in-Alberta-Current-cases-by-local-geograp/ix8f-s9xp)
    * [ab/edmonton-cases-by-area/COVID-19_in_Alberta__Current_cases_by_local_geographic_area.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/ab/edmonton-cases-by-area)
    * Terms of use: Assumed to be [City of Edmonton Open Data Terms of Use](https://data.edmonton.ca/stories/s/City-of-Edmonton-Open-Data-Terms-of-Use/msh8-if28/)

### British Columbia

* [BC COVID-19 Data](http://www.bccdc.ca/health-info/diseases-conditions/covid-19/data)
    * Case data: [bc/case-data/BCCDC_COVID19_Dashboard_Case_Details.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/case-data)
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
    * Laboratory data: [bc/laboratory-data/BCCDC_COVID19_Dashboard_Lab_Information.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/laboratory-data)
    * Terms of use: [Disclaimer and data notes](http://www.bccdc.ca/Health-Info-Site/Documents/BC_COVID-19_Disclaimer_Data_Notes.pdf)
* [COVID-19 Public Exposures](http://www.bccdc.ca/health-info/diseases-conditions/covid-19/public-exposures)
    * Public exposures webpage screenshot: [bc/public-exposures-webpage/public-exposures-screenshot.png](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/public-exposures-webpage)
    * Public exposures - flights: [bc/public-exposures-flights/public-exposures-flights-tables-Current.pdf](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/public-exposures-flights)
    * [Public exposures - cruises, long distance bus, train, work sites, public events](http://www.bccdc.ca/Health-Info-Site/Documents/Archived_COVID-19_Exposures.pdf): [bc/public-exposures-cruises-bus-train-work-public/Archived_COVID-19_Exposures.pdf](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/public-exposures-cruises-bus-train-work-public) (Not included as part of the nightly update, as it is archived)
    * Public exposures Fraser webpage: [bc/regional-exposure-events-fraser-webpage/regional-exposure-events-fraser-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/regional-exposure-events-fraser-webpage) (warning: some early files are .png screenshots and named differently)
    * Public exposures Interior webpage: [bc/regional-exposure-events-interior-webpage/regional-exposure-events-interior-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/regional-exposure-events-interior-webpage) (warning: some early files are .png screenshots and named differently)
    * Public exposures Island webpage: [bc/regional-exposure-events-island-webpage/regional-exposure-events-island-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/regional-exposure-events-island-webpage) (warning: some early files are .png screenshots and named differently)
    * Public exposures Northern webpage: [bc/regional-exposure-events-northern-webpage/regional-exposure-events-northern-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/regional-exposure-events-northern-webpage) (warning: some early files are .png screenshots and named differently)
    * Public exposures Vancouver Coastal webpage: [bc/regional-exposure-events-vancouver-coastal-webpage/regional-exposure-events-vancouver-coastal-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/regional-exposure-events-vancouver-coastal-webpage) (warning: some early files are .png screenshots or .pdf files and named differently and/or formatted differently)
    * School exposures Fraser webpage: [bc/school-exposures-fraser-webpage/school-exposures-fraser-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/school-exposures-fraser-webpage) (warning: some early files are .png screenshots and named differently)
    * School exposures Interior webpage: [bc/school-exposures-interior-webpage/school-exposures-interior-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/school-exposures-interior-webpage) (warning: some early files are .png screenshots and named differently)
    * School exposures Island webpage: [bc/school-exposures-island-webpage/school-exposures-island-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/school-exposures-island-webpage) (warning: some early files are .png screenshots and named differently)
    * School exposures Northern webpage: [bc/school-exposures-northern-webpage/school-exposures-northern-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/school-exposures-northern-webpage) (warning: some early files are .png screenshots and named differently)
    * School exposures Vancouver Coastal webpage: [bc/school-exposures-vancouver-coastal-webpage/school-exposures-vancouver-coastal-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/bc/school-exposures-vancouver-coastal-webpage) (warning: some early files are .png screenshots and named differently)
    * Vancouver Coastal reported its first school outbreak on 2020-09-22. However, due to a change in the page format, the first day these data were captured in the dataset was 2020-10-05. Screenshots prior to this date ommit the list of schools. However, it is unlikely that any schools were removed from the list prior to it first being captured on 2020-10-05.
    * Terms of use: TBD

### Canada

* [Epidemiological summary of COVID-19 cases in Canada](https://health-infobase.canada.ca/covid-19/epidemiological-summary-covid-19-cases.html) / [COVID-19 Situational Awareness Dashboard](https://health-infobase.canada.ca/covid-19/dashboard/)
    * Epidemiology update / [Data on COVID-19 in Canada](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc): [can/epidemiology-update/covid19.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/epidemiology-update)
    	* Includes supplementary material: [Data dictionary (English)](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc) and [data dictionary (French)](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc)
* [Epidemiological summary of COVID-19 cases in Canada](https://health-infobase.canada.ca/covid-19/epidemiological-summary-covid-19-cases.html) / [COVID-19 Situational Awareness Dashboard](https://health-infobase.canada.ca/covid-19/dashboard/)
    * Epidemiology update / [Data on COVID-19 in Canada](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc): [can/epidemiology-update/covid19-download.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/epidemiology-update-2)
    	* Identical to the above dataset but the date column is in YYYY-MM-DD format instead of DD-MM-YYYY
    	* Includes supplementary material: [Data dictionary (English)](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc) and [data dictionary (French)](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc)
    * Epidemiology summary statements: [can/epidemiology-summary-statements/covid19-epiSummary-statements.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/epidemiology-summary-statements)
    * NML summary: [can/nml-summary/covid19-epiSummary-NML.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/nml-summary)
    * NML weekly testing: [can/nml-weekly-testing/NML_weekly_testing.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/nml-weekly-testing)
    * Number of cases with detailed case report data: [can/detailed-case-report-n/covid19-nTotal.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/detailed-case-report-n)
    * Cases and deaths by health region time series: [can/cases-and-deaths-by-hr-time-series/file_out_v5.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/cases-and-deaths-by-hr-time-series)
    * Health region UID table: [can/health-region-uid/covid19-healthregions-hruid.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/health-region-uid)
    * Cases by exposure setting time series: [can/cases-by-exposure-time-series/covid19-epiSummary-casesovertime.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/cases-by-exposure-time-series)
    * Epidemic curve by date of illness onset by age group: [can/epidemic-curve-by-age/covid19-epiSummary-epiCurveByAge.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/epidemic-curve-by-age)
    * Severity by age group and sex: [can/severity-by-age-and-sex/covid19-epiSummary-severityUpdate.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/severity-by-age-and-sex)
    * Cases by severity: [can/cases-by-severity/covid19-epiSummary-severity.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/cases-by-severity)
    * Cases by age group and sex: [can/cases-by-age-and-sex/covid19-epiSummary-agegroups2.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/cases-by-age-and-sex)
    * Cases by probable exposure setting: [can/cases-by-probable-exposure-setting/covid19-epiSummary-probableexposure2.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/cases-by-probable-exposure-setting)
    * Symptoms summary: [can/symptoms-summary/covid19-epiSummary-symptoms.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/symptoms-summary)
    * Situational awareness dashboard update time: [can/situational-awareness-dashboard-update-time/covid19-updateTime.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/situational-awareness-dashboard-update-time)
    * Terms of use: [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada)
* [Detailed preliminary information on cases of COVID-19: 6 Dimensions (Aggregated data)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310077401)
    * [can/detailed-preliminary-case-info-aggregated-6-dimensions/13100774.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/detailed-preliminary-case-info-aggregated-6-dimensions)
    * Includes supplementary material: Footnotes, metadata
    * Terms of use: [Statistics Canada Open Licence](https://www.statcan.gc.ca/eng/reference/licence)
* [Detailed preliminary information on cases of COVID-19: 4 Dimensions (Aggregated data)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310077501)
    * [can/detailed-preliminary-case-info-aggregated-4-dimensions/13100775.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/detailed-preliminary-case-info-aggregated-4-dimensions)
    * Includes supplementary material: Footnotes, metadata
    * Terms of use: [Statistics Canada Open Licence](https://www.statcan.gc.ca/eng/reference/licence)
* [Detailed preliminary information on confirmed cases of COVID-19 (Revised)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310078101)
    * [can/detailed-preliminary-confirmed-case-info-revised/13100781.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/can/detailed-preliminary-confirmed-case-info-revised)
    * Variable value definitions are given in footnotes (see supplementary material).
    * **This file has been processed to avoid the 100mb file limit on GitHub.** (Base file size is > 400mb)
        * Dataset has been pivoted from long to wide (names from: 'Case information', values from: 'VALUE').
        * Columns containing no information have been dropped (GEO, DGUID, UOM, UOM_ID, SCALAR_FACTOR, SCALAR_ID, VECTOR, COORDINATE, STATUS, SYMBOL, TERMINATED, DECIMALS).
        * Example of original data format is preserved (see supplementary material).
    * Includes supplementary material: Footnotes, example of original data format, metadata
    * Terms of use: [Statistics Canada Open Licence](https://www.statcan.gc.ca/eng/reference/licence)

### Manitoba

* [Cases and Risk of COVID-19 in Manitoba](https://www.gov.mb.ca/covid19/updates/cases.html)
    * COVID-19 data by RHA and district: [mb/covid-data-by-rha-and-district/covid-data-by-rha-and-district.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/mb/covid-data-by-rha-and-district)
    * Cases by demographics and RHA: [mb/cases-demographics-by-rha/cases-demographics-by-rha.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/mb/cases-demographics-by-rha)
    * Cases by status and RHA (Regional Health Authority): [mb/cases-by-status-and-rha/cases-by-status-and-rha.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/mb/cases-by-status-and-rha)
    * Manitoba five-day test positivity rate: [mb/five-day-test-positivity/five-day-test-positivity.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/mb/five-day-test-positivity)
    * Terms of use: TBD
    * Data have been converted from JSON queries to CSV

#### Winnipeg

* [COVID-19 By-law Enforcement (Winnipeg)](https://data.winnipeg.ca/Neighbourhood-Liveability-Property-Standards-Licen/COVID-19-By-law-Enforcement/ndr6-96vi)
    * [mb/winnipeg-by-law-enforcement/COVID-19_By-law_Enforcement.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/mb/winnipeg-by-law-enforcement)
    * Terms of use: [Open Government Licence - Winnipeg](https://data.winnipeg.ca/open-data-licence)
    Not included as part of the nightly update, as it does not seem to be receiving regular updates (last new data: June 5, 2020)
* [COVID-19 Designated Active Transportation Route Counts (Winnipeg)](https://data.winnipeg.ca/Transportation-Planning-Traffic-Management/COVID-19-Designated-Active-Transportation-Route-Co/aqka-nz2g)
    * [mb/winnipeg-active-transportation/COVID-19_Designated_Active_Transportation_Route_Counts.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/mb/winnipeg-active-transportation)
    * Terms of use: [Open Government Licence - Winnipeg](https://data.winnipeg.ca/open-data-licence)
    * Not included as part of the nightly update, as it does not seem to be receiving regular updates (last updated: June 29, 2020)

### Nova Scotia

* [Coronavirus (COVID-19): case data](https://novascotia.ca/coronavirus/data/)
    * [ns/case-data/ns-covid19-data.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/ns/case-data)
    * Terms of use: Assumed to be [Open Government Licence – Nova Scotia](https://novascotia.ca/opendata/licence.asp)

### Ontario

* [How Ontario is responding to COVID-19](https://www.ontario.ca/page/how-ontario-is-responding-covid-19)
    * Webpage: [on/ontario-webpage/ontario-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/ontario-webpage) (warning: some early files are .png screenshots and named differently)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Confirmed positive cases of COVID19 in Ontario](https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario/resource/455fd63b-603d-4608-8216-7d8647f43350)
    * [on/confirmed-positive-cases/conposcovidloc.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/confirmed-positive-cases)
    * Includes supplementary material: [Data dictionary (English and French)](https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario/resource/a2ea0536-1eae-4a17-aa04-e5a1ab89ca9a)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Status of COVID-19 cases in Ontario](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11)
    * [on/status-of-cases/covidtesting.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/status-of-cases)
    * Includes supplementary material: [Data dictionary (English and French)](https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario/resource/7be0a14c-bf50-4340-9304-2b189d507541)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [COVID-19 testing of inmates in Ontario’s Provincial Correctional Institutions](https://data.ontario.ca/dataset/covid-19-testing-of-inmates-in-ontario-s-correctional-institutions)
    * [on/correctional-institutions-inmates-testing/inmatetesting.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/correctional-institutions-inmates-testing)
    * Includes supplementary material: [Technical documentation (English and French)](https://data.ontario.ca/dataset/covid-19-testing-of-inmates-in-ontario-s-correctional-institutions/resource/6e2868ab-a242-48d6-9f73-235d19a6668e)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Status of COVID-19 cases in Ontario’s Provincial Correctional Institutions](https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario-s-correctional-institutions)
    * [on/correctional-institutions-status/correctionsinmatecases.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/correctional-institutions-status)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Long-Term Care Home COVID-19 Data](https://data.ontario.ca/dataset/long-term-care-home-covid-19-data)
    * Summary data: [on/long-term-care-home-summary/ltccovidsummary.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/long-term-care-home-summary)
    * Active outbreaks: [on/long-term-care-home-active/activeltcoutbreak.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/long-term-care-home-active)
    * Resolved outbreaks: [on/long-term-care-home-resolved/resolvedltc.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/long-term-care-home-resolved)
    * Includes supplementary material: [Data dictionary (English and French)](https://data.ontario.ca/dataset/long-term-care-home-covid-19-data/resource/adbcf9f8-e473-4f27-b85f-0f05f686067b)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [COVID-19 cases in schools and child care centres](https://www.ontario.ca/page/covid-19-cases-schools-and-child-care-centres)
    * Webpage: [on/cases-schools-and-child-care-centres-webpage/cases-schools-and-child-care-centres-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/cases-schools-and-child-care-centres-webpage) (warning: some early files are .png screenshots and named differently)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Schools COVID-19 data](https://data.ontario.ca/dataset/summary-of-cases-in-schools)
    * Summary of cases in schools: [on/schools-summary/schoolcovidsummary.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/schools-summary)
    * Schools with active COVID-19 cases: [on/schools-active/schoolsactivecovid.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/schools-active)
    * Cases in school board partners: [on/school-board-partners/schoolpartnersactivecovid.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/school-board-partners)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Licensed child care settings COVID-19 data](https://data.ontario.ca/dataset/summary-of-cases-in-licensed-child-care-settings)
    * Summary of cases in licensed child care settings: [on/licensed-child-care-settings-summary/lccovidsummary.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/licensed-child-care-settings-summary)
    * Licensed child care centres and agencies with active COVID-19 cases: [on/licensed-child-care-settings-active/lccactivecovid.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/licensed-child-care-settings-active)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)

#### Toronto

* [City of Toronto Daily Status of COVID-19 Cases](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-daily-status/CityofToronto_COVID-19_Daily_Public_Reporting.xlsx](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/toronto-daily-status)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto COVID-19 Summary](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-covid-summary/CityofToronto_COVID-19_Data.xlsx](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/toronto-covid-summary)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto COVID-19 Neighbourhood Case Data](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-neighbourhood-data/CityofToronto_COVID-19_NeighbourhoodData.xlsx](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/toronto-neighbourhood-data)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto COVID-19 Neighbourhood Testing Data](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-neighbourhood-test-data/CityofToronto_COVID-19_Testing.xlsx](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/toronto-neighbourhood-test-data)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto COVID-19 Monitoring Dashboard](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-monitoring-dashboard/CityofToronto_COVID-19_RecoveryData.xlsx](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/toronto-monitoring-dashboard)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [COVID-19 Cases in Toronto](https://open.toronto.ca/dataset/covid-19-cases-in-toronto/)
    * [on/toronto-cases/COVID19_cases.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/toronto-cases)
    * Data are extracted at 3 PM on the Monday of a given week and posted by Wednesday [dataset is updated only on Wednesdays]
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [University of Toronto COVID-19 tracking](https://www.utoronto.ca/utogether2020/covid19-dashboard)
    * [on/u-of-t-covid-tracking-webpage/u-of-t-covid-tracking-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/u-of-t-covid-tracking-webpage) (warning: some early files are .png screenshots and named differently)
    * Data are reported every Monday with cumulative cases through the previous Friday [screenshots will be take every day in case the update frequency increases]
    * Terms of use: TBD

#### Ottawa

* [Daily COVID-19 Dashboard (Ottawa)](https://www.ottawapublichealth.ca/en/reports-research-and-statistics/daily-covid19-dashboard.aspx)
    * [Demographics and Source of Infection for Cases, Deaths, and Hospitalizations](https://www.arcgis.com/home/item.html?id=6bfe7832017546e5b30c5cc6a201091b): [on/ottawa-cases-deaths-hosp-demographics-source-of-infection/COVID-19_Cases_and_Deaths_Ottawa_EN.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/ottawa-cases-deaths-hosp-demographics-source-of-infection)
    * [Outbreaks in Healthcare Institutions, Childcare, Summer Camps, and Educational Establishments](https://www.arcgis.com/home/item.html?id=5b24f70482fe4cf1824331d89483d3d3): [on/ottawa-outbreaks-healthcare-childcare-camps-schools/COVID-19_Institutional_Outbreaks.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/ottawa-outbreaks-healthcare-childcare-camps-schools)
    * [Community Outbreaks](https://open.ottawa.ca/datasets/0df365456c254fbc942fe3d85c3dbf83): [on/ottawa-community-outbreaks/COVID-19_Community_Outbreaks_in_Ottawa.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/ottawa-community-outbreaks)
    * [Weekly Rates](https://www.arcgis.com/home/item.html?id=734a327141b14a55b666953c9141abf3): [on/ottawa-weekly-rates/COVID-19_Weekly_Cases_and_Rates_by_Age_in_Ottawa_EN.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/ottawa-weekly-rates)
    * [Estimated Reproduction Number in Ottawa](https://www.arcgis.com/home/item.html?id=d010a848b6e54f4990d60a202f2f2f99): [on/ottawa-estimated-rt/EN_-_Covid-19_Reproduction_Number,_R(t).csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/ottawa-estimated-rt)
    * [Testing - Ottawa Residents](https://www.arcgis.com/home/item.html?id=26c902bf1da44d3d90b099392b544b81): [on/ottawa-residents-tested/COVID-19_Ottawa_Residents_Tested_EN.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/ottawa-residents-tested)
    * Ottawa cases and deaths: [on/ottawa-cases-and-deaths/COVID-19_Cases_and_Deaths_in_Ottawa_EN.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/ottawa-cases-and-deaths) (Archived as of 2020-09-21, no longer part of the nightly update)
    * Ottawa outbreaks in healthcare institutions: [on/ottawa-outbreaks-in-healthcare-institutions/COVID-19_Outbreaks_in_Ottawa_Healthcare_Institutions_EN.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/ottawa-outbreaks-in-healthcare-institutions) (Archived as of 2020-09-21, no longer part of the nightly update)
    * Ottawa hospitalization data: [on/ottawa-hospitalization/Hospitalizations_of_Ottawa_residents_with_confirmed_COVID-19.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/on/ottawa-hospitalization) (Archived as of 2020-09-21, no longer part of the nightly update)
    * Include supplementary material: User guide, technical guide, overall status assessment
    * Terms of use: [Open Government Licence – City of Ottawa](https://ottawa.ca/en/city-hall/get-know-your-city/open-data#open-data-licence-version-2-0)

### Quebec

* [Données COVID-19 au Québec](https://www.inspq.qc.ca/covid-19/donnees)
    * COVID-19 time series by region and demographics: [qc/covid-time-series-by-region-and-demographics/covid19-hist.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/covid-time-series-by-region-and-demographics)
    * COVID-19 data (charts - summary, time series, and hospitalization by age): [qc/covid-data-charts-summary-time-series-hosp-by-age/manual-data.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/covid-data-charts-summary-time-series-hosp-by-age)
    * Summary by region: [qc/summary-by-region/regions.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/summary-by-region)
    * Deaths by RSS (health region) and living environment: [qc/deaths-by-rss-and-living-environment/tableau-rpa-new.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/deaths-by-rss-and-living-environment) (Renamed from tableau-rpa.csv after 2020-09-16)
    * Cases by RSS (health region) and RLS (local service network): [qc/cases-by-rss-and-rls/tableau-rls-new.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/cases-by-rss-and-rls) (Renamed from tableau-rls.csv after 2020-09-16)
    * Comparisons (provinces): [qc/comparisons-provinces/comparaisons_prov.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/comparisons-provinces)
    * Comparisons (countries): [qc/comparisons-countries/comparaisons_pays.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/comparisons-countries)
    * COVID-19 time series by region: [qc/covid-time-series-by-region/PL_DATE.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/covid-time-series-by-region) (Archived as of 2020-10-15, no longer part of the nightly update)
        * [Advice for data process by Simon Coulombe](https://gist.github.com/SimonCoulombe/9a329052ac4cefd421febd8650ed84e2)
    * COVID-19 data: [qc/covid-data/combine.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/covid-data) (Archived as of 2020-09-16, no longer part of the nightly update)
    * COVID-19 data (charts): [qc/covid-data-charts/combine2.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/covid-data-charts) (Archived as of 2020-09-16, no longer part of the nightly update)
    * Terms of use: TBD
* [https://www.inspq.qc.ca/covid-19/donnees/age-sexe](https://www.inspq.qc.ca/covid-19/donnees/age-sexe)
    * COVID-19 data by age group and sex: [qc/covid-data-by-age-and-sex/PL_AGE_SEXE.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/covid-data-by-age-and-sex)
    * Terms of use: TBD
* [Situation du coronavirus (COVID-19) au Québec](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    * Deaths time series by living environment: [qc/deaths-time-series-by-living-environment/decesquotidien.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/deaths-time-series-by-living-environment)
    * Recent daily cases by region: [qc/recent-daily-cases-by-region/cas-region.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/recent-daily-cases-by-region)
    * Cumulative deaths by region: [qc/cumulative-deaths-by-region/deces-region.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/cumulative-deaths-by-region)
    * Situation in Quebec: [qc/situation-in-quebec/situation-au-quebec.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/situation-in-quebec)
    * Cases percentage by age group: [qc/cases-percentage-by-age-group/pourcentage-cas-age.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/cases-percentage-by-age-group)
    * Deaths percentage by age group: [qc/deaths-percentage-by-age-group/pourcentage-deces-age.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/deaths-percentage-by-age-group)
    * COVID-19 daily data 7 days: [qc/covid-data-daily-7-days/synthese-7jours.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/covid-data-daily-7-days)
    * Cases by region 7 days: [qc/cases-by-region-7-days/cas-region-7jours.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/cases-by-region-7-days)
    * Terms of use: TBD
* [Situation dans les milieux de vie pour personnes aînées et vulnérables](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    * Status report on confirmed cases and deaths by RPA (private residences for seniors): [qc/status-report-cases-and-deaths-by-rpa/etat_situation_rpa.pdf](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/status-report-cases-and-deaths-by-rpa)
    * Status report on confirmed cases and deaths by CHSLD (residential and long-term care centres): [qc/status-report-cases-and-deaths-by-chsld/etat_situation_chsld.pdf](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/status-report-cases-and-deaths-by-chsld)
    * Supplementary material: [Canadian Armed Forces report on their presence in CHSLDs](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec)
    * Terms of use: TBD
* [Situation dans les établissements scolaires](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    * Highlights - public and private school system: [qc/schools-highlights/reseauScolaire_faitsSaillants.pdf](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/schools-highlights)
    * List of schools - public and private school system: [qc/schools-list-of-schools/reseauScolaire_listeEcoles.pdf](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/schools-list-of-schools)
    * Formerly [Situation dans les établissements scolaires relative à la COVID-19](https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/etat_situation_ecole.pdf): [qc/schools-list-of-schools/etat_situation_ecole_2020-09-04_2020-09-06/etat_situation_ecole.pdf](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/schools-list-of-schools/etat_situation_ecole_2020-09-04_2020-09-06)
    * Formerly [Liste des écoles ayant au moins un cas rapporté de la COVID-19 depuis le 1er septembre 2020](https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/liste-ecole-cas-rapportes.pdf): [qc/schools-list-of-schools/liste-ecole-cas-rapportes_2020-09-08_2020-09-09/liste-ecole-cas-rapportes.pdf](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/schools-list-of-schools/liste-ecole-cas-rapportes_2020-09-08_2020-09-09)
    * Terms of use: TBD

#### Montreal

* [Situation du coronavirus (COVID-19) à Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/situation-du-coronavirus-covid-19-a-montreal/)
    * **Note that these files are actually semicolon-separated since they use a comma as the decimal marker (rather than a period) and are encoded as ISO 8859-15 (rather than UTF-8)**
    * Montréal cases and deaths by CIUSSS (integrated health and social services centres): [qc/montreal-cases-and-deaths-by-ciusss/ciusss.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/montreal-cases-and-deaths-by-ciusss)
    * Montréal cases by area: [qc/montreal-cases-by-area/municipal.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/montreal-cases-by-area)
    * Montréal cases and deaths by age group: [qc/montreal-cases-and-deaths-by-age-group/grage.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/montreal-cases-and-deaths-by-age-group)
    * Montréal cases and deaths by sex: [qc/montreal-cases-and-deaths-by-sex/sexe.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/montreal-cases-and-deaths-by-sex)
    * Montréal epidemic curve: [qc/montreal-epidemic-curve/courbe.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/qc/montreal-epidemic-curve)
    * Terms of use: TBD

### Saskatchewan

* [Saskatchewan's Dashboard - Total Cases](https://dashboard.saskatchewan.ca/health-wellness/covid-19/cases)
    * CSV: [sk/cases-by-region/cases.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/sk/cases-by-region)
    * Webpage: [sk/cases-by-region-webpage/cases-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/sk/cases-by-region-webpage) (warning: some early files are .png screenshots and named differently)
    * Terms of use: TBD
* [Saskatchewan's Dashboard - Total Tests](https://dashboard.saskatchewan.ca/health-wellness/covid-19/tests)
    * CSV: [sk/tests-by-region/tests.csv](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/sk/tests-by-region)
    * Webpage: [sk/tests-by-region-webpage/tests-webpage.html](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/sk/tests-by-region-webpage) (warning: some early files are .png screenshots and named differently)
    * Terms of use: TBD

### Other: Non-governmental sources

#### Canada

* [Canada COVID-19 School Case Tracker](https://masks4canada.org/canada-covid-19-school-case-tracker/)
    * [other/can/canada-covid-19-school-case-tracker/Canada_COVID-19_School_Report_Tracker.kml](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/other/can/canada-covid-19-school-case-tracker) (original file name is Canada COVID-19 School Report Tracker.kml, renamed to avoid spaces in file name; warning: some early files are in .kmz format, which is compressed but handled almost identically to .kml)
    * Terms of use: TBD
* [Unofficial COVID Alert Dashboard](https://github.com/uhengart/covid-alert-dashboard)
    * [other/can/unofficial-covid-alert-dashboard/estimated_infections_per_day.txt](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/other/can/unofficial-covid-alert-dashboard)
    * Terms of use: TBD   

#### Quebec

* [Covid Écoles Québec: Number of schools](https://www.covidecolesquebec.org/liste-alphabtique)
    * [Excel spreadsheet](https://drive.google.com/file/d/1xOl0uhyx9IuHZfJuRH-OR7BcGFuWYUex/view): [other/qc/covid-ecoles-quebec-school-list/COVIDECOLESQUEBEC.xlsx](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/tree/master/other/qc/covid-ecoles-quebec-school-list) (original file name is COVIDECOLESQUEBEC_20200905.xlsx, renamed to avoid confusion)
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
* [Shraddha Pai](https://twitter.com/spaiglass)
* [Matti Aleve](https://twitter.com/maleve)
