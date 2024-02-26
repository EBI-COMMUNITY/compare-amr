# Antibiogram Submission

This script allows validation and submission of Antibiograms to ENA. It should be noted that there are two servers on ENA: [test](https://wwwdev.ebi.ac.uk/ena/submit/webin/login) and [production](https://www.ebi.ac.uk/ena/submit/webin/login). Data submitted to the test server will be removed after 24 hours.

## Prerequisites
```
pip install argparse pandas lxml
```

## Upload Your File

You must upload your file before using the script. You can upload your Antibiogram file using the Webin file uploader. [link for more information](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/upload.html#uploading-files-to-ena).  
See the template at: ```packages/template.txt```
## Process

Before submitting your Antibiogram, please ensure that you have submitted:
1. Project: [link for more information](https://ena-docs.readthedocs.io/en/latest/submit/study.html)
2. Sample: [link for more information](https://ena-docs.readthedocs.io/en/latest/submit/samples.html)

## Usage

### Help
To learn how to use this script, type:
```
python ENAAntibiogrammSub.py
```
or 
```
python ENAAntibiogrammSub.py -h 
```

### Example
```
python ENAAntibiogrammSub.py -u Webin-XXX -p PASSWORD -f antibiogram.txt -S PRJEBXXXX -s ERSXXX -a alias  -T 'my title'  -d  'This is a short description' -t
```

The options -u, -p, -f, -S, -s, and -a are mandatory.
1. -u indicates the Webin submission account.
2. -p indicates the password for your Webin submission account.
3. -f indicates your Antigram file. This must be tab-separated.
4. -S indicates the project to which you want to link your submission and must be in the format PRJEBXXXX.
5. -s indicates the sample to which you want to link your submission and must be in the format ERSXXX.

The options -T, -d, and -t are optional.
1. -T indicates the title of your submission. Please enclose your title in single quotes if you use spaces or special characters.
2. -d indicates a description of your submission. Please enclose your description in single quotes if you use spaces or special characters.
3. -t indicates that you are submitting your antibiogram as a test and it will be removed after 24 hours. Otherwise, it will be submitted directly to the production server.


**For any error or assistance please contact the [ENA helpdesk](https://www.ebi.ac.uk/ena/browser/support)**