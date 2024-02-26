import argparse
import os , sys
import pandas as pd

from packages.XMLGenerator import XML_generator
from packages.submission import submission
from packages.antibiogram import validation


def get_args():
    epilog = ("""
            \033[93mNote:
            (1) \033[0mPlease register your project and sample object before registering the antibiogram. 
            Here is the link for more information: \033[94mhttps://ena-docs.readthedocs.io/en/latest/\033[0m.
            \033[93m(2) \033[0mPlease make sure to provide the title and description using single quotes if they contain spaces or special characters. 
            For any error or assistance please contact the ENA helpdesk: \033[94mhttps://www.ebi.ac.uk/ena/browser/support \033[0m
        """) 
    parser = argparse.ArgumentParser(description='Script for validating AMR antibiograms and optionally submitting them to the public repository ENA.'
                                    ,epilog= epilog ,
                                    )
    
    #Required arguments
    mandatory = parser.add_argument_group('\033[93mMandatory arguments\033[0m')
    mandatory.add_argument('-u', '--username', type=str, help='Webin submission account (e.g., Webin-XXX)', required=True)
    mandatory.add_argument('-p', '--password', type=str, help='Password for the submission account', required=True)
    mandatory.add_argument('-f', '--filename', type=str, help='Name of the AMR antibiogram file', required=True)
    mandatory.add_argument('-S', '--Study', type=str, help='Study ID (e.g., PRJEBXXX) to add the antibiograms', required=True)
    mandatory.add_argument('-s', '--sample', type=str, help='Sample ID (e.g., ERSXXXX) to add the antibiograms', required=True)
    mandatory.add_argument('-a', '--alias', type=str, help='Analysis alias to add the antibiograms', required=True)

    # Optional arguments
    optional = parser.add_argument_group('\033[93mOptional arguments\033[0m')
    optional.add_argument('-T', '--Title', type=str, help='Title of the submission (Optional). Use single quotes to provide the title, e.g., \'My Title\'')
    optional.add_argument('-d', '--description', type=str, help='Description of the submission (Optional). Use single quotes to provide the description, e.g., \'My Description\'')
    optional.add_argument('-t', '--test', action='store_true', help='Send the submission to the test server (Optional)')

    
    #args = parser.parse_args()

    return parser


def process():
    if len(sys.argv) <= 1: 
        print(get_args().print_help())
        sys.exit()
        
    args = get_args().parse_args()

    result_directory = 'results'  
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    try:
        antibiogram_file = pd.read_csv (args.filename, sep='\t')
    except Exception as e:
        print(f"\033[91mError: reading file {args.filename}.\033[0m\nException: {e}")
        sys.exit() 
    
    validation.validate_biosample_id(antibiogram_file['bioSample_ID'])
    validation.validate_antibiotic_name (antibiogram_file['antibiotic_name'])
    validation.validate_ast_standard(antibiogram_file['ast_standard'])
    validation.validate_resistance_phenotype(antibiogram_file['resistance_phenotype'])

    submission_file = XML_generator.antibiogram_build_submission_xml(result_directory)
    submission_set_file = XML_generator.antibiogram_generate_set_xml (result_directory, args)
    submission.submit_to_ENA(submission_file , submission_set_file, args , 'ANALYSIS')

    print(f"\033[93m\n-------[ done ]-------\033[0m")
    print(f"\033[94mFor any error or assistance please contact the ENA helpdesk: https://www.ebi.ac.uk/ena/browser/support \n\n\033[0m")


if __name__ == '__main__':
    process()
    