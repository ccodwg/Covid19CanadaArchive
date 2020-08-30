# import modules
import sys
import time
import os
from datetime import datetime
import pytz
from github import Github
import requests
import tempfile
from selenium import webdriver # requires ChromeDriver and Chromium/Chrome
from selenium.webdriver.chrome.options import Options
from colorit import *

# allow script to be run in testing mode (no commits written)
if len(sys.argv) == 1:
        mode = 'prod'
elif len(sys.argv) == 2 and sys.argv[1] == 'test':
        mode = 'test' # testing on server
elif len(sys.argv) == 2 and sys.argv[1] == 'localtest':
        mode = 'localtest' # testing on local machine
else:
        sys.exit("Error: Invalid arguments.")

# print with colour
init_colorit()

# access repo
if mode == 'prod':
        token = os.environ['GH_TOKEN']
        g = Github(token)
        repo = g.get_repo('jeanpaulrsoucy/covid-19-canada-gov-data')

# commit string
t = datetime.now(pytz.timezone('America/Toronto'))
commit = 'Nightly update: ' + str(t.date())

# function: download and commit file
def dl_file(url, path, file, commit, user=False, ext='.csv'):
        if user == True:
                headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
                req = requests.get(url, headers=headers)
        else:
                req = requests.get(url)
        name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
        if not req.ok:
                print(background('Error downloading: ' + name, Colors.red))
        elif mode != 'prod':
                print(color('Test download successful: ' + name, Colors.green))
        else:
                data = req.content
                repo.create_file(path + name + ext, commit + ' (' + path + ')', data)
                print(color('Commit successful: ' + name, Colors.green))

# function: download and commit csv from AB - "COVID-19 Alberta statistics"
def dl_ab_cases(url, path, file, commit, ext='.csv', wait=5, attempts=3, verbose=False):
        
        ## attempts begin at 0
        a = 0
        
        ## attempt download
        while(a < attempts):
                ## create temporary directory
                tmpdir = tempfile.TemporaryDirectory()
                
                ## setup webdriver
                options = Options()
                if mode != 'localtest':
                        options.binary_location = os.environ['GOOGLE_CHROME_BIN']
                options.add_argument("--headless")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--no-sandbox")
                prefs = {'download.default_directory' : tmpdir.name}
                options.add_experimental_option('prefs', prefs)
                if mode != 'localtest':
                        driver = webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_PATH'], options=options)
                else:
                        driver = webdriver.Chrome(options=options)
                driver.implicitly_wait(10)
                
                ## click to export
                driver.get(url)
                elements = driver.find_elements_by_tag_name("li")
                for element in elements:
                        if element.text == 'Data export':
                                element.click()
                elements = driver.find_elements_by_tag_name("button")
                for element in elements:
                        if element.text == 'CSV':
                                element.click()
                
                ## verify download
                fpath = os.path.join(tmpdir.name, file + ext)
                time.sleep(wait) # wait for download to finish before checking
                if not os.path.isfile(fpath):
                        a += 1
                        if verbose:
                                print(color('Attempt ' + str(a) + ' failed...', (150, 150, 150)))
                        continue
                else:
                        break
        
        ## commit file
        name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
        if not os.path.isfile(fpath):
                print(background('Error downloading: ' + name, Colors.red))
        elif mode != 'prod':
                print(color('Test download successful: ' + name, Colors.green))
        else:
                with open(fpath, 'r') as f:
                        data = f.read()
                repo.create_file(path + name + ext, commit + ' (' + path + ')', data)
                print(color('Commit successful: ' + name, Colors.green))

