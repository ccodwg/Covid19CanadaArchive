# archiver.py: Automated, daily dataset updates to the Canadian COVID-19 Data Archive #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# import modules
print('Importing modules...')

## core utilities
import os
import json

## other utilities
from colorit import * # colourful printing
init_colorit() # enable printing with colour

## archivist
import archivist

# list of environmental variables used in this script (through functions in archivist)
## AWS_ID: AWS ID [prod only]
## AWS_KEY: AWS key [prod only]
## MAIL_NAME: email account
## MAIL_PASS: email password
## MAIL_TO: account receiving email logs
## MAIL_ALIAS: (optional) alias email sender name
## SMTP_SERVER: email server address
## SMTP_PORT: email server port
## PO_TOKEN: Pushover application token
## PO_KEY: Pushover application key
## CHROME_BIN: path to Chromium/Chrome binary
## CHROMEDRIVER_BIN: path to Chromedriver

# parse arguments
## positional (first argument): file path to datasets.json
## -m / --mode
### prod: Download files and upload them to the server.
### test: Download files but don't upload them to the server, just test that they can be successfully downloaded.
## --uuid
### run only the specified list of datasets (identified by UUID), otherwise run all datasets
## --no-email
### don't send an email at the end of the run

# parse arguments
archivist.parse_args()

# define time script started running in America/Toronto time zone
t = archivist.get_datetime('America/Toronto')

# access Amazon S3
if archivist.Archivist.mode == 'prod':
        ## load AWS credentials
        aws_id = os.environ['AWS_ID']
        aws_key = os.environ['AWS_KEY']
        
        ## access S3
        archivist.Archivist.setS3(archivist.access_s3(bucket='data.opencovid.ca', aws_id=aws_id, aws_key=aws_key))
        
        ## set S3 path prefix root for achived files
        archivist.Archivist.setPrefixRoot('archive')

# create dict of download functions
dl_funs = {
        "dl_file": archivist.dl_file,
        "html_page": archivist.html_page,
        "ss_page": archivist.ss_page
}

# import final dataset list
ds = archivist.Archivist.ds

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
        
        ## if URL is not static, get URL
        if 'url' not in ds[key]:
                # try to get URL
                try:
                        # create local namespace
                        loc = {}
                        # execute url_fun_python, which returns the URL as url_current in the local namespace
                        url_current = exec(ds[key]['url_fun_python'], {}, loc)
                        ds[key]['url'] = loc['url_current']
                        print('Retrieved URL: ' + ds[key]['url']) # print result
                except Exception as e:
                        name_error = ds[key]['file_name'] + '_' + archivist.get_datetime('America/Toronto').strftime('%Y-%m-%d_%H-%M')
                        full_name_error = os.path.join(ds[key]['dir_parent'], ds[key]['dir_file'], name_error + '.' + ds[key]['file_ext']) 
                        archivist.Archivist.log = archivist.Archivist.log + 'Failure: ' + full_name_error + '\n'
                        print(e)
                        print(background('Failed to retrieve URL for dataset: ' + ds[key]['id_name'], Colors.red))
                        archivist.Archivist.recFailure(key)
                        continue
        
        ## print key
        print(ds[key]['id_name'])
        
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
        ### rand_url (dl_file)
        if 'rand_url' in ds[key]['args']:
                ds[key]['args']['rand_url'] = arg_bool('rand_url')
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
        ### js (html_page)
        if 'js' in ds[key]['args']:
                ds[key]['args']['js'] = arg_bool('js')
        ### wait (html_page, ss_page)
        if 'wait' in ds[key]['args']:
                ds[key]['args']['wait'] = arg_int('wait')
        ### width (html_page, ss_page)
        if 'width' in ds[key]['args']:
                ds[key]['args']['width'] = arg_int('width')
        ### height (html_page, ss_page)
        if 'height' in ds[key]['args']:
                ds[key]['args']['height'] = arg_int('height')
        
        # use dl_file instead of html_page for simple HTML pages (no JS)
        if dl_fun == archivist.html_page:
                if 'js' in ds[key]['args']:
                        if ds[key]['args']['js'] is False:
                                dl_fun = archivist.dl_file
                else:
                        dl_fun = archivist.dl_file

        ## filter out unwanted keywords
        ### verify is not used for html_page() but is used elsewhere
        if dl_fun == archivist.html_page:
                ds[key]['args'].pop('verify', None)

        ## run download function
        dl_fun(
                url = ds[key]['url'],
                dir_parent = ds[key]['dir_parent'],
                dir_file = ds[key]['dir_file'],
                file = ds[key]['file_name'],
                ext = ext,
                uuid = key,
                **ds[key]['args']
        )

# summarize successes and failures
archivist.print_success_failure()

# print rerun code, if necessary
if archivist.Archivist.failure > 0:
        print(background('\n' + archivist.generate_rerun_code(), (150, 150, 150)))
        print('') # newline

# assemble log entry
log = archivist.output_log(archivist.Archivist.log, t)

# upload and email log of file uploads, send notification (when mode == prod)
if archivist.Archivist.mode == 'prod':
        
        ## upload log
        archivist.upload_log(log)
        
        ## compose email message (current log entry)
        subject = " ".join(['PROD', 'Covid19CanadaArchive Log', t.strftime('%Y-%m-%d %H:%M') + ',', 'Failed:', str(archivist.Archivist.failure)])
        body = log        
        
        ## email log
        if archivist.Archivist.email:
                archivist.send_email(subject, body)
        
        ## send notification
        if archivist.Archivist.notify:
                notif = 'Success: ' + str(archivist.Archivist.success) + '\nFailure: ' + str(archivist.Archivist.failure)
                archivist.pushover(notif, priority=1, title = 'Archive update completed')

# email log of failed downloads, if any (when mode == test)
if archivist.Archivist.mode == 'test':
        
        ## email log if there are any failures
        if archivist.Archivist.failure > 0:
                
                ## compose email message (current log entry)
                subject = " ".join(['TEST', 'Covid19CanadaArchive Log', t.strftime('%Y-%m-%d %H:%M') + ',', 'Failed:', str(archivist.Archivist.failure)])
                body = log
                if archivist.Archivist.email:
                        archivist.send_email(subject, body)
        else:

                ## inform user that log will not be sent as there were no errors
                print("No errors detected during test run. Log will not be sent.")
