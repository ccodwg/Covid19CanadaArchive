# archiver.py: Automated, daily backups of COVID-19 data from Canadian government sources #
# https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data #
# Maintainer: Jean-Paul R. Soucy #

# import modules

## core utilities
import sys
import time
import os
from shutil import copyfile
from datetime import datetime, timedelta
import json
import re
import tempfile

## other utilities
import pandas as pd # better data processing
import pytz # better time zones
from colorit import * # colourful printing

## git
from git import Repo

## web-scraping
import requests
from selenium import webdriver # requires ChromeDriver and Chromium/Chrome
from selenium.webdriver.chrome.options import Options

# list of environmental variables used in this script
## GH_TOKEN: personal access token for the GitHub API (used when mode = prod)
## GH_NAME: name to use for GitHub commits (used when mode = prod)
## GH_MAIL: email address to use for GitHub commits (used when mode = prod)
## GOOGLE_CHROME_BIN: path to binary in heroku-buildpack-google-chrome (used when mode = server)
## CHROMEDRIVER_PATH: path to binary in heroku-buildpack-chromedriver (used when mode = server)

# set mode (server vs. local and prod vs. test)
## server: read environmental variables from Heroku config variables
## local: read environmental variables from local files (in directory .gh/) or from system environmental variables
## prod: download GitHub repo so that downloaded files can be added via commit
## test: don't download GitHub repo, just test that files can be successfully downloaded
if len(sys.argv) == 1 or ((len(sys.argv) == 2) and (sys.argv[1] == 'serverprod')):
        mode = 'serverprod' # server / prod
elif len(sys.argv) == 2 and sys.argv[1] == 'localprod':
        mode = 'localprod' # local / prod
elif len(sys.argv) == 2 and sys.argv[1] == 'servertest':
        mode = 'servertest' # server / test
elif len(sys.argv) == 2 and sys.argv[1] == 'localtest':
        mode = 'localtest' # local / test
else:
        sys.exit("Error: Invalid arguments.")

# enable printing with colour
init_colorit()

# define date and time in America/Toronto time zone
t = datetime.now(pytz.timezone('America/Toronto'))

# access repo
if mode == 'serverprod' or mode == 'localprod':
        ## access token
        if mode == 'serverprod':
                token = os.environ['GH_TOKEN']
                gh_name = os.environ['GH_NAME']
                gh_mail = os.environ['GH_MAIL']
        elif mode == 'localprod':
                token = open('.gh/token.txt', 'r').readline().rstrip()
                gh_name = open('.gh/gh_name.txt', 'r').readline().rstrip()
                gh_mail = open('.gh/gh_mail.txt', 'r').readline().rstrip()
        ## set repository directory
        repo_dir = 'temp_archive'
        ## shallow clone (minimize download size while still allowing a commit to be made)
        repo_remote = 'https://' + token + ':x-oauth-basic@github.com/jeanpaulrsoucy/covid-19-canada-gov-data'
        repo = Repo.clone_from(repo_remote, repo_dir, depth=1)
        origin = repo.remote('origin')
        ### set GitHub identity
        repo.config_writer().set_value("user", "name", gh_name).release()
        repo.config_writer().set_value("user", "email", gh_mail).release()
        ## initialize file list for commit
        file_list = []
        ## initialize commit message for commit
        commit_message = 'Nightly update: ' + str(t.date()) + '\n\n'

# define functions

def prep_file(repo_dir, name, full_name, data = None, fpath=None, copy=False):
        """Prepare file for commit.
        
        File is either written into the git repository (when copy is False) or copied from a temporary directory into the git repository (when copy is True).
        
        Parameters:
        repo_dir (str): Directory containing the git repository.
        name (str): Output file name with timestamp and no extension.
        full_name (str): Output filename with timestamp, extension, and relative path.
        data (bytes): The file as a bytes object (provide only when copy is False).
        fpath (str): The path of the file in the temporary directory (provide only when copy is True).
        copy (bool): Is the file already written and needs to be copied? (Default: False, see fpath and data)
        
        """
        global commit_message
        ## define path to save file
        spath = os.path.join(repo_dir, full_name)
        ## create directory if necessary
        os.makedirs(os.path.dirname(spath), exist_ok=True)
        ## copy is True: downloaded file exists as a file in a temporary directory,
        ## need to copy it to the save path
        if copy:
                copyfile(fpath, spath)
        ## copy is False: downloaded file exists as an object in Python,
        ## need to write it to the save path
        else:
                with open(spath, mode='wb') as local_file:
                        local_file.write(data)
        ## append file to the list of files in the commit
        file_list.append(full_name)
        ## append name of file to the commit message
        commit_message = commit_message + 'Success: ' + full_name + '\n'
        print(color('Copy successful: ' + full_name, Colors.blue))

