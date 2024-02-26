from lxml import etree
import os
import hashlib
import sys
import platform
import shutil

class XML_generator:
    
    # ------------------Method to build the submission XML file
    def antibiogram_build_submission_xml(result_directory):
        # Create XML elements
        submission_set = etree.Element('SUBMISSION')
        actions_elt = etree.SubElement(submission_set, 'ACTIONS')
        action_elt = etree.SubElement(actions_elt, 'ACTION')
        add_elt = etree.SubElement(action_elt, 'ADD')

        # Create XML tree
        submission_xml = etree.ElementTree(submission_set)

        # Specify the path for the submission XML file
        submission_file = os.path.join(result_directory, 'submission.xml')

        # Write to the XML file
        with open(submission_file, 'wb') as f:
            submission_xml.write(f, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        print(f"\033[93mSubmission XML file saved to: {submission_file}\033[0m")
        return submission_file
        

    # -----------------------Calculation of the MD5 hash for a given file
    def calculate_md5(filename_full):
        try:
            # Open the file in binary read mode and read its contents
            with open(filename_full, 'rb') as file:
                file_contents = file.read()
            
            # Calculate the MD5 hash of the file's contents
            file_md5 = hashlib.md5(file_contents).hexdigest()
            
            return file_md5
        
        except Exception as e:
            print(f"\033[91mError: Unable to calculate MD5 hash for file {filename_full}\033[0m")
            print("Exception:", e)
            sys.exit()
            
    # --------------------Method to generate the set XML file
    def antibiogram_generate_set_xml(result_directory, args):
        # Create ANALYSIS_SET element
        analysis_set = etree.Element('ANALYSIS_SET')

        # Create ANALYSIS element
        analysis = etree.SubElement(analysis_set, 'ANALYSIS', alias=args.alias)

        # Add TITLE and DESCRIPTION elements to ANALYSIS
        title = etree.SubElement(analysis, 'TITLE')
        if args.Title:
            title.text = args.Title
        else:
            title.text = f'Antibiogram for study {args.Study}, sample {args.sample}' 
        if args.description:
            description = etree.SubElement(analysis, 'DESCRIPTION')
            description.text = args.description

        # Add STUDY_REF, SAMPLE_REF, and RUN_REF elements to ANALYSIS
        study_ref = etree.SubElement(analysis, 'STUDY_REF', accession=args.Study)
        sample_ref = etree.SubElement(analysis, 'SAMPLE_REF', accession=args.sample)

        # Add ANALYSIS_TYPE element to ANALYSIS
        analysis_type = etree.SubElement(analysis, 'ANALYSIS_TYPE')
        AMR_ANTIBIOGRAM = etree.SubElement(analysis_type, 'AMR_ANTIBIOGRAM')

        # Add FILES element to ANALYSIS
        files = etree.SubElement(analysis, 'FILES')

        # Add FILE element to FILES
        checksum = XML_generator.calculate_md5(args.filename)
        try:
            shutil.copy(args.filename, result_directory)
            filename = os.path.basename(args.filename)
        except Exception as e: 
            print(f"\033[91mError: Unable to copy the file {args.filename} to {result_directory} \033[0m")
            sys.exit()

        file = etree.SubElement(files, 'FILE', filename=filename, filetype="tab", checksum_method="MD5", checksum=checksum)

        # Create XML tree
        xml_tree = etree.ElementTree(analysis_set)

        # Write XML tree to file
        output_path = os.path.join(result_directory, f'Antibiogram_for_{args.sample}.xml')
        xml_tree.write(output_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        print(f"\033[93mSubmission Set XML file saved to: {output_path}\033[0m")
        return output_path