# function: download and commit csv from AB - "COVID-19 relaunch status map"
def dl_ab_relaunch(url, path, file, commit, ext='.csv', wait=5, attempts=3, verbose=False):
        
        ## attempts begin at 0
        a = 0
        
        ## attempt download        
        while(a < attempts):
                ## create temporary directory
                tmpdir = tempfile.TemporaryDirectory()        
                
                ## setup webdriver
                options = Options()
                if mode != 'localtest':
                        options.binary_location = os.environ['GOOGLE_CHROME_BIN']
                options.add_argument("--headless")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--no-sandbox")
                prefs = {'download.default_directory' : tmpdir.name}
                options.add_experimental_option('prefs', prefs)
                if mode != 'localtest':
                        driver = webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_PATH'], options=options)
                else:
                        driver = webdriver.Chrome(options=options)
                driver.implicitly_wait(10)
                
                ## click to export
                driver.get(url)
                elements = driver.find_elements_by_tag_name("button")
                for element in elements:
                        if element.text == 'CSV':
                                element.click()
                                
                ## verify download
                fpath = os.path.join(tmpdir.name, file + ext)
                time.sleep(wait) # wait for download to finish before checking
                if not os.path.isfile(fpath):
                        a += 1
                        if verbose:
                                print(color('Attempt ' + str(a) + ' failed...', (150, 150, 150)))
                        continue
                else:
                        break

        ## commit file
        name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
        if not os.path.isfile(fpath):
                print(background('Error downloading: ' + name, Colors.red))
        elif mode != 'prod':
                print(color('Test download successful: ' + name, Colors.green))
        else:
                with open(fpath, 'r') as f:
                        data = f.read()
                repo.create_file(path + name + ext, commit + ' (' + path + ')', data)
                print(color('Commit successful: ' + name, Colors.green))

# AB - COVID-19 Alberta statistics
dl_ab_cases('https://www.alberta.ca/stats/covid-19-alberta-statistics.htm',
            'ab/cases/',
            'covid19dataexport',
            commit,
            verbose=True)

# AB - COVID-19 relaunch status map
dl_ab_relaunch('https://www.alberta.ca/maps/covid-19-status-map.htm',
               'ab/active-cases-by-region/',
               'covid19dataexport-relaunch',
               commit,
               verbose=True)

# AB - COVID-19 in Alberta: Current cases by local geographic area (Edmonton)
dl_file('https://data.edmonton.ca/api/views/ix8f-s9xp/rows.csv?accessType=DOWNLOAD',
        'ab/edmonton-cases-by-area/',
        'COVID-19_in_Alberta__Current_cases_by_local_geographic_area',
        commit)

# BC - BC COVID-19 Data (Case data)
dl_file('http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv',
        'bc/case-data/',
        'BCCDC_COVID19_Dashboard_Case_Details',
        commit)

# BC - BC COVID-19 Data (Laboratory data)
dl_file('http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Lab_Information.csv',
        'bc/laboratory-data/',
        'BCCDC_COVID19_Dashboard_Lab_Information',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (Epidemiology update)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19.csv',
        'can/epidemiology-update/',
        'covid19',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (Epidemiology summary statements)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-statements.csv',
        'can/epidemiology-summary-statements/',
        'covid19-epiSummary-statements',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (NML summary)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-NML.csv',
        'can/nml-summary/',
        'covid19-epiSummary-NML',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (NML weekly testing)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/NML_weekly_testing.csv',
        'can/nml-weekly-testing/',
        'NML_weekly_testing',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (Number of cases with detailed case report data)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-nTotal.csv',
        'can/detailed-case-report-n/',
        'covid19-nTotal',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (Cases and deaths by health region time series)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/file_out_v5.csv',
        'can/cases-and-deaths-by-hr-time-series/',
        'file_out_v5',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (Health region UID table)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-healthregions-hruid.csv',
        'can/health-region-uid/',
        'covid19-healthregions-hruid',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (Cases by exposure setting time series)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-casesovertime.csv',
        'can/cases-by-exposure-time-series/',
        'covid19-epiSummary-casesovertime',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (Epidemic curve by date of illness onset by age group)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-epiCurveByAge.csv',
        'can/epidemic-curve-by-age/',
        'covid19-epiSummary-epiCurveByAge',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (Severity by age group and sex)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-severityUpdate.csv',
        'can/severity-by-age-and-sex/',
        'covid19-epiSummary-severityUpdate',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (Cases by severity)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-severity.csv',
        'can/cases-by-severity/',
        'covid19-epiSummary-severity',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (Cases by age group and sex)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-agegroups2.csv',
        'can/cases-by-age-and-sex/',
        'covid19-epiSummary-agegroups2',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (Cases by probable exposure setting)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-probableexposure2.csv',
        'can/cases-by-probable-exposure-setting/',
        'covid19-epiSummary-probableexposure2',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (Symptoms summary)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-symptoms.csv',
        'can/symptoms-summary/',
        'covid19-epiSummary-symptoms',
        commit)

