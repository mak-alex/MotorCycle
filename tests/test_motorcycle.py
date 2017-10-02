import sys, os
import unittest
testdir = os.path.dirname(__file__)
srcdir = '../src/'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
from MotorCycle import MotorCycle

credentials = {}
# Credentials for connect to DropBox
# In that case, if you are going to save the PDF files in Dropbox
credentials['dropbox'] = {
    'access_token': None,
    'app_key': 'INSERT YOUR APP_KEY',
    'app_secret': 'INSERT YOUR APP_SECRET'
}
# Credentials for connect to remote server
# In that case, if you are going to save the PDF files in remote server
credentials['remote_server'] = {
    'ip': 'localhost',
    'username': 'user',
    'password': 'pass'
}
# Create new instance, where arguments:
# website url, credentials dict, method for saving files
mc = MotorCycle('https://carlsalter.com/', credentials, 'local')


class TestStringMethods(unittest.TestCase):
    def test_get_list_manuals(self):
        # Getting a list of manufacturers and all links to the files for them
        mc.get_list_manuals('Adly')

        self.assertTrue(
            mc.manuals,
            'Something went wrong,' +
            ' I couldn\'t get a list of manufacturers and links to the files'
        )

if __name__ == '__main__':
    unittest.main()