def commit_files(repo, origin, file_list, commit_message):
        """Commit files to git repository and push to remote.
        
        Parameters:
        repo: Repo object from gitpython.
        origin: Remote object from gitpython.
        file_list (list): List of paths to files to commit.
        commit_message (str): Commit message.
        
        """
        print("Commiting files...")
        try:
                repo.index.add(file_list)
                repo.index.commit(commit_message)
                origin.push()
                print(color('Commit successful!', Colors.green))
        except:
                print(background('Commit failed!', Colors.red))

def dl_file(url, path, file, user=False, ext='.csv', mb_json_to_csv=None):
        """Download file (generic).
        
        Used to download most file types (when Selenium is not required).
        
        Parameters:
        url (str): URL to download file from.
        path (str): Path to output file (excluding file name). Example: 'can/epidemiology-update/'
        file (str): Output file name (excluding extension). Example: 'covid19'
        user (bool): Should the request impersonate a normal browser? Needed to access some data. Default: False.
        ext (str): Extension of the output file. Defaults to '.csv'.
        mb_json_to_csv (bool): If True, this is a Manitoba JSON file that that should be converted to CSV. Default: None.
        
        """
        global commit_message
        
        ## set names with timestamp and file ext
        name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
        full_name = os.path.join(path, name + ext)        
        
        ## some websites will reject the request unless you look like a normal web browser
        ## user is True provides a normal-looking user agent string to bypass this
        if user is True:
                headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
                req = requests.get(url, headers=headers)
        else:
                req = requests.get(url)
        
        ## check if request was successful
        if not req.ok:
                ## print failure
                print(background('Error downloading: ' + full_name, Colors.red))
                ## write failure to commit message if mode == prod
                if mode == 'serverprod' or mode == 'localprod':
                        commit_message = commit_message + 'Failure: ' + full_name + '\n'
        ## successful request: if mode == test, print success and end
        elif mode == 'servertest' or mode == 'localtest':
                ## print success
                print(color('Test download successful: ' + full_name, Colors.green))
        ## successful request: mode == prod, prepare files for commit
        else:
                if mb_json_to_csv:
                        ## for Manitoba JSON data only: convert JSON to CSV and save as temporary file
                        name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
                        full_name = os.path.join(path, name + ext)                          
                        tmpdir = tempfile.TemporaryDirectory()
                        fpath = os.path.join(tmpdir.name, file + ext)
                        data = pd.json_normalize(json.loads(req.content)['features'])
                        data.columns = data.columns.str.lstrip('attributes.') # strip prefix
                        ## replace timestamps with actual dates
                        data.Date = pd.to_datetime(data.Date / 1000, unit='s').dt.date
                        data = data.to_csv(fpath, index=None)
                        ## prepare file for commit
                        prep_file(repo_dir, name=name, full_name=full_name, fpath=fpath, copy=True)
                else:
                        ## all other data: grab content from request as an object
                        data = req.content
                        ## prepare file for commit
                        prep_file(repo_dir, name=name, full_name=full_name, data=data)

