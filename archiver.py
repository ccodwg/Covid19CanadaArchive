# archiver.py: Automated, daily backups of COVID-19 data from Canadian government sources #
# https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data #
# Maintainer: Jean-Paul R. Soucy #

# import modules

## core utilities
import sys
import time
import os
from os.path import dirname, abspath
from shutil import copyfile
from datetime import datetime, timedelta
from array import *
import json
import re
import tempfile
import csv
from zipfile import ZipFile

## other utilities
import pandas as pd # better data processing
import pytz # better time zones
from colorit import * # colourful printing

## web-scraping
import requests
from selenium import webdriver # requires ChromeDriver and Chromium/Chrome
from selenium.webdriver.chrome.options import Options

## Google Drive
from oauth2client import service_account
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# list of environmental variables used in this script
## GD_KEY: environmental variable of Google Drive credentials as a simple string (used when mode = server)
## GOOGLE_CHROME_BIN: path to binary in heroku-buildpack-google-chrome (used when mode = server)
## CHROMEDRIVER_PATH: path to binary in heroku-buildpack-chromedriver (used when mode = server)

# set mode (server vs. local and prod vs. test)
## server: read environmental variables from Heroku config variables
## local: read environmental variables from system environmental variables
## prod: upload files to Google Drive
## test: don't upload files to Google Drive, just test that files can be successfully downloaded
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

# initialize success and failure counters
success = 0
failure = 0

# access repo
if mode == 'serverprod' or mode == 'localprod':
              
        ## retrieve Google Drive credentials
        if mode == 'serverprod':
                gd_key_val = json.loads(os.environ['GD_KEY'], strict=False)
                tmpdir = tempfile.TemporaryDirectory()
                gd_key = os.path.join(tmpdir.name, ".gd_key.json")
                with open(gd_key, mode='w', encoding='utf-8') as local_file:
                        json.dump(gd_key_val, local_file, ensure_ascii=False, indent=4)
        elif mode == 'localprod':
                script_path = dirname(abspath(__file__))
                gd_key = os.path.join(script_path, ".gd", ".gd_key.json")                
        
        ## authenticate Google Drive access
        gauth = GoogleAuth()
        scope = ['https://www.googleapis.com/auth/drive']
        gauth.credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(gd_key, scope)
        
        ## initialize Drive object
        drive = GoogleDrive(gauth)
        
        ## create httplib.Http() object
        ## see https://pypi.org/project/PyDrive/ - "Concurrent access made easy"
        http = drive.auth.Get_Http_Object()
        
        ## initialize log message
        log_message = ''
        
        ## load Google Drive directory IDs
        dir_id_list = pd.read_csv("https://raw.githubusercontent.com/jeanpaulrsoucy/covid-19-canada-gov-data/master/data_catalogue.csv")
        
        ## set log file IDs
        archive_id = '10ET5FBqO-K8FBdEaXgBjBZwJskIZGKNG'
        log_id = '10tbxUYVfghhzvoGOi8piHBHHGn0MgU7X'
        log_recent_id = '1x0zCPzgKRpme5NOxUiYWHCrfiDUbsAFM'
        
# define functions

def upload_file(full_name, f_path):
        """Upload local file to Google Drive.
        
        Parameters:
        full_name (str): Output filename with timestamp, extension, and relative path.
        f_path (str): The path to the local file to upload.
        
        """
        global log_message, success, failure, dir_id_list, http
        
        ## get Google Drive folder ID        
        dir_file = os.path.dirname(full_name).split('/')[-1]
        dir_parent = os.path.dirname(os.path.dirname(full_name))
        dir_id = dir_id_list.loc[(dir_id_list['dir_parent'] == dir_parent) & (dir_id_list['dir_file'] == dir_file), 'dir_id'].values[0]
        
        ## generate file name
        f_name = os.path.basename(full_name)
        
        ## upload file to Google Drive
        try:
                ## file upload
                drive_file = drive.CreateFile(metadata={'title': f_name, 'parents': [{'id': dir_id}]})
                drive_file.SetContentFile(f_path)
                drive_file.Upload(param={"http": http})
                ## append name of file to the log message
                log_message = log_message + 'Success: ' + full_name + '\n'
                print(color('Upload successful: ' + full_name, Colors.blue))
                success+=1
        except:
                log_message = log_message + 'Failure: ' + full_name + '\n'
                print(background('Upload failed: ' + full_name, Colors.red))
                failure+=1

def upload_log(archive_id, log_id, log_recent_id, log_message, success, failure, t):
        """Upload the log of file uploads to Google Drive.
        
        The most recent log entry is placed in a separate file for easy access.
        
        Parameters:
        archive_id (str): Google Drive ID of the folder containing the logs (root of the archive).
        log_id (str): Google Drive ID of log.txt.
        log_recent_id (str): Google Drive ID of log_recent.txt.
        log_message (str): Log message.
        t (datetime): Date and time script began running (America/Toronto).
        
        """
        global http
        print("Uploading recent log...")
        try:
                ## build most recent log entry
                total_files = str(success + failure)
                log_message = 'Successful downloads : ' + str(success) + '/' + total_files + '\n' + 'Failed downloads: ' + str(failure) + '/' + total_files + '\n\n' + log_message
                log_message = str(t) + '\n\n' + 'Nightly update: ' + str(t.date()) + '\n\n' + log_message
                
                ## upload log_recent.txt
                drive_file = drive.CreateFile({'id': log_recent_id})
                drive_file.SetContentString(log_message)
                drive_file.Upload(param={"http": http})
                
                ## report success
                print(color('Recent log upload successful!', Colors.green))
        except:
                print(background('Recent log upload failed!', Colors.red))
        print("Appending recent log to full log...")
        try:
                ## read in full log
                drive_file = drive.CreateFile({'id': log_id})
                tmpdir = tempfile.TemporaryDirectory()
                log_file = os.path.join(tmpdir.name, 'log.txt')
                drive_file.GetContentFile(log_file)
                with open(log_file, 'r') as full_log:
                        full_log = full_log.read()
                
                ## append recent log to full log
                log_message = full_log + '\n\n' + log_message
                
                ## upload log.txt
                drive_file = drive.CreateFile({'id': log_id})
                drive_file.SetContentString(log_message)
                drive_file.Upload(param={"http": http})                
                
                ## report success
                print(color('Full log upload successful!', Colors.green))                
        except:
                print(background('Full log upload failed!', Colors.red))

