# archivist.py: Helper functions for Covid19CanadaArchive #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# import modules

## core utilities
import sys
import os
import argparse
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

## Amazon S3
import boto3

## email
import smtplib

# define functions

## misc functions

def parse_args():
    global mode, uuid
    
    # initialize parser with arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", choices = ['test', 'prod'], required = True, help = "Run mode: prod or test")
    parser.add_argument("--uuid", nargs = '+', required = False, help = "Specify UUIDs of individual datasets to download")
    parser.add_argument("--no-email", required = False, action = "store_false", dest = "email", help = "If present, no email will be produced at the end of the run.")
    args = parser.parse_args()
    
    # set run mode
    mode = args.mode
    print('Run mode set to ' + mode + '.')
    
    # set email mode
    email = args.email
    if email:
        print('An email will be sent at the end of this run.')
    else:
        print('No email will be sent at the end of this run.')
    
    # report datasets to be downloaded
    uuid = args.uuid
    if uuid:
        print('Specified datasets: ', ', '.join(uuid))
    else:
        print('No datasets specified. Downloading all datasets...')

def get_datetime(tz):
    t = datetime.now(pytz.timezone(tz))
    return t

def print_success_failure():
    global success, failure
    total_files = str(success + failure)
    print(background('Successful downloads: ' + str(success) + '/' + total_files, Colors.blue))
    print(background('Failed downloads: ' + str(failure) + '/' + total_files, Colors.red))

def generate_rerun_code():
    global mode, failure_uuid
    code = 'The following code will rerun failed datasets:\n' + 'python archiver.py -m ' + mode + ' --uuid ' + ' '.join(failure_uuid)
    return code

def find_url(search_url, regex, base_url):
    url = base_url + re.search(regex, requests.get(search_url).text).group(0)
    return url

## functions for Amazon S3

def access_s3(bucket, aws_id, aws_key):
    """Authenticate with AWS and return s3 object.
    
    Parameters:
    bucket (str): Name of Amazon S3 bucket.
    aws_id (str): ID for AWS.
    aws_key (str): Key for AWS.
    
    """
    global mode, s3
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

def upload_file(full_name, f_path, uuid, s3_dir=None, s3_prefix=None):
    """Upload local file to Amazon S3.

    Parameters:
    full_name (str): Output filename with timestamp, extension and relative path.
    f_path (str): The path to the local file to upload.
    uuid (str): The UUID of the dataset.
    s3_dir(str): Optional. The directory on Amazon S3.
    s3_prefix (str): Optional. The prefix to the directory on Amazon S3.

    """
    global s3, download_log, success, failure, failure_uuid
    
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
    except Exception as e:
        download_log = download_log + 'Failure: ' + full_name + '\n'
        print(e)
        print(background('Upload failed: ' + full_name, Colors.red))
        failure+=1
        failure_uuid.append(uuid)

## functions for emailing