def dl_ab_cases(url, path, file, ext='.csv', wait=5):
        """Download CSV file: AB - "COVID-19 Alberta statistics".
        https://www.alberta.ca/stats/covid-19-alberta-statistics.htm
        
        The file requires Selenium to click a tab then click a CSV button.
        
        Parameters:
        url (str): URL to download file from.
        path (str): Path to output file (excluding file name). Example: 'can/epidemiology-update/'
        file (str): Output file name (excluding extension). Example: 'covid19'
        ext (str): Extension of the output file. Defaults to '.csv'.
        wait (int): Time in seconds that the function should wait. Should be > 0 to ensure the download is successful.
        
        """
        global commit_message
        
        ## set names with timestamp and file ext
        name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
        full_name = os.path.join(path, name + ext)           
        
        ## create temporary directory
        tmpdir = tempfile.TemporaryDirectory()
        
        ## setup webdriver
        options = Options()
        if mode == 'serverprod' or mode == 'servertest':
                options.binary_location = os.environ['GOOGLE_CHROME_BIN']
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        prefs = {'download.default_directory' : tmpdir.name} # download to temporary directory
        options.add_experimental_option('prefs', prefs)
        if mode == 'serverprod' or mode == 'servertest':
                driver = webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_PATH'], options=options)
        else:
                driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        
        ## click to correct tab then click CSV button to export
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
        time.sleep(wait) # wait for download to finish
        if not os.path.isfile(fpath):
                ## print failure
                print(background('Error downloading: ' + full_name, Colors.red))
                ## write failure to commit message if mode == prod
                if mode == 'serverprod' or mode == 'localprod':
                        commit_message = commit_message + 'Failure: ' + full_name + '\n'
        ## successful request: if mode == test, print success and end
        elif mode == 'servertest' or mode == 'localtest':
                ## print success
                print(color('Test download successful: ' + full_name, Colors.green))
        ## successful request: mode == prod, prepare files for commit
        else:
                ## prepare file for commit
                prep_file(repo_dir, name=name, full_name=full_name, fpath=fpath, copy=True)

def dl_ab_oneclick(url, path, file, ext='.csv', wait=5):
        """Download CSV file: AB - "COVID-19 relaunch status map" or AB - "COVID-19 school status map"
        https://www.alberta.ca/maps/covid-19-status-map.htm
        https://www.alberta.ca/schools/covid-19-school-status-map.htm
        
        The file requires Selenium to click a CSV button.
        
        Parameters:
        url (str): URL to download file from.
        path (str): Path to output file (excluding file name). Example: 'can/epidemiology-update/'
        file (str): Output file name (excluding extension). Example: 'covid19'
        ext (str): Extension of the output file. Defaults to '.csv'.
        wait (int): Time in seconds that the function should wait. Should be > 0 to ensure the download is successful.
        
        """        
        global commit_message
        
        ## set names with timestamp and file ext
        name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
        full_name = os.path.join(path, name + ext)        
        
        ## create temporary directory
        tmpdir = tempfile.TemporaryDirectory()
        
        ## setup webdriver
        options = Options()
        if mode == 'serverprod' or mode == 'servertest':
                options.binary_location = os.environ['GOOGLE_CHROME_BIN']
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        prefs = {'download.default_directory' : tmpdir.name} # download to temporary directory
        options.add_experimental_option('prefs', prefs)
        if mode == 'serverprod' or mode == 'servertest':
                driver = webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_PATH'], options=options)
        else:
                driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        
        ## click CSV button to export
        driver.get(url)
        elements = driver.find_elements_by_tag_name("button")
        for element in elements:
                if element.text == 'CSV':
                        element.click()
                        
        ## verify download
        fpath = os.path.join(tmpdir.name, file + ext)
        time.sleep(wait) # wait for download to finish
        if not os.path.isfile(fpath):
                ## print failure
                print(background('Error downloading: ' + full_name, Colors.red))
                ## write failure to commit message if mode == prod
                if mode == 'serverprod' or mode == 'localprod':
                        commit_message = commit_message + 'Failure: ' + full_name + '\n'
        ## successful request: if mode == test, print success and end
        elif mode == 'servertest' or mode == 'localtest':
                ## print success
                print(color('Test download successful: ' + full_name, Colors.green))
        ## successful request: mode == prod, prepare files for commit
        else:
                ## prepare file for commit
                prep_file(repo_dir, name=name, full_name=full_name, fpath=fpath, copy=True)