def dl_file(url, path, file, user=False, ext='.csv', unzip=False, mb_json_to_csv=False):
        """Download file (generic).
        
        Used to download most file types (when Selenium is not required). Some files are handled with file-specific code:
        
        - unzip=True and file='13100781' has unique code.
        - Each instance of mb_json_to_csv=True has unique code.
        
        Parameters:
        url (str): URL to download file from.
        path (str): Path to output file (excluding file name). Example: 'can/epidemiology-update/'
        file (str): Output file name (excluding extension). Example: 'covid19'
        user (bool): Should the request impersonate a normal browser? Needed to access some data. Default: False.
        ext (str): Extension of the output file. Defaults to '.csv'.
        unzip (bool): If True, this file requires unzipping. Default: False.
        mb_json_to_csv (bool): If True, this is a Manitoba JSON file that that should be converted to CSV. Default: False.
        
        """
        global log_message, success, failure
        
        ## set names with timestamp and file ext
        name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
        full_name = os.path.join(path, name + ext)
        
        ## download file
        try:
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
                        failure+=1
                        ## write failure to log message if mode == prod
                        if mode == 'serverprod' or mode == 'localprod':
                                log_message = log_message + 'Failure: ' + full_name + '\n'
                ## successful request: if mode == test, print success and end
                elif mode == 'servertest' or mode == 'localtest':
                        ## print success
                        print(color('Test download successful: ' + full_name, Colors.green))
                        success+=1
                ## successful request: mode == prod, upload file
                else:
                        if unzip:
                                ## unzip data
                                name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
                                full_name = os.path.join(path, name + ext)
                                tmpdir = tempfile.TemporaryDirectory()
                                zpath = os.path.join(tmpdir.name, 'zip_file.zip')
                                with open(zpath, mode='wb') as local_file:
                                        local_file.write(req.content)                        
                                with ZipFile(zpath, 'r') as zip_file:
                                        zip_file.extractall(tmpdir.name)
                                f_path = os.path.join(tmpdir.name, file + ext)
                                if file == '13100781':
                                        ## read CSV (informative columns only)
                                        data = pd.read_csv(f_path, usecols=['REF_DATE', 'Case identifier number', 'Case information', 'VALUE'])
                                        ## save original order of column values
                                        col_order = data['Case information'].unique()
                                        ## pivot long to wide
                                        data = data.pivot(index=['REF_DATE', 'Case identifier number'], columns='Case information', values='VALUE').reset_index()
                                        ## use original column order
                                        data = data[['REF_DATE', 'Case identifier number'] + col_order.tolist()]
                                        ## write CSV
                                        data.to_csv(f_path, index=None, quoting=csv.QUOTE_NONNUMERIC)                       
                        elif mb_json_to_csv:
                                ## for Manitoba JSON data only: convert JSON to CSV and save as temporary file
                                name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
                                full_name = os.path.join(path, name + ext)                          
                                tmpdir = tempfile.TemporaryDirectory()
                                f_path = os.path.join(tmpdir.name, file + ext)
                                data = pd.json_normalize(json.loads(req.content)['features'])
                                data.columns = data.columns.str.lstrip('attributes.') # strip prefix
                                ## replace timestamps with actual dates
                                if 'Date' in data.columns:
                                        data.Date = pd.to_datetime(data.Date / 1000, unit='s').dt.date
                                data = data.to_csv(f_path, index=None)
                        else:
                                ## all other data: write contents to temporary file
                                tmpdir = tempfile.TemporaryDirectory()
                                f_path = os.path.join(tmpdir.name, file + ext)
                                with open(f_path, mode='wb') as local_file:
                                        local_file.write(req.content)
                        ## upload file
                        upload_file(full_name, f_path)
        except:
                if mode == 'serverprod' or mode == 'localprod':
                        log_message = log_message + 'Failure: ' + full_name + '\n'
                elif mode == 'servertest' or mode == 'localtest':
                        print(background('Error downloading: ' + full_name, Colors.red))

