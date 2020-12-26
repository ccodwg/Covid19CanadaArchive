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

# set mode from argv (server vs. local and prod vs. test)
archivist.set_mode()

# access Google Drive
if archivist.mode == 'serverprod' or archivist.mode == 'localprod':
    ## access Google Drive
    archivist.drive = archivist.access_gd()

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

# create index
index = archivist.create_index()

# write index to CSV
archivist.write_index(index)