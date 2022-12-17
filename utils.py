# utils.py: Utility functions for the Canadian COVID-19 Data Archive #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# import modules from Python standard library
import sys
import json
import tempfile
import requests
import sqlite3

### list_inactive_datasets: List datasets that have not been updated for an unusually long time ###
def list_inactive_datasets():

  ## import modules
  import pandas as pd
  pd.options.mode.chained_assignment = None # disable chained assignment warning

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
  ind = ind[ind["uuid"].isin(ds.keys())]

  ## filter to final file from each date
  ind["file_final_for_date"] = ind.groupby(["uuid", "file_date"])["file_timestamp"].transform("max") == ind["file_timestamp"]
  ind = ind[ind["file_final_for_date"] == True]

  ## join datasets metadata
  datasets_meta = pd.DataFrame.from_dict(ds, orient = "index")[["uuid", "dir_parent", "dir_file"]]
  ind = pd.merge(ind, datasets_meta, on = "uuid", how = "left")

  ## order datasets by UUID and timestamp
  ind = ind.sort_values(by = ["uuid", "file_timestamp"]).reset_index(drop = True)

  ## add name column
  ind["name"] = ind["dir_parent"] + "/" + ind["dir_file"]

  ## list to hold results
  log = []

  ## for each UUID, calculate a cumulative sum for file_duplicate, resetting at each 0 (i.e., each new file)
  ## then, see if the current run of duplicates is longer than all previous runs of duplicates
  for uuid in ind["uuid"].unique():
    # filter data
    u = ind[ind["uuid"] == uuid]
    # calculate runs of 1s (i.e., consecutive duplicates)
    u["file_duplicate"] = u["file_duplicate"] != 0
    d = u["file_duplicate"]
    u["file_duplicate"] = d.cumsum()-d.cumsum().where(~d).ffill().fillna(0).astype(int)
    # get last value
    last = u["file_duplicate"].iloc[-1]
    # get max value excluding final run
    # filter to everything before final zero
    final_zero = u[u["file_duplicate"] == 0]
    if len(final_zero) == 0:
      # every entry but the first is a duplicate
      max = 0
    else:
      final_zero = final_zero.index[-1]
      ## filter to everything before final zero
      u = u[u.index.isin(range(final_zero))]
      max = u["file_duplicate"].max()
    # if last value is larger than max and at least 7, add to log
    if last > max and last >= 7:
      log.append([u["name"].iloc[-1], last, max])
  
  ## save result and sort
  log = pd.DataFrame(log, columns = ["name", "current_dup_run", "previous_max_dup_run"]).sort_values(by = ["current_dup_run", "name"], ascending = [False, True])
  log = log.to_string(index=False)
  
  ## print result
  print(log)
  
### retire_datasets: Move dataset(s) from 'active' to 'inactive'
def retire_datasets(uuids):

  # load datasets.json
  with open('datasets.json') as json_file:
    datasets = json.load(json_file)
  
  # loops through UUIDs
  for uuid in uuids:
    # find location of dataset
    i_uuid = None
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
      print('No matching active dataset found with UUID: ' + u)
    else:
      # copy dataset
      d = datasets['active'][k_uuid][i_uuid]
      
      # add inactive flag
      d['active'] = 'False'

      # remove dataset from active
      datasets['active'][k_uuid].pop(i_uuid)

      # append dataset to inactive
      datasets['inactive'][k_uuid].append(d)

  # write datasets.json
  with open('datasets.json', 'w') as json_file:
    json.dump(datasets, json_file, indent=2, ensure_ascii=False)

# run utility functions from command line by calling them by name
if __name__ == '__main__':
  # no positional argument
  if len(sys.argv) == 2:
    globals()[sys.argv[1]]()
  # one or more positional arguments
  elif len(sys.argv) > 2:
    globals()[sys.argv[1]](sys.argv[2:len(sys.argv)])