def load_webdriver(mode, tmpdir):
        """Load Chromium headless webdriver for Selenium.
        
        Parameters:
        mode (str): One of serverprod, localprod, servertest, localtest. Defines how the webdriver is loaded.
        tmpdir (TemporaryDirectory): A temporary directory for saving files.
        
        """
        options = Options()
        if mode == 'serverprod' or mode == 'servertest':
                options.binary_location = os.environ['GOOGLE_CHROME_BIN']
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        prefs = {'download.default_directory' : tmpdir.name}
        options.add_experimental_option('prefs', prefs)
        if mode == 'serverprod' or mode == 'servertest':
                return webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_PATH'], options=options)
        else:
                return webdriver.Chrome(options=options)

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
        global log_message, success, failure
        
        ## set names with timestamp and file ext
        name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
        full_name = os.path.join(path, name + ext)           
        
        ## download file
        try:
                ## create temporary directory
                tmpdir = tempfile.TemporaryDirectory()
                
                ## load webdriver
                driver = load_webdriver(mode, tmpdir)
                driver.implicitly_wait(wait + 10)
                
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
                f_path = os.path.join(tmpdir.name, file + ext)
                time.sleep(wait) # wait for download to finish
                if not os.path.isfile(f_path):
                        ## print failure
                        print(background('Error downloading: ' + full_name, Colors.red))
                        failure+=1
                        ## write failure to log message if mode == prod
                        if mode == 'serverprod' or mode == 'localprod':
                                log_message = log_message + 'Failure: ' + full_name + '\n'
                ## successful request: if mode == test, print success and end
                elif mode == 'servertest' or mode == 'localtest':
                        ## print success
                        print(color('Test download successful: ' + full_name, Colors.green))
                        success+=1
                ## successful request: mode == prod, prepare files for data upload
                else:
                        ## upload file
                        upload_file(full_name, f_path)
                
                ## quit webdriver
                driver.quit()
        except:
                if mode == 'serverprod' or mode == 'localprod':
                        log_message = log_message + 'Failure: ' + full_name + '\n'
                elif mode == 'servertest' or mode == 'localtest':
                        print(background('Error downloading: ' + full_name, Colors.red))

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
        global log_message, success, failure
        
        ## set names with timestamp and file ext
        name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
        full_name = os.path.join(path, name + ext)        
        
        ## download file
        try:
                ## create temporary directory
                tmpdir = tempfile.TemporaryDirectory()
                
                ## load webdriver
                driver = load_webdriver(mode, tmpdir)
                driver.implicitly_wait(wait + 10)
                
                ## click CSV button to export
                driver.get(url)
                elements = driver.find_elements_by_tag_name("button")
                for element in elements:
                        if element.text == 'CSV':
                                element.click()
                                
                ## verify download
                f_path = os.path.join(tmpdir.name, file + ext)
                time.sleep(wait) # wait for download to finish
                if not os.path.isfile(f_path):
                        ## print failure
                        print(background('Error downloading: ' + full_name, Colors.red))
                        failure+=1
                        ## write failure to log message if mode == prod
                        if mode == 'serverprod' or mode == 'localprod':
                                log_message = log_message + 'Failure: ' + full_name + '\n'
                ## successful request: if mode == test, print success and end
                elif mode == 'servertest' or mode == 'localtest':
                        ## print success
                        print(color('Test download successful: ' + full_name, Colors.green))
                        success+=1
                ## successful request: mode == prod, prepare files for data upload
                else:
                        ## upload file
                        upload_file(full_name, f_path)
                
                ## quit webdriver
                driver.quit()
        except:
                if mode == 'serverprod' or mode == 'localprod':
                        log_message = log_message + 'Failure: ' + full_name + '\n'
                elif mode == 'servertest' or mode == 'localtest':
                        print(background('Error downloading: ' + full_name, Colors.red))

def html_page(url, path, file, ext='.html', js=False, wait=None):
        """Save HTML of a webpage.
        
        Parameters:
        url (str): URL to screenshot.
        path (str): Path to output file (excluding file name). Example: 'can/epidemiology-update/'
        file (str): Output file name (excluding extension). Example: 'covid19'
        ext (str): Extension of the output file. Defaults to '.html'.
        js (bool): Is the HTML source rendered by JavaScript?
        wait (int): Used only if js = True. Time in seconds that the function should wait for the page to render. If the time is too short, the source code may not be captured.
        
        """
        global log_message, success, failure
        
        ## set names with timestamp and file ext
        name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
        full_name = os.path.join(path, name + ext)        
        
        ## download file
        try:
                ## create temporary directory
                tmpdir = tempfile.TemporaryDirectory()
                
                ## load webdriver
                driver = load_webdriver(mode, tmpdir)
                
                ## load page
                driver.get(url)
                
                ## save HTML of webpage
                f_path = os.path.join(tmpdir.name, file + ext)
                if js:
                        time.sleep(wait)
                        with open(f_path, 'w') as local_file:
                                local_file.write(driver.find_element_by_tag_name('html').get_attribute('innerHTML'))
                else:
                        with open(f_path, 'w') as local_file:
                                local_file.write(driver.page_source)
                        
                ## verify download
                if not os.path.isfile(f_path):
                        ## print failure
                        print(background('Error downloading: ' + full_name, Colors.red))
                        failure+=1
                        ## write failure to log message if mode == prod
                        if mode == 'serverprod' or mode == 'localprod':
                                log_message = log_message + 'Failure: ' + full_name + '\n'
                ## successful request: if mode == test, print success and end
                elif mode == 'servertest' or mode == 'localtest':
                        ## print success
                        print(color('Test download successful: ' + full_name, Colors.green))
                        success+=1
                ## successful request: mode == prod, prepare files for data upload
                else:
                        ## upload file
                        upload_file(full_name, f_path)
                
                ## quit webdriver
                driver.quit()
        except:
                if mode == 'serverprod' or mode == 'localprod':
                        log_message = log_message + 'Failure: ' + full_name + '\n'
                elif mode == 'servertest' or mode == 'localtest':
                        print(background('Error downloading: ' + full_name, Colors.red))                

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
        global log_message, success, failure
        
        ## set names with timestamp and file ext
        name = file + '_' + datetime.now(pytz.timezone('America/Toronto')).strftime('%Y-%m-%d_%H-%M')
        full_name = os.path.join(path, name + ext)        
        
        ## download file
        try:
                ## create temporary directory
                tmpdir = tempfile.TemporaryDirectory()
                
                ## load webdriver
                driver = load_webdriver(mode, tmpdir)
                
                ## load page and wait
                driver.get(url)
                time.sleep(wait) # wait for page to load      
                                
                ## take screenshot
                f_path = os.path.join(tmpdir.name, file + ext)
                
                ## get total width of the page if it is not set by the user
                if width is None:
                        width = driver.execute_script('return document.body.parentNode.scrollWidth')
                ## get total height of the page if it is not set by the user
                if height is None:
                        height = driver.execute_script('return document.body.parentNode.scrollHeight')
                ## set window size
                driver.set_window_size(width, height)
                ## take screenshot (and don't stop the script if it fails)
                try:
                        driver.find_element_by_tag_name('body').screenshot(f_path) # remove scrollbar
                        
                        ## verify screenshot
                        if not os.path.isfile(f_path):
                                ## print failure
                                print(background('Error downloading: ' + full_name, Colors.red))
                                failure+=1
                                ## write failure to log message if mode == prod
                                if mode == 'serverprod' or mode == 'localprod':
                                        log_message = log_message + 'Failure: ' + full_name + '\n'
                        elif mode == 'servertest' or mode == 'localtest':
                                ## print success
                                print(color('Test download successful: ' + full_name, Colors.green))
                                success+=1
                        else:
                                ## upload file
                                upload_file(full_name, f_path)
                except Exception as e:
                        ## print exception
                        print(e)
                        ## print failure
                        print(background('Error downloading: ' + full_name, Colors.red))
                        failure+=1
                        ## write failure to log message if mode == prod
                        if mode == 'serverprod' or mode == 'localprod':
                                log_message = log_message + 'Failure: ' + full_name + '\n'
                
                ## quit webdriver
                driver.quit()
        except:
                if mode == 'serverprod' or mode == 'localprod':
                        log_message = log_message + 'Failure: ' + full_name + '\n'
                elif mode == 'servertest' or mode == 'localtest':
                        print(background('Error downloading: ' + full_name, Colors.red))                

