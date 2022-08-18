# utils.py: Utility functions for the Canadian COVID-19 Data Archive #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# import modules from Python standard library
import sys
import json

### list_inactive_datasets: List datasets that have not been updated in at least 7 days ###
def list_inactive_datasets():

  ## import modules
  import pandas as pd
  
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
