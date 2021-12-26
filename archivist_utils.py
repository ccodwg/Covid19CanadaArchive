# archivist_utils.py: Utility functions for Covid19CanadaArchive #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# import modules
print('Importing modules...')

## core utilities
import sys
import os
import json
import collections

## other utilities
import pandas as pd

## email
import smtplib

# define functions

### send_email: Send an email ###
def send_email(subject, body):
    """Send email (e.g., a download log).
    
    Parameters:
    subject (str): Subject line for the email.
    body (str): Body of the email.
    """
    
    ## load email configuration
    mail_name = os.environ['MAIL_NAME'] # email account the message will be sent from
    mail_pass = os.environ['MAIL_PASS'] # email password for the account the message will be sent from
    mail_to = os.environ['MAIL_TO'] # email the message will be sent to
    mail_sender = (os.environ['MAIL_ALIAS'] if 'MAIL_ALIAS' in os.environ.keys() else os.environ['MAIL_NAME']) # the listed sender of the email (either the mail_name or an alias email)
    smtp_server = os.environ['SMTP_SERVER'] # SMTP server address
    smtp_port = int(os.environ['SMTP_PORT']) # SMTP server port
    
    ## compose message
    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (mail_sender, mail_to, subject, body)
    
    ## send message
    try:
        print('Sending message...')
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.ehlo()
        server.login(mail_name, mail_pass)
        server.sendmail(mail_sender, mail_to, email_text)
        server.close()
        print('Message sent!')
    except Exception as e:
        print(e)
        print('Message failed to send.')

### gen_readme: Generate README.md (from datasets.json & docs/README_content.md) ###
def gen_readme():
  
  ## function: process metadata into list entries
  def meta_items(ds, txt):
    # generic archive index link
    archive_link = 'http://data.opencovid.ca/archive/index.html#archive/'
    # processing
    urls = list({d: ds[d]['metadata']['meta_url'] for d in ds}.values())
    urls = list(dict.fromkeys(urls)) # remove duplicates
    for url in urls:
      # get list items
      items = {k:ds[k] for k in ds.keys() if ds[k]['metadata']['meta_url'] == url}
      # get url name from first entry
      url_name = items[list(items)[0]]['metadata']['meta_url_name']
      # write URL and URL name
      txt = txt + '* [' + url_name + ']' + '(' + url + ')\n'
      # write list items
      for k in items.keys():
        txt = txt + '    * ' + items[k]['metadata']['meta_name'] + ': ' + \
        '[' + ds[k]['dir_parent'] + '/' + ds[k]['dir_file'] + '/' + \
        ds[k]['file_name'] + '.' + ds[k]['file_ext'] + ']' + \
        '(' + archive_link + ')'
        # if applicable, add inactive dataset flag
        if (items[k]['active'] == 'False'):
          txt = txt + ' [inactive, no longer updated]'
        # line break
        txt = txt + '\n'
    return(txt)
  
  ## load datasets.json
  with open('datasets.json') as json_file:
          datasets = json.load(json_file)
  
  ## note dataset attributes to verify uniqueness
  uuids = []
  dirs = []
  
  ## flatten datasets into single dictionary
  ds = {} # create empty dictionary
  for a in datasets:
    for b in datasets[a]:
      for i in range(len(datasets[a][b])):
        uuids.append(datasets[a][b][i]['uuid'])
        dirs.append('/'.join([datasets[a][b][i]['dir_parent'], datasets[a][b][i]['dir_file']]))
        ds[datasets[a][b][i]['uuid']] = datasets[a][b][i]
  
  ## verify uniqueness of UUID and directories, otherwise throw error
  dup_uuids = [item for item, count in collections.Counter(uuids).items() if count > 1]
  if len(dup_uuids) > 0:
    sys.exit("There are duplicated UUIDs: " + ", ".join(dup_uuids))
  else:
    print("All UUIDs are unique.")
  dup_dirs = [item for item, count in collections.Counter(dirs).items() if count > 1]
  if len(dup_dirs) > 0:
    sys.exit("There are duplicated diectories: " + ", ".join(dup_dirs))
  else:
    print("All directories are unique.")
  
  ## initialize dataset list
  print("Generating README...")
  txt = ""
  
  ## get all unique values for top-level groups (meta_group_1) and sort alphabetically
  g1 = list({ds[d]['metadata']['meta_group_1'] for d in ds})
  g1.remove('Other: Non-governmental sources')
  g1.sort()
  g1.append('Other: Non-governmental sources') # ensure this entry is at the end
  
  ## loop through all top-level groups
  for g in g1:
    ## header for top-level group
    txt = txt + '<details>\n<summary><b>' + g + '</b></summary>\n\n'
    ## subset data
    dg = {k:ds[k] for k in ds.keys() if ds[k]['metadata']['meta_group_1'] == g}
    ## check for sub-groups
    g2 = list({dg[d]['metadata'].get('meta_group_2') for d in dg}) # meta_group_2 only exists if it has a value
    if None in g2: g2.remove(None) # remove None
    ## process data without sub-groups
    dtop = {k:dg[k] for k in dg.keys() if dg[k]['metadata'].get('meta_group_2') is None}
    txt = meta_items(dtop, txt)
    ## process data with sub-groups (if they exist)
    if len(g2) != 0:
      g2.sort() # alphabetical order
      for h in g2:
        txt = txt + '\n<details>\n<summary><i>' + h + '</i></summary>\n\n'
        dh = {k:dg[k] for k in dg.keys() if dg[k]['metadata'].get('meta_group_2') == h}
        txt = meta_items(dh, txt)
        txt = txt + '</details>\n'
    ## add line break and close <details> tag
    txt = txt + '</details>\n'
  
  ## load README_content.md
  with open('docs/README_content.md', 'r') as text_file:
    content = text_file.read()
  
  ## add in data catalogue
  readme = content.replace('[INSERT DATA CATALOGUE HERE]', txt)
  
  ## write complete README.md
  with open('README.md', 'w') as f:
      f.write(readme)

### list_inactive_datasets: List datasets that have not been updated in at least 7 days ###
def list_inactive_datasets():
  
  ## download file index
  ind = pd.read_csv("http://data.opencovid.ca.s3-us-east-2.amazonaws.com/archive/file_index.csv")
  
  ## filter to longest consecutive sequence of duplicates starting from the bottom for each UUID
  ind = ind[['dir_parent', 'dir_file', 'uuid', 'file_etag_duplicate']] # subset to relevant columns
  ind['name'] = ind['dir_parent'] + '/' + ind['dir_file']
  ind = ind[['name', 'uuid', 'file_etag_duplicate']]
  ind = ind.reindex(index=ind.index[::-1]) # reverse order
  ind['dup'] = ind['file_etag_duplicate'] == 0
  ind['dup'] = ind['dup'].astype(int)
  ind['dup'] = ind.groupby(['name', 'uuid'])['dup'].cumsum()
  ind = ind.query('dup == 0')
  ind = ind.groupby(['name', 'uuid']).size().to_frame().reset_index()
  ind.columns = ['name', 'uuid', 'count']
  ind = ind.query('count >= 7').sort_values(by='count', ascending=False)
  
  ## save result
  log = ind.to_string(index=False)
  
  ## print result
  print(log)
  
  ## compose email message
  subject = 'Covid19CanadaArchive Inactive Datasets'
  body = log
  
  ## email message
  send_email(subject, body)

# run utility functions from command line by calling them by name
if __name__ == '__main__':
    globals()[sys.argv[1]]()