# AB - COVID-19 Alberta statistics
dl_ab_cases('https://www.alberta.ca/stats/covid-19-alberta-statistics.htm',
            'ab/cases/',
            'covid19dataexport',
            wait=30)

# AB - COVID-19 relaunch status map
dl_ab_oneclick('https://www.alberta.ca/maps/covid-19-status-map.htm',
               'ab/active-cases-by-region/',
               'covid19dataexport-relaunch',
               wait=20)

# AB - COVID-19 school status map
dl_ab_oneclick('https://www.alberta.ca/schools/covid-19-school-status-map.htm',
               'ab/school-status-by-region/',
               'covid19dataexport-schools',
               wait=15)

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

# BC - Public exposures (webpage)
ss_page('http://www.bccdc.ca/health-info/diseases-conditions/covid-19/public-exposures',
        'bc/public-exposures-webpage/',
        'public-exposures-screenshot',
        width=1920,
        height=5500) # set height otherwise truncated

# BC - Public exposures: flights
dl_file('http://www.bccdc.ca/Health-Info-Site/Documents/public-exposures-flights-tables-Current.pdf',
        'bc/public-exposures-flights/',
        'public-exposures-flights-tables-Current',
        ext = '.pdf')

# BC - Public exposures by setting and regional health authority (webpage)
bc_exposures = [
    ['https://www.fraserhealth.ca/covid19exposure', 'bc/regional-exposure-events-fraser-webpage', 'regional-exposure-events-fraser-webpage'],
    ['https://news.interiorhealth.ca/news/public-exposures/', 'bc/regional-exposure-events-interior-webpage', 'regional-exposure-events-interior-webpage'],
    ['https://www.islandhealth.ca/learn-about-health/covid-19/outbreaks-and-exposures', 'bc/regional-exposure-events-island-webpage', 'regional-exposure-events-island-webpage'],
    ['https://www.northernhealth.ca/health-topics/public-exposures-and-outbreaks#covid-19-public-exposures#covid-19-communityfacility-outbreaks#non-covid-19-communityfacility-outbreaks', 'bc/regional-exposure-events-northern-webpage', 'regional-exposure-events-northern-webpage'],
    ['http://www.vch.ca/covid-19/public-exposures', 'bc/regional-exposure-events-vancouver-coastal-webpage', 'regional-exposure-events-vancouver-coastal-webpage'],
    ['https://www.fraserhealth.ca/schoolexposures', 'bc/school-exposures-fraser-webpage', 'school-exposures-fraser-webpage'],
    ['https://news.interiorhealth.ca/news/school-exposures/', 'bc/school-exposures-interior-webpage', 'school-exposures-interior-webpage'],
    ['https://www.islandhealth.ca/learn-about-health/covid-19/exposures-schools', 'bc/school-exposures-island-webpage', 'school-exposures-island-webpage'],
    ['https://www.northernhealth.ca/health-topics/public-exposures-and-outbreaks#covid-19-school-exposures', 'bc/school-exposures-northern-webpage', 'school-exposures-northern-webpage'],
    ['http://www.vch.ca/covid-19/school-outbreaks', 'bc/school-exposures-vancouver-coastal-webpage', 'school-exposures-vancouver-coastal-webpage']
]
for i in range(0, len(bc_exposures)):
        html_page(bc_exposures[i][0],
                  bc_exposures[i][1],
                  bc_exposures[i][2])

# CAN - COVID-19 Situational Awareness Dashboard (Epidemiology update)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19.csv',
        'can/epidemiology-update/',
        'covid19')

# CAN - COVID-19 Situational Awareness Dashboard (Epidemiology update - as above but different date format)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv',
        'can/epidemiology-update-2/',
        'covid19-download')

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

