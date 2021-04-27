# archivist.py: Helper functions for Covid19CanadaArchive #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# import modules

## core utilities
import sys
import os
import re
import time
from datetime import datetime, timedelta
import pytz  # better time zones
from shutil import copyfile
import tempfile
import csv
import json
from zipfile import ZipFile
from array import *

## other utilities
import pandas as pd # better data processing
import numpy as np # better data processing
from colorit import * # colourful printing

## web scraping
import requests
from selenium import webdriver # requires ChromeDriver and Chromium/Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

## Amazon S3
import boto3

## email
import smtplib

# define functions

## misc functions

def set_mode(run_args=sys.argv, manual=None):
    global mode
    print('Setting run mode...')
    if manual is None:
        if len(run_args) == 2 and run_args[1] == 'prod':
            mode = 'prod'
        elif len(run_args) == 2 and run_args[1] == 'test':
            mode = 'test'
        else:
            sys.exit('Error: Invalid arguments.')
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

## functions for Amazon S3

def access_s3(bucket):
    """Authenticate with AWS and return s3 object.
    
    Parameters:
    bucket (str): Name of Amazon S3 bucket.
    
    """
    global mode
    print('Authenticating with AWS...') 
    ## connect to AWS
    aws = boto3.Session(
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_key
        )
    
    ## connect to S3 bucket
    s3 = aws.resource('s3').Bucket(bucket)
    
    ## confirm authentication was successful
    print('Authentication was successful.')    
    
    ## return s3 object
    return s3

def upload_file(full_name, f_path, s3_dir=None, s3_prefix=None):
    """Upload local file to Amazon S3.

    Parameters:
    full_name (str): Output filename with timestamp, extension and relative path.
    f_path (str): The path to the local file to upload.
    s3_dir(str): Optional. The directory on Amazon S3.
    s3_prefix (str): Optional. The prefix to the directory on Amazon S3.

    """
    global s3, download_log, success, failure
    
    ## generate file name
    f_name = os.path.basename(full_name)
    if (s3_dir):
        f_name = os.path.join(s3_dir, f_name)
    if (s3_prefix):
        f_name = os.path.join(s3_prefix, f_name)
    ## upload file to Amazon S3
    try:
        ## file upload
        s3.upload_file(Filename=f_path, Key=f_name)
        ## append name of file to the log message
        download_log = download_log + 'Success: ' + full_name + '\n'
        print(color('Upload successful: ' + full_name, Colors.blue))
        success+=1
    except:
        download_log = download_log + 'Failure: ' + full_name + '\n'
        print(background('Upload failed: ' + full_name, Colors.red))
        failure+=1

## functions for logging

def output_log(download_log, t):
    """Assemble log from current run.
    
    Parameters:
    download_log (str): Raw text of the download log.
    t (datetime): Date and time script began running (America/Toronto).
    
    """
    global success, failure

    ## process download log: place failures at the top, successes below
    download_log = download_log.split('\n')
    download_log.sort()
    download_log = '\n'.join(download_log)

    ## count total files
    total_files = str(success + failure)

    ## assemble log
    log = 'Successful downloads : ' + str(success) + '/' + total_files + '\n' + 'Failed downloads: ' + str(failure) + '/' + total_files + '\n' + download_log
    log = str(t) + '\n\n' + 'Nightly update: ' + str(t.date()) + '\n\n' + log

    ## return log
    return log

def upload_log(log):
    """Upload the log of file uploads to Amazon S3.

    The most recent log entry is placed in a separate file for easy access.

    Parameters:
    log (str): Log entry from current run.

    """
    global s3, success, failure
    print("Uploading recent log...")
    try:
        ## write most recent log entry temporarily and upload
        tmpdir = tempfile.TemporaryDirectory()
        log_file = os.path.join(tmpdir.name, 'log.txt')
        with open(log_file, 'w') as local_file:
            local_file.write(log)
        s3.upload_file(Filename=log_file, Key='archive/log_recent.txt')

        ## report success
        print(color('Recent log upload successful!', Colors.green))
    except:
        print(background('Recent log upload failed!', Colors.red))
    print("Appending recent log to full log...")
    try:
        ## read in full log
        tmpdir = tempfile.TemporaryDirectory()
        log_file = os.path.join(tmpdir.name, 'log.txt')
        s3.download_file(Filename=log_file, Key='archive/log.txt')
        with open(log_file, 'r') as full_log:
            full_log = full_log.read()

        ## append recent log to full log
        log = full_log + '\n\n' + log

        ## write log temporarily and upload
        tmpdir = tempfile.TemporaryDirectory()
        log_file = os.path.join(tmpdir.name, 'log.txt')
        with open(log_file, 'w') as local_file:
            local_file.write(log)
        s3.upload_file(Filename=log_file, Key='archive/log.txt')

        ## report success
        print(color('Full log upload successful!', Colors.green))
    except:
        print(background('Full log upload failed!', Colors.red))

