# Archive of COVID-19 Data from Canadian Government Sources

This repository provides automated, daily backups of COVID-19 data from various Canadian government sources.

**File name timestamps are given in ET (America/Toronto) in the following format: %Y%-m-%d_%H-%M.** The script is run nightly around 23:00 ET.

All code in this repository is covered by the [MIT License](https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data/blob/master/LICENSE). Licenses and terms of use for each archived dataset are given below.

## Contributing

Community members may contribute to this repository in three ways:

* Create an issue to request a dataset be added to the archive.
* Create a pull request for *archiver.py* adding the ability to automatically archive a requested or not-yet-implemented dataset.
* Submit archived versions of an existing, requested, or not-yet-implemented dataset. If possible, please use the original file name plus timestamp in the format described above.

## Data sources/terms of use

The sources and terms of use for each included dataset are linked below.

### Alberta

* [COVID-19 Alberta statistics](https://www.alberta.ca/stats/covid-19-alberta-statistics.htm)
    * To be added
    * Terms of use: See “data notes” tab of [website](https://www.alberta.ca/stats/covid-19-alberta-statistics.htm)
* [COVID-19 in Alberta: Current cases by local geographic area (Edmonton)](https://data.edmonton.ca/Community-Services/COVID-19-in-Alberta-Current-cases-by-local-geograp/ix8f-s9xp)
    * ab/edmonton-cases-by-areas/COVID-19_in_Alberta__Current_cases_by_local_geographic_area.csv
    * Terms of use: [City of Edmonton Open Data Terms of Use](https://data.edmonton.ca/stories/s/City-of-Edmonton-Open-Data-Terms-of-Use/msh8-if28/)

### British Columbia

* [BC COVID-19 Data](http://www.bccdc.ca/health-info/diseases-conditions/covid-19/data)
    * Case data: bc/case-data/BCCDC_COVID19_Dashboard_Case_Details.csv
    * Laboratory data: bc/laboratory-data/BCCDC_COVID19_Dashboard_Lab_Information.csv
    * Terms of use: [Disclaimer and data notes](http://www.bccdc.ca/Health-Info-Site/Documents/BC_COVID-19_Disclaimer_Data_Notes.pdf)

### Canada

* [Coronavirus disease 2019 (COVID-19): Epidemiology update](https://health-infobase.canada.ca/covid-19/epidemiological-summary-covid-19-cases.html)
    * can/epidemiology-update/covid19.csv
    * Terms of use: [Open Government Licence - Canada](https://open.canada.ca/en/open-government-licence-canada)

### Ontario

* [Confirmed positive cases of COVID19 in Ontario](https://data.ontario.ca/dataset/confirmed-positive-cases-of-covid-19-in-ontario/resource/455fd63b-603d-4608-8216-7d8647f43350)
    * on/confirmed-positive-cases/conposcovidloc.csv
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [Status of COVID-19 cases in Ontario](https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11)
    * on/status-of-cases/covidtesting.csv
    * Terms of use: [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario)
* [City of Toronto COVID-19 Summary](https://www.toronto.ca/home/covid-19/covid-19-latest-city-of-toronto-news/covid-19-status-of-cases-in-toronto/)
    * on/toronto-covid-summary/CityofToronto_COVID-19_Data.xlsx
    * Terms of use: [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)
* [COVID-19 Cases in Toronto](https://open.toronto.ca/dataset/covid-19-cases-in-toronto/)
    * Data are extracted at 3 PM on the Monday of a given week and posted by Wednesday [dataset is updated only on Wednesdays]
    * Terms of use: [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/)

## Acknowledgements

Many people are to thank for contributing archived data to this repository.

* [Jens von Bergmann](https://github.com/mountainMath)
