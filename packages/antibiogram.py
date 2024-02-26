import sys
class validation:
    def validate_biosample_id (biosample_id):
        for i in range(len(biosample_id)):
            if 'SAM' not in biosample_id[i]:
                print(f"\033[91mValidation ERROR: {biosample_id[i]} is not a valid biosample accession in line number {i+1}. \033[0m")
                sys.exit()

    def validate_antibiotic_name(antibiotic):
        antibiotic_name = open('packages/antibiotics.txt','r').read()
        for i in range(len(antibiotic)):
            if antibiotic[i] not in antibiotic_name:
                print(f"\033[91mValidation ERROR: {antibiotic[i]} is not a valid antibiotic_name in line number {i+1}. This must be in {antibiotic_name} \033[0m")
                sys.exit()

    def validate_ast_standard(ast_standard):
        accepted_ast_standards = ['CLSI', 'EUCAST', 'CA-SFM', 'BSAC', 'DIN', 'SIR', 'WRG']
        for i in range(len(ast_standard)):
            if ast_standard[i] not in accepted_ast_standards:
                print(f"\033[91mValidation ERROR: {ast_standard[i]} is not a valid ast_standard in line number {i+1}. This must be in {accepted_ast_standards} \033[0m")
                sys.exit()

    def validate_laboratory_typing_method(laboratory_typing_method):
        laboratory_typing_methods = ['BROTH DILUTION', 'MICROBROTH DILUTION', 'AGAR DILUTION', 'DISC-DIFFUSION', 'NEO-SENSITABS', 'ETEST']
        for i in range(len(laboratory_typing_method)):
            if laboratory_typing_method[i] not in laboratory_typing_methods:
                print(f"\033[91mValidation ERROR: {laboratory_typing_method[i]} is not a valid laboratory_typing_method in line number {i+1}. This must be in {laboratory_typing_methods} \033[0m")
                sys.exit()

    def validate_resistance_phenotype(resistance_phenotype):
        accepted_resistance_phenotype = ['intermediate', 'susceptible', 'resistant', 'non-susceptible', 'not-defined']
        for i in range(len(resistance_phenotype)):
            if resistance_phenotype[i] not in accepted_resistance_phenotype:
                print(f"\033[91mValidation ERROR: {resistance_phenotype[i]}  is not a valid resistance phenotype in line number {i+1}. This must be in {accepted_resistance_phenotype}\033[0m")
                sys.exit()