def send_email(mail_name, mail_pass, mail_to, subject, body, smtp_server, smtp_port):
    """Send email (e.g., a download log).
    
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
    
    ## send message
    try:
        print('Sending message...')
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.ehlo()
        server.login(mail_name, mail_pass)
        server.sendmail(mail_name, mail_to, email_text)
        server.close()
        print('Message sent!')
    except Exception as e:
        print(e)
        print('Message failed to send.')

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
    log = 'Successful downloads : ' + str(success) + '/' + total_files + '\n' + 'Failed downloads: ' + str(failure) + '/' + total_files + '\n' + download_log + '\n\n' + generate_rerun_code()
    log = str(t.date()) + ' ' + str(t.hour) + ':' + str(t.minute) + '\n\n' + log

    ## return log
    return log

def upload_log(log):
    """Upload the log of file uploads to Amazon S3.

    The most recent log entry is placed in a separate file for easy access.

    Parameters:
    log (str): Log entry from current run.

    """
    global s3
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

## functions for web scraping

def dl_file(url, dir_parent, dir_file, file, ext, uuid, user=False, rand_url=False, verify=True, unzip=False, ab_json_to_csv=False, mb_json_to_csv=False):
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
    ext (str): Extension of the output file.
    uuid (str): The UUID of the dataset.
    user (bool): Should the request impersonate a normal browser? Needed to access some data. Default: False.
    rand_url(bool): Should the URL have a number appended as a parameter to prevent caching? Default: False.
    verify (bool): If False, requests will skip SSL verification. Default: True.
    unzip (bool): If True, this file requires unzipping. Default: False.
    ab_json_to_csv (bool): If True, this is an Alberta JSON file embedded in a webpage that should be converted to CSV. Default: False.
    mb_json_to_csv (bool): If True, this is a Manitoba JSON file that that should be converted to CSV. Default: False.

    """
    global mode, download_log, success, failure, failure_uuid, prefix_root

    ## set names with timestamp and file ext
    name = file + '_' + get_datetime('America/Toronto').strftime('%Y-%m-%d_%H-%M')
    full_name = os.path.join(dir_parent, dir_file, name + ext)  

    ## download file
    try:

        ## add no-cache headers
        headers = {"Cache-Control": "no-cache", "Pragma": "no-cache"}

        ## some websites will reject the request unless you look like a normal web browser
        ## user is True provides a normal-looking user agent string to bypass this
        if user is True:
            headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"

        ## add random number to url to prevent caching, if requested
        if rand_url is True:
            url = url + "?randNum=" + str(int(datetime.now().timestamp()))

        ## request URL
        req = requests.get(url, headers=headers, verify=verify)

        ## check if request was successful
        if not req.ok:
            ## print failure
            print(background('Error downloading: ' + full_name, Colors.red))
            failure+=1
            failure_uuid.append(uuid)
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
            upload_file(full_name, f_path, uuid, s3_dir=s3_dir, s3_prefix=prefix_root)
    except Exception as e:
        ## print failure
        print(e)
        print(background('Error downloading: ' + full_name, Colors.red))
        failure+=1
        failure_uuid.append(uuid)
        ## write failure to log message
        download_log = download_log + 'Failure: ' + full_name + '\n'

def load_webdriver(tmpdir, user=False):
    """Load Chromium headless webdriver for Selenium.

    Parameters:
    tmpdir (TemporaryDirectory): A temporary directory for saving files downloaded by the headless browser.
    user (bool): Should the request impersonate a normal browser? Needed to access some data. Default: False.
    """
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

def html_page(url, dir_parent, dir_file, file, ext, uuid, user=False, js=False, wait=None):
    """Save HTML of a webpage.

    Parameters:
    url (str): URL to screenshot.
    dir_parent (str): The parent directory. Example: 'other/can'.
    dir_file (str): The file directory ('epidemiology-update').
    ext (str): Extension of the output file.
    uuid (str): The UUID of the dataset.
    user (bool): Should the request impersonate a normal browser? Needed to access some data. Default: False.
    js (bool): Is the HTML source rendered by JavaScript?
    wait (int): Used only if js = True. Time in seconds that the function should wait for the page to render. If the time is too short, the source code may not be captured.

    """
    global mode, download_log, success, failure, prefix_root
    
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
        
        ## special processing
        try:
            if uuid == '66fbe91e-34c0-4f7f-aa94-cf6c14db0158':
                # wait for tab link to be clickable then click
                element = WebDriverWait(driver, timeout=wait).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/nav/div/ul/li[2]/a')))
                element.click()
                # time.sleep(wait); driver.find_element_by_id('complete').get_attribute('innerHTML') # test
            elif uuid == '391d177d-1ea8-45ac-bca4-d9f86733c253':
                # wait for tab link to be clickable then click
                element = WebDriverWait(driver, timeout=wait).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/nav/div/ul/li[3]/a')))
                element.click()
                # time.sleep(wait); driver.find_element_by_id('Title2').get_attribute('innerHTML') # test
            elif uuid == 'effdfd82-7c59-4f49-8445-f1f8f73b6dc2':
                # wait for tab link to be clickable then click
                element = WebDriverWait(driver, timeout=wait).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/nav/div/ul/li[4]/a')))
                element.click()
                element = WebDriverWait(driver, timeout=wait).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/nav/div/ul/li[4]/ul/li[1]/a')))
                element.click()
                # time.sleep(wait); driver.find_element_by_id('VCTitle2').get_attribute('innerHTML') # test
            elif uuid == '454de458-f7b4-4814-96a6-5a426f8c8c60':
                # wait for tab link to be clickable then click
                element = WebDriverWait(driver, timeout=wait).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/nav/div/ul/li[4]/a')))
                element.click()
                element = WebDriverWait(driver, timeout=wait).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/nav/div/ul/li[4]/ul/li[2]/a')))
                element.click()
                # time.sleep(wait); driver.find_element_by_id('VCTitle').get_attribute('innerHTML') # test
        ## prints exception but still proceeds (for now)
        except Exception as e:
            ## print exception
            print(e)
        
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
            failure_uuid.append(uuid)
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
            upload_file(full_name, f_path, uuid, s3_dir=s3_dir, s3_prefix=prefix_root)

        ## quit webdriver
        driver.quit()
    except Exception as e:
        ## print failure
        print(e)
        print(background('Error downloading: ' + full_name, Colors.red))
        failure+=1
        failure_uuid.append(uuid)
        ## write failure to log message
        download_log = download_log + 'Failure: ' + full_name + '\n'