def ss_page(url, path, file, ext='.png', wait=5, width=None, height=None):
        """Take a screenshot of a webpage.
        
        By default, Selenium attempts to capture the entire page.
        
        Parameters:
        
        url (str): URL to screenshot.
        path (str): Path to output file (excluding file name). Example: 'can/epidemiology-update/'
        file (str): Output file name (excluding extension). Example: 'covid19'
        ext (str): Extension of the output file. Defaults to '.png'.
        wait (int): Time in seconds that the function should wait. Should be > 0 to ensure the entire page is captured.
        width (int): Width of the output screenshot. Default: None. If not set, the function attempts to detect the maximum width.
        height (int): Height of the output screenshot. Default: None. If not set, the function attempts to detect the maximum height.
        
        """
        global commit_message
        
        ## set names with timestamp and file ext
        name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
        full_name = os.path.join(path, name + ext)        
        
        ## create temporary directory
        tmpdir = tempfile.TemporaryDirectory()
        
        ## setup webdriver
        options = Options()
        if mode == 'serverprod' or mode == 'servertest':
                options.binary_location = os.environ['GOOGLE_CHROME_BIN']
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        prefs = {'download.default_directory' : tmpdir.name} # download to temporary directory
        options.add_experimental_option('prefs', prefs)
        ## successful screenshot: if mode == test, print success and end
        if mode == 'serverprod' or mode == 'servertest':
                driver = webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_PATH'], options=options)
        ## successful screenshot: mode == prod, prepare files for commit
        else:
                driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        
        ## load page and wait
        driver.get(url)
        time.sleep(wait) # wait for page to load      
                        
        ## take screenshot
        fpath = os.path.join(tmpdir.name, file + ext)
        ## get total width of the page if it is not set by the user
        if width is None:
                width = driver.execute_script('return document.body.parentNode.scrollWidth')
        ## get total height of the page if it is not set by the user
        if height is None:
                height = driver.execute_script('return document.body.parentNode.scrollHeight')
        ## set window size
        driver.set_window_size(width, height)
        ## take screenshot
        driver.find_element_by_tag_name('body').screenshot(fpath) # remove scrollbar

        ## verify screenshot
        if not os.path.isfile(fpath):
                ## print failure
                print(background('Error downloading: ' + full_name, Colors.red))
                ## write failure to commit message if mode == prod
                if mode == 'serverprod' or mode == 'localprod':
                        commit_message = commit_message + 'Failure: ' + full_name + '\n'                
        elif mode == 'servertest' or mode == 'localtest':
                ## print success
                print(color('Test download successful: ' + full_name, Colors.green))
        else:
                ## prepare file for commit
                prep_file(repo_dir, name=name, full_name=full_name, fpath=fpath, copy=True)

# AB - COVID-19 Alberta statistics
dl_ab_cases('https://www.alberta.ca/stats/covid-19-alberta-statistics.htm',
            'ab/cases/',
            'covid19dataexport')

# AB - COVID-19 relaunch status map
dl_ab_oneclick('https://www.alberta.ca/maps/covid-19-status-map.htm',
               'ab/active-cases-by-region/',
               'covid19dataexport-relaunch')

# AB - COVID-19 school status map
dl_ab_oneclick('https://www.alberta.ca/schools/covid-19-school-status-map.htm',
               'ab/school-status-by-region/',
               'covid19dataexport-schools')

# AB - COVID-19 in Alberta: Current cases by local geographic area (Edmonton)
dl_file('https://data.edmonton.ca/api/views/ix8f-s9xp/rows.csv?accessType=DOWNLOAD',
        'ab/edmonton-cases-by-area/',
        'COVID-19_in_Alberta__Current_cases_by_local_geographic_area')

# BC - BC COVID-19 Data (Case data)
dl_file('http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv',
        'bc/case-data/',
        'BCCDC_COVID19_Dashboard_Case_Details')

# BC - BC COVID-19 Data (Laboratory data)
dl_file('http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Lab_Information.csv',
        'bc/laboratory-data/',
        'BCCDC_COVID19_Dashboard_Lab_Information')

# CAN - COVID-19 Situational Awareness Dashboard (Epidemiology update)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19.csv',
        'can/epidemiology-update/',
        'covid19')

# CAN - COVID-19 Situational Awareness Dashboard (Epidemiology summary statements)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-statements.csv',
        'can/epidemiology-summary-statements/',
        'covid19-epiSummary-statements')

# CAN - COVID-19 Situational Awareness Dashboard (NML summary)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-NML.csv',
        'can/nml-summary/',
        'covid19-epiSummary-NML')

# CAN - COVID-19 Situational Awareness Dashboard (NML weekly testing)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/NML_weekly_testing.csv',
        'can/nml-weekly-testing/',
        'NML_weekly_testing')

# CAN - COVID-19 Situational Awareness Dashboard (Number of cases with detailed case report data)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-nTotal.csv',
        'can/detailed-case-report-n/',
        'covid19-nTotal')

