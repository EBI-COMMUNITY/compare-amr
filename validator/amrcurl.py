import requests
import os.path
import sys

class amrcurl:

    def __init__(self,submission_xml,analysis_xml,account_id,password):

        self.submission_xml=self.check_file(submission_xml)
        self.analysis_xml=self.check_file(analysis_xml)
        self.url='https://www-test.ebi.ac.uk/ena/submit/drop-box/submit/?auth=ENA%20' + account_id + '%20' + password 
        self.post()


    def check_file(self, file):

        if os.path.isfile(file):
            return file
        else:
            print "could not find file %s required for sending request for submission. exiting ..."%file
            sys.exit()



    def post(self):
        
        files = [
            ('SUBMISSION', open(self.submission_xml, 'rb')),
            ('ANALYSIS', open(self.analysis_xml, 'rb')),
        ]
#        print self.url
        r = requests.post(self.url, files=files)
        print(r.text)
