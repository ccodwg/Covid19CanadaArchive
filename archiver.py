# archiver.py: Automated, daily backups of COVID-19 data from Canadian governmental and non-governmental sources #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# import modules
print('Importing modules...')

## core utilities
import os
import json

## other utilities
from colorit import *  # colourful printing
init_colorit() # enable printing with colour

## archivist.py
import archivist

# list of environmental variables used in this script (through functions in archivist.py)
## GD_KEY: environmental variable of Google Drive credentials as a simple string (used when mode = server)
## GH_TOKEN: personal access token for the GitHub API (used when mode = server)
## GH_NAME: name to use for GitHub commits (used when mode = server)
## GH_MAIL: email address to use for GitHub commits (used when mode = server)
## GOOGLE_CHROME_BIN: path to binary in heroku-buildpack-google-chrome (used when mode = server): /app/.chromedriver/bin/chromedriver
## CHROMEDRIVER_PATH: path to binary in heroku-buildpack-chromedriver (used when mode = server): /app/.apt/usr/bin/google-chrome

# set mode from argv (server vs. local and prod vs. test)
## server - read secrets from Heroku config variables
## local - read secrets from local files
## prod - archiver.py: upload files to Google Drive
## test - archiver.py: don't upload files to Google Drive, just test that files can be successfully downloaded
archivist.set_mode()

# initialize global variables
archivist.success = 0 # success counter
archivist.failure = 0 # failure counter
archivist.log_text = '' # recent log

# access Google Drive
if archivist.mode == 'serverprod' or archivist.mode == 'localprod':
        ## access Google Drive
        archivist.drive = archivist.access_gd()

        ## create httplib.Http() object
        archivist.http = archivist.create_http(archivist.drive)

        ## set log file IDs
        archivist.log_id = '10tbxUYVfghhzvoGOi8piHBHHGn0MgU7X'  # ID of log.txt
        archivist.log_recent_id = '1x0zCPzgKRpme5NOxUiYWHCrfiDUbsAFM'  # ID of log_recent.txt

# load directory ID list
archivist.dir_ids = archivist.load_dir_ids()

# clone GitHub repo
if archivist.mode == 'serverprod' or archivist.mode == 'localprod':
        ## get GitHub access token, name, mail
        if archivist.mode == 'serverprod':
                archivist.gh_token = os.environ['GH_TOKEN']
                archivist.gh_name = os.environ['GH_NAME']
                archivist.gh_mail = os.environ['GH_MAIL']
        elif archivist.mode == 'localprod':
                archivist.gh_token = open('.gh/.gh_token.txt', 'r').readline().rstrip()
                archivist.gh_name = open('.gh/.gh_name.txt', 'r').readline().rstrip()
                archivist.gh_mail = open('.gh/.gh_mail.txt', 'r').readline().rstrip()
        ## clone repo to temporary directory
        repo_tmpdir = archivist.tempfile.TemporaryDirectory()
        archivist.repo = archivist.clone_gh(repo_tmpdir)

# define time script started running in America/Toronto time zone
t = archivist.get_datetime('America/Toronto')

# load dataset info
with open('data/datasets.json') as json_file:
        ds = json.load(json_file)
ds = {item['id_name']: item for item in ds} # convert to single dict

# create dict of download functions
dl_funs = {
        "dl_file": archivist.dl_file,
        "html_page": archivist.html_page,
        "ss_page": archivist.ss_page
}

# define functions to process arguments

## define function to process true/false arguments
def arg_bool(arg):
        if ds[key]['args'][arg] == "True":
                arg_val = True
        elif ds[key]['args'][arg] == "False":
                arg_val = False
        else:
                print('Error decoding arg ' + arg + ', setting value to False.')
                arg_val = False
        return(arg_val)

## define function to process integer arguments
def arg_int(arg):
        arg_val = int(ds[key]['args'][arg])
        return(arg_val)

# announce beginning file uploads
print('Beginning file downloads...')

# loop through all datasets
for key in ds:
        
        ## print key
        print(key)
        
        ## some datasets only download on a particular day
        if 'day_to_run' in ds[key]:
                day_to_run = int(ds[key]['day_to_run'])
                if t.weekday() != day_to_run:
                        print('This dataset downloads only on when weekday is: ' + str(day_to_run) + '. Skipping...')
                        continue # throws an error if final item in loop
        
        ## if URL is not static, get URL
        if 'url' not in ds[key]:
                exec(ds[key]['url_fun_python']) # url saved as global var 'url_current'
                ds[key]['url'] = url_current
                print(ds[key]['url']) # print result
        
        ## get download function for dataset according to 'dl_fun'
        dl_fun = dl_funs[ds[key]['dl_fun']]
        
        ## process file extension
        if ds[key]['url'] == '':
                ext = ''
        else:
                ext = '.' + ds[key]['file_ext']
        
        ## process other arguments
        
        ### user (dl_file, html_page, ss_page)
        if 'user' in ds[key]['args']:
                ds[key]['args']['user'] = arg_bool('user')
        ### verify (dl_file)
        if 'verify' in ds[key]['args']:
                ds[key]['args']['verify'] = arg_bool('verify')
        ### unzip (dl_file)
        if 'unzip' in ds[key]['args']:
                ds[key]['args']['unzip'] = arg_bool('unzip')
        ### ab_json_to_csv (dl_file)
        if 'ab_json_to_csv' in ds[key]['args']:
                ds[key]['args']['ab_json_to_csv'] = arg_bool('ab_json_to_csv')
        ### mb_json_to_csv (dl_file)
        if 'mb_json_to_csv' in ds[key]['args']:
                ds[key]['args']['mb_json_to_csv'] = arg_bool('mb_json_to_csv')
        ## js (html_page)
        if 'js' in ds[key]['args']:
                ds[key]['args']['js'] = arg_bool('js')
        ## wait (html_page, ss_page)
        if 'wait' in ds[key]['args']:
                ds[key]['args']['wait'] = arg_int('wait')
        ## width (html_page, ss_page)
        if 'width' in ds[key]['args']:
                ds[key]['args']['width'] = arg_int('width')
        ## height (html_page, ss_page)
        if 'height' in ds[key]['args']:
                ds[key]['args']['height'] = arg_int('height')
        ## run download function
        dl_fun(
                url = ds[key]['url'],
                path = '/'.join([ds[key]['dir_parent'], ds[key]['dir_file']]) + '/',
                file = ds[key]['file_name'],
                ext = ext,
                **ds[key]['args']
        )

# Summarize successes and failures
archivist.print_success_failure()

# Upload log of file uploads
if archivist.mode == 'serverprod' or archivist.mode == 'localprod':
        archivist.upload_log(t)
