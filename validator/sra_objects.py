from lxml import etree
import lxml.builder 

#sudo pip install --upgrade setuptools
#wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python
#sudo pip install lxml

class analysis_amr:
	
	
	def __init__(self,alias,centre_name,sample_accession,study_accession,analysis_files,title,description,analysis_xml_file):
		self.alias=alias
		self.analysis_xml_file=analysis_xml_file
		#self.analysis_centre=analysis_centre
		self.centre_name=centre_name
                self.sample_accession=sample_accession
		self.study_accession=study_accession
		self.analysis_files=analysis_files
		self.title=title
		self.description=description
		
	def next_el(self, next_alias, next_samp_acc, next_files, next_title, next_desc):
		self.alias=next_alias
                self.sample_accession=next_samp_acc
		self.analysis_files=next_files
		self.title=next_title
		self.description=next_desc

	def build_set(self):
		self.analysis_set = etree.Element('ANALYSIS_SET')
		self.analysis_xml = etree.ElementTree(self.analysis_set)
		
	def build_anal(self):
		analysisElt = etree.SubElement(self.analysis_set, 'ANALYSIS', alias=self.alias , center_name=self.centre_name)

		title = etree.SubElement(analysisElt, 'TITLE')
		title.text = self.title
		description = etree.SubElement(analysisElt, 'DESCRIPTION')
		description.text = self.description
		studyrefElt = etree.SubElement(analysisElt, 'STUDY_REF', accession=self.study_accession)
		samplerefElt = etree.SubElement(analysisElt, 'SAMPLE_REF', accession=self.sample_accession)
		analysis_type = etree.SubElement(analysisElt, 'ANALYSIS_TYPE')
		type = etree.SubElement(analysis_type, 'AMR_ANTIBIOGRAM')
		files = etree.SubElement(analysisElt, 'FILES')
		file1Elt = etree.SubElement(files,'FILE', filename=self.analysis_files[0].file_name,filetype=self.analysis_files[0].file_type,checksum_method="MD5", checksum=self.analysis_files[0].file_md5)

	def write_anal(self):
		self.analysis_xml.write(self.analysis_xml_file,pretty_print=True,xml_declaration = True, encoding='UTF-8')

	def build_analysis(self): #to be deleted
		analysis_set = etree.Element('ANALYSIS_SET')
		analysis_xml = etree.ElementTree(analysis_set)
		analysisElt = etree.SubElement(analysis_set, 'ANALYSIS', alias=self.alias , center_name=self.centre_name)
		title = etree.SubElement(analysisElt, 'TITLE')
		title.text = self.title
		description = etree.SubElement(analysisElt, 'DESCRIPTION')
		description.text = self.description
		studyrefElt = etree.SubElement(analysisElt, 'STUDY_REF', accession=self.study_accession)
		samplerefElt = etree.SubElement(analysisElt, 'SAMPLE_REF', accession=self.sample_accession)
		analysis_type = etree.SubElement(analysisElt, 'ANALYSIS_TYPE')
		type = etree.SubElement(analysis_type, 'AMR_ANTIBIOGRAM')
		files = etree.SubElement(analysisElt, 'FILES')
		file1Elt = etree.SubElement(files,'FILE', filename=self.analysis_files[0].file_name,filetype=self.analysis_files[0].file_type,checksum_method="MD5", checksum=self.analysis_files[0].file_md5)
#		print lxml.etree.tostring(analysis_xml, pretty_print=True,xml_declaration = True, encoding='UTF-8')
		analysis_xml.write(self.analysis_xml_file,pretty_print=True,xml_declaration = True, encoding='UTF-8')
		
		


class submission:
	
	
	def __init__(self,alias,submission_centre,action,submission_xml_file,source_xml,schema):
		self.submission_centre=submission_centre
		self.action=action
		self.source_xml=source_xml
		self.alias=alias
		self.submission_xml_file=submission_xml_file
		self.schema=schema
	
	def build_submission(self):
		submission_set = etree.Element('SUBMISSION_SET')
		submission_xml = etree.ElementTree(submission_set)
		submissionElt = etree.SubElement(submission_set, 'SUBMISSION', alias=self.alias , center_name=self.submission_centre)
		actionsElt=etree.SubElement(submissionElt, 'ACTIONS')
		actionElt=etree.SubElement(actionsElt,'ACTION')
		actionSub=etree.SubElement(actionElt,self.action,source=self.source_xml,schema=self.schema)
#		actionElt2=etree.SubElement(actionsElt,'ACTION')
#		actionRollback=etree.SubElement(actionElt2,'ROLLBACK')
		submission_xml.write(self.submission_xml_file,pretty_print=True,xml_declaration = True, encoding='UTF-8')


	
	
class analysis_file:

	def __init__(self,file_name,file_type,file_md5):
		self.file_name=file_name
		self.file_type=file_type
		self.file_md5=file_md5
