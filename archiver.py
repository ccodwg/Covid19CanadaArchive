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
## AWS_ID: environmental variable of AWS ID (used when mode = server)
## AWS_KEY: environmental variable of AWS key (used when mode = server)
## MAIL_NAME: environmental variable of email account (used when mode = server)
## MAIL_PASS: environemntal variable of email password (used when mode = server)
## MAIL_TO: environmental variable of account receiving email logs (used when mode = server)
## SMTP_SERVER: environmental variable of email server address (used when mode = server)
## SMTP_PORT: environmental variable of email server port (used when mode = server)
## GOOGLE_CHROME_BIN: path to binary in heroku-buildpack-google-chrome (used when mode = server): /app/.chromedriver/bin/chromedriver
## CHROMEDRIVER_PATH: path to binary in heroku-buildpack-chromedriver (used when mode = server): /app/.apt/usr/bin/google-chrome

# set mode from argv (server vs. local and prod vs. test)
## server - read secrets from environmental variables
## local - read secrets from local files
## prod - archiver.py: upload files to file server
## test - archiver.py: don't upload files to file server, just test that files can be successfully downloaded
archivist.set_mode()

# initialize global variables
archivist.success = 0 # success counter
archivist.failure = 0 # failure counter
archivist.download_log = '' # download log

# load email configuration
if archivist.mode == 'localprod' or archivist.mode == 'localtest':
        mail_name = open('.gm/.mail_name', 'r').readline().rstrip()
        mail_pass = open('.gm/.mail_pass', 'r').readline().rstrip()
        mail_to = open('.gm/.mail_to', 'r').readline().rstrip()
        smtp_server = open('.gm/.smtp_server', 'r').readline().rstrip()
        smtp_port = int(open('.gm/.smtp_port', 'r').readline().rstrip())
elif archivist.mode == 'serverprod' or archivist.mode == 'servertest':
        mail_name = os.environ['MAIL_NAME']
        mail_pass = os.environ['MAIL_PASS']
        mail_to = os.environ['MAIL_TO']
        smtp_server = os.environ['SMTP_SERVER']
        smtp_port = int(os.environ['SMTP_PORT'])

# access Amazon S3
if archivist.mode == 'serverprod' or archivist.mode == 'localprod':
        ## access S3
        archivist.s3 = archivist.access_s3(bucket='data.opencovid.ca')
        
        ## set S3 path prefix for achived files
        archivist.prefix = 'archive'

# define ChromeDriver location (for localprod/localtest)
if archivist.mode == 'localprod' or archivist.mode == 'localtest':
        archivist.CHROMEDRIVER_PATH_LOCAL = '/snap/bin/chromium.chromedriver' # Snap Chromium Chromedriver

# define time script started running in America/Toronto time zone
t = archivist.get_datetime('America/Toronto')

# load active datasets
with open('data/datasets.json') as json_file:
        datasets = json.load(json_file)
datasets = datasets['active'] # subset active datasets

# convert datasets into single dictionary
ds = {} # create empty dictionary
for d in datasets:
        for i in range(len(datasets[d])):
                ds[datasets[d][i]['id_name']] = datasets[d][i]

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
        
        ## skip if dataset is not active
        if ds[key]['active'] != "True":
                print('Skipping inactive dataset...')
                continue
        
        ## print key
        print(key)
        
        ## some datasets only download on a particular day
        if 'day_to_run' in ds[key]:
                day_to_run = int(ds[key]['day_to_run'])
                if t.weekday() != day_to_run:
                        print('This dataset downloads only on when weekday is: ' + str(day_to_run) + '. Skipping...')
                        continue
        
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
                dir_parent = ds[key]['dir_parent'],
                dir_file = ds[key]['dir_file'],
                file = ds[key]['file_name'],
                ext = ext,
                **ds[key]['args']
        )

# summarize successes and failures
archivist.print_success_failure()

# assemble log entry
log = archivist.output_log(archivist.download_log, t)

# upload and email log of file uploads (wehn mode = prod)
if archivist.mode == 'localprod' or archivist.mode == 'serverprod':
        
        ## upload log
        archivist.upload_log(log)
        
        ## compose email message (current log entry)
        subject = " ".join(['PROD', 'Covid19CanadaArchive Log', t.strftime('%Y-%m-%d %H:%M') + ',', 'Failed:', str(archivist.failure)])
        body = log        
        
        ## email log
        archivist.email_log(mail_name, mail_pass, mail_to, subject, body, smtp_server, smtp_port)

# email log of failed downloads, if any (when mode = test)
if archivist.mode == 'localtest' or archivist.mode == 'servertest':
        
        ## email log if there are any failures
        if archivist.failure > 0:
                
                ## compose email message (current log entry)
                subject = " ".join(['TEST', 'Covid19CanadaArchive Log', t.strftime('%Y-%m-%d %H:%M') + ',', 'Failed:', str(archivist.failure)])
                body = log
                archivist.email_log(mail_name, mail_pass, mail_to, subject, body, smtp_server, smtp_port)