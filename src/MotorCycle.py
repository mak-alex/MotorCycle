#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import requests
from lxml import html

__author__ = 'Alexandr Mikhailenko a.k.a Alex M.A.K.'
__version__ = '0.1.0'
__copyright__ = "Copyright 2017, Alex M.A.K."
__license__ = "GPL"
__email__ = "alex-m.a.k@yandex.kz"
__status__ = "Production"


class MotorCycle:
    '''
    Name:
        MotorCycle

    Description:
        Script for downloading PDF files from website carlsalter.com

    Dependencies:
        * requests - pip install requests --user (mandatory)
        * lxml - pip install lxml --user (mandatory)
        * argsparse - pip install argparse --user (mandatory)
        * dropbox - pip install dropbox --user (not required, need to work with a DropBox)
        * paramiko - pip install paramiko --user (not required, need to work with a remote server)

    Usage:
        MotorCycle.py [-h] [--url URL] [-m METHOD] [-f _FILTER]
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
    '''
    def __init__(self, url='https://carlsalter.com/', credentials=None, method='local', verbose=False):
        ''' Create new instance

        Save all PDF from carlsalter.com

        Keyword arguments:
        url - URL address for downloading PDF files (str)
        credentials - Dictionary with credentials including IP address and
         information to connect to DropBox (if needed) (dict)
        method - Method used to saved PDF files: local, scp, dropbox (str) (default: local)
        verbose - increase output verbosity (bool)
        '''
        self.url = url
        self.credentials = credentials
        self.method = method
        self.verbose = verbose

        self.manuals = []
        self.access_token = None

    def get_list_manuals(self, _filter=None):
        ''' To obtain a list of manufacturers and links

        Keyword arguments:
        _filter - Filter string for downloading only needed PDF files,
         ex.: Adly or Adly Service Manuals (str)
        return self.manuals - The data dictionary, the manufacturer,
         the file name, file reference (dict)
        '''
        if self.verbose is True:
            print('Getting a links to download the PDF file...please wait')

        if _filter is not None:
            try:
                _filter = _filter.split(' ')[0]
            except:
                pass

            if self.verbose is True:
                print('Set filter string: {}'.format(_filter))

        try:
            mm = requests.get(self.url + 'motorcycle-manuals.asp').text
        except requests.exceptions.Timeout:
            print(e)
            sys.exit(1)
        except requests.exceptions.TooManyRedirects:
            print(e)
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

        try:
            links = html.fromstring(mm).xpath('//div[@id=\'content\']')[0].xpath('//a')
        except:
            return '', ''

        if self.verbose is True:
            print('The generate list file upload...please wait')

        for link in links:
            name = link.text
            if name is not None and name.find('Manuals') >= 0:
                name_group = name.split(' ')[::-1][2]
                if (_filter and name_group.find(_filter) >= 0) or _filter is None:
                    for k,v in link.items():
                        self.manuals.append({
                            name_group: self.get_list_link(name_group, v)
                        })

        return self.manuals

    def get_list_link(self, n, l):
        '''Get link for PDF files.

        Keyword arguments:
        n - group name, ex.: Adly (["Adly", "Service", "Manuals"]), (str)
        l - link in PDF file
        return slinks - The data dictionary, the file name, file reference (dict)
        '''
        try:
            man = requests.get(self.url + l).text
        except requests.exceptions.Timeout:
            print(e)
            sys.exit(1)
        except requests.exceptions.TooManyRedirects:
            print(e)
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

        try:
            links = html.fromstring(man).xpath('//table')[0].xpath('//a')
        except:
            return '', ''

        slinks = []

        for link in links:
            name = link.text
            if name is not None:
                if name.find(n) >= 0 and isinstance(name, str):
                    slinks.append({
                        'name': name,
                        'link': self.url + '/pdfs/' + name + '.pdf'
                    })

        return slinks

    def download_pdf(self, dirname='/tmp'):
        '''Download PDF file.

        Download PDF file and save in the local pc
         or in the remote server, or in the DropBox

        Keyword arguments:
        dirname - The full path for the local saving of PDF files (str)
        '''
        if self.method is None:
            self.method = method

        for j in self.manuals:
            for k, v in j.items():
                for i in v:
                    name = '{}-{}.pdf'.format(k, i['name'])
                    if self.verbose is True:
                        print('Getting file: \'{}\', from the website: \'{}\''.format(name, self.url))

                    req = requests.get(i['link'], stream=True)
                    if self.method == 'dropbox':
                        try:
                            import dropbox
                        except:
                            print('[Warning!] dropbox module is not found,'
                                  'this method not work, please install module'
                                  '`pip install dropbox --user` for use this method')
                            sys.exit(-1)

                        if self.credentials['dropbox']['access_token'] is None:
                            app_key = self.credentials['dropbox']['app_key']
                            app_secret = self.credentials['dropbox']['app_secret']
                            flow = dropbox.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
                            authorize_url = flow.start()
                            print('1. Go to: {}\n2. Click "Allow" (you might have to log in first)'
                                  .format(authorize_url))

                            try:
                                code = raw_input("3. Enter the authorization code here: ").strip()
                            except:
                                code = input("3. Enter the authorization code here: ").strip()

                            self.credentials['dropbox']['access_token'], user_id = flow.finish(code)

                        dbx = dropbox.Dropbox(self.credentials['dropbox']['access_token'])
                        try:
                            dbx.files_upload(req.raw.read(),'/Books/'+name,mute=True)
                        except Exception as e:
                            print('Cannot save file: {} in Dropbox. Error: {}'.format(name, e))

                        if self.verbose is True:
                            print('Saving a PDF file: \'{}\', on the DropBox'.format(name))

                    elif self.method == 'scp':
                        try:
                            import paramiko
                        except:
                            print('[Warning!] paramiko module is not found,'
                                  'this method not work, please install module'
                                  '`pip install paramiko --user` for use this method')
                            sys.exit(-1)

                        def put_file(dirname, filename, data):
                            ssh = paramiko.SSHClient()
                            ssh.load_host_keys("~/.ssh/known_hosts")
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            my_key = paramiko.RSAKey.from_private_key_file("~/.ssh/id_rsa")
                            try:
                                ssh.connect(hostname=self.credentials['remote_server']['ip'],
                                            username=self.credentials['remote_server']['username'],
                                            pkey=my_key)
                            except:
                                ssh.connect(hostname=self.credentials['remote_server']['ip'],
                                            username=self.credentials['remote_server']['username'],
                                            password=self.credentials['remote_server']['password'])
                            sftp = ssh.open_sftp()

                            try:
                                sftp.mkdir(dirname)
                            except IOError:
                                pass

                            f = sftp.open(dirname + '/' + filename, 'w')
                            f.write(data)
                            f.close()
                            ssh.close()

                        if self.verbose is True:
                            print('Saving a PDF file: \'{}\', on the remote server: \'{}\''
                              .format(name, self.credentials['remote_server']['ip']))

                        put_file(dirname, name, req.raw.read())
                    else:
                        if self.verbose is True:
                            print('Saving a PDF file: \'{}\', on the local machine'.format(name))

                        with(open(dirname + '/' + name, 'ab')) as f:
                            for chunk in req.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)