def email_log(mail_name, mail_pass, mail_to, subject, body, smtp_server, smtp_port):
    """Email log of current run.
    
    Parameters:
    mail_name (str): Email account the log will be sent from.
    mail_pass (str): Email password for the account the log will be sent from.
    mail_to (str): Email the log will be sent to.
    subject (str): Subject line for the email.
    body (str): Body of the email.
    smtp_server (str): SMTP server address.
    smtp_port (int): SMTP server port.
    
    """
    
    ## compose message
    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (mail_name, mail_to, subject, body)
    
    ## send email
    try:
        print('Sending log...')
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.ehlo()
        server.login(mail_name, mail_pass)
        server.sendmail(mail_name, mail_to, email_text)
        server.close()
        print('Log sent!')
    except Exception as e:
        print(e)
        print('Log failed to send.')

## functions for web scraping

def dl_file(url, dir_parent, dir_file, file, ext='.csv', user=False, verify=True, unzip=False, ab_json_to_csv=False, mb_json_to_csv=False):
    """Download file (generic).

    Used to download most file types (when Selenium is not required). Some files are handled with file-specific code:

    - unzip=True and file='13100781' has unique code.
    - Each instance of ab_json_to_csv=True has unique code.
    - Each instance of mb_json_to_csv=True has unique code.

    Parameters:
    url (str): URL to download file from.
    dir_parent (str): The parent directory. Example: 'other/can'.
    dir_file (str): The file directory ('epidemiology-update').
    file (str): Output file name (excluding extension). Example: 'covid19'
    ext (str): Extension of the output file. Defaults to '.csv'.
    user (bool): Should the request impersonate a normal browser? Needed to access some data. Default: False.
    verify (bool): If False, requests will skip SSL verification. Default: True.
    unzip (bool): If True, this file requires unzipping. Default: False.
    ab_json_to_csv (bool): If True, this is an Alberta JSON file embedded in a webpage that should be converted to CSV. Default: False.
    mb_json_to_csv (bool): If True, this is a Manitoba JSON file that that should be converted to CSV. Default: False.

    """
    global mode, download_log, success, failure, prefix

    ## set names with timestamp and file ext
    name = file + '_' + get_datetime('America/Toronto').strftime('%Y-%m-%d_%H-%M')
    full_name = os.path.join(dir_parent, dir_file, name + ext)  

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
            ## write failure to log message
            download_log = download_log + 'Failure: ' + full_name + '\n'
        ## successful request: if mode == test, print success and end
        elif mode == 'test':
            ## print success and write to log
            download_log = download_log + 'Success: ' + full_name + '\n'
            print(color('Test download successful: ' + full_name, Colors.green))
            success+=1
        ## successful request: mode == prod, upload file
        else:
            if unzip:
                ## unzip data
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
            elif ab_json_to_csv:
                ## for Alberta JSON data only: extract JSON from webpage, convert JSON to CSV and save as temporary file                    
                tmpdir = tempfile.TemporaryDirectory()
                f_path = os.path.join(tmpdir.name, file + ext)
                data = re.search("(?<=\"data\"\:)\[\[.*\]\]", req.text).group(0)
                if url == "https://www.alberta.ca/maps/covid-19-status-map.htm":
                    data = BeautifulSoup(data, features="html.parser")
                    data = data.get_text() # strip HTML tags
                    ## this regex may need some tweaking if measures column changes in the future
                    data = re.sub("<\\\/a><\\\/li><\\\/ul>", "", data) # strip remaining tags
                    data = re.sub("(?<=\") ", "", data) # strip whitespace
                    data = re.sub(" (?=\")", "", data) # strip whitespace
                    data = pd.read_json(data).transpose()
                    data = data.rename(columns={0: "", 1: "Region name", 2: "Measures", 3: "Active case rate (per 100,000 population)", 4: "Active cases", 5: "Population"})
                elif url == "https://www.alberta.ca/schools/covid-19-school-status-map.htm":
                    data = re.sub(',"container":.*', "", data) # strip remaining tags
                    data = pd.read_json(data).transpose()
                    data = data.rename(columns={0: "", 1: "Region name", 2: "School status", 3: "Schools details", 4: "num_ord"})
                    data['num_ord'] = data['num_ord'].astype(str).astype(int) # convert to int
                    data[''] = data[''].astype(str).astype(int) # convert to int
                    data = data.sort_values(by=['num_ord', '']) # sort ascending by num_ord and first column (like CSV output on website)
                data = data.to_csv(None, quoting=csv.QUOTE_ALL, index=False) # to match website output: quote all lines, don't terminate with new line
                with open(f_path, 'w') as local_file:
                    local_file.write(data[:-1])
            elif mb_json_to_csv:
                ## for Manitoba JSON data only: convert JSON to CSV and save as temporary file                    
                tmpdir = tempfile.TemporaryDirectory()
                f_path = os.path.join(tmpdir.name, file + ext)
                data = pd.json_normalize(json.loads(req.content)['features'])
                data.columns = data.columns.str.lstrip('attributes.') # strip prefix
                ## replace timestamps with actual dates
                if 'Date' in data.columns:
                    data.Date = pd.to_datetime(data.Date / 1000, unit='s').dt.date
                data.to_csv(f_path, index=None)
            else:
                ## all other data: write contents to temporary file
                tmpdir = tempfile.TemporaryDirectory()
                f_path = os.path.join(tmpdir.name, file + ext)
                with open(f_path, mode='wb') as local_file:
                    local_file.write(req.content)
            ## upload file
            s3_dir = os.path.join(dir_parent, dir_file)
            upload_file(full_name, f_path, s3_dir=s3_dir, s3_prefix=prefix)
    except Exception as e:
        ## print failure
        print(e)
        print(background('Error downloading: ' + full_name, Colors.red))
        failure+=1
        ## write failure to log message
        download_log = download_log + 'Failure: ' + full_name + '\n'