def ss_page(url, dir_parent, dir_file, file, ext, uuid, user=False, wait=5, width=None, height=None):
    """Take a screenshot of a webpage.

    By default, Selenium attempts to capture the entire page.

    Parameters:
    url (str): URL to screenshot.
    dir_parent (str): The parent directory. Example: 'other/can'.
    dir_file (str): The file directory ('epidemiology-update').
    ext (str): Extension of the output file.
    uuid (str): The UUID of the dataset.
    user (bool): Should the request impersonate a normal browser? Needed to access some data. Default: False.
    wait (int): Time in seconds that the function should wait. Should be > 0 to ensure the entire page is captured.
    width (int): Width of the output screenshot. Default: None. If not set, the function attempts to detect the maximum width.
    height (int): Height of the output screenshot. Default: None. If not set, the function attempts to detect the maximum height.

    """
    global mode, download_log, success, failure, prefix_root

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
                failure_uuid.append(uuid)
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
                upload_file(full_name, f_path, uuid, s3_dir=s3_dir, s3_prefix=prefix_root)
        except Exception as e:
            ## print exception
            print(e)
            ## print failure
            print(background('Error downloading: ' + full_name, Colors.red))
            failure+=1
            failure_uuid.append(uuid)
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
        failure_uuid.append(uuid)
        ## write failure to log message if mode == prod
        if mode == 'prod':
            download_log = download_log + 'Failure: ' + full_name + '\n'

## indexing