# CAN - COVID-19 Situational Awareness Dashboard (Cases and deaths by health region time series)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/file_out_v5.csv',
        'can/cases-and-deaths-by-hr-time-series/',
        'file_out_v5')

# CAN - COVID-19 Situational Awareness Dashboard (Health region UID table)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-healthregions-hruid.csv',
        'can/health-region-uid/',
        'covid19-healthregions-hruid')

# CAN - COVID-19 Situational Awareness Dashboard (Cases by exposure setting time series)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-casesovertime.csv',
        'can/cases-by-exposure-time-series/',
        'covid19-epiSummary-casesovertime')

# CAN - COVID-19 Situational Awareness Dashboard (Epidemic curve by date of illness onset by age group)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-epiCurveByAge.csv',
        'can/epidemic-curve-by-age/',
        'covid19-epiSummary-epiCurveByAge')

# CAN - COVID-19 Situational Awareness Dashboard (Severity by age group and sex)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-severityUpdate.csv',
        'can/severity-by-age-and-sex/',
        'covid19-epiSummary-severityUpdate')

# CAN - COVID-19 Situational Awareness Dashboard (Cases by severity)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-severity.csv',
        'can/cases-by-severity/',
        'covid19-epiSummary-severity')

# CAN - COVID-19 Situational Awareness Dashboard (Cases by age group and sex)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-agegroups2.csv',
        'can/cases-by-age-and-sex/',
        'covid19-epiSummary-agegroups2')

# CAN - COVID-19 Situational Awareness Dashboard (Cases by probable exposure setting)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-probableexposure2.csv',
        'can/cases-by-probable-exposure-setting/',
        'covid19-epiSummary-probableexposure2')

# CAN - COVID-19 Situational Awareness Dashboard (Symptoms summary)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-symptoms.csv',
        'can/symptoms-summary/',
        'covid19-epiSummary-symptoms')

# CAN - COVID-19 Situational Awareness Dashboard (Situational awareness dashboard update time)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-updateTime.csv',
        'can/situational-awareness-dashboard-update-time/',
        'covid19-updateTime')
# MB - Cases by status and RHA
dl_file('https://services.arcgis.com/mMUesHYPkXjaFGfS/arcgis/rest/services/mb_covid_cases_by_status_daily_rha/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&groupByFieldsForStatistics=Date%2CRHA',
        'mb/cases-by-status-and-rha/',
        'cases-by-status-and-rha',
        mb_json_to_csv=True)

# MB - Manitoba Five-Day Test Positivity Rate
dl_file('https://services.arcgis.com/mMUesHYPkXjaFGfS/arcgis/rest/services/mb_covid_5_day_positivity_rate/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Date%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true',
        'mb/five-day-test-positivity/',
        'five-day-test-positivity',
        mb_json_to_csv=True)

# NS - Coronavirus (COVID-19): case data
dl_file('https://novascotia.ca/coronavirus/data/ns-covid19-data.csv',
        'ns/case-data/',
        'ns-covid19-data')

# ON - How Ontario is responding to COVID-19 (webpage screenshot)
ss_page('https://www.ontario.ca/page/how-ontario-is-responding-covid-19',
        'on/ontario-webpage/',
        'ontario-screenshot',
        width=1920)

# ON - Confirmed positive cases of COVID19 in Ontario
dl_file('https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv',
        'on/confirmed-positive-cases/',
        'conposcovidloc')

# ON - Status of COVID-19 cases in Ontario
dl_file('https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv',
        'on/status-of-cases/',
        'covidtesting')

# ON - Testing of inmates in provincial correctional institutions
dl_file('https://data.ontario.ca/dataset/c4022f0f-6f3d-4e16-bd28-5312333a4bac/resource/d0d6ccc7-fc60-4a18-ac96-7f9493e9f10e/download/inmatetesting.csv',
        'on/correctional-institutions-inmates-testing/',
        'inmatetesting')

# ON - Status of cases in provincial correctional institutions
dl_file('https://data.ontario.ca/dataset/ecb75ea0-8b72-4f46-a14a-9bd54841d6ab/resource/1f95eda9-53b5-448e-abe0-afc0b71581ed/download/correctionsinmatecases.csv',
        'on/correctional-institutions-status/',
        'correctionsinmatecases')

