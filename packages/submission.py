import subprocess
import sys

class submission:
    def submit_to_ENA(submission_file , submission_set_file , args, type):
        
        # Construct the curl command
        if args.test:
        
            curl_command = [
                'curl',
                '-u', f'{args.username}:{args.password}',
                '-F', f'SUBMISSION=@{submission_file}',
                '-F', f'{type}=@{submission_set_file}',
                'https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/'
            ]
        else:
            curl_command = [
                'curl',
                '-u', f'{args.username}:{args.password}',
                '-F', f'SUBMISSION=@{submission_file}',
                '-F', f'{type}=@{submission_set_file}',
                'https://www.ebi.ac.uk/ena/submit/drop-box/submit/'
            ]

        # Execute the curl command
        try:
            subprocess.run(curl_command, check=True)
            #print("\033[93mSubmission successful.\033[0m")
        except subprocess.CalledProcessError as e:
            print(f"\033[91mError: Submission failed.\033[0m\nException: {e}")
            sys.exit()

