# indexer.py: Index files included in Covid19CanadaArchive #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# import modules
print('Importing modules...')

## archivist.py
import archivist

# list of environmental variables used in this script (through functions in archivist.py)
## AWS_ID: environmental variable of AWS ID
## AWS_KEY: environmental variable of AWS key

# load AWS credentials
archivist.aws_id = os.environ['AWS_ID']
archivist.aws_key = os.environ['AWS_KEY']

## access S3
archivist.s3 = archivist.access_s3(bucket='data.opencovid.ca')
        
## set S3 path prefix for achived files
archivist.prefix_root = 'archive'

# create index
index = archivist.create_index(
  url_base='https://s3.us-east-2.amazonaws.com/data.opencovid.ca/',
  inventory='/data.opencovid.ca/archive/data/')

# write index to CSV
archivist.write_index(index)