# ON - Long term care homes: Summary data
dl_file('https://data.ontario.ca/dataset/42df36df-04a0-43a9-8ad4-fac5e0e22244/resource/0f8b343e-fc28-4ca5-9aab-c3a1d2c919f1/download/ltccovidsummary.csv',
        'on/long-term-care-home/',
        'ltccovidsummary')

# ON - Long term care homes: Active outbreaks
dl_file('https://data.ontario.ca/dataset/42df36df-04a0-43a9-8ad4-fac5e0e22244/resource/4b64488a-0523-4ebb-811a-fac2f07e6d59/download/activeltcoutbreak.csv',
        'on/long-term-care-home/',
        'activeltcoutbreak')

# ON - Long term care homes: Resolved outbreaks
dl_file('https://data.ontario.ca/dataset/42df36df-04a0-43a9-8ad4-fac5e0e22244/resource/0cf2f01e-d4e1-48ed-8027-2133d059ec8b/download/resolvedltc.csv',
        'on/long-term-care-home/',
        'resolvedltc')

# ON - Schools: Summary of cases in schools
dl_file('https://data.ontario.ca/dataset/b1fef838-8784-4338-8ef9-ae7cfd405b41/resource/7fbdbb48-d074-45d9-93cb-f7de58950418/download/schoolcovidsummary.csv',
        'on/schools/',
        'schoolcovidsummary')

# ON - Schools: Schools with active COVID-19 cases
dl_file('https://data.ontario.ca/dataset/b1fef838-8784-4338-8ef9-ae7cfd405b41/resource/8b6d22e2-7065-4b0f-966f-02640be366f2/download/schoolsactivecovid.csv',
        'on/schools/',
        'schoolsactivecovid')

# ON - Licensed child care settings: Summary of cases in licensed child care settings
dl_file('https://data.ontario.ca/dataset/5bf54477-6147-413f-bab0-312f06fcb388/resource/74f9ac9f-7ca8-4860-b2c3-189a2c25e30c/download/lccovidsummary.csv',
        'on/licensed-child-care-settings/',
        'lccovidsummary')

# ON - Licensed child care settings: Licensed child care centres and agencies with active COVID-19 cases
dl_file('https://data.ontario.ca/dataset/5bf54477-6147-413f-bab0-312f06fcb388/resource/eee282d3-01e6-43ac-9159-4ba694757aea/download/lccactivecovid.csv',
        'on/licensed-child-care-settings/',
        'lccactivecovid')

# ON - City of Toronto COVID-19 Summary
dl_file('https://docs.google.com/spreadsheets/d/1euhrML0rkV_hHF1thiA0G5vSSeZCqxHY/export?format=xlsx&id=1euhrML0rkV_hHF1thiA0G5vSSeZCqxHY',
        'on/toronto-covid-summary/',
        'CityofToronto_COVID-19_Data',
        ext='.xlsx')

# ON - COVID-19 Cases in Toronto
# run only on Wednesdays
if t.weekday() == 2:
        dl_file('https://ckan0.cf.opendata.inter.prod-toronto.ca/download_resource/e5bf35bc-e681-43da-b2ce-0242d00922ad?format=csv',
                'on/toronto-cases/',
                'COVID19_cases')

# ON - Ottawa cases and deaths
dl_file('https://www.arcgis.com/sharing/rest/content/items/cf9abb0165b34220be8f26790576a5e7/data',
        'on/ottawa-cases-and-deaths/',
        'COVID-19_Cases_and_Deaths_in_Ottawa_EN')

# ON - Ottawa outbreaks in healthcare institutions
dl_file('https://www.arcgis.com/sharing/rest/content/items/77078920fea8499dbb6f54cc69c03a90/data',
        'on/ottawa-outbreaks-in-healthcare-institutions/',
        'COVID-19_Outbreaks_in_Ottawa_Healthcare_Institutions_EN')

# ON - Ottawa hospitalization data
dl_file('https://www.arcgis.com/sharing/rest/content/items/02c99319ef44488e85cd4f96f5061f20/data',
        'on/ottawa-hospitalization/',
        'Hospitalizations_of_Ottawa_residents_with_confirmed_COVID-19')

# QC - COVID-19 data
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/combine.csv',
        'qc/covid-data/',
        'combine',
        user=True)

