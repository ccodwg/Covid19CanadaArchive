# utils.py: Utility functions for the Canadian COVID-19 Data Archive #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# import modules from Python standard library
import sys
import json
import tempfile
import requests
import sqlite3

### list_inactive_datasets: List datasets that have not been updated in at least 7 days ###
def list_inactive_datasets():

  ## import modules
  import pandas as pd
  
  ## load active datasets and extract active UUIDs as list
  with open('datasets.json') as json_file:
    datasets = json.load(json_file)
  datasets = datasets['active'] # subset active datasets
  ds = {}
  for d in datasets:
    for i in range(len(datasets[d])):
      ds[datasets[d][i]["uuid"]] = datasets[d][i]
  
  ## download file index and read into dataframe
  no_cache_headers = {"Cache-Control": "no-cache", "Pragma": "no-cache"}
  temp = tempfile.NamedTemporaryFile()
  with open(temp.name, "wb") as f:
    f.write(requests.get("https://data.opencovid.ca/archive/index.db", headers = no_cache_headers).content)
    ind = pd.read_sql("SELECT * FROM archive", sqlite3.connect(temp.name))

  ## filter out datasets already marked as inactive
  ind = ind[ind['uuid'].isin(ds.keys())]

  ## filter to final file from each date
  ind["file_final_for_date"] = ind.groupby(["uuid", "file_date"])["file_timestamp"].transform(max) == ind["file_timestamp"]
  ind = ind[ind["file_final_for_date"] == True]

  ## join datasets metadata
  datasets_meta = pd.DataFrame.from_dict(ds, orient = "index")[["uuid", "dir_parent", "dir_file"]]
  ind = pd.merge(ind, datasets_meta, on = "uuid", how = "left")
  
  ## filter to longest consecutive sequence of duplicates starting from the bottom for each UUID
  ind = ind[['dir_parent', 'dir_file', 'uuid', 'file_duplicate']] # subset to relevant columns
  ind['name'] = ind['dir_parent'] + '/' + ind['dir_file']
  ind = ind[['name', 'uuid', 'file_duplicate']]
  ind = ind.reindex(index=ind.index[::-1]) # reverse order
  ind['dup'] = ind['file_duplicate'] == 0
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
