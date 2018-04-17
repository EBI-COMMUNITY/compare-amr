from val import val
from sra_objects import analysis_amr
from sra_objects import analysis_file
from sra_objects import submission
import sys
import os
import glob
import shutil
import argparse
import hashlib
from ftper import ftper
from amrcurl import amrcurl



def build_dir(rows):

	new_dirs = []
	if rows.error_detect:
		print "%s rows have an error. removing temporary files and exiting ..."%str(rows.error_detect) #temporary files are from val.get_antibiogram_data()
#		for f in glob.glob("*"+month):
#			os.remove(f)

		for prefix in rows.files_created:
			expectedfname = prefix + ".txt"
			try:
				os.remove(expectedfname)
			except OSError as e:
				print "trouble removing %s. Exiting without continuing."%expectedfname
				print e
				sys.exit(0)

def validate_header(header_line):
	values =header_line.strip().lower().split("\t")
	header_len=len(values)
	exit=1
	print values
	if header_len <10:
		print "ERORR: The header of the file (line number 0) has less number of column than the minimum accepted column (10).\nIt is possible that your file is not a tab delimited file (tsv)"
		exit=0
	
	if "biosample_id" not in values:
		print "ERROR: biosample_id column is missing."
		exit=0
	if "species" not in values:
		print "ERROR: species column is missing."
		exit=0
	if "antibiotic_name" not in values:
		print "ERROR: antibiotic_name column is missing."
		exit=0
	if "ast_standard" not in values:
		print "ERROR: ast_standard column is missing."
		exit=0
	if "breakpoint_version" not in values:
		print "ERROR: breakpoint_version column is missing."
		exit=0
	if "laboratory_typing_method" not in values:
		print "ERROR: laboratory_typing_method column is missing."
		exit=0
	if "measurement" not in values:
		print "ERROR: measurement column is missing."
		exit=0
	if "measurement_units" not in values:
		print "ERROR: measurement_units column is missing."
		exit=0
	if "measurement_sign" not in values:
		print "ERROR: measurement_sign column is missing."
		exit=0
	if "resistance_phenotype" not in values:
		print "ERROR: resistance_phenotype column is missing."
		exit=0
		
	if exit==0:
		print "Validator has been exited because of above error(s) and has't been proceeded to rest of validation"
		sys.exit(0)
				
	else:
		for prefix in rows.files_created:
			directoryname= prefix
			expectedfname= prefix + ".txt"
			try:
				os.makedirs(directoryname)
			except OSError as e:
				print "trouble creating a directory called %s. Exiting without continuing"%directoryname
				print e
				sys.exit(0)
			try:
				shutil.move(expectedfname,directoryname)
			except IOError as e:
				print "trouble moving file %s to directory %s. Exiting without continuing"%(expectedfname,directoryname)
				print e
				sys.exit(0)


			
	return


def make_xml(rows):

	xml_name="all_anal" + rows.month + ".xml"
	xml_name_sub="all_anal_sub" + rows.month + ".xml"
	all_anal=analysis_amr("temp",rows.args.center,"temp",rows.args.study,list(),"temp","temp",xml_name) 
	sub=submission("all_anal_sub" + rows.month,rows.args.center,"ADD",xml_name_sub,xml_name,"analysis")
	sub.build_submission()
	all_anal.build_set() 
	for d in rows.files_created:
		sample_accession= d.split('_')[0]
		analysis_files=list()
		root_analysis_files=list()
		filename= d + ".txt"
		filename_full= d + "/" + d + ".txt"
		try:
			file_md5= hashlib.md5(open(filename_full, 'rb').read()).hexdigest()
		except:
			print "trouble opening and creating md5sum for file %s. Exiting without continuing"%filename_full
			print str(sys.exc_info()[1])
			sys.exit(0)

		file_detail= analysis_file(filename,'tab',file_md5)
		root_file_detail= analysis_file(filename_full,'tab',file_md5) 
		analysis_files.append(file_detail)
		root_analysis_files.append(root_file_detail) 
		title= "Antibiogram for study %s, sample %s"%(rows.args.study,sample_accession)
		analysis_xml_relative= d + ".xml"
		analysis_xml= d + "/" + d + ".xml"
		submission_xml= d + "/submission_" + d + ".xml"
		anal = analysis_amr(d,rows.args.center,sample_accession,rows.args.study,analysis_files,title,title,analysis_xml)
#		anal.build_analysis()
		anal.build_set()
		anal.build_anal()
		anal.write_anal() # these must happen in this order. no check in place yet
		lsub=submission("submission_" + d,rows.args.center,"ADD",submission_xml,analysis_xml_relative,"analysis")
		lsub.build_submission()
		all_anal.next_el(d,sample_accession,root_analysis_files,title,title)
		all_anal.build_anal()



	all_anal.write_anal() 
	return [xml_name_sub,xml_name]


def get_args():

	parser = argparse.ArgumentParser(description='Script for validating AMR antibiograms and optionally submitting them to public repository ENA')
	parser.add_argument ('-f','--filename',type=str, help='Please provide the name of AMR antibiogram file')
#	parser.add_argument('-p', '--properties_file', type=str, help='Please provide the properties file that is required by SELECTA system', required=False)
	parser.add_argument('-m', '--mode', type=str, help='Options for mode are validate/submit', choices=["validate","submit"], nargs='?', required=False)
	parser.add_argument('-u', '--user_name', type=str, help='Please provide a username if you are using submit mode. Looks like Webin-XXX', required=False)
	parser.add_argument('-p', '--password', type=str, help='Please provide a password if you are using submit mode.', required=False)
       	parser.add_argument('-c', '--center', type=str, help='Please provide the centre name for your Webin account if you are using submit mode.', required=False)
       	parser.add_argument('-s', '--study', type=str, help='Please provide the study id (looks like PRJEBXXX) to add the antibiograms to if you are using submit mode.', required=False)
       	parser.add_argument('-t', '--test', action='store_true', help='If you are using the submit flag, this option will send the submission to the test server. To submit to the production server leave this option out', required=False)


	args=parser.parse_args()
	if args.mode is None:
		args.mode = "validate"

	if args.mode == "submit" :
		if not args.user_name or not args.password or not args.center or not args.study:
			print "if using submit mode you must provide: Webin account username, password and center name. As well as a valid study id"
			parser.print_help()
			sys.exit()
	return args



# NOTE: all submissions have ROLLBACK for testing (remove line 88 & 89 in sra_objects.py for actual submission)
# NOTE: URL in amrcurl is set to TEST server for testing (change line 12 in amrcurl.py for submission to production)

if __name__ == '__main__':
	
	args = get_args()
	antibiograms=val(args)
	if args.mode == "submit":
		build_dir(antibiograms)
		all_sub=make_xml(antibiograms) #all_sub[0] = submission xml, all_sub[1] = analysis xml
		ftper=ftper(antibiograms.files_created,args.user_name,args.password)
		crl=amrcurl(all_sub[0],all_sub[1],args.user_name,args.password,args.test)