def load_webdriver(tmpdir, user=False):
    """Load Chromium headless webdriver for Selenium.

    Parameters:
    tmpdir (TemporaryDirectory): A temporary directory for saving files downloaded by the headless browser.
    user (bool): Should the request impersonate a normal browser? Needed to access some data. Default: False.
    """
    global mode
    
    options = Options()
    options.binary_location = os.environ['CHROME_BIN']
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    prefs = {'download.default_directory' : tmpdir.name}
    options.add_experimental_option('prefs', prefs)
    if user:
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0")
    driver = webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_BIN'], options=options)
    return driver

def html_page(url, dir_parent, dir_file, file, ext='.html', user=False, js=False, wait=None):
    """Save HTML of a webpage.

    Parameters:
    url (str): URL to screenshot.
    dir_parent (str): The parent directory. Example: 'other/can'.
    dir_file (str): The file directory ('epidemiology-update').
    ext (str): Extension of the output file. Defaults to '.html'.
    user (bool): Should the request impersonate a normal browser? Needed to access some data. Default: False.
    js (bool): Is the HTML source rendered by JavaScript?
    wait (int): Used only if js = True. Time in seconds that the function should wait for the page to render. If the time is too short, the source code may not be captured.

    """
    global mode, download_log, success, failure
    
    ## set names with timestamp and file ext
    name = file + '_' + get_datetime('America/Toronto').strftime('%Y-%m-%d_%H-%M')
    full_name = os.path.join(dir_parent, dir_file, name + ext)        

    ## download file
    try:
        ## create temporary directory
        tmpdir = tempfile.TemporaryDirectory()

        ## load webdriver
        driver = load_webdriver(tmpdir, user=user)

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
            ## write failure to log message
            download_log = download_log + 'Failure: ' + full_name + '\n'
        ## successful request: if mode == test, print success and end
        elif mode == 'test':
            ## print success and write to log
            download_log = download_log + 'Success: ' + full_name + '\n'
            print(color('Test download successful: ' + full_name, Colors.green))
            success+=1
        ## successful request: mode == prod, prepare files for data upload
        else:
            ## upload file
            s3_dir = os.path.join(dir_parent, dir_file)
            upload_file(full_name, f_path, s3_dir=s3_dir, s3_prefix=prefix)

        ## quit webdriver
        driver.quit()
    except Exception as e:
        ## print failure
        print(e)
        print(background('Error downloading: ' + full_name, Colors.red))
        failure+=1
        ## write failure to log message
        download_log = download_log + 'Failure: ' + full_name + '\n'

