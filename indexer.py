# indexer.py: Index files included in the covid-19-canada-gov-data archive #
# https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data #
# Maintainer: Jean-Paul R. Soucy #

# import modules
print('Importing modules...')

## archivist.py
import archivist

# list of environmental variables used in this script (through functions in archivist.py)
## GD_KEY: environmental variable of Google Drive credentials as a simple string (used when mode = server)
## GH_TOKEN: personal access token for the GitHub API (used when mode = server)
## GH_NAME: name to use for GitHub commits (used when mode = server)
## GH_MAIL: email address to use for GitHub commits (used when mode = server)

# create index
index = archivist.create_index()

# write index to CSV
archivist.write_index(index)