# CAN - COVID-19 Situational Awareness Dashboard (Hospitalizations, intensive care unit (ICU), mechanical ventilation)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-hospVentICU.csv',
        'can/hospitalizations-icu-mechanical-ventilation/',
        'covid19-epiSummary-hospVentICU')

# CAN - COVID-19 Situational Awareness Dashboard (Situational awareness dashboard update time)
dl_file('https://health-infobase.canada.ca/src/data/covidLive/covid19-updateTime.csv',
        'can/situational-awareness-dashboard-update-time/',
        'covid19-updateTime')

# CAN - COVIDTrends (Mobility)
# run only on Thursdays
if t.weekday() == 3:
        dl_file('https://health-infobase.canada.ca/src/data/covidLive/covidTrends/mobility.csv',
                'can/covidtrends-mobility/',
                'mobility')

# CAN - COVIDTrends (FluWatchers)
# run only on Thursdays
if t.weekday() == 3:
        dl_file('https://health-infobase.canada.ca/src/data/covidLive/covidTrends/fluwatchers.csv',
                'can/covidtrends-fluwatchers/',
                'fluwatchers')

# CAN - Detailed preliminary information on cases of COVID-19: 6 Dimensions (Aggregated data)
dl_file('https://www150.statcan.gc.ca/n1/tbl/csv/13100774-eng.zip',
        'can/detailed-preliminary-case-info-aggregated-6-dimensions/',
        '13100774',
        unzip=True)

# CAN - Detailed preliminary information on cases of COVID-19: 4 Dimensions (Aggregated data)
dl_file('https://www150.statcan.gc.ca/n1/tbl/csv/13100775-eng.zip',
        'can/detailed-preliminary-case-info-aggregated-4-dimensions/',
        '13100775',
        unzip=True)

# CAN - Preliminary dataset on confirmed cases of COVID-19, Public Health Agency of Canada
dl_file('https://www150.statcan.gc.ca/n1/pub/13-26-0003/2020001/COVID19-eng.zip',
        'can/preliminary-dataset-on-confirmed-cases/',
        'COVID19-eng',
        unzip=True)

# MB - COVID 19 Updates
html_page('https://www.gov.mb.ca/covid19/updates/index.html',
          'mb/manitoba-webpage/',
          'manitoba-webpage')

# MB - COVID-19 data by RHA and district
dl_file('https://services.arcgis.com/mMUesHYPkXjaFGfS/arcgis/rest/services/mb_covid_cases_summary_stats_geography/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*',
        'mb/covid-data-by-rha-and-district/',
        'covid-data-by-rha-and-district',
        mb_json_to_csv=True)

# MB - Cases by demographics and RHA
dl_file('https://services.arcgis.com/mMUesHYPkXjaFGfS/arcgis/rest/services/mb_covid_cases_by_demographics_rha_all/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&groupByFieldsForStatistics=Age_Group%2CGender&orderByFields=Age_Group%20desc',
        'mb/cases-demographics-by-rha/',
        'cases-demographics-by-rha',
        mb_json_to_csv=True)

# MB - Cases by status and RHA
dl_file('https://services.arcgis.com/mMUesHYPkXjaFGfS/arcgis/rest/services/mb_covid_cases_by_status_daily_rha/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&groupByFieldsForStatistics=Date%2CRHA',
        'mb/cases-by-status-and-rha/',
        'cases-by-status-and-rha',
        mb_json_to_csv=True)

# MB - Manitoba five-day test positivity rate
dl_file('https://services.arcgis.com/mMUesHYPkXjaFGfS/arcgis/rest/services/mb_covid_5_day_positivity_rate/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Date%20asc',
        'mb/five-day-test-positivity/',
        'five-day-test-positivity',
        mb_json_to_csv=True)

# NT - GNWT's Response to COVID-19 (webpage)
html_page('https://www.gov.nt.ca/covid-19/',
          'nt/nwt-webpage/',
          'nwt-webpage')

# NU - COVID-19 (Novel Coronavirus) (webpage)
html_page('https://gov.nu.ca/health/information/covid-19-novel-coronavirus',
          'nu/nunavut-webpage/',
          'nunavut-webpage')

# NS - Coronavirus (COVID-19): case data
dl_file('https://novascotia.ca/coronavirus/data/ns-covid19-data.csv',
        'ns/case-data/',
        'ns-covid19-data')

# ON - How Ontario is responding to COVID-19 (webpage)
html_page('https://www.ontario.ca/page/how-ontario-is-responding-covid-19',
          'on/ontario-webpage/',
          'ontario-webpage',
          js=True,
          wait=10)

# ON - Confirmed positive cases of COVID19 in Ontario
dl_file('https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv',
        'on/confirmed-positive-cases/',
        'conposcovidloc')

# ON - Status of COVID-19 cases in Ontario
dl_file('https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv',
        'on/status-of-cases/',
        'covidtesting')

# ON - Status of COVID-19 cases in Ontario by Public Health Unit (PHU)
dl_file('https://data.ontario.ca/dataset/1115d5fe-dd84-4c69-b5ed-05bf0c0a0ff9/resource/d1bfe1ad-6575-4352-8302-09ca81f7ddfc/download/cases_by_status_and_phu.csv',
        'on/status-of-cases-by-phu/',
        'cases_by_status_and_phu')

# ON - Ontario COVID-19 testing metrics by Public Health Unit (PHU)
dl_file('https://data.ontario.ca/dataset/a2dfa674-a173-45b3-9964-1e3d2130b40f/resource/07bc0e21-26b5-4152-b609-c1958cb7b227/download/testing_metrics_by_phu.csv',
        'on/testing-metrics-by-phu/',
        'testing_metrics_by_phu')

