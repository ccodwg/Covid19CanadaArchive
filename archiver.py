# import modules
from os
import pandas as pd
from datetime import datetime
import pytz
from github import Github

# access repo
token = os.environ['GH_TOKEN']
g = Github(token)
repo = g.get_repo('jeanpaulrsoucy/covid-19-canada-gov-data')

# commit string
commit = 'Nightly update: ' + str(datetime.now(pytz.timezone('America/Toronto')).date())

# function: download and commit csv
def dl_csv(link, path, file, commit):
    data = pd.read_csv(link)
    name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
    repo.create_file(path + name + '.csv', commit, data.to_csv(index=False))

# AB - COVID-19 in Alberta: Current cases by local geographic area (Edmonton)
dl_csv('https://data.edmonton.ca/api/views/ix8f-s9xp/rows.csv?accessType=DOWNLOAD',
       'ab/edmonton-cases-by-areas/',
       'COVID-19_in_Alberta__Current_cases_by_local_geographic_area',
       commit)

# BC - BC COVID-19 Data (Case data)
dl_csv('http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv',
       'bc/case-data/',
       'BCCDC_COVID19_Dashboard_Case_Details',
       commit)

# BC - BC COVID-19 Data (Laboratory data)
dl_csv('http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Lab_Information.csv',
       'bc/laboratory-data/',
       'BCCDC_COVID19_Dashboard_Lab_Information',
       commit)

# CAN - Coronavirus disease 2019 (COVID-19): Epidemiology update
dl_csv('https://health-infobase.canada.ca/src/data/covidLive/covid19.csv',
       'can/epidemiology-update/',
       'covid19',
       commit)

# ON - Confirmed positive cases of COVID19 in Ontario
dl_csv('https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv',
       'on/confirmed-positive-cases/',
       'conposcovidloc',
       commit)

# ON - Status of COVID-19 cases in Ontario
dl_csv('https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv',
       'on/status-of-cases/',
       'covidtesting',
       commit)