if __name__ == '__main__':
    try:
        import argparse

        class StoreDictKeyPair(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                args_dict = {}
                for kv in values.split(","):
                    k,v = kv.split("=")
                    args_dict[k] = v

                setattr(namespace, self.dest, args_dict)
    except:
        print('[Warning!] argparse module is not found,'
                'this method not work, please install module'
                '`pip install argparse --user` for use this method')
        sys.exit(-1)

    parser = argparse.ArgumentParser(description='Save all PDF from carlsalter.com')
    parser.add_argument('--url', dest='url',
        help='URL for download PDF files, default: https://carlsalter.com/', default='https://carlsalter.com/')
    parser.add_argument('-m', '--method', dest='method',
        help='Where to save: local/scp/dropbox', default='local')
    parser.add_argument('-f', '--filter', dest='_filter',
        help='Filter string, ex.: Adly Service Manuals or first only word Adly')
    parser.add_argument('--app', dest='app', action=StoreDictKeyPair,
        metavar="app_key=YOUR_APP_KEY,app_secret=YOUR_APP_SECRET",
                        help='DropBox auth, ex.: --app app_key=\'YOUR APP KEY\',app_secret=\'YOUR APP SECRET\'',
    )
    parser.add_argument('--remote', dest='remote', action=StoreDictKeyPair,
        metavar='ip=localhost,username=admin,password=password',
        help='Credentials including IP address of the remote server'
        ' to save the PDF files, ex.: --remote ip=localhost,username=admin,password=password')
    parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')

    args = parser.parse_args()

    try:
        credentials = {}
        if args.method == 'dropbox':
            credentials['dropbox'] = {
                'access_token': 'pzTH_pckjxAAAAAAAAAAEUcna9JwbEduqyGMUjouIoc-bgmzm9tDurGC7G2-qqtc',
                'app_key': None,
                'app_secret': None
            }
            if args.app is not None:
                if 'app_key' in args.app:
                    credentials['app_key'] = args.app['app_key'],
                if 'app_secret' in args.app:
                    credentials['app_secret'] = args.app['app_secret']

        elif args.method == 'scp':
            if args.remote is not None:
                if not 'ip' in args.remote:
                    print('Please add the `ip\' address for remote server and try again')
                    sys.exit(-1)
                if not 'username' in args.remote:
                    print('Please add the `username\' for remote server and try again')
                    sys.exit(-1)
                if not 'password' in args.remote:
                    print('Please add the `password\' for remote server and try again')
                    sys.exit(-1)
            else:
                print('Please add the `ip\', `username\' and `password\''
                      ' for connect to remote server and try again')
                sys.exit(-1)

            credentials['remote_server'] = {
                'ip': args.remote['ip'],
                'username': args.remote['username'],
                'password': args.remote['password']
            }

        # Create new instance, where arguments:
        # website url, credentials dict, method for saving files
        mc = MotorCycle(args.url, credentials, args.method, args.verbose)
        # Getting a list of manufacturers and all links to the files for them
        mc.get_list_manuals(args._filter)
        # Save all locally/remotely/dropbox depends on user selection
        mc.download_pdf()
    except KeyboardInterrupt:
        print('You interrupted program execution, see you soon ;-)')
        sys.exit(1)