# QC - COVID-19 data (charts)
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/combine2.csv',
        'qc/covid-data-charts/',
        'combine2',
        user=True)

# QC - Deaths by RSS (health region) and living environment
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/tableau-rpa.csv',
        'qc/deaths-by-rss-and-living-environment/',
        'tableau-rpa',
        user=True)

# QC - Cases by RSS (health region) and RLS (local service network)
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/tableau-rls.csv',
        'qc/cases-by-rss-and-rls/',
        'tableau-rls',
        user=True)

# QC - Montréal cases and deaths by CIUSSS (integrated health and social services centres)
dl_file('https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/ciusss.csv',
        'qc/montreal-cases-and-deaths-by-ciusss/',
        'ciusss',
        user=True)

# QC - Status report on confirmed cases and deaths by RPA
dl_file('https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/etat_situation_rpa.pdf',
        'qc/status-report-cases-and-deaths-by-rpa/',
        'etat_situation_rpa',
        ext = '.pdf')

# QC - Status report on confirmed cases and deaths by CHSLD
dl_file('https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/etat_situation_chsld.pdf',
        'qc/status-report-cases-and-deaths-by-chsld/',
        'etat_situation_chsld',
        ext = '.pdf')

# QC - Highlights - public and private school system
dl_file('https://cdn-contenu.quebec.ca/cdn-contenu/adm/min/education/publications-adm/covid-19/reseauScolaire_faitsSaillants.pdf',
        'qc/schools-highlights/',
        'reseauScolaire_faitsSaillants',
        ext = '.pdf')

# QC - List of schools - public and private school system
dl_file('https://cdn-contenu.quebec.ca/cdn-contenu/adm/min/education/publications-adm/covid-19/reseauScolaire_listeEcoles.pdf',
        'qc/schools-list-of-schools/',
        'reseauScolaire_listeEcoles',
        ext = '.pdf')

# QC - Montréal cases by area
dl_file('https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/municipal.csv',
        'qc/montreal-cases-by-area/',
        'municipal',
        user=True)

# QC - Montréal cases and deaths by age group
dl_file('https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/grage.csv',
        'qc/montreal-cases-and-deaths-by-age-group/',
        'grage',
        user=True)

# QC - Montréal cases and deaths by sex
dl_file('https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/sexe.csv',
        'qc/montreal-cases-and-deaths-by-sex/',
        'sexe',
        user=True)

# QC - Montréal epidemic curve
dl_file('https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/courbe.csv',
        'qc/montreal-epidemic-curve/',
        'courbe',
        user=True)

# SK - Saskatchewan's Dashboard - Total Cases
sk_url_cases = 'https://dashboard.saskatchewan.ca' + re.search('(?<=href=\").*(?=\">CSV)', requests.get('https://dashboard.saskatchewan.ca/health-wellness/covid-19/cases').text).group(0)
dl_file(sk_url_cases,
        'sk/cases-by-region/',
        'cases')

# SK - Saskatchewan's Dashboard - Total Cases (webpage screenshot)
ss_page('https://dashboard.saskatchewan.ca/health-wellness/covid-19/cases',
        'sk/cases-by-region-webpage/',
        'cases-screenshot',
        width=1526)

# SK - Saskatchewan's Dashboard - Total Tests
sk_url_tests = 'https://dashboard.saskatchewan.ca' + re.search('(?<=href=\").*(?=\">CSV)', requests.get('https://dashboard.saskatchewan.ca/health-wellness/covid-19/tests').text).group(0)
dl_file(sk_url_tests,
        'sk/tests-by-region/',
        'tests')

# SK - Saskatchewan's Dashboard - Total Tests (webpage screenshot)
ss_page('https://dashboard.saskatchewan.ca/health-wellness/covid-19/tests',
        'sk/tests-by-region-webpage/',
        'tests-screenshot',
        width=1526)

# Other: QC - Covid Écoles Québec (Excel)
dl_file('https://drive.google.com/uc?export=download&id=1xOl0uhyx9IuHZfJuRH-OR7BcGFuWYUex',
        'other/qc/covid-ecoles-quebec-school-list/',
        'COVIDECOLESQUEBEC',
        ext = '.xlsx')

# Commit files
if mode == 'serverprod' or mode == 'localprod':
        commit_files(repo, origin, file_list, commit_message)