from amr import antibiogram
import sys

#TODO: check to see if a file tab file DONE
#TODO: check to see all the headers column are available DONE
#TODO: check the taxonomy/species  DONE
#TODO: add ignore case to all the string matches DONE
#TODO: check a 10 column file to works Not needed
#TODO: check to see all the sample_ids are the same DONE
#TODO: check to see if all the species are the same DONE
#TODO: accept  the range to the measurment 
#TODO: let everybody know about the removal of #

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
	 
	 
	



def get_antibiogram_data(tsv_file):
	with open(tsv_file) as f:
		lines = f.readlines()
	
	validate_header(lines[0])   
	values = lines[0].strip().lower().split("\t")
	header_len=len(values)
	biosample_id_set=set()
	species_set=set()
	

   
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

	antibiograms=list()
	
	i=1
	for line in lines:
		columns = line.strip().split("\t")
		if len(columns) <10:
			print "ERORR: line number %s of the file has less number of column than the minimum accepted column (10).\nIt is possible that your file has missed tabs"%str(i)
			sys.exit(0)
		
		if i>1:
			if len(columns)!=header_len:
				print "ERROR: Line number:%s has wrong number of column. It has %s columns while your header has %s columns."%(i,len(columns),header_len)
				print "The wrong line has these columns:%s"%columns
				
			else:
				biosample_id=columns[biosample_id_index]
				biosample_id_set.add(biosample_id)
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

				antibiograms.append(antibio)
		i += 1
	if len(biosample_id_set) > 1:
		print "ERROR: there are multiple biosample_id in this file. biosample_id shall be unique. current ones are:\n %s"%list(biosample_id_set)
	if len(species_set) > 1:
		print "ERROR: there are multiple species in this file. Species shall be unique. Current ones are:\n %s"%list(species_set)

	return antibiograms



if __name__ == '__main__':
	antibiograms=get_antibiogram_data(sys.argv[1])
	
