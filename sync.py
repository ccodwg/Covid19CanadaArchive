# sync.py: Sync to local directory files from Google Drive in Covid19CanadaArchive using rclone #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# Note: This script requires that rclone already be configured locally to interface with Google Drive #
# The root directory of the rclone remote should be the root directory of the archive on Google Drive #

# import modules
print('Importing modules...')

## core utilities
import sys
import os

# read local directory from script argument
if (len(sys.argv) !=3 ):
    sys.exit('Error: Please provide arguments of the form: dir_remote dir_local.')
else:
    dir_remote = sys.argv[1]
    dir_local = sys.argv[2]

# rclone remote to local directory
cmd = 'rclone copy ' + dir_remote + ' ' + dir_local + ' --verbose'
os.system(cmd)