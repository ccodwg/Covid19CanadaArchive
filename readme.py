# readme.py: Assemble README.md for Covid19CanadaArchive #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# import modules
print('Importing modules...')

## core utilities
import json
import collections

### CREATE DATA CATALOGUE FROM METADATA STORED IN DATASETS.JSON ###

# define functions

## process metadata into list entries
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

# load datasets.json
with open('datasets.json') as json_file:
        datasets = json.load(json_file)

# note dataset attributes to verify uniqueness
uuids = []
dirs = []

# flatten datasets into single dictionary
ds = {} # create empty dictionary
for a in datasets:
  for b in datasets[a]:
    for i in range(len(datasets[a][b])):
      uuids.append(datasets[a][b][i]['uuid'])
      dirs.append('/'.join([datasets[a][b][i]['dir_parent'], datasets[a][b][i]['dir_file']]))
      ds[datasets[a][b][i]['uuid']] = datasets[a][b][i]

# verify uniqueness of UUID and directories, otherwise throw error
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

# initialize dataset list
print("Generating README...")
txt = ""

# get all unique values for top-level groups (meta_group_1) and sort alphabetically
g1 = list({ds[d]['metadata']['meta_group_1'] for d in ds})
g1.remove('Other: Non-governmental sources')
g1.sort()
g1.append('Other: Non-governmental sources') # ensure this entry is at the end

# loop through all top-level groups
for g in g1:
  ## header for top-level group
  txt = txt + '### ' + g + '\n\n'
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
      txt = txt + '\n#### ' + h + '\n\n'
      dh = {k:dg[k] for k in dg.keys() if dg[k]['metadata'].get('meta_group_2') == h}
      txt = meta_items(dh, txt)
  ## add line break
  txt = txt + '\n'

### ASSEMBLE README.MD ###

# load README_content.md
with open('docs/README_content.md', 'r') as text_file:
  content = text_file.read()

# add in data catalogue
readme = content.replace('[INSERT DATA CATALOGUE HERE]', txt)

# write complete README.md
with open('README.md', 'w') as f:
    f.write(readme)
