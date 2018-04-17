from ftplib import FTP
import sys

class ftper:

    def __init__(self,file_list,u_name,p_word):

        self.pref=file_list
        self.ftp= FTP('webin.ebi.ac.uk',u_name,p_word)
        self.contents=self.list()
        self.make_remote_d()
        self.quit()

    def make_remote_d(self):

        for prefix in self.pref:
            file_name = prefix + '/' + prefix + '.txt'
            xml_name =  prefix + '/' + prefix + '.xml'
            xml_sub = prefix + '/submission_' + prefix + '.xml'
            if prefix in self.contents:
                print "making remote directory '%s' but there is already a remote directory (or file) with this name"%prefix
                print "exiting program"
                self.quit()
                sys.exit()
            try:
                upload_file = open(file_name,'r')
                upload_xml = open(xml_name,'r')
                upload_sub = open(xml_sub,'r')
                self.ftp.mkd(prefix)
                self.ftp.storbinary('STOR ' + file_name, upload_file )
                self.ftp.storbinary('STOR ' + xml_name, upload_xml )
                self.ftp.storbinary('STOR ' + xml_sub, upload_sub )
            except:
                print "problem reading local file %s and %s and %s and then storing remote file %s and %s and %s" % (file_name,xml_name,xml_sub,file_name,xml_name,xml_sub)
                str(sys.exc_info()[1])
                sys.exit(0)


    def list(self):

        try:
            file_listing=self.ftp.nlst()
        except:
            print "trouble loading remote file list"
            print str(sys.exc_info()[1])
        return file_listing

    def quit(self):
        self.ftp.quit()
