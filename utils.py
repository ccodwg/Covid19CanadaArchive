# utils.py: Utility functions for the Canadian COVID-19 Data Archive #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# import modules from Python standard library
import sys
import json
import collections

### gen_readme: Generate README.md (from datasets.json & docs/README_content.md) ###
def gen_readme():
  
  ## function: process metadata into list entries
  def meta_items(ds, txt):
    # generic archive index link
    archive_link = 'https://ccodwg.github.io/Covid19CanadaArchive-data-explorer/'
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

  ## import modules
  import pandas as pd
  import archivist
  
  ## load active datasets and extract UUIDs as list
  with open('datasets.json') as json_file:
    datasets = json.load(json_file)
  datasets = datasets['active'] # subset active datasets
  uuids = [] # create empty list
  for d in datasets:
          for i in range(len(datasets[d])):
                  uuids.append(datasets[d][i]['uuid'])
  
  ## download file index
  ind = pd.read_csv("http://data.opencovid.ca.s3-us-east-2.amazonaws.com/archive/file_index.csv")

  ## filter out datasets already marked as inactive
  ind = ind[ind['uuid'].isin(uuids)]
  
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
  
### retire_dataset: Move dataset from 'active' to 'inactive'
def retire_dataset(uuid):

  # load datasets.json
  with open('datasets.json') as json_file:
    datasets = json.load(json_file)
  
  # find location of dataset
  i_uuid = None
  k_uuid = None
  for k in datasets['active'].keys():
    for i in range(len(datasets['active'][k])):
      u = datasets['active'][k][i]['uuid']
      if u == uuid:
        i_uuid = i
        k_uuid = k
        break
    else:
      continue
    break

  # stop if no matching active dataset found
  if i_uuid is None:
    print('No matching active dataset found with that UUID.')
    return

  # copy dataset
  d = datasets['active'][k][i]
  
  # add inactive flag
  d['active'] = 'False'

  # remove dataset from active
  datasets['active'][k].pop(i)

  # append dataset to inactive
  datasets['inactive'][k].append(d)

  # write datasets.json
  with open('datasets.json', 'w') as json_file:
    json.dump(datasets, json_file, indent=2, ensure_ascii=False)

# run utility functions from command line by calling them by name
if __name__ == '__main__':
  # no positional argument
  if len(sys.argv) == 2:
    globals()[sys.argv[1]]()
  # one positional argument
  elif len(sys.argv) == 3:
    globals()[sys.argv[1]](sys.argv[2])
  else:
    print("This method only accepts at most one positional argument.")
