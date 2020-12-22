# Archive of COVID-19 Data from Canadian Government Sources

## The data in this archive have moved. They can be accessed at the following link: [https://drive.google.com/drive/folders/10ET5FBqO-K8FBdEaXgBjBZwJskIZGKNG?usp=sharing](https://drive.google.com/drive/folders/10ET5FBqO-K8FBdEaXgBjBZwJskIZGKNG?usp=sharing)

###### From now on, this archive will be used only to store and collorate on archival scripts and metadata. Links to the data have been updated. Other options to explore and download the data will be available soon.

This repository provides automated, daily backups of COVID-19 data from various Canadian government sources. Selected non-governmental sources are also included.

**File name timestamps are given in ET (America/Toronto) in the following format: %Y-%m-%d_%H-%M.** The script is run nightly around 23:00 ET.

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
  * [Northwest Territories](#northwest-territories)
  * [Nova Scotia](#nova-scotia)
  * [Nunavut](#nunavut)
  * [Ontario](#ontario)
     * [Toronto](#toronto)
     * [Ottawa](#ottawa)
  * [Quebec](#quebec)
     * [Montreal](#montreal)
  * [Saskatchewan](#saskatchewan)
  * [Yukon](#yukon)
  * [Other: Non-governmental sources](#other-non-governmental-sources)
     * [Canada](#canada-1)
     * [Quebec](#quebec-1)
  * [COVID-19 Canada Open Data Working Group](#covid-19-canada-open-data-working-group)
* [Data notes](#data-notes)
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
    * [ab/cases/covid19dataexport.csv](https://drive.google.com/drive/folders/1iovWxEIDHPfS1foRZCPgugxXTBeoMjsc)
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence); see also the disclaimer in the "data notes" tab of the [website](https://www.alberta.ca/stats/covid-19-alberta-statistics.htm)
* [COVID-19 relaunch status map](https://www.alberta.ca/maps/covid-19-status-map.htm)
    * [ab/active-cases-by-region/covid19dataexport-relaunch.csv](https://drive.google.com/drive/folders/1IdoOr_ncaujctgkD4bmqLfl5QalTBcIF)
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence)
* [COVID-19 school status map](https://www.alberta.ca/schools/covid-19-school-status-map.htm)
    * [ab/school-status-by-region/covid19dataexport-schools.csv](https://drive.google.com/drive/folders/1x1VYSe39dymoyLWy0ZhwR01cbk0pzL2y)
    * Terms of use: Assumed to be [Open Government Licence - Alberta](https://open.alberta.ca/licence)

#### Edmonton

* [COVID-19 in Alberta: Current cases by local geographic area (Edmonton)](https://data.edmonton.ca/Community-Services/COVID-19-in-Alberta-Current-cases-by-local-geograp/ix8f-s9xp)
    * [ab/edmonton-cases-by-area/COVID-19_in_Alberta__Current_cases_by_local_geographic_area.csv](https://drive.google.com/drive/folders/1kSMAgRDBJLco_bmgPP3rde-hgqT7NUiw)
    * Terms of use: Assumed to be [City of Edmonton Open Data Terms of Use](https://data.edmonton.ca/stories/s/City-of-Edmonton-Open-Data-Terms-of-Use/msh8-if28/)

### British Columbia

* [BC COVID-19 Data](http://www.bccdc.ca/health-info/diseases-conditions/covid-19/data)
    * Case data: [bc/case-data/BCCDC_COVID19_Dashboard_Case_Details.csv](https://drive.google.com/drive/folders/1rvsPQenCXuSuS5kTB-sZPqLb6eokU9b1)
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
    * Laboratory data: [bc/laboratory-data/BCCDC_COVID19_Dashboard_Lab_Information.csv](https://drive.google.com/drive/folders/1SBe3JAmy6D3ed0zTAdn2v9EyN3DRsV-i)
    * Regional data: [bc/regional-case-summary/BCCDC_COVID19_Regional_Summary_Data.csv](https://drive.google.com/drive/folders/12fgD4L4AfAaIx2u7eLnauX_z_IO2wFsU)
    * Terms of use: [Disclaimer and data notes](http://www.bccdc.ca/Health-Info-Site/Documents/BC_COVID-19_Disclaimer_Data_Notes.pdf)
* [COVID-19 Public Exposures](http://www.bccdc.ca/health-info/diseases-conditions/covid-19/public-exposures)
    * Public exposures webpage screenshot: [bc/public-exposures-webpage/public-exposures-screenshot.png](https://drive.google.com/drive/folders/1n-KrxIOXGH8drUf0Hb_-xfGUUdcvPy_U)
    * Public exposures - flights: [bc/public-exposures-flights/public-exposures-flights-tables-Current.pdf](https://drive.google.com/drive/folders/1LoIXBzFN6GtiOpz4SFmxWuvhfsx1vPSE)
    * [Public exposures - cruises, long distance bus, train, work sites, public events](http://www.bccdc.ca/Health-Info-Site/Documents/Archived_COVID-19_Exposures.pdf): [bc/public-exposures-cruises-bus-train-work-public/Archived_COVID-19_Exposures.pdf](https://drive.google.com/drive/folders/1HPu-kki3GUdX5uLDqjJL_RvnKExJv5Un) (Not included as part of the nightly update, as it is archived)
    * Public exposures Fraser webpage: [bc/regional-exposure-events-fraser-webpage/regional-exposure-events-fraser-webpage.html](https://drive.google.com/drive/folders/1mvchjctnzICre6bQrkYYSiXSt17Z73q5) (warning: some early files are .png screenshots and named differently)
    * Public exposures Interior webpage: [bc/regional-exposure-events-interior-webpage/regional-exposure-events-interior-webpage.html](https://drive.google.com/drive/folders/104BE89ytRvoJD3jYihJazC8G_x7AO74E) (warning: some early files are .png screenshots and named differently)
    * Public exposures Island webpage: [bc/regional-exposure-events-island-webpage/regional-exposure-events-island-webpage.html](https://drive.google.com/drive/folders/1eN7oRKGGl-62zIaZ_yNSp2kguQBt9gpk) (warning: some early files are .png screenshots and named differently)
    * Public exposures Northern webpage: [bc/regional-exposure-events-northern-webpage/regional-exposure-events-northern-webpage.html](https://drive.google.com/drive/folders/1Vzu5ulpEmXGy3I8J4yPaWHIxL3bWV59a) (warning: some early files are .png screenshots and named differently)
    * Public exposures Vancouver Coastal webpage: [bc/regional-exposure-events-vancouver-coastal-webpage/regional-exposure-events-vancouver-coastal-webpage.html](https://drive.google.com/drive/folders/1F10Fd3yDjFvDObnNFUVhnrLObLeNIK4y) (warning: some early files are .png screenshots or .pdf files and named differently and/or formatted differently)
    * School exposures Fraser webpage: [bc/school-exposures-fraser-webpage/school-exposures-fraser-webpage.html](https://drive.google.com/drive/folders/1Y66EqcQJbqOoV-UEgdncJs3MbVMww_QE) (warning: some early files are .png screenshots and named differently)
    * School exposures Interior webpage: [bc/school-exposures-interior-webpage/school-exposures-interior-webpage.html](https://drive.google.com/drive/folders/1fWdzcEDuIt2eplR1My5SFfCe69dd-mrU) (warning: some early files are .png screenshots and named differently)
    * School exposures Island webpage: [bc/school-exposures-island-webpage/school-exposures-island-webpage.html](https://drive.google.com/drive/folders/1eN7oRKGGl-62zIaZ_yNSp2kguQBt9gpk) (warning: some early files are .png screenshots and named differently)
    * School exposures Northern webpage: [bc/school-exposures-northern-webpage/school-exposures-northern-webpage.html](https://drive.google.com/drive/folders/1GAJ4Fh6Oq5DQPshWEpktzfDcMXq24S2q) (warning: some early files are .png screenshots and named differently)
    * School exposures Vancouver Coastal webpage: [bc/school-exposures-vancouver-coastal-webpage/school-exposures-vancouver-coastal-webpage.html](https://drive.google.com/drive/folders/1weMgD-gaaJ4B4m01lKWqBjUD_l42A-LL) (warning: some early files are .png screenshots and named differently)
    * Vancouver Coastal reported its first school outbreak on 2020-09-22. However, due to a change in the page format, the first day these data were captured in the dataset was 2020-10-05. Screenshots prior to this date ommit the list of schools. However, it is unlikely that any schools were removed from the list prior to it first being captured on 2020-10-05.
    * Terms of use: TBD

### Canada

* [Epidemiological summary of COVID-19 cases in Canada](https://health-infobase.canada.ca/covid-19/epidemiological-summary-covid-19-cases.html) / [COVID-19 Situational Awareness Dashboard](https://health-infobase.canada.ca/covid-19/dashboard/)
    * Epidemiology update / [Data on COVID-19 in Canada](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc): [can/epidemiology-update/covid19.csv](https://drive.google.com/drive/folders/1XV5MYKoU0_L506TxLLXYcLwqpTlIjLPd)
    	* Includes supplementary material: [Data dictionary (English)](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc) and [data dictionary (French)](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc)
* [Epidemiological summary of COVID-19 cases in Canada](https://health-infobase.canada.ca/covid-19/epidemiological-summary-covid-19-cases.html) / [COVID-19 Situational Awareness Dashboard](https://health-infobase.canada.ca/covid-19/dashboard/)
    * Epidemiology update / [Data on COVID-19 in Canada](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc): [can/epidemiology-update/covid19-download.csv](https://drive.google.com/drive/folders/1mDFGml4mEbHxM-iDDz2eZ2Hudr1r6EdB)
    	* Identical to the above dataset but the date column is in YYYY-MM-DD format instead of DD-MM-YYYY
    	* Includes supplementary material: [Data dictionary (English)](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc) and [data dictionary (French)](https://open.canada.ca/data/en/dataset/261c32ab-4cfd-4f81-9dea-7b64065690dc)
    * Epidemiology summary statements: [can/epidemiology-summary-statements/covid19-epiSummary-statements.csv](https://drive.google.com/drive/folders/1ye3nqS3qYNZtKdbNL1zoy8JY32bIVAq5)
    * NML summary: [can/nml-summary/covid19-epiSummary-NML.csv](https://drive.google.com/drive/folders/1HrHMnlm8i7Oh4OWAjDkYlIvguPuQDL9U)
    * NML weekly testing: [can/nml-weekly-testing/NML_weekly_testing.csv](https://drive.google.com/drive/folders/1NSCMEFZZ6JXPUFnPIb5HWwd4vXzoC8Fu)
    * Number of cases with detailed case report data: [can/detailed-case-report-n/covid19-nTotal.csv](https://drive.google.com/drive/folders/1-fJIOejwY_5jcTjUgv0sUiXCNqTZCqzO)
    * Cases and deaths by health region time series: [can/cases-and-deaths-by-hr-time-series/file_out_v5.csv](https://drive.google.com/drive/folders/1i6s8qCfxgBKH4kWAfe2Om_PT8FKkF6VX)
    * Health region UID table: [can/health-region-uid/covid19-healthregions-hruid.csv](https://drive.google.com/drive/folders/1mFXAnK0w8I-_QwdmzZE0ggyVgZWv-Hja)
    * Cases by exposure setting time series: [can/cases-by-exposure-time-series/covid19-epiSummary-casesovertime.csv](https://drive.google.com/drive/folders/1jtwuaKALJ7878Zd_a5TUqvm2JBf0jJTF)
    * Epidemic curve by date of illness onset by age group: [can/epidemic-curve-by-age/covid19-epiSummary-epiCurveByAge.csv](https://drive.google.com/drive/folders/1cbtuG5fdNRkrDuYa-mCUgrl-xGLf5dVA)
    * Severity by age group and sex: [can/severity-by-age-and-sex/covid19-epiSummary-severityUpdate.csv](https://drive.google.com/drive/folders/1_tux6ZwhCGtLt8fu8j-dcwd7ZsfYg3Dl)
    * Cases by severity: [can/cases-by-severity/covid19-epiSummary-severity.csv](https://drive.google.com/drive/folders/1SglBBOrkaUX9kgQnKFuGx8zYfWB-f4H2)
    * Cases by age group and sex: [can/cases-by-age-and-sex/covid19-epiSummary-agegroups2.csv](https://drive.google.com/drive/folders/1iTnavMq9a88c64arPRdmUN3w8V2UnugH)
    * Cases by probable exposure setting: [can/cases-by-probable-exposure-setting/covid19-epiSummary-probableexposure2.csv](https://drive.google.com/drive/folders/1hCGVda7X8NSJio4Km4sAHVvIKeY1WUbs)
    * Symptoms summary: [can/symptoms-summary/covid19-epiSummary-symptoms.csv](https://drive.google.com/drive/folders/1VoX9WJGkJQwCQMeOcTruitYjjIyGaFhZ)
    * Hospitalizaiton, intensive care (ICU), mechanical ventilation: [can/hospitalizations-icu-mechanical-ventilation/covid19-epiSummary-hospVentICU.csv](https://drive.google.com/drive/folders/1ZgeV7BTE_GZ8yTQgG3ema8OAT8vzHq5V)
    * Situational awareness dashboard update time: [can/situational-awareness-dashboard-update-time/covid19-updateTime.csv](https://drive.google.com/drive/folders/1Jf_083skdvYA9JW2-lPZ37l-NvdQ8AQY)
    * Terms of use: [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada)
* [COVIDTrends](https://health-infobase.canada.ca/covid-19/covidtrends/)
    * Mobility: [can/covidtrends-mobility/mobility.csv](https://drive.google.com/drive/folders/1rywSZlhHQzv7L9r8dIo7_hWgquTG7U45) [dataset is updated only on Thursdays]
    * FluWatchers: [can/covidtrends-fluwatchers/fluwatchers.csv](https://drive.google.com/drive/folders/1l9C7WppFIIc-hSxKRLd8i0dAon6YfbAs) [dataset is updated only on Thursdays]
    * Terms of use: [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada)
* [Detailed preliminary information on cases of COVID-19: 6 Dimensions (Aggregated data)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310077401)
    * [can/detailed-preliminary-case-info-aggregated-6-dimensions/13100774.csv](https://drive.google.com/drive/folders/1i_r1VTTylcwFUJU5Z2NxyDj58evLdICt)
    * Includes supplementary material: Footnotes, metadata
    * Terms of use: [Statistics Canada Open Licence](https://www.statcan.gc.ca/eng/reference/licence)
* [Detailed preliminary information on cases of COVID-19: 4 Dimensions (Aggregated data)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310077501)
    * [can/detailed-preliminary-case-info-aggregated-4-dimensions/13100775.csv](https://drive.google.com/drive/folders/1DAVw9bHgJ6HeIhR9gkDKqWb5mYmJeL6C)
    * Includes supplementary material: Footnotes, metadata
    * Terms of use: [Statistics Canada Open Licence](https://www.statcan.gc.ca/eng/reference/licence)
* [Detailed preliminary information on confirmed cases of COVID-19 (Revised)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310078101)
    * [can/detailed-preliminary-confirmed-case-info-revised/13100781.csv](https://drive.google.com/drive/folders/17yNdBoKhWikgRrosSvevZEJ7y75qpCxk) (Archived as of 2020-12-10, no longer part of the nightly update)
    * Variable value definitions are given in footnotes (see supplementary material).
    * **This file has been processed to avoid the 100mb file limit on GitHub.** (Base file size is > 400mb)
        * Dataset has been pivoted from long to wide (names from: 'Case information', values from: 'VALUE').
        * Columns containing no information have been dropped (GEO, DGUID, UOM, UOM_ID, SCALAR_FACTOR, SCALAR_ID, VECTOR, COORDINATE, STATUS, SYMBOL, TERMINATED, DECIMALS).
        * Example of original data format is preserved (see supplementary material).
    * Includes supplementary material: Footnotes, example of original data format, metadata
    * Terms of use: [Statistics Canada Open Licence](https://www.statcan.gc.ca/eng/reference/licence)
* [Preliminary dataset on confirmed cases of COVID-19, Public Health Agency of Canada](https://www150.statcan.gc.ca/n1/pub/13-26-0003/132600032020001-eng.htm)
    * [can/preliminary-dataset-on-confirmed-cases/COVID19-eng.csv](https://drive.google.com/drive/folders/1pxV8Wb1sqdeD-W6BIqUOPABLPvNTJPsX)
    * Includes supplementary material: user guide and data dictionary, metadata
    * Terms of use: [Statistics Canada Open Licence](https://www.statcan.gc.ca/eng/reference/licence)

### Manitoba

* [COVID-19 Updates](https://www.gov.mb.ca/covid19/updates/index.html)
    * Webpage: [mb/manitoba-webpage/manitoba-webpage.html](https://drive.google.com/drive/folders/13gGo5pdUJw1_4hVkPzrl3eNzUPjf6-4M)
    * Terms of use: TBD
* [Cases and Risk of COVID-19 in Manitoba](https://www.gov.mb.ca/covid19/updates/cases.html)
    * COVID-19 data by RHA and district: [mb/covid-data-by-rha-and-district/covid-data-by-rha-and-district.csv](https://drive.google.com/drive/folders/1mTTp74weBKLWXNrgdzfeJmWROP9NH6mM)
    * Cases by demographics and RHA: [mb/cases-demographics-by-rha/cases-demographics-by-rha.csv](https://drive.google.com/drive/folders/1XE4mZpz8hrqIC3JBExuGJdJYXs6Sg1rk)
    * Cases by status and RHA (Regional Health Authority): [mb/cases-by-status-and-rha/cases-by-status-and-rha.csv](https://drive.google.com/drive/folders/12Iqr-1tz085DB7Bsggm3tC0OKT0pNRSr)
    * Manitoba five-day test positivity rate: [mb/five-day-test-positivity/five-day-test-positivity.csv](https://drive.google.com/drive/folders/1FVZ9gQbSLjOJHGdq_FXjJIZrFsp12lOo)
    * Terms of use: TBD
    * Data have been converted from JSON queries to CSV

#### Winnipeg

* [COVID-19 By-law Enforcement (Winnipeg)](https://data.winnipeg.ca/Neighbourhood-Liveability-Property-Standards-Licen/COVID-19-By-law-Enforcement/ndr6-96vi)
    * [mb/winnipeg-by-law-enforcement/COVID-19_By-law_Enforcement.csv](https://drive.google.com/drive/folders/1LR1UTIs_r7w_uvC-ScZ8k3WlU-0SIVlc)
    * Terms of use: [Open Government Licence - Winnipeg](https://data.winnipeg.ca/open-data-licence)
    Not included as part of the nightly update, as it does not seem to be receiving regular updates (last new data: June 5, 2020)
* [COVID-19 Designated Active Transportation Route Counts (Winnipeg)](https://data.winnipeg.ca/Transportation-Planning-Traffic-Management/COVID-19-Designated-Active-Transportation-Route-Co/aqka-nz2g)
    * [mb/winnipeg-active-transportation/COVID-19_Designated_Active_Transportation_Route_Counts.csv](https://drive.google.com/drive/folders/1HvDvmC9fkNMPgmr-kQT1Lj6Rg-CHOh75)
    * Terms of use: [Open Government Licence - Winnipeg](https://data.winnipeg.ca/open-data-licence)
    * Not included as part of the nightly update, as it does not seem to be receiving regular updates (last updated: June 29, 2020)

### Northwest Territories

* [https://www.gov.nt.ca/covid-19/](https://www.gov.nt.ca/covid-19/)
    * Webpage: [nt/nwt-webpage/nwt-webpage.html](https://drive.google.com/drive/folders/1K_lZ20FsBr3uc8z7VhbdP22xaD-_SFaV)
    * Terms of use: TBD

### Nova Scotia

* [Coronavirus (COVID-19): case data](https://novascotia.ca/coronavirus/data/)
    * [ns/case-data/ns-covid19-data.csv](hhttps://drive.google.com/drive/folders/1topV_6XkI2uz-Amwlibi8V_jbnHx4MG5)
    * Terms of use: Assumed to be [Open Government Licence – Nova Scotia](https://novascotia.ca/opendata/licence.asp)

### Nunavut

* [COVID-19 (Novel Coronavirus)](https://gov.nu.ca/health/information/covid-19-novel-coronavirus)
    * Webpage: [nu/nunavut-webpage/nunavut-webpage.html](https://drive.google.com/drive/folders/1bQ9qKAGjWXupRKdQcIOxyZf4lKZW5Obe)
    * Terms of use: TBD

### Ontario

* [How Ontario is responding to COVID-19](https://www.ontario.ca/page/how-ontario-is-responding-covid-19)
    * Webpage: [on/ontario-webpage/ontario-webpage.html](https://drive.google.com/drive/folders/19XxdLXVYaHdeks55FHcgAqFAifbETapT) (warning: some early files are .png screenshots and named differently)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Confirmed positive cases of COVID19 in Ontario](https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario/resource/455fd63b-603d-4608-8216-7d8647f43350)
    * [on/confirmed-positive-cases/conposcovidloc.csv](https://drive.google.com/drive/folders/16IDLOq9Q50Co4SEGAnu6ajzkKh8Xitgd)
    * Includes supplementary material: [Data dictionary (English and French)](https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario/resource/a2ea0536-1eae-4a17-aa04-e5a1ab89ca9a)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Status of COVID-19 cases in Ontario](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11)
    * [on/status-of-cases/covidtesting.csv](https://drive.google.com/drive/folders/1cbQvjhQkgHmk1BU6XrGFFuGXPUeNwVXX)
    * Includes supplementary material: [Data dictionary (English and French)](https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario/resource/7be0a14c-bf50-4340-9304-2b189d507541)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Status of COVID-19 cases in Ontario by Public Health Unit (PHU)](https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario-by-public-health-unit-phu)
    * [on/status-of-cases-by-phu/cases_by_status_and_phu.csv](https://drive.google.com/drive/folders/179ZsgcnrOIRTh2a04qlhH3HUafxrWWr3)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Ontario COVID-19 testing metrics by Public Health Unit (PHU)](https://data.ontario.ca/dataset/ontario-covid-19-testing-metrics-by-public-health-unit-phu)
    * [on/testing-metrics-by-phu/testing_metrics_by_phu.csv](https://drive.google.com/drive/folders/1W4mbKlbokc3Ebvpg6H96c-BZDCflWsyO)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Ontario COVID-19 testing percent positive by age group](https://data.ontario.ca/dataset/ontario-covid-19-testing-percent-positive-by-age-group)
    * [on/percent-positive-by-age-group/percent_positive_by_agegrp.csv](https://drive.google.com/drive/folders/1YGexaicLvEsasdhurYbjl_vKytmqF0hI)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [COVID-19 hospital metrics in Ontario by Local Health Integration Network (LHIN) regions](https://data.ontario.ca/dataset/covid-19-hospital-metrics-in-ontario-by-local-health-integration-network-lhin-regions)
    * [on/hosp-icu-by-lhin/lhin_hospital_icu_covid_data.csv](https://drive.google.com/drive/folders/11YJ2FvhHPWrLa__iTyuKAddsIq1yMcAS)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Effective reproduction number (Re) for COVID-19 in Ontario](https://data.ontario.ca/dataset/effective-reproduction-number-re-for-covid-19-in-ontario)
    * [on/effective_reproduction_number_ontario/effective_reproduction_number_ontario.csv](https://drive.google.com/drive/folders/19mPYJXuXcIta5B5bj0s_go5UUfNW0Gu6)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [COVID Alert Impact Data](https://data.ontario.ca/dataset/covid-alert-impact-data)
    * [on/covid_alert_downloads_canada/covid_alert_downloads_canada.csv](https://drive.google.com/drive/folders/11tsJ8mWvHpIrMK8TAfL_C8YZYvibdyQu)
    * [on/covid-alert-uploads-ontario/covid_alert_positive_uploads_ontario.csv](https://drive.google.com/drive/folders/1J80DArVNd-mduOexCY-CNZqBP8plfSTF)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [COVID-19 testing locations](https://data.ontario.ca/dataset/covid-19-assessment-centre-locations)
    * [on/testing-locations/locations.json](https://drive.google.com/drive/folders/1ugIMV9FyvRd2cgy_cctgMCaLUcccshLh)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Ontario COVID-19 outbreaks data](https://data.ontario.ca/dataset/ontario-covid-19-outbreaks-data)
    * Ongoing outbreaks: [on/ongoing-outbreaks/ongoing_outbreaks.csv](https://drive.google.com/drive/folders/1qgabHZsvO0YC4s5mQxE4G76wOhUF4Ns2)
    * Summary of cases associated with outbreaks: [on/summary-outbreak-cases/outbreak_cases.csv](https://drive.google.com/drive/folders/1X0vnDtDQkrbFJHcCV4nmhaPvqDligqcL)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [COVID-19 testing of inmates in Ontario’s Provincial Correctional Institutions](https://data.ontario.ca/dataset/covid-19-testing-of-inmates-in-ontario-s-correctional-institutions)
    * [on/correctional-institutions-inmates-testing/inmatetesting.csv](https://drive.google.com/drive/folders/1EH-C9nVEJTGpayGVLM908UA5Z5YHWf6t)
    * Includes supplementary material: [Technical documentation (English and French)](https://data.ontario.ca/dataset/covid-19-testing-of-inmates-in-ontario-s-correctional-institutions/resource/6e2868ab-a242-48d6-9f73-235d19a6668e)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Status of COVID-19 cases in Ontario’s Provincial Correctional Institutions](https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario-s-correctional-institutions)
    * [on/correctional-institutions-status/correctionsinmatecases.csv](https://drive.google.com/drive/folders/1XaPpPqJSKqA6G9IyJiPcP7vxh5Kd7sXm)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Long-Term Care Home COVID-19 Data](https://data.ontario.ca/dataset/long-term-care-home-covid-19-data)
    * Summary data: [on/long-term-care-home-summary/ltccovidsummary.csv](https://drive.google.com/drive/folders/12ZgUvwMaWRpNJlLZeJAzX_D9E26zW_9D)
    * Active outbreaks: [on/long-term-care-home-active/activeltcoutbreak.csv](https://drive.google.com/drive/folders/1E8qIt9REhO19jQyq970l9huc1y88OJIr)
    * Resolved outbreaks: [on/long-term-care-home-resolved/resolvedltc.csv](https://drive.google.com/drive/folders/1mjJUsbXVNm2UbdMDI_fNXngz4uCdYGq3)
    * Includes supplementary material: [Data dictionary (English and French)](https://data.ontario.ca/dataset/long-term-care-home-covid-19-data/resource/adbcf9f8-e473-4f27-b85f-0f05f686067b)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [COVID-19 cases in schools and child care centres](https://www.ontario.ca/page/covid-19-cases-schools-and-child-care-centres)
    * Webpage: [on/cases-schools-and-child-care-centres-webpage/cases-schools-and-child-care-centres-webpage.html](https://drive.google.com/drive/folders/1ammQkFJl9xeoOKkVNtGDGwu4z5WFImZW) (warning: some early files are .png screenshots and named differently)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Schools COVID-19 data](https://data.ontario.ca/dataset/summary-of-cases-in-schools)
    * Summary of cases in schools: [on/schools-summary/schoolcovidsummary.csv](https://drive.google.com/drive/folders/1PNTdW1MWrj3Xjrhu8lQbqn3gtzkluepz)
    * Schools with active COVID-19 cases: [on/schools-active/schoolsactivecovid.csv](https://drive.google.com/drive/folders/1NhQmGYR0l4Don6YGJiU5s_X6e7b2zVfQ)
    * Cases in school board partners: [on/school-board-partners/schoolpartnersactivecovid.csv](https://drive.google.com/drive/folders/1LRJ8z_a1N99O4sscNBXBY84yjHDoYLy9)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Licensed child care settings COVID-19 data](https://data.ontario.ca/dataset/summary-of-cases-in-licensed-child-care-settings)
    * Summary of cases in licensed child care settings: [on/licensed-child-care-settings-summary/lccovidsummary.csv](https://drive.google.com/drive/folders/1Z0Z5nA1CjkqhJyQlIXDHXFJi4H4d_xQG)
    * Licensed child care centres and agencies with active COVID-19 cases: [on/licensed-child-care-settings-active/lccactivecovid.csv](https://drive.google.com/drive/folders/1CFmQCx6Q0GKTqyyKK-UOSvoMb3VgpaNk)
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)

#### Toronto

* [City of Toronto Daily Status of COVID-19 Cases](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-daily-status/CityofToronto_COVID-19_Daily_Public_Reporting.xlsx](https://drive.google.com/drive/folders/1ie-DHoYsbMcWRBrBZRqsbV50BIon0MU_)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto COVID-19 Summary](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-covid-summary/CityofToronto_COVID-19_Data.xlsx](https://drive.google.com/drive/folders/1iZPRXgEoKslYNQpY_nbo_NmP2LYThFkA)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto COVID-19 Neighbourhood Case Data](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-neighbourhood-data/CityofToronto_COVID-19_NeighbourhoodData.xlsx](https://drive.google.com/drive/folders/1c7xVzZIwOx2M1dN9XvKYEf_Di51tQyD9)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto COVID-19 Neighbourhood Testing Data](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-neighbourhood-test-data/CityofToronto_COVID-19_Testing.xlsx](https://drive.google.com/drive/folders/16cwwF0IAiXpB2cbXNA7A9hCuaG8DF3bR)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto COVID-19 Monitoring Dashboard](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-monitoring-dashboard/CityofToronto_COVID-19_RecoveryData.xlsx](https://drive.google.com/drive/folders/1fHmGdLjTGoQXVuyGnTfMZ1UbMrQrnQ6P)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [City of Toronto Ethno-Racial Group, Income, & Infection](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * [on/toronto-ethno-racial-income/Ethno-Racial_Group,_Income,_and_COVID-19_Infection.xlsx](https://drive.google.com/drive/folders/1Q4esWyxm6SstZGQr-kR_32bpichsICYo) (original file name is Ethno-Racial Group, Income, and COVID-19 Infection.xlsx, renamed to avoid spaces in file name)
    * Include supplementary material: Technical notes
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
    * Not included as part of the nightly update, as it does not seem to be receiving regular updates (data as of September 30, 2020)
* [COVID-19 Cases in Toronto](https://open.toronto.ca/dataset/covid-19-cases-in-toronto/)
    * [on/toronto-cases/COVID19_cases.csv](https://drive.google.com/drive/folders/1npUc4yyVR865IAX1DuqPosc-TjpO14M3)
    * Data are extracted at 3 PM on the Monday of a given week and posted by Wednesday [dataset is updated only on Wednesdays]
    * Terms of use: Assumed to be [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [University of Toronto COVID-19 tracking](https://www.utoronto.ca/utogether2020/covid19-dashboard)
    * [on/u-of-t-covid-tracking-webpage/u-of-t-covid-tracking-webpage.html](https://drive.google.com/drive/folders/1D4KzZVWz-vw96dxJVJHNpFpXnRh9or5J) (warning: some early files are .png screenshots and named differently)
    * Data are reported every Monday with cumulative cases through the previous Friday [screenshots will be take every day in case the update frequency increases]
    * Terms of use: TBD

#### Ottawa

* [Daily COVID-19 Dashboard (Ottawa)](https://www.ottawapublichealth.ca/en/reports-research-and-statistics/daily-covid19-dashboard.aspx)
    * [Demographics and Source of Infection for Cases, Deaths, and Hospitalizations](https://www.arcgis.com/home/item.html?id=6bfe7832017546e5b30c5cc6a201091b): [on/ottawa-cases-deaths-hosp-demographics-source-of-infection/COVID-19_Cases_and_Deaths_Ottawa_EN.csv](https://drive.google.com/drive/folders/1e-u-utGtP-NDBAigdrW36sDeWSCwz5Ji)
    * [Outbreaks in Healthcare Institutions, Childcare, Summer Camps, and Educational Establishments](https://www.arcgis.com/home/item.html?id=5b24f70482fe4cf1824331d89483d3d3): [on/ottawa-outbreaks-healthcare-childcare-camps-schools/COVID-19_Institutional_Outbreaks.csv](https://drive.google.com/drive/folders/1wZ27q90_Uom6QCP0UMr6wGSlzQc_sAOo)
    * [Community Outbreaks](https://open.ottawa.ca/datasets/0df365456c254fbc942fe3d85c3dbf83): [on/ottawa-community-outbreaks/COVID-19_Community_Outbreaks_in_Ottawa.csv](https://drive.google.com/drive/folders/13j5pzMJAigvkgxMsxvx1lKfH_rEC2G84)
    * [Weekly Rates](https://www.arcgis.com/home/item.html?id=734a327141b14a55b666953c9141abf3): [on/ottawa-weekly-rates/COVID-19_Weekly_Cases_and_Rates_by_Age_in_Ottawa_EN.csv](https://drive.google.com/drive/folders/1dovKNHy8EgGajqIqP-tn3j9v2GpdlHUn)
    * [Estimated Reproduction Number in Ottawa](https://www.arcgis.com/home/item.html?id=d010a848b6e54f4990d60a202f2f2f99): [on/ottawa-estimated-rt/EN_-_Covid-19_Reproduction_Number,_R(t).csv](https://drive.google.com/drive/folders/1PM3nvFv3a1zZ6755aT2jpyvpjFjnaqUb)
    * [Testing - Ottawa Residents](https://www.arcgis.com/home/item.html?id=26c902bf1da44d3d90b099392b544b81): [on/ottawa-residents-tested/COVID-19_Ottawa_Residents_Tested_EN.csv](https://drive.google.com/drive/folders/1E3udpKQCqEaOh4aCt1zk7cUb8uZoasqg)
    * Ottawa cases and deaths: [on/ottawa-cases-and-deaths/COVID-19_Cases_and_Deaths_in_Ottawa_EN.csv](https://drive.google.com/drive/folders/18qasHo8WbSbKMKap8O0125vnvUb81OjB) (Archived as of 2020-09-21, no longer part of the nightly update)
    * Ottawa outbreaks in healthcare institutions: [on/ottawa-outbreaks-in-healthcare-institutions/COVID-19_Outbreaks_in_Ottawa_Healthcare_Institutions_EN.csv](https://drive.google.com/drive/folders/16rbTbd5EcwENtGNf9RgnQbojzf4he_0D) (Archived as of 2020-09-21, no longer part of the nightly update)
    * Ottawa hospitalization data: [on/ottawa-hospitalization/Hospitalizations_of_Ottawa_residents_with_confirmed_COVID-19.csv](https://drive.google.com/drive/folders/1v_5gCnHxRRzKZ8cdmWEnCFkLotY3K-7R) (Archived as of 2020-09-21, no longer part of the nightly update)
    * Include supplementary material: User guide, technical guide, overall status assessment
    * Terms of use: [Open Government Licence – City of Ottawa](https://ottawa.ca/en/city-hall/get-know-your-city/open-data#open-data-licence-version-2-0)

### Quebec

When both French and English data files are available, French files should be considered definitive (and in many cases, these files have been captured in the archive for a longer duration). The English versions of files avaiable in both languages will always have their directories marked with "-en" at the end.

* [Data on COVID-19 in Québec (province)](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    * [Webpage EN](https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/): [qc/qc-webpage-en/qc-webpage-en.html](https://drive.google.com/drive/folders/1dpolshJwFvHWZQxOG58LY-l0pztntYdi)
    * [Webpage FR](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/): [qc/qc-webpage-fr/qc-webpage-fr.html](https://drive.google.com/drive/folders/1nQvnGfZdxIkhibJZHyp4ahbn27q_z3ll)
    * Situation in Quebec: [qc/situation-in-quebec/situation-au-quebec.csv](https://drive.google.com/drive/folders/1en-wC4O6X6CGKJjBWuyqcP9NRT9O8D61)
    * Correctional facilities - cases among employees (FR): [qc/correctional-cases-employees/donnees_covid_detention_employes_FR.csv](https://drive.google.com/drive/u/2/folders/1FZ8Edx6Xv2cx1mOsh7a5FFY1nI3UGLYE)
    * Correctional facilities - cases among employees (EN): [qc/correctional-cases-employees-en/donnees_covid_detention_employes_EN.csv](https://drive.google.com/drive/u/2/folders/18PcQcnuS0gPLi7D2Tnd40l7VOMeJm4hf)
    * Correctional facilities - cases among detainees (FR): [qc/correctional-cases-detainees/](https://drive.google.com/drive/u/2/folders/1WjUeIALF5440iKvvEUvm6cyDav4rYDcq)
    * Correctional facilities - cases among detainees (EN): [qc/correctional-cases-detainees/donnees_covid_detention_personnes_incarcerees_EN.csv](https://drive.google.com/drive/u/2/folders/1aBEKVOBqMqpqShE_feXQTvHDgZC3M1dl)
    * Vaccine doses administered by RSS (FR): [qc/vaccine-doses-admin-by-rss/doses-vaccins.csv](https://drive.google.com/drive/u/2/folders/1-ileQelY2aoJFcCSJSu3JG6bZrGWFFbS)
    * Vaccine doses administered by RSS (EN): [qc/vaccine-doses-admin-by-rss-en/doses-vaccins-en.csv](https://drive.google.com/drive/u/2/folders/1MWPkSGMfOMGqJNNv7LEJzWA1AAB3h3yI)
    * Outbreaks by setting (FR): [qc/outbreaks-by-setting/eclosions-par-milieu.csv](https://drive.google.com/drive/u/2/folders/1tz41XR2Y0ToSW4fAFU5qf7HP3E4u3AFw)
    * Outbreaks by setting (EN): [qc/outbreaks-by-setting-en/eclosions-par-milieu-en.csv](https://drive.google.com/drive/u/2/folders/1p4EFQ_r4x4wjp76zOwlW9gD7-3sKX4z4)
    * Cases percentage by age group (FR): [qc/cases-percentage-by-age-group/pourcentage-cas-age.csv](https://drive.google.com/drive/folders/1lJhiUMKOoDUwltflhOhtmDnjKpD8-zll)
    * Cases percentage by age group (EN): [qc/cases-percentage-by-age-group-en/pourcentage-cas-age-en.csv](https://drive.google.com/drive/u/2/folders/1tIW1eONhV1tvhYbappJ44zfvzTpb2RSA)
    * Deaths percentage by age group (FR): [qc/deaths-percentage-by-age-group/pourcentage-deces-age.csv](https://drive.google.com/drive/folders/1Ef1oPsTMGckPZu3sG87zDRjJRWdp864t)
    * Deaths percentage by age group (EN): [qc/deaths-percentage-by-age-group-en/pourcentage-deces-age-en.csv](https://drive.google.com/drive/u/2/folders/1CPP_HMuwljqcktPUgM8TaZK3DF7fRJP9)
    * Cumulative deaths by region (FR): [qc/cumulative-deaths-by-region/deces-region.csv](https://drive.google.com/drive/folders/1RH4vu1SlIefnk-tr1qaKueJrVsSDUrk7)
    * Cumulative deaths by region (EN): [qc/cumulative-deaths-by-region-en/deces-region-en.csv](https://drive.google.com/drive/u/2/folders/1uL2HHOqEDTl3GoBJDo2EAxkzl2OFw34F)
    * Recent daily cases by region (FR): [qc/recent-daily-cases-by-region/cas-region.csv](https://drive.google.com/drive/folders/1_HAaI1p-gB7cEOKNXOo2-A-TaBiD79WB)
    * Recent daily cases by region (EN): [qc/recent-daily-cases-by-region-en/cas-region-en.csv](https://drive.google.com/drive/u/2/folders/18sAMq1Rv5NkxJPUP__Kc4uUWkvllHoAR)
    * COVID-19 daily data 7 days (FR): [qc/covid-data-daily-7-days/synthese-7jours.csv](https://drive.google.com/drive/folders/1-1Y6dKczLPQU5Rm48eTzJVf9Vpio2pas) (Renamed to synthese-7joursV2.csv from synthese-7jours.csv after 2020-11-09; later renamed again to synthese-7jours.csv - a substantial number of files from November and December are missing due to this change)
    * COVID-19 daily data 7 days (EN): [qc/covid-data-daily-7-days-en/synthese-7jours-en.csv](https://drive.google.com/drive/u/2/folders/1hiLaw3OLYZK9FIHs68iBheGdJXGRy-9E)
    * Cases by region 7 days (FR): [qc/cases-by-region-7-days/cas-region-7jours.csv](https://drive.google.com/drive/folders/1FMpdMDozL9ywLrOR-i0ZF7TAiq5rozqF)
    * Cases by region 7 days (EN): [qc/cases-by-region-7-days-en/cas-region-7jours-en.csv](https://drive.google.com/drive/u/2/folders/10xY0nXr1_kDzeMh-duCepokVg7zSX6I6)
* [Données COVID-19 au Québec (INSPQ)](https://www.inspq.qc.ca/covid-19/donnees)
    * COVID-19 time series by region and demographics: [qc/covid-time-series-by-region-and-demographics/covid19-hist.csv](https://drive.google.com/drive/folders/18IVG9ivYK-kQ7joEZptyje6fu0rf4T7M)
    * COVID-19 data (charts - summary, time series, and hospitalization by age): [qc/covid-data-charts-summary-time-series-hosp-by-age/manual-data.csv](https://drive.google.com/drive/folders/1imkAJIUffYtI5KaYZxgiAtagXXDwckoX)
    * Summary by region: [qc/summary-by-region/regions.csv](https://drive.google.com/drive/folders/1uUZjV0sxOEoMZSQj-PFArGwhEvIrspDq)
    * Deaths by RSS (health region) and living environment: [qc/deaths-by-rss-and-living-environment/tableau-rpa-new.csv](https://drive.google.com/drive/folders/1w5VHBvF3JTQ12Y_gKMGGOcszpvSY8rwy) (Renamed from tableau-rpa.csv after 2020-09-16)
    * Cases by RSS (health region) and RLS (local service network): [qc/cases-by-rss-and-rls/tableau-rls-new.csv](https://drive.google.com/drive/folders/1bv4tNVmKUhoRUYsMIubKwEdy7U3fmsF2) (Renamed from tableau-rls.csv after 2020-09-16)
    * Comparisons (provinces): [qc/comparisons-provinces/comparaisons_prov.csv](https://drive.google.com/drive/folders/1060dqZQJ2SMkygJHNSEsl3FSTXE6TMIX)
    * Comparisons (countries): [qc/comparisons-countries/comparaisons_pays.csv](https://drive.google.com/drive/folders/1x0RZUSKCk7Ou6Z9i7udfuxe7WgQDfZwU)
    * COVID-19 time series by region: [qc/covid-time-series-by-region/PL_DATE.csv](https://drive.google.com/drive/folders/11scpEF8GUwV_qRCLTn-y9-po6PHiZYmW) (Archived as of 2020-10-15, no longer part of the nightly update)
        * [Advice for data process by Simon Coulombe](https://gist.github.com/SimonCoulombe/9a329052ac4cefd421febd8650ed84e2)
    * COVID-19 data: [qc/covid-data/combine.csv](https://drive.google.com/drive/folders/1Mx9H2AfYncQGifc_lNcUWr32MrPIepc7) (Archived as of 2020-09-16, no longer part of the nightly update)
    * COVID-19 data (charts): [qc/covid-data-charts/combine2.csv](https://drive.google.com/drive/folders/11lkpfIvQW6tVH4c7w6ZlQ36R4mMudbxX) (Archived as of 2020-09-16, no longer part of the nightly update)
    * Terms of use: TBD
* [Données COVID-19 par âge et sexe au Québec](https://www.inspq.qc.ca/covid-19/donnees/age-sexe)
    * COVID-19 data by age group and sex: [qc/covid-data-by-age-and-sex/PL_AGE_SEXE.csv](https://drive.google.com/drive/folders/1o7tM8U8BiLufnEecVEZthKHactdv1UfY)
    * Terms of use: TBD
* [Données sur la COVID-19 au Québec](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    * Deaths time series by living environment: [qc/deaths-time-series-by-living-environment/decesquotidien.csv](https://drive.google.com/drive/folders/1Pb1yqZsQsq40EBH0MVPGIJtS_Uoe1Fj2)
    * Terms of use: TBD
* [Situation dans les milieux de vie pour personnes aînées et vulnérables](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    * Status report on confirmed cases and deaths by RPA (private residences for seniors): [qc/status-report-cases-and-deaths-by-rpa/etat_situation_rpa.pdf](https://drive.google.com/drive/folders/1nkDpCrXj6Y9Qc-E2fWzRznZx97HXAE6Y)
    * Status report on confirmed cases and deaths by CHSLD (residential and long-term care centres): [qc/status-report-cases-and-deaths-by-chsld/etat_situation_chsld.pdf](https://drive.google.com/drive/folders/15uQXy5cVSBYePYA5kb0-S7tIZ_ylCYF9)
    * Supplementary material: [Canadian Armed Forces report on their presence in CHSLDs](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec)
    * Terms of use: TBD
* [Situation dans les établissements scolaires](https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/)
    * Highlights - public and private school system: [qc/schools-highlights/reseauScolaire_faitsSaillants.pdf](https://drive.google.com/drive/folders/1HtX-WTyzqo1FICQfJ08N0fTlPeJOMU_H)
    * List of schools - public and private school system: [qc/schools-list-of-schools/reseauScolaire_listeEcoles.pdf](https://drive.google.com/drive/folders/10CgT6m9BXmE4oeyNgNh3fm0ix1fvLuD2)
    * Formerly [Situation dans les établissements scolaires relative à la COVID-19](https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/etat_situation_ecole.pdf): qc/schools-list-of-schools/etat_situation_ecole_2020-09-04_2020-09-06/etat_situation_ecole.pdf
    * Formerly [Liste des écoles ayant au moins un cas rapporté de la COVID-19 depuis le 1er septembre 2020](https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/liste-ecole-cas-rapportes.pdf): qc/schools-list-of-schools/liste-ecole-cas-rapportes_2020-09-08_2020-09-09/liste-ecole-cas-rapportes.pdf
    * Terms of use: TBD

#### Montreal

* [Situation du coronavirus (COVID-19) à Montréal](https://santemontreal.qc.ca/population/coronavirus-covid-19/situation-du-coronavirus-covid-19-a-montreal/)
    * **Note that these files are actually semicolon-separated since they use a comma as the decimal marker (rather than a period) and are encoded as ISO 8859-15 (rather than UTF-8)**
    * Montréal cases and deaths by CIUSSS (integrated health and social services centres): [qc/montreal-cases-and-deaths-by-ciusss/ciusss.csv](https://drive.google.com/drive/folders/1uamAn7K3n6WSIxiX9eGC6y63zPItMJAU)
    * Montréal cases by area: [qc/montreal-cases-by-area/municipal.csv](https://drive.google.com/drive/folders/1pLFw7YV4MjmvYT0D5NfGRcbHyShYyvzV)
    * Montréal cases and deaths by age group: [qc/montreal-cases-and-deaths-by-age-group/grage.csv](https://drive.google.com/drive/folders/1C8Ss53ZAMB0wsMR_lUoVAY5E_u3D49Rm)
    * Montréal cases and deaths by sex: [qc/montreal-cases-and-deaths-by-sex/sexe.csv](https://drive.google.com/drive/folders/1Lmo64ITgPBcDhsYqM7s7J2xyGlTfLpj8)
    * Montréal epidemic curve: [qc/montreal-epidemic-curve/courbe.csv](https://drive.google.com/drive/folders/1kF-aOahhGJzAyZv0KAlwyi_l-HPoaETi)
    * Terms of use: TBD

### Saskatchewan

* [Saskatchewan's Dashboard - Total Cases](https://dashboard.saskatchewan.ca/health-wellness/covid-19/cases)
    * CSV: [sk/cases-by-region/cases.csv](https://drive.google.com/drive/folders/1BKhWul6Vo2FZXK5dVmn9frIaMicFLfzD)
    * Webpage: [sk/cases-by-region-webpage/cases-webpage.html](hhttps://drive.google.com/drive/folders/1m7_t1qB0x-yVpOb6e1Rzfk5uUQ6iFmqO) (warning: some early files are .png screenshots and named differently)
    * Terms of use: TBD
* [Saskatchewan's Dashboard - Total Tests](https://dashboard.saskatchewan.ca/health-wellness/covid-19-tests/tests)
    * CSV: [sk/tests-by-region/tests.csv](https://drive.google.com/drive/folders/1iOdc5ij_1xWNrkwWWe1qwbW3GM5wbq1Y)
    * Webpage: [sk/tests-by-region-webpage/tests-webpage.html](https://drive.google.com/drive/folders/1ixZJWXkMMV3Mftb51_sRGtGwJ3RV-QXX) (warning: some early files are .png screenshots and named differently)
    * Terms of use: TBD

### Yukon

* [Case counts: COVID-19](https://yukon.ca/en/case-counts-covid-19)
    * Webpage: [yt/yukon-case-counts-webpage/yukon-case-counts-webpage.html](https://drive.google.com/drive/folders/1NSTT2mi_oGQNxU0iL5zBAGj51E5xrAEo)
    * Terms of use: TBD

* [Current COVID-19 situation](https://yukon.ca/en/health-and-wellness/covid-19-information/latest-updates-covid-19/current-covid-19-situation)
    * Webpage: [yt/yukon-current-situation-webpage/yukon-current-situation-webpage.html](https://drive.google.com/drive/folders/1a6XY7QavteiB2QBd4zMdFVWl08j0k83b)
    * Terms of use: TBD

### Other: Non-governmental sources

#### Canada

* [Canada COVID-19 School Case Tracker](https://masks4canada.org/canada-covid-19-school-case-tracker/)
    * [other/can/canada-covid-19-school-case-tracker/Canada_COVID-19_School_Report_Tracker.kml](https://drive.google.com/drive/folders/1Ssj8EcPDd-yQpCKvDuokrRpwQLkgWUEG) (original file name is Canada COVID-19 School Report Tracker.kml, renamed to avoid spaces in file name; warning: some early files are in .kmz format, which is compressed but handled almost identically to .kml)
    * Terms of use: TBD
* [Unofficial COVID Alert Dashboard](https://github.com/uhengart/covid-alert-dashboard)
    * Estimated infections per day: [other/can/unofficial-covid-alert-dashboard/estimated_infections_per_day.txt](https://drive.google.com/drive/folders/1tCtgZArFKt1jOwzSvBLguJz2r5TUScPd) (Replaced after 2020-11-14 by unofficial-covid-alert-dashboard-analysis, no longer part of the nightly update)
    * Diagnosis key analysis: [other/can/unofficial-covid-alert-dashboard-analysis/DiagnosisKeysAnalysis.csv](https://drive.google.com/drive/folders/1u02hYgE98Mm731AGYm85Iq5nreMX8E3S)
    * Upload delay: [other/can/unofficial-covid-alert-dashboard-upload-delay/UploadDelay.csv](https://drive.google.com/drive/folders/13RWuBGsOqlz1g4qoeUxa58qYY0aUnymK)
    * Terms of use: TBD   

#### Quebec

* [Covid Écoles Québec: Number of schools](https://www.covidecolesquebec.org/liste-alphabtique)
    * [Excel spreadsheet](https://drive.google.com/file/d/1xOl0uhyx9IuHZfJuRH-OR7BcGFuWYUex/view): [other/qc/covid-ecoles-quebec-school-list/COVIDECOLESQUEBEC.xlsx](https://drive.google.com/drive/folders/1wOEm8a6HsHXbCwp0dVCe9iwDa1kymS5o) (original file name is COVIDECOLESQUEBEC_20200905.xlsx, renamed to avoid confusion)
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