# ON - Ontario COVID-19 testing percent positive by age group
dl_file('https://data.ontario.ca/dataset/ab5f4a2b-7219-4dc7-9e4d-aa4036c5bf36/resource/05214a0d-d8d9-4ea4-8d2a-f6e3833ba471/download/percent_positive_by_agegrp.csv',
        'on/percent-positive-by-age-group/',
        'percent_positive_by_agegrp')

# ON - COVID-19 hospital metrics in Ontario by Local Health Integration Network (LHIN) regions
dl_file('https://data.ontario.ca/dataset/8f3a449b-bde5-4631-ada6-8bd94dbc7d15/resource/e760480e-1f95-4634-a923-98161cfb02fa/download/lhin_hospital_icu_covid_data.csv',
        'on/hosp-icu-by-lhin/',
        'lhin_hospital_icu_covid_data')

# ON - Effective reproduction number (Re) for COVID-19 in Ontario
dl_file('https://data.ontario.ca/dataset/8da73272-8078-4cbd-ae35-1b5c60c57796/resource/1ffdf824-2712-4f64-b7fc-f8b2509f9204/download/effective_reproduction_number_ontario.csv',
        'on/effective-reproduction-number/',
        'effective_reproduction_number_ontario')

# ON - COVID Alert Impact Data (COVID Alert downloads - Canada)
dl_file('https://data.ontario.ca/dataset/06a61019-62c1-48d8-8d4d-2267ae0f1144/resource/37cfeca2-059e-4a5f-a228-249f6ab1b771/download/covid_alert_downloads_canada.csv',
        'on/covid_alert_downloads_canada/',
        'covid_alert_downloads_canada')

# ON - COVID Alert Impact Data (Uploads of COVID-19 diagnosis to COVID Alert - Ontario)
dl_file('https://data.ontario.ca/dataset/06a61019-62c1-48d8-8d4d-2267ae0f1144/resource/b792e734-9c69-47d5-8451-40fc85c2f3c6/download/covid_alert_positive_uploads_ontario.csv',
        'on/covid-alert-uploads-ontario/',
        'covid_alert_positive_uploads_ontario')

# ON - COVID-19 testing locations
dl_file('https://covid-19.ontario.ca/covid-19-ac-assets/data/locations.json',
        'on/testing-locations/',
        'locations',
        ext='.json')

# ON - Ongoing outbreaks
dl_file('https://data.ontario.ca/dataset/5472ffc1-88e2-48ca-bc9f-4aa249c1298d/resource/66d15cce-bfee-4f91-9e6e-0ea79ec52b3d/download/ongoing_outbreaks.csv',
        'on/ongoing-outbreaks/',
        'ongoing_outbreaks')

# ON - Summary of cases associated with outbreaks
dl_file('https://data.ontario.ca/dataset/5472ffc1-88e2-48ca-bc9f-4aa249c1298d/resource/d5d8f478-765c-4246-b8a7-c3b13a4a1a41/download/outbreak_cases.csv',
        'on/summary-outbreak-cases/',
        'outbreak_cases')

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
        'on/long-term-care-home-summary/',
        'ltccovidsummary')

# ON - Long term care homes: Active outbreaks
dl_file('https://data.ontario.ca/dataset/42df36df-04a0-43a9-8ad4-fac5e0e22244/resource/4b64488a-0523-4ebb-811a-fac2f07e6d59/download/activeltcoutbreak.csv',
        'on/long-term-care-home-active/',
        'activeltcoutbreak')

# ON - Long term care homes: Resolved outbreaks
dl_file('https://data.ontario.ca/dataset/42df36df-04a0-43a9-8ad4-fac5e0e22244/resource/0cf2f01e-d4e1-48ed-8027-2133d059ec8b/download/resolvedltc.csv',
        'on/long-term-care-home-resolved/',
        'resolvedltc')

# ON - Cases in schools and childcare centres (webpage)
html_page('https://www.ontario.ca/page/covid-19-cases-schools-and-child-care-centres',
          'on/cases-schools-and-child-care-centres-webpage/',
          'cases-schools-and-child-care-centres-webpage',
          js=True,
          wait=10)

# ON - Schools: Summary of cases in schools
dl_file('https://data.ontario.ca/dataset/b1fef838-8784-4338-8ef9-ae7cfd405b41/resource/7fbdbb48-d074-45d9-93cb-f7de58950418/download/schoolcovidsummary.csv',
        'on/schools-summary/',
        'schoolcovidsummary')

# ON - Schools: Schools with active COVID-19 cases
dl_file('https://data.ontario.ca/dataset/b1fef838-8784-4338-8ef9-ae7cfd405b41/resource/8b6d22e2-7065-4b0f-966f-02640be366f2/download/schoolsactivecovid.csv',
        'on/schools-active/',
        'schoolsactivecovid')

# ON - Schools: Cases in school board partners
dl_file('https://data.ontario.ca/dataset/b1fef838-8784-4338-8ef9-ae7cfd405b41/resource/245479eb-db0a-4ec4-97af-459d61da0801/download/schoolpartnersactivecovid.csv',
        'on/school-board-partners/',
        'schoolpartnersactivecovid')

# ON - Licensed child care settings: Summary of cases in licensed child care settings
dl_file('https://data.ontario.ca/dataset/5bf54477-6147-413f-bab0-312f06fcb388/resource/74f9ac9f-7ca8-4860-b2c3-189a2c25e30c/download/lccovidsummary.csv',
        'on/licensed-child-care-settings-summary/',
        'lccovidsummary')

# ON - Licensed child care settings: Licensed child care centres and agencies with active COVID-19 cases
dl_file('https://data.ontario.ca/dataset/5bf54477-6147-413f-bab0-312f06fcb388/resource/eee282d3-01e6-43ac-9159-4ba694757aea/download/lccactivecovid.csv',
        'on/licensed-child-care-settings-active/',
        'lccactivecovid')

# ON - City of Toronto Daily Status of COVID-19 Cases
dl_file('https://docs.google.com/spreadsheets/d/11KF1DuN5tntugNc10ogQDzFnW05ruzLH/export?format=xlsx&id=11KF1DuN5tntugNc10ogQDzFnW05ruzLH',
        'on/toronto-daily-status/',
        'CityofToronto_COVID-19_Daily_Public_Reporting',
        ext='.xlsx')

# ON - City of Toronto COVID-19 Summary
dl_file('https://docs.google.com/spreadsheets/d/1euhrML0rkV_hHF1thiA0G5vSSeZCqxHY/export?format=xlsx&id=1euhrML0rkV_hHF1thiA0G5vSSeZCqxHY',
        'on/toronto-covid-summary/',
        'CityofToronto_COVID-19_Data',
        ext='.xlsx')

# ON - City of Toronto COVID-19 Neighbourhood Case Data
dl_file('https://docs.google.com/spreadsheets/d/1jzH64LvFQ-UsDibXO0MOtvjbL2CvnV3N/export?format=xlsx&id=1jzH64LvFQ-UsDibXO0MOtvjbL2CvnV3N',
        'on/toronto-neighbourhood-data/',
        'CityofToronto_COVID-19_NeighbourhoodData',
        ext='.xlsx')

# ON - City of Toronto COVID-19 Neighbourhood Testing Data
dl_file('https://docs.google.com/spreadsheets/d/1xI6ckKQIOt_RNCuI0HXs7WJsgqFP015c/export?format=xlsx&id=1xI6ckKQIOt_RNCuI0HXs7WJsgqFP015c',
        'on/toronto-neighbourhood-test-data/',
        'CityofToronto_COVID-19_Testing',
        ext='.xlsx')

# ON - City of Toronto COVID-19 Monitoring Dashboard
dl_file('https://docs.google.com/spreadsheets/d/1-7j48S_KQY-I-4Qu3N3lsEOALXON2StG/export?format=xlsx&id=1-7j48S_KQY-I-4Qu3N3lsEOALXON2StG',
        'on/toronto-monitoring-dashboard/',
        'CityofToronto_COVID-19_RecoveryData',
        ext='.xlsx')

# ON - COVID-19 Cases in Toronto
# run only on Wednesdays
if t.weekday() == 2:
        dl_file('https://ckan0.cf.opendata.inter.prod-toronto.ca/download_resource/e5bf35bc-e681-43da-b2ce-0242d00922ad?format=csv',
                'on/toronto-cases/',
                'COVID19_cases')

# ON - University of Toronto COVID-19 tracking (webpage)
html_page('https://www.utoronto.ca/utogether2020/covid19-dashboard',
          'on/u-of-t-covid-tracking-webpage/',
          'u-of-t-covid-tracking-webpage')

# ON - Ottawa Demographics and Source of Infection for Cases, Deaths, and Hospitalizations
dl_file('https://www.arcgis.com/sharing/rest/content/items/6bfe7832017546e5b30c5cc6a201091b/data',
        'on/ottawa-cases-deaths-hosp-demographics-source-of-infection/',
        'COVID-19_Cases_and_Deaths_Ottawa_EN')

# ON - Ottawa Outbreaks in Healthcare Institutions, Childcare, Summer Camps, and Educational Establishments
dl_file('https://www.arcgis.com/sharing/rest/content/items/5b24f70482fe4cf1824331d89483d3d3/data',
        'on/ottawa-outbreaks-healthcare-childcare-camps-schools/',
        'COVID-19_Institutional_Outbreaks')

# ON - Ottawa Community Outbreaks
dl_file('https://opendata.arcgis.com/datasets/0df365456c254fbc942fe3d85c3dbf83_0.csv',
        'on/ottawa-community-outbreaks/',
        'COVID-19_Community_Outbreaks_in_Ottawa')

# ON - Ottawa Weekly Rates
dl_file('https://www.arcgis.com/sharing/rest/content/items/734a327141b14a55b666953c9141abf3/data',
        'on/ottawa-weekly-rates/',
        'COVID-19_Weekly_Cases_and_Rates_by_Age_in_Ottawa_EN')

# ON - Ottawa Estimated Reproduction Number in Ottawa
dl_file('https://www.arcgis.com/sharing/rest/content/items/d010a848b6e54f4990d60a202f2f2f99/data',
        'on/ottawa-estimated-rt/',
        'EN_-_Covid-19_Reproduction_Number,_R(t)')

# ON - Ottawa Testing - Ottawa Residents
dl_file('https://www.arcgis.com/sharing/rest/content/items/26c902bf1da44d3d90b099392b544b81/data',
        'on/ottawa-residents-tested/',
        'COVID-19_Ottawa_Residents_Tested_EN')

# QC - Data on COVID-19 in Quebec (webpage EN)
html_page('https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/',
          'qc/qc-webpage-en/',
          'qc-webpage-en')

# QC - Données sur la COVID-19 au Québec (webpage FR)
html_page('https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/',
          'qc/qc-webpage-fr/',
          'qc-webpage-fr')

# QC - COVID-19 time series by region and demographics
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/covid19-hist.csv',
        'qc/covid-time-series-by-region-and-demographics/',
        'covid19-hist')

