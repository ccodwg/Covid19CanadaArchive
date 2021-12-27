# indexer.py: Update file index for the Canadian COVID-19 Data Archive #
# https://github.com/ccodwg/Covid19CanadaArchive #
# Maintainer: Jean-Paul R. Soucy #

# import modules
print('Importing modules...')

## core utilities
import os

## archivist
import archivist

# list of environmental variables used in this script (through functions in archivist)
## AWS_ID: environmental variable of AWS ID
## AWS_KEY: environmental variable of AWS key

# load AWS credentials
aws_id = os.environ['AWS_ID']
aws_key = os.environ['AWS_KEY']

## access S3
archivist.Archivist.setS3(archivist.access_s3(
  bucket='data.opencovid.ca',
  aws_id=aws_id,
  aws_key=aws_key))

## set S3 path prefix for achived files
archivist.Archivist.setPrefixRoot('archive')

# create index
ind = archivist.create_index(
  url_base='https://s3.us-east-2.amazonaws.com/data.opencovid.ca/',
  bucket='data.opencovid.ca',
  aws_id=aws_id,
  aws_key=aws_key)

# write index to S3
archivist.write_index(ind)
