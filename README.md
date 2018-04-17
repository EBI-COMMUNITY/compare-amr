# AMR


compare-amr directory contains (among other files)

amrcurl.py <br />
amr.py <br />
antibiotics.txt <br />
ftper.py <br />
samp.txt <br />
sra_objects.py <br />
validator.py <br />
val.py <br />


The package is accessed from main file 'validator.py' <br />
You can run the below to see available options <br />
python validator.py --help <br />


The tool will add directories and files into the working directory so it is reccommended to work outside of compare-amr directory but you must copy over antibiotics.txt to your working directory to have a local list of accepted antibiotics terms.

minimum_samp.txt is an example anitbiogram file. Copy this to your local directory too, for testing. 

Step 1: using option 'validate' (-m validate) on the provided minimum_samp.txt file

python ../compare-amr/validator.py -f minimum_samp.txt -m validate -u Webin-XXX -p PASS -s PRJEBXXXX -c CENT -t

If all is well, the headers in the antibiogram file are printed and no other messages will appear if there are no errors detected. 
Webin-XXX must be replaced with your account id
PASS must be replaced with the password for your account.
PRJEBXXXX must be replaced with a valid project id (to which you are adding the antibiogram file)
CENT must be replaced by a valid centre name that is associated with your Webin account
Use the correct path to call validator.py if it is in a different directory to the working directory

The -t flag means "test" in the command above. It does nothing at this stage but if the 'validate' option was turned off and the submission went through, it would go to the test server instead of the production server. The test server behaves like the production server and you will get back accessions if the submission is good. But the test server is wiped and replaced every day so the accessions will not persist and are not real! 


output on success:

['biosample_id', 'species', 'antibiotic_name', 'ast_standard', 'breakpoint_version', 'laboratory_typing_method', 'measurement', 'measurement_units', 'measurement_sign', 'resistance_phenotype', 'platform']



Step 2: using option 'submit' (-m submit) to submit and receive an ERZ accession for each unique sample in the antibiogram file.

python ../compare-amr/validator.py -f minimum_samp.txt -m submit -u Webin-XXX -p PASS -s PRJEBXXXX -c CENT -t

The source antibiogram file is split by source sample (column 1). The example file "minimum_samp.txt" has 8 distinct samples (SAMEA3993570, SAMEA3993572, SAMEA3993567, SAMEA3993569, SAMEA3993571, SAMEA3993565, SAMEA3993573, SAMEA3993566) so 8 antibiogram files are created, each in a separate directory which is named by the current month (to help organise future and historic submissions) also included in each directory is a submittable XML submission file and XML analysis file. Each directory is transferred by ftp to your Webin ftp area. The final step is to submit all antibiograms. This is done in one step so that all antibiogram files will have the same submission event id and it will also save making multiple calls to the server. An all-encompasing submission XML file and analysis XML file are created in the working directory. The analysis XML refers to each one of the antibiogram files in the subdirectories. The 2 XML files are sent to the ENA REST server and a receipt in XML format is obtained from the server. If the submission is successful the receipt XML will contain an ERZ (analysis) accession for each antibiogram file. The receipt is printed to standard output when the program has completed. Also look out for the string 'success="true"' for verification that the submission completed without error.

example output on success:

['biosample_id', 'species', 'antibiotic_name', 'ast_standard', 'breakpoint_version', 'laboratory_typing_method', 'measurement', 'measurement_units', 'measurement_sign', 'resistance_phenotype', 'platform']
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
<RECEIPT receiptDate="2017-11-30T15:32:46.640Z" submissionFile="all_anal_sub_Nov-2017.xml" success="true">
     <ANALYSIS accession="ERZ243560" alias="SAMEA3993570_Nov-2017" status="PRIVATE"/>
     <ANALYSIS accession="ERZ243561" alias="SAMEA3993572_Nov-2017" status="PRIVATE"/>
     <ANALYSIS accession="ERZ243562" alias="SAMEA3993567_Nov-2017" status="PRIVATE"/>
     <ANALYSIS accession="ERZ243563" alias="SAMEA3993569_Nov-2017" status="PRIVATE"/>
     <ANALYSIS accession="ERZ243564" alias="SAMEA3993571_Nov-2017" status="PRIVATE"/>
     <ANALYSIS accession="ERZ243565" alias="SAMEA3993565_Nov-2017" status="PRIVATE"/>
     <ANALYSIS accession="ERZ243566" alias="SAMEA3993573_Nov-2017" status="PRIVATE"/>
     <ANALYSIS accession="ERZ243567" alias="SAMEA3993566_Nov-2017" status="PRIVATE"/>
     <SUBMISSION accession="ERA398936" alias="all_anal_sub_Nov-2017"/>
     <MESSAGES>
          <INFO>This submission is a TEST submission and will be discarded within 24 hours</INFO>
     </MESSAGES>
     <ACTIONS>ADD</ACTIONS>
</RECEIPT>


Finally:
Example of trying to submit an antibiogram file with an error in it:

python ../compare-amr/validator.py -f with_error.txt -m submit -u Webin-XXXX -PASS -s PRJEBXXXX -c CENT -t

['biosample_id', 'species', 'antibiotic_name', 'ast_standard', 'breakpoint_version', 'laboratory_typing_method', 'measurement', 'measurement_units', 'measurement_sign', 'resistance_phenotype', 'platform']
ERROR: 'amjicillin' is not a valid antibiotic_name name in line number 2.
1 rows have an error. removing temporary files and exiting ...

In this case, attempt to correct the error and try again. The 'validate' option is recommended when testing for the first time to avoid uneccesary file creation and file upload in case there is an error in the original antibiogram file.