# QC - COVID-19 data (charts - summary, time series, and hospitalization by age)
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/manual-data.csv',
        'qc/covid-data-charts-summary-time-series-hosp-by-age/',
        'manual-data')

# QC - Summary by region
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/regions.csv',
        'qc/summary-by-region/',
        'regions')

# QC - Deaths by RSS (health region) and living environment
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/tableau-rpa-new.csv',
        'qc/deaths-by-rss-and-living-environment/',
        'tableau-rpa-new')

# QC - Cases by RSS (health region) and RLS (local service network)
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/tableau-rls-new.csv',
        'qc/cases-by-rss-and-rls/',
        'tableau-rls-new')

# QC - Comparisons (provinces)
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/comparaisons_prov.csv',
        'qc/comparisons-provinces/',
        'comparaisons_prov')

# QC - Comparisons (countries)
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/comparaisons_pays.csv',
        'qc/comparisons-countries/',
        'comparaisons_pays')

# QC - COVID-19 data by age group and sex
dl_file('https://www.inspq.qc.ca/sites/default/files/covid/donnees/PL_AGE_SEXE.csv',
        'qc/covid-data-by-age-and-sex/',
        'PL_AGE_SEXE')

# QC - Deaths time series by living environment
dl_file('https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/decesquotidien.csv',
        'qc/deaths-time-series-by-living-environment/',
        'decesquotidien')

# QC - Recent daily cases by region
dl_file('https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/cas-region.csv',
        'qc/recent-daily-cases-by-region/',
        'cas-region')

# QC - Cumulative deaths by region
dl_file('https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/deces-region.csv',
        'qc/cumulative-deaths-by-region/',
        'deces-region')

# QC - Situation in Quebec
dl_file('https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/situation-au-quebec.csv',
        'qc/situation-in-quebec/',
        'situation-au-quebec')

# QC - Cases percentage by age group
dl_file('https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/pourcentage-cas-age.csv',
        'qc/cases-percentage-by-age-group/',
        'pourcentage-cas-age')

# QC - Deaths percentage by age group
dl_file('https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/pourcentage-deces-age.csv',
        'qc/deaths-percentage-by-age-group/',
        'pourcentage-deces-age')

# QC - COVID-19 daily data 7 days
dl_file('https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/synthese-7joursV2.csv',
        'qc/covid-data-daily-7-days/',
        'synthese-7joursV2')

# QC - Cases by region 7 days
dl_file('https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/apercu/cas-region-7jours.csv',
        'qc/cases-by-region-7-days/',
        'cas-region-7jours')

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

# QC - Montréal cases and deaths by CIUSSS (integrated health and social services centres)
dl_file('https://santemontreal.qc.ca/fileadmin/fichiers/Campagnes/coronavirus/situation-montreal/ciusss.csv',
        'qc/montreal-cases-and-deaths-by-ciusss/',
        'ciusss',
        user=True)

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

# SK - Saskatchewan's Dashboard - Total Cases (webpage)
html_page('https://dashboard.saskatchewan.ca/health-wellness/covid-19/cases',
          'sk/cases-by-region-webpage/',
          'cases-webpage')

# SK - Saskatchewan's Dashboard - Total Tests
sk_url_tests = 'https://dashboard.saskatchewan.ca' + re.search('(?<=href=\").*(?=\">CSV)', requests.get('https://dashboard.saskatchewan.ca/health-wellness/covid-19/tests').text).group(0)
dl_file(sk_url_tests,
        'sk/tests-by-region/',
        'tests')

# SK - Saskatchewan's Dashboard - Total Tests (webpage)
html_page('https://dashboard.saskatchewan.ca/health-wellness/covid-19/tests',
          'sk/tests-by-region-webpage/',
          'tests-webpage')

# YT - Case counts: COVID-19 (webpage)
html_page('https://yukon.ca/en/case-counts-covid-19',
          'yt/yukon-case-counts-webpage/',
          'yukon-case-counts-webpage')

# YT - Current COVID-19 situation (webpage)
html_page('https://yukon.ca/en/health-and-wellness/covid-19-information/latest-updates-covid-19/current-covid-19-situation',
          'yt/yukon-current-situation-webpage/',
          'yukon-current-situation-webpage')

# Other: CAN - Unofficial COVID Alert Dashboard - Diagnosis Keys Analysis
dl_file('https://raw.githubusercontent.com/uhengart/covid-alert-dashboard/master/DiagnosisKeysAnalysis.csv',
        'other/can/unofficial-covid-alert-dashboard-analysis/',
        'DiagnosisKeysAnalysis',
        ext = '.csv')

# Other: QC - Covid Écoles Québec (Excel)
dl_file('https://drive.google.com/uc?export=download&id=1xOl0uhyx9IuHZfJuRH-OR7BcGFuWYUex',
        'other/qc/covid-ecoles-quebec-school-list/',
        'COVIDECOLESQUEBEC',
        ext = '.xlsx')

# Other: CAN - Canada COVID-19 School Case Tracker (KML)
dl_file('https://www.google.com/maps/d/u/0/kml?mid=1blA_H3Hv5S9Ii_vyudgDk-j6SfJQil9S&forcekml=1',
        'other/can/canada-covid-19-school-case-tracker/',
        'Canada_COVID-19_School_Report_Tracker',
        ext = '.kml')

# Summarize successes and failures
total_files = str(success + failure)
print(background('Successful downloads: ' + str(success) + '/' + total_files, Colors.blue))
print(background('Failed downloads: ' + str(failure) + '/' + total_files, Colors.red))

## Upload log of file uploads
if mode == 'serverprod' or mode == 'localprod':
        upload_log(archive_id, log_id, log_recent_id, log_message, success, failure, t)
