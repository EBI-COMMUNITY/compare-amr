import os
import datetime
from amr import antibiogram


class val:

    month = datetime.date.today().strftime('_%b-%Y')
    error_detect = 0
    files_created=set()

    def __init__(self,arguments):



        self.args = arguments
        self.antibiograms = self.get_antibiogram_data()

#        self.month = datetime.date.today().strftime('_%b-%Y')+".txt"
#        self.error_detect = 0


    def validate_header(self,header_line):
        values = header_line.strip().lower().split("\t")
        header_len= len(values)
        exit = 1
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

        return header_line


    def get_antibiogram_data(self):

	
        tsv_file = self.args.filename
	with open(tsv_file) as f:
		lines = f.readlines()
	
	header_line = self.validate_header(lines[0])  
	values = lines[0].strip().lower().split("\t")
	header_len=len(values)
	biosample_id_set=set()
 	species_set=set()

	antibiograms=list()

   
	biosample_id_index=values.index("biosample_id")
	species_index=values.index("species")
	antibiotic_name_index=values.index("antibiotic_name")
	ast_standard_index=values.index("ast_standard")
	breakpoint_version_index=values.index("breakpoint_version")
	laboratory_typing_method_index=values.index("laboratory_typing_method")
	measurement_index=values.index("measurement")
	measurement_units_index=values.index("measurement_units")
	measurement_sign_index=values.index("measurement_sign")
	resistance_phenotype_index=values.index("resistance_phenotype")
	platform_index=values.index("platform")

	
	
	
	i=1
	for line in lines:
		columns = line.strip().split("\t")
		if len(columns) <10:
			print "ERROR: line number %s of the file has less number of column than the minimum accepted column (10).\nIt is possible that your file has missed tabs"%str(i)
			sys.exit(0)
		
		if i>1:
			if len(columns)!=header_len:
				print "ERROR: Line number:%s has wrong number of column. It has %s columns while your header has %s columns."%(i,len(columns),header_len)
				print "The wrong line has these columns:%s"%columns
				
			else:
				biosample_id=columns[biosample_id_index]
#				biosample_id_set.add(biosample_id)
				species=columns[species_index]
				species_set.add(species)
				antibiotic_name=columns[antibiotic_name_index]
				ast_standard=columns[ast_standard_index]
				breakpoint_version=columns[breakpoint_version_index]
				laboratory_typing_method=columns[laboratory_typing_method_index]
				measurement=columns[measurement_index]
				measurement_units=columns[measurement_units_index]
				measurement_sign=columns[measurement_sign_index]
				resistance_phenotype=columns[resistance_phenotype_index]
				platform=columns[platform_index]
					
				

				antibio=antibiogram(biosample_id,species,antibiotic_name,ast_standard,breakpoint_version,
									laboratory_typing_method,measurement,measurement_units,measurement_sign,
									resistance_phenotype,platform,i)

				if self.args.mode == "submit": 
					if antibio.has_error:
						self.error_detect += 1 # could put bad antibio in separate list to 'antibiograms'
					else:
                                                file_name = biosample_id + self.month
                                                self.files_created.add(file_name)
						with open(file_name + ".txt", "a") as singsamp:
							if biosample_id not in biosample_id_set:
								singsamp.write(header_line)
							singsamp.write(line)
						biosample_id_set.add(biosample_id)
				antibiograms.append(antibio)
		i += 1
 
        self.header_line=header_line
	return antibiograms


