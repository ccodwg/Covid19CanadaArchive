# archivist.py: Helper functions for covid-19-canada-gov-data archive #
# https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data #
# Maintainer: Jean-Paul R. Soucy #

# import modules

## core utilities
import sys
import os
import re
import time
from datetime import datetime
import pytz  # better time zones
from shutil import copyfile
import tempfile
import csv
import json
from zipfile import ZipFile
from array import *

## other utilities
import pandas as pd  # better data processing
from colorit import *  # colourful printing

## web scraping
import requests
from selenium import webdriver # requires ChromeDriver and Chromium/Chrome
from selenium.webdriver.chrome.options import Options

## Google Drive
from oauth2client import service_account
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# define functions

## misc functions

def set_mode(run_args=sys.argv, manual=None):
    global mode
    print('Setting run mode...')
    if manual is None:
        if len(run_args) == 1 or ((len(run_args) == 2) and (sys.argv[1] == 'serverprod')):
            mode = 'serverprod'  # server / prod
        elif len(run_args) == 2 and run_args[1] == 'localprod':
            mode = 'localprod'  # local / prod
        elif len(run_args) == 2 and run_args[1] == 'servertest':
            mode = 'servertest'  # server / test
        elif len(run_args) == 2 and run_args[1] == 'localtest':
            mode = 'localtest'  # local / test
        else:
            sys.exit("Error: Invalid arguments.")
    else:
        mode=manual
    print('Run mode set to ' + mode + '.')

def get_datetime(tz):
    t = datetime.now(pytz.timezone(tz))
    return t

def print_success_failure():
    global success, failure
    total_files = str(success + failure)
    print(background('Successful downloads: ' + str(success) + '/' + total_files, Colors.blue))
    print(background('Failed downloads: ' + str(failure) + '/' + total_files, Colors.red))    

def find_url(search_url, regex, base_url):
    url = base_url + re.search(regex, requests.get(search_url).text).group(0)
    return url

## functions for Google Drive

def access_gd():
    """Authenticate with Google Drive and return GoogleDrive object.
    
    """
    global mode
    print('Authenticating with Google Drive...')
    ## retrieve Google Drive credentials
    if mode == 'serverprod' or mode == 'servertest':
        gd_key_val = json.loads(os.environ['GD_KEY'], strict=False)
        tmpdir = tempfile.TemporaryDirectory()
        d_key = os.path.join(tmpdir.name, ".gd_key.json")
        with open(gd_key, mode='w', encoding='utf-8') as local_file:
            json.dump(gd_key_val, local_file, ensure_ascii=False, indent=4)
    elif mode == 'localprod' or mode == 'localtest':
        if '__file__' in globals():
            script_path = os.path.dirname(os.path.abspath(__file__))
        else:
            script_path = os.getcwd()
        gd_key = os.path.join(script_path, ".gd", ".gd_key.json")                
    
    ## authenticate Google Drive access
    gauth = GoogleAuth()
    scope = ['https://www.googleapis.com/auth/drive']
    gauth.credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(gd_key, scope)
    
    ## initialize Goodle Drive object
    drive = GoogleDrive(gauth)
    
    ## confirm authentication was successful
    print('Authentication was successful.')    
    
    ## return Google Drive object
    return drive  

def create_http(drive):
    """Create httplib.Http() object for re-use when uploading using PyDrive.
    
    Parameters:
    drive: The GoogleDrive object for which to.
    
    See "Concurrent access made easy" at the following URL for why this may be useful: https://pypi.org/project/PyDrive/
    
    """
    ## create httplib.Http() object
    http = drive.auth.Get_Http_Object()
    
    ## return httplib.Http() object
    return(http)