def create_index(url_base, bucket, aws_id, aws_key):
    """ Create an index of files in datasets.json stored in the S3 bucket.
    
    Parameters:
    url_base (str): The base URL to the S3 bucket, used to construct file URLs.
    bucket (str): Name of Amazon S3 bucket.
    aws_id (str): ID for AWS.
    aws_key (str): Key for AWS.
    
    """
    global s3, prefix_root
    
    ## temporarily disable pandas chained assignment warning
    pd_option = pd.get_option('chained_assignment') # save previous value
    pd.set_option('chained_assignment', None) # disable
    
    ## load datasets.json
    with open('datasets.json') as json_file:
        datasets = json.load(json_file)
    
    ## convert datasets into single dictionary
    ds = {} # create empty dictionary
    for a in datasets: # active and inactive
        for d in datasets[a]:
            for i in range(len(datasets[a][d])):
                ds[datasets[a][d][i]['uuid']] = datasets[a][d][i]
    
    ## prepare paginator for list of all files in the archive
    paginator = boto3.client(
        's3',
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_key).get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix_root)
    
    ## create inventory of files in the archive
    inv = []
    for page in pages:
        for obj in page['Contents']:
            inv.append([obj['Key'], obj['Size'], obj['ETag']])
    inv = pd.DataFrame(inv, columns = ['file_path', 'file_size', 'file_etag'])
    
    ## process inventory
    # calculate other columns
    inv['dir_parent'] = inv['file_path'].apply(lambda x: os.path.dirname(x).split('/')[1:-1])
    inv['dir_parent'] = inv['dir_parent'].apply(lambda x: '/'.join(x))
    inv['dir_file'] = inv['file_path'].apply(lambda x: os.path.dirname(x).split('/')[-1])
    inv['file_name'] = inv['file_path'].apply(lambda x: os.path.basename(x))
    inv['file_timestamp'] = inv['file_name'].str.extract('(?<=_)(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}).*$', expand=True)
    inv['file_date'] = pd.to_datetime(inv['file_timestamp'], format='%Y-%m-%d_%H-%M').dt.date
    inv['file_url'] = url_base + inv['file_path']
    # initialize other columns
    inv['file_date_true'] = inv['file_date'] # set initial values for true date
    inv['file_etag_duplicate'] = np.nan
    # remove directories, log files and supplementary files
    inv = inv[inv['file_name'] != ''] # remove directories
    inv = inv[inv['dir_file'] != prefix_root] # remove log files (stored in root)
    inv = inv[inv['dir_file'] != 'supplementary'] # remove supplementary files
    # keep only necessary columns and reorder
    inv = inv[['dir_parent', 'dir_file', 'file_name', 'file_timestamp', 'file_date', 'file_date_true', 'file_size', 'file_etag', 'file_etag_duplicate', 'file_url']]
    # sort
    inv = inv.sort_values(by=['dir_parent', 'dir_file', 'file_timestamp'])
    
    ## initialize index
    ind = pd.DataFrame(columns=inv.columns)
    
    ## calculate true dates and etag duplicates - loop through each dataset
    for key in ds:
        d_p = ds[key]['dir_parent']
        d_f = ds[key]['dir_file']
        # get data
        d = inv[(inv['dir_parent'] == d_p) & (inv['dir_file'] == d_f)]
        # check if there are multiple hashes on the first date of data
        d_first_date = d[d['file_date'] == d['file_date'].min()].drop_duplicates(['file_etag'])
        if (len(d_first_date) > 1):
            # if there multiple hashes on the first date, assume the earliest file is actually from the previous date
            d.loc[d['file_name'] == d_first_date.iloc[0]['file_name'], 'file_date_true'] = d.loc[d['file_name'] == d_first_date.iloc[0]['file_name'], 'file_date'] - timedelta(days=1)
        # generate list of all possible dates: from first true date to last true date
        d_dates_seq = pd.date_range(d['file_date_true'].min(), d['file_date'].max()).tolist()
        # generate list of all dates in the dataset
        d_dates = d['file_date_true'].unique().tolist()
        # are any expected dates are missing?
        d_dates_missing = np.setdiff1d(d_dates_seq, d_dates)
        if (len(d_dates_missing) > 0):
            # if there are any missing dates, check if there are multiple hashes in the following day
            for j in d_dates_missing:
                d_dates_next = d[d['file_date_true'] == j + timedelta(days=1)].drop_duplicates(['file_etag'])
                if len(d_dates_next) > 1:
                    # if there are more than 0 or 1 hashes on the previous date, assume the earliest hash actually corresponds to the missing day
                    d.loc[d['file_name'] == d_dates_next.iloc[0]['file_name'], 'file_date_true'] = d.loc[d['file_name'] == d_dates_next.iloc[0]['file_name'], 'file_date_true'] - timedelta(days=1)
        # using true date, keep only the final hash of each date ('definitive file' for that date)
        d = d.drop_duplicates(['file_date_true'], keep='last')
        # using hash, mark duplicates appearing after the first instance (e.g., duplicate hashes of Friday value for weekend versions of files updated only on weekdays)
        d['file_etag_duplicate'] = d['file_etag'].duplicated()
        # mark duplicates using 1 and 0 rather than True and False
        d['file_etag_duplicate'] = np.where(d['file_etag_duplicate']==True, 1, 0)
        # save modified index
        ind = ind.append(d)
        # print progress
        print(d_p + '/' + d_f)
    
    ## reset pandas chained assignment warning option
    pd.set_option('chained_assignment', pd_option) # reset
    
    ## return index
    return(ind)

def write_index(ind, file_path=None):
    """ Write index locally or upload to Amazon S3.
    
    If file_path is not provided, the index is uploaded to Amazon S3.
    
    Parameters:
    index: The index returned by create_index().
    file_path (str): Optional. Path to write file locally.
    
    """
    global s3, prefix_root
    
    if file_path is None:
        print('Uploading file index...')
        try:
            ## write file index temporarily and upload to Amazon S3
            tmpdir = tempfile.TemporaryDirectory()
            file_index = os.path.join(tmpdir.name, 'file_index.csv')
            ind.to_csv(file_index, index=False)
            s3.upload_file(Filename=file_index, Key=prefix_root + '/file_index.csv')
            ## report success
            print(color('File index upload successful!', Colors.green))
        except:
            ## report failure
            print(background('File index upload failed!', Colors.red))
    else:
        print('Writing file index...')
        try:
            ## write file index
            ind.to_csv(file_index, index=False)
            ## report success
            print(color('File index upload successful!', Colors.green))
        except:
            ## report failure
            print(background('File index upload failed!', Colors.red))