def ss_page(url, dir_parent, dir_file, file, ext='.png', user=False, wait=5, width=None, height=None):
    """Take a screenshot of a webpage.

    By default, Selenium attempts to capture the entire page.

    Parameters:
    url (str): URL to screenshot.
    dir_parent (str): The parent directory. Example: 'other/can'.
    dir_file (str): The file directory ('epidemiology-update').
    ext (str): Extension of the output file. Defaults to '.png'.
    user (bool): Should the request impersonate a normal browser? Needed to access some data. Default: False.
    wait (int): Time in seconds that the function should wait. Should be > 0 to ensure the entire page is captured.
    width (int): Width of the output screenshot. Default: None. If not set, the function attempts to detect the maximum width.
    height (int): Height of the output screenshot. Default: None. If not set, the function attempts to detect the maximum height.

    """
    global mode, download_log, success, failure

    ## set names with timestamp and file ext
    name = file + '_' + get_datetime('America/Toronto').strftime('%Y-%m-%d_%H-%M')
    full_name = os.path.join(dir_parent, dir_file, name + ext)        

    ## download file
    try:
        ## create temporary directory
        tmpdir = tempfile.TemporaryDirectory()

        ## load webdriver
        driver = load_webdriver(tmpdir, user)

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
                if mode == 'prod':
                    download_log = download_log + 'Failure: ' + full_name + '\n'
            elif mode == 'test':
                ## print success and write to log
                download_log = download_log + 'Success: ' + full_name + '\n'
                print(color('Test download successful: ' + full_name, Colors.green))
                success+=1
            else:
                ## upload file
                s3_dir = os.path.join(dir_parent, dir_file)
                upload_file(full_name, f_path, s3_dir=s3_dir, s3_prefix=prefix)
        except Exception as e:
            ## print exception
            print(e)
            ## print failure
            print(background('Error downloading: ' + full_name, Colors.red))
            failure+=1
            ## write failure to log message if mode == prod
            if mode == 'prod':
                download_log = download_log + 'Failure: ' + full_name + '\n'

        ## quit webdriver
        driver.quit()
    except Exception as e:
        ## print failure
        print(e)
        print(background('Error downloading: ' + full_name, Colors.red))
        failure+=1
        ## write failure to log message if mode == prod
        if mode == 'prod':
            download_log = download_log + 'Failure: ' + full_name + '\n'

## indexing