def upload_file(full_name, f_path):
    """Upload local file to Google Drive.

    Parameters:
    full_name (str): Output filename with timestamp, extension, and relative path.
    f_path (str): The path to the local file to upload.

    """
    global drive, http, log_text, success, failure, dir_ids

    ## get Google Drive folder ID        
    dir_file = os.path.dirname(full_name).split('/')[-1]
    dir_parent = os.path.dirname(os.path.dirname(full_name))
    dir_id = dir_ids.loc[(dir_ids['dir_parent'] == dir_parent) & (dir_ids['dir_file'] == dir_file), 'dir_id'].values[0]
    
    ## generate file name
    f_name = os.path.basename(full_name)
    
    ## upload file to Google Drive
    try:
        ## file upload
        drive_file = drive.CreateFile(metadata={'title': f_name, 'parents': [{'id': dir_id}]})
        drive_file.SetContentFile(f_path)
        drive_file.Upload(param={"http": http})
        ## append name of file to the log message
        log_text = log_text + 'Success: ' + full_name + '\n'
        print(color('Upload successful: ' + full_name, Colors.blue))
        success+=1
    except:
        log_text = log_text + 'Failure: ' + full_name + '\n'
        print(background('Upload failed: ' + full_name, Colors.red))
        failure+=1

def upload_log(t):
    """Upload the log of file uploads to Google Drive.

    The most recent log entry is placed in a separate file for easy access.

    Parameters:
    t (datetime): Date and time script began running (America/Toronto).

    """
    global drive, http, log_id, log_recent_id, log_text, success, failure
    print("Uploading recent log...")
    try:
        ## build most recent log entry
        total_files = str(success + failure)
        log_text = 'Successful downloads : ' + str(success) + '/' + total_files + '\n' + 'Failed downloads: ' + str(failure) + '/' + total_files + '\n\n' + log_text
        log_text = str(t) + '\n\n' + 'Nightly update: ' + str(t.date()) + '\n\n' + log_text
        
        ## upload log_recent.txt
        drive_file = drive.CreateFile({'id': log_recent_id})
        drive_file.SetContentString(log_text)
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
        log_text = full_log + '\n\n' + log_text

        ## upload log.txt
        drive_file = drive.CreateFile({'id': log_id})
        drive_file.SetContentString(log_text)
        drive_file.Upload(param={"http": http})                

        ## report success
        print(color('Full log upload successful!', Colors.green))                
    except:
        print(background('Full log upload failed!', Colors.red))

## functions for GitHub

## functions for web scraping

def dl_file(url, path, file, user=False, ext='.csv', verify=True, unzip=False, mb_json_to_csv=False):
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
    verify (bool): If False, requests will skip SSL verification. Default: True.
    unzip (bool): If True, this file requires unzipping. Default: False.
    mb_json_to_csv (bool): If True, this is a Manitoba JSON file that that should be converted to CSV. Default: False.

    """
    global mode, log_text, success, failure

    ## set names with timestamp and file ext
    name = file + '_' + get_datetime('America/Toronto').strftime('%Y-%m-%d_%H-%M')
    full_name = os.path.join(path, name + ext)

    ## download file
    try:
        ## some websites will reject the request unless you look like a normal web browser
        ## user is True provides a normal-looking user agent string to bypass this
        if user is True:
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
            req = requests.get(url, headers=headers, verify=verify)
        else:
            req = requests.get(url, verify=verify)

        ## check if request was successful
        if not req.ok:
            ## print failure
            print(background('Error downloading: ' + full_name, Colors.red))
            failure+=1
            ## write failure to log message if mode == prod
            if mode == 'serverprod' or mode == 'localprod':
                log_text = log_text + 'Failure: ' + full_name + '\n'
        ## successful request: if mode == test, print success and end
        elif mode == 'servertest' or mode == 'localtest':
            ## print success
            print(color('Test download successful: ' + full_name, Colors.green))
            success+=1
        ## successful request: mode == prod, upload file
        else:
            if unzip:
                ## unzip data
                name = file + '_' + get_datetime('America/Toronto').strftime('%Y-%m-%d_%H-%M')
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
                name = file + '_' + get_datetime('America/Toronto').strftime('%Y-%m-%d_%H-%M')
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
        ## print failure
        print(background('Error downloading: ' + full_name, Colors.red))
        failure+=1
        ## write failure to log message if mode == prod
        if mode == 'serverprod' or mode == 'localprod':
            log_text = log_text + 'Failure: ' + full_name + '\n'

def load_webdriver(tmpdir):
    """Load Chromium headless webdriver for Selenium.

    Parameters:
    tmpdir (TemporaryDirectory): A temporary directory for saving files downloaded by the headless browser.

    """
    global mode
    
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
    global mode, log_text, success, failure

    ## set names with timestamp and file ext
    name = file + '_' + get_datetime('America/Toronto').strftime('%Y-%m-%d_%H-%M')
    full_name = os.path.join(path, name + ext)           

    ## download file
    try:
        ## create temporary directory
        tmpdir = tempfile.TemporaryDirectory()

        ## load webdriver
        driver = load_webdriver(tmpdir)
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
                log_text = log_text + 'Failure: ' + full_name + '\n'
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
            log_text = log_text + 'Failure: ' + full_name + '\n'
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
    global mode, log_text, success, failure

    ## set names with timestamp and file ext
    name = file + '_' + get_datetime('America/Toronto').strftime('%Y-%m-%d_%H-%M')
    full_name = os.path.join(path, name + ext)        

    ## download file
    try:
        ## create temporary directory
        tmpdir = tempfile.TemporaryDirectory()

        ## load webdriver
        driver = load_webdriver(tmpdir)
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
                log_text = log_text + 'Failure: ' + full_name + '\n'
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
        ## print failure
        print(background('Error downloading: ' + full_name, Colors.red))
        failure+=1
        ## write failure to log message if mode == prod
        if mode == 'serverprod' or mode == 'localprod':
            log_text = log_text + 'Failure: ' + full_name + '\n'

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
    global mode, log_text, success, failure

    ## set names with timestamp and file ext
    name = file + '_' + get_datetime('America/Toronto').strftime('%Y-%m-%d_%H-%M')
    full_name = os.path.join(path, name + ext)        

    ## download file
    try:
        ## create temporary directory
        tmpdir = tempfile.TemporaryDirectory()

        ## load webdriver
        driver = load_webdriver(tmpdir)

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
                log_text = log_text + 'Failure: ' + full_name + '\n'
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
        ## print failure
        print(background('Error downloading: ' + full_name, Colors.red))
        failure+=1
        ## write failure to log message if mode == prod
        if mode == 'serverprod' or mode == 'localprod':
            log_text = log_text + 'Failure: ' + full_name + '\n'             

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
    global mode, log_text, success, failure

    ## set names with timestamp and file ext
    name = file + '_' + get_datetime('America/Toronto').strftime('%Y-%m-%d_%H-%M')
    full_name = os.path.join(path, name + ext)        

    ## download file
    try:
        ## create temporary directory
        tmpdir = tempfile.TemporaryDirectory()

        ## load webdriver
        driver = load_webdriver(tmpdir)

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
                    log_text = log_text + 'Failure: ' + full_name + '\n'
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
                log_text = log_text + 'Failure: ' + full_name + '\n'

        ## quit webdriver
        driver.quit()
    except:
        ## print failure
        print(background('Error downloading: ' + full_name, Colors.red))
        failure+=1
        ## write failure to log message if mode == prod
        if mode == 'serverprod' or mode == 'localprod':
            log_text = log_text + 'Failure: ' + full_name + '\n'

# initialize global variables
success = 0 # success counter
failure = 0 # failure counter
log_text = '' # recent log
dir_ids = pd.read_csv("https://raw.githubusercontent.com/jeanpaulrsoucy/covid-19-canada-gov-data/master/data/data_id.csv")

# set mode from argument when running the script (server vs. local and prod vs. test)
# server: read secrets from Heroku config variables
# local: read secrets from local files
# prod: upload files to Google Drive
# test: don't upload files to Google Drive, just test that files can be successfully downloaded
set_mode()

# access Google Drive
if mode == 'serverprod' or mode == 'localprod':
    # access Google Drive
    drive = access_gd()

    # create httplib.Http() object
    http = create_http(drive)

    # set log file IDs
    log_id = '10tbxUYVfghhzvoGOi8piHBHHGn0MgU7X'  # ID of log.txt
    log_recent_id = '1x0zCPzgKRpme5NOxUiYWHCrfiDUbsAFM'  # ID of log_recent.txt