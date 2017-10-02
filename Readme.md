### MotorCycle - Script for downloading PDF files
 ![alt text](http://www.unixstickers.com/image/cache/data/stickers/python/python.sh-180x180.png)        ![alt text](http://www.pngmart.com/files/2/Ghost-Rider-Bike-PNG-Photos.png "carlsalter.com - PDF files")           
#### Description
Script for downloading PDF files from website carlsalter.com
#### Dependencies
  - requests - pip install requests --user (mandatory)
  - lxml - pip install lxml --user (mandatory)
  - argsparse - pip install argparse --user (mandatory)
  - dropbox - pip install dropbox --user (not required, need to work with a DropBox)
  - paramiko - pip install paramiki --user (not required, need to work with a remote server)
#### Usage
	usage: MotorCycle.py [-h] [--url URL] [-m METHO] [-f _FILTER]
	                     [--app app_key=YOUR_APP_KEY,app_secret=YOUR_APP_SECRET]
	                     [--remote ip=localhost,username=admin,password=password]
	                     [-v]
	
	Save all PDF from carlsalter.com
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --url URL             URL for download PDF files, default:
	                        https://carlsalter.com/
	  -m METHOD, --method METHOD
	                        Where to save: local/scp/dropbox
	  -f _FILTER, --filter _FILTER
	                        Filter string, ex.: Adly Service Manuals or first only
	                        word Adly
	  --app app_key=YOUR_APP_KEY,app_secret=YOUR_APP_SECRET
	                        DropBox auth, ex.: --app app_key='YOUR APP
	                        KEY',app_secret='YOUR APP SECRET'
	  --remote ip=localhost,username=admin,password=password
	                        Credentials including IP address of the remote server
	                        to save the PDF files, ex.: --remote
	                        ip=localhost,username=admin,password=password
	  -v, --verbose         increase output verbosity