# CAN - COVID-19 Situational Awareness Dashboard (Situational awareness dashboard update time)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-updateTime.csv',
        'can/situational-awareness-dashboard-update-time/',
        'covid19-updateTime',
        commit)

# ON - Confirmed positive cases of COVID19 in Ontario
dl_file('https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv',
        'on/confirmed-positive-cases/',
        'conposcovidloc',
        commit)

# ON - Status of COVID-19 cases in Ontario
dl_file('https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv',
        'on/status-of-cases/',
        'covidtesting',
        commit)

# ON - City of Toronto COVID-19 Summary
dl_file('https://docs.google.com/spreadsheets/d/1euhrML0rkV_hHF1thiA0G5vSSeZCqxHY/export?format=xlsx&id=1euhrML0rkV_hHF1thiA0G5vSSeZCqxHY',
        'on/toronto-covid-summary/',
        'CityofToronto_COVID-19_Data',
        commit,
        ext='.xlsx')

# ON - COVID-19 Cases in Toronto
# run only on Wednesdays
if t.weekday() == 2:
        dl_file('https://ckan0.cf.opendata.inter.prod-toronto.ca/download_resource/e5bf35bc-e681-43da-b2ce-0242d00922ad?format=csv',
                'on/toronto-cases/',
                'COVID19_cases',
                commit)

# ON - Ottawa cases and deaths
dl_file('https://www.arcgis.com/sharing/rest/content/items/cf9abb0165b34220be8f26790576a5e7/data',
        'on/ottawa-cases-and-deaths/',
        'COVID-19_Cases_and_Deaths_in_Ottawa_EN',
        commit)

# ON - Ottawa outbreaks in healthcare institutions
dl_file('https://www.arcgis.com/sharing/rest/content/items/77078920fea8499dbb6f54cc69c03a90/data',
        'on/ottawa-outbreaks-in-healthcare-institutions/',
        'COVID-19_Outbreaks_in_Ottawa_Healthcare_Institutions_EN',
        commit)

# ON - Ottawa hospitalization data
dl_file('https://www.arcgis.com/sharing/rest/content/items/02c99319ef44488e85cd4f96f5061f20/data',
        'on/ottawa-hospitalization/',
        'Hospitalizations_of_Ottawa_residents_with_confirmed_COVID-19',
        commit)

# QC - COVID-19 data
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/combine.csv',
        'qc/covid-data/',
        'combine',
        commit,
        user=True)

# QC - COVID-19 data (charts)
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/combine2.csv',
        'qc/covid-data-charts/',
        'combine2',
        commit,
        user=True)

# QC - Deaths by RSS (health region) and living environment
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/tableau-rpa.csv',
        'qc/deaths-by-rss-and-living-environment/',
        'tableau-rpa',
        commit,
        user=True)

# QC - Cases by RSS (health region) and RLS (local service network)
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/tableau-rls.csv',
        'qc/cases-by-rss-and-rls/',
        'tableau-rls',
        commit,
        user=True)

# QC - Montréal cases and deaths by CIUSSS (integrated health and social services centres)
dl_file('https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/ciusss.csv',
        'qc/montreal-cases-and-deaths-by-ciusss/',
        'ciusss',
        commit,
        user=True)

# QC - Montréal cases by area
dl_file('https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/municipal.csv',
        'qc/montreal-cases-by-area/',
        'municipal',
        commit,
        user=True)

# QC - Montréal cases and deaths by age group
dl_file('https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/grage.csv',
        'qc/montreal-cases-and-deaths-by-age-group/',
        'grage',
        commit,
        user=True)

# QC - Montréal cases and deaths by sex
dl_file('https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/sexe.csv',
        'qc/montreal-cases-and-deaths-by-sex/',
        'sexe',
        commit,
        user=True)

# QC - Montréal epidemic curve
dl_file('https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/courbe.csv',
        'qc/montreal-epidemic-curve/',
        'courbe',
        commit,
        user=True)