def create_index():
    """ Create an index of files in datasets.json.
    
    """
    global s3  
    
    ## load datasets.json
    with open('data/datasets.json') as json_file:
        datasets = json.load(json_file)
    
    ## convert datasets into single dictionary
    ds = {} # create empty dictionary
    for a in datasets: # active and inactive
        for d in datasets[a]:
            for i in range(len(datasets[a][d])):
                ds[datasets[a][d][i]['id_name']] = datasets[a][d][i]
    
    ## load existing index
    ## only filter out keys already present in index - don't re-request etags
    
    ## intialize index
    index = pd.DataFrame(columns = ['dir_parent', 'dir_file', 'dir_id', 'file_name', 'file_timestamp', 'file_date', 'file_date_true', 'file_id', 'file_mime_type', 'file_size', 'file_md5', 'file_md5_duplicate', 'file_url'])
    
    ## loop through each dataset
    for key in ds:
        ## get prefix
        prefix = 'archive/' + ds[key]['dir_parent'] + '/' + ds[key]['dir_file'] + '/'
        files = []
        for file in s3.objects.filter(Prefix=prefix):
            print(file)
    
    ## loop through each dir_id
    for i in dir_ids.index.to_list():
        ## fetch list of files
        d = drive.ListFile({'q': drive_template.format(dir_id=dir_ids.loc[i, 'dir_id'])}).GetList()
        ## turn into DataFrame
        d = pd.DataFrame(d)
        ## keep only necessary columns
        d = d[['id', 'title', 'mimeType', 'webContentLink', 'md5Checksum', 'fileSize']]
        ## rename columns
        d = d.rename(columns={'id': 'file_id', 'title': 'file_name', 'mimeType': 'file_mime_type', 'webContentLink': 'file_url', 'md5Checksum': 'file_md5', 'fileSize': 'file_size'})
        ## extract timestamp from file
        d['file_timestamp'] = d['file_name'].str.extract('(?<=_)(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}).*$', expand=True)
        d['file_timestamp'] = pd.to_datetime(d['file_timestamp'], format='%Y-%m-%d_%H-%M')
        ## sort files by timestamp in ascending order
        d = d.sort_values(by=['file_timestamp'])
        ## extract file date from timestamp
        d['file_date'] = d['file_timestamp'].dt.date
        ## set initial values for true date
        d['file_date_true'] = d['file_date']
        ## check if there are multiple hashes on the first date of data
        d_first_date = d[d['file_date'] == d['file_date'].min()].drop_duplicates(['file_md5'])
        if (len(d_first_date) > 1):
            ## if there multiple hashes on the first date, assume the earliest file is actually from the previous date
            d.loc[d['file_name'] == d_first_date.iloc[0]['file_name'], 'file_date_true'] = d.loc[d['file_name'] == d_first_date.iloc[0]['file_name'], 'file_date'] - timedelta(days=1)
        ## generate list of all possible dates: from first true date to last true date
        d_dates_seq = pd.date_range(d['file_date_true'].min(), d['file_date'].max()).tolist()
        ## generate list of all dates in the dataset
        d_dates = d['file_date_true'].unique().tolist()
        ## are any expected dates are missing?
        d_dates_missing = np.setdiff1d(d_dates_seq, d_dates)
        if (len(d_dates_missing) > 0):
            ## if there are any missing dates, check if there are multiple hashes in the following day
            for j in d_dates_missing:
                d_dates_next = d[d['file_date_true'] == j + timedelta(days=1)].drop_duplicates(['file_md5'])
                if len(d_dates_next) > 1:
                    ## if there are more than 0 or 1 hashes on the previous date, assume the earliest hash actually corresponds to the missing day
                    d.loc[d['file_name'] == d_dates_next.iloc[0]['file_name'], 'file_date_true'] = d.loc[d['file_name'] == d_dates_next.iloc[0]['file_name'], 'file_date_true'] - timedelta(days=1)
        ## using true date, keep only the final hash of each date ('definitive file' for that date)
        d = d.drop_duplicates(['file_date_true'], keep='last')
        ## using hash, mark duplicates appearing after the first instance (e.g., duplicate hashes of Friday value for weekend versions of files updated only on weekdays)
        d['file_md5_duplicate'] = d['file_md5'].duplicated()
        ## mark duplicates using 1 and 0 rather than True and False
        d['file_md5_duplicate'] = np.where(d['file_md5_duplicate']==True, 1, 0)
        ## add columns: dir_parent, dir_file, dir_id
        d['dir_parent'] = dir_ids.loc[i, 'dir_parent']
        d['dir_file'] = dir_ids.loc[i, 'dir_file']
        d['dir_id'] = dir_ids.loc[i, 'dir_id']
        index = index.append(d)
        ## print progress
        print(dir_ids.loc[i, 'dir_parent'] + '/' + dir_ids.loc[i, 'dir_file'])
    
    ## return index
    return(index)

def write_index(index):
    print('Writing data index...')
    index.to_csv('data/data_index.csv', index=False)
    print('Data index written.')
