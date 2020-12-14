# archivist.py: Helper functions for covid-19-canada-gov-data archive #
# https://github.com/jeanpaulrsoucy/covid-19-canada-gov-data #
# Maintainer: Jean-Paul R. Soucy #

# import modules

## core utilities
import os
import tempfile

## web scraping
from selenium import webdriver # requires ChromeDriver and Chromium/Chrome
from selenium.webdriver.chrome.options import Options

## Google Drive
from oauth2client import service_account
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# functions for Google Drive

def access_gd(mode):
    """Authenticate with Google Drive and return GoogleDrive object.
    
    Parameters:
    mode (str): One of 'serverprod', 'localprod', 'servertest', 'localtest'. Determines where the function looks for credentials.
        
    """
    print('Authenticating with Google Drive...')
    
    ## retrieve Google Drive credentials
    if mode == 'serverprod' or mode == 'servertest':
            gd_key_val = json.loads(os.environ['GD_KEY'], strict=False)
            tmpdir = tempfile.TemporaryDirectory()
            gd_key = os.path.join(tmpdir.name, ".gd_key.json")
            with open(gd_key, mode='w', encoding='utf-8') as local_file:
                    json.dump(gd_key_val, local_file, ensure_ascii=False, indent=4)
    elif mode == 'localprod' or mode == 'localtest':
            script_path = os.path.dirname(os.path.abspath(__file__))
            gd_key = os.path.join(script_path, ".gd", ".gd_key.json")                
    
    ## authenticate Google Drive access
    gauth = GoogleAuth()
    scope = ['https://www.googleapis.com/auth/drive']
    gauth.credentials = service_account.ServiceAccountCredentials.from_json_keyfile_name(gd_key, scope)
    
    ## initialize Goodle Drive object
    drive = GoogleDrive(gauth)
    
    ## confirm authentication was successful
    print('Authentication was successful.')    
    
    ## return Google Drive object
    return drive  

def create_http(drive):
    """Create httplib.Http() object for re-use when uploading using PyDrive.
    
    Parameters:
    drive: The GoogleDrive object for which to.
    
    See "Concurrent access made easy" at the following URL for why this may be useful: https://pypi.org/project/PyDrive/
    
    """
    ## create httplib.Http() object
    http = drive.auth.Get_Http_Object()
    
    ## return httplib.Http() object
    return(http)

# functions web scraping

def load_webdriver(mode, tmpdir):
    """Load Chromium headless webdriver for Selenium.

    Parameters:
    mode (str): One of serverprod, localprod, servertest, localtest. Defines how the webdriver is loaded.
    tmpdir (TemporaryDirectory): A temporary directory for saving files.

    """
    options = Options()
    if mode == 'serverprod' or mode == 'servertest':
        options.binary_location = os.environ['GOOGLE_CHROME_BIN']
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    prefs = {'download.default_directory' : tmpdir.name}
    options.add_experimental_option('prefs', prefs)
    if mode == 'serverprod' or mode == 'servertest':
        return webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_PATH'], options=options)
    else:
        return webdriver.Chrome(options=options)