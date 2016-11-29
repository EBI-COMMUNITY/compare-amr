import requests
import sys

class antibiogram:
		
		global antibiotic_file
		global laboratory_typing_methods
		global dilution_methods
		global diffusion_methods
		
		
		laboratory_typing_methods=['BROTH DILUTION','MICROBROTH DILUTION','AGAR DILUTION','DISC-DIFFUSION','NEO-SENSITABS','ETEST']
		dilution_methods=['BROTH DILUTION','MICROBROTH DILUTION','AGAR DILUTION']
		diffusion_methods=['DISC-DIFFUSION','NEO-SENSITABS','ETEST']
		antibiotic_file="antibiotics.txt"

		def __init__(self,biosample_id,species,antibiotic_name,ast_standard,breakpoint_version,laboratory_typing_method,measurement,measurement_units,measurement_sign,resistance_phenotype,platform,line_number):
			self.biosample_id = self.val_biosample_id(biosample_id,line_number) 
			self.species=self.val_species(species,line_number)
			self.antibiotic_name=self.val_antibiotic_name(antibiotic_name,antibiotic_file,line_number)
			self.ast_standard=self.val_ast_standard(ast_standard,line_number)
			self.breakpoint_version=self.val_breakpoint_version(breakpoint_version,line_number)
			self.laboratory_typing_method=self.val_laboratory_typing_method(laboratory_typing_method,line_number)
			self.measurement=self.val_measurement(measurement,laboratory_typing_method,line_number)
			self.measurement_units=self.val_measurement_units(measurement_units,laboratory_typing_method,line_number)
			self.measurement_sign=self.val_measurement_sign(measurement_sign,line_number)
			self.resistance_phenotype=self.val_resistance_phenotype(resistance_phenotype,line_number)
			self.platform=self.val_platform(platform,line_number)
			self.line_number=line_number
				
				
		def val_biosample_id(self,biosample_id,line_number):
				if not biosample_id.upper().startswith("SAM"):
						print "ERROR: %s is not a valid biosample accession in line number %s"%(biosample_id,line_number)
				return biosample_id
		
		def val_species(self,species,line_number):
				sp=species.replace (" ", "%20")
				scientific_name_url="http://www.ebi.ac.uk/ena/data/taxonomy/v1/taxon/scientific-name/%s"%sp
				any_name_url="http://www.ebi.ac.uk/ena/data/taxonomy/v1/taxon/any-name/%s"%sp
				resp = requests.get(scientific_name_url)
				if resp.status_code != 200:
						resp = requests.get(any_name_url)
						print "ERROR: scientific name for species '%s' does not exist in taxonomy database in line number %s."%(species,line_number)
						if resp.status_code == 200:
							 print "Some close matches scientific names are:\n%s"%resp.json()[0]['scientificName']
				
		#TODOL Clara to check the official antiobiotic names 
		def val_antibiotic_name(self,antibiotic_name,antibiotic_file,line_number):
				with open(antibiotic_file) as f:
						 antibiotics = f.read().upper().splitlines()
				if antibiotic_name.upper() not in antibiotics:
					 print "ERROR: %s is not a valid antibiotic_name name in line number %s."%(antibiotic_name,line_number)
				return antibiotic_name
				
		def val_ast_standard(self,ast_standard,line_number):
				accepted_ast_standards=['CLSI','EUCAST','CA-SFM','BSAC','DIN','SIR','WRG']
				if ast_standard.upper() not in accepted_ast_standards:
					 print "ERROR: %s is not a valid ast_standard in line number %s."%(ast_standard,line_number)
				return ast_standard
				
		def val_breakpoint_version(self,breakpoint_version,line_number):
				return breakpoint_version
				
		def val_laboratory_typing_method(self,laboratory_typing_method,line_number):
				if laboratory_typing_method.upper() not in laboratory_typing_methods:
					 print "ERROR: %s is not a valid laboratory_typing_method in line number %s."%(laboratory_typing_method,line_number)
				return laboratory_typing_method
		
		def val_measurement(self,measurement,laboratory_typing_method,line_number):
				if measurement.find('-')!=-1:
						measurements=measurement.split('-')
						for meas in measurements:
								if laboratory_typing_method.upper() in dilution_methods:
									try:
											if not 0.01 <= float(meas) <= 2048:
													print "ERROR: %s is not a valid measurement, accepted one is between 0.01 and 2048 for dilution methods in line number %s."%(meas,line_number)
									except:
											print "ERROR: the measurement value format of %s in not correct in line number %s."%(meas,line_number)
											message=str(sys.exc_info()[1])
											print "    Exception: %s"%message
								elif laboratory_typing_method.upper() in diffusion_methods:
									try:
											if not 6 <= float(meas) <= 99:
													print "ERROR: %s is not a valid measurement, accepted one is between 6 and 99 for diffusion methods in line number %s."%(meas,line_number)
									except:
											print "ERROR: the measurement value format of %s in not correct in line number %s."%(meas,line_number)
											message=str(sys.exc_info()[1])
											print "    Exception: %s"%message
								else:
									 print "ERROR: measurement can't be validated as laboratory_typing_method needs to be valid to validate the measurement in line number %s."%line_number
				else:
						if laboratory_typing_method.upper() in dilution_methods:
								try:
									if not 0.01 <= float(measurement) <= 2048:
											print "ERROR: %s is not a valid measurement, accepted one is between 0.01 and 2048 for dilution methods in line number %s."%(measurement,line_number)
								except:
										print "ERROR: the measurement value format of %s in not correct in line number %s."%(measurement,line_number)
										message=str(sys.exc_info()[1])
										print "    Exception: %s"%message
						elif laboratory_typing_method.upper() in diffusion_methods:
								try:
									if not 6 <= float(measurement) <= 99:
											print "ERROR: %s is not a valid measurement, accepted one is between 6 and 99 for diffusion methods in line number %s."%(measurement,line_number)
								except:
										print "ERROR: the measurement value format of %s in not correct in line number %s."%(measurement,line_number)
										message=str(sys.exc_info()[1])
										print "    Exception: %s"%message
						else:
							 print "ERROR: measurement can't be validated as laboratory_typing_method needs to be valid to validate the measurement in line number %s."%line_number
						
				return measurement
				
		def val_measurement_units(self,measurement_units,laboratory_typing_method,line_number):
				if laboratory_typing_method.upper() in dilution_methods:
					 if measurement_units.lower() !='mg/l':
							print "ERROR: %s is not a valid measurement unit, accepted one is 'mg/L' for dilution methods in line number %s."%(measurement_units,line_number)
				elif laboratory_typing_method.upper() in diffusion_methods:
					 if measurement_units.lower() !='mm':
							print "ERROR: %s is not a valid measurement unit, accepted one is 'mm' for dilution methods in line number %s."%(measurement_units,line_number)
				else:
						print "ERROR: measurement unit can't be validated as laboratory_typing_method needs to be valid to validate the measurement unit in line number %s."%line_number
						
				return measurement_units
		
		#TODO: check the signes like >=
		def val_measurement_sign(self,measurement_sign,line_number):
				accepted_val_measurement_signs=['>','<','=','<=','>=']
				if measurement_sign not in accepted_val_measurement_signs:
						print "ERROR: %s is not a valid measurement sign. Valid ones are '>','<',<=','>=' and '=' in line number %s."%(measurement_sign,line_number)
				return measurement_sign
		
		def val_resistance_phenotype(self,resistance_phenotype,line_number):
				accepted_resistance_phenotype=['intermediate','susceptible','resistant','non-susceptible','not-defined']
				if resistance_phenotype not in accepted_resistance_phenotype:
						print "ERROR: %s is not a valid resistance phenotype. Valid ones are 'intermediate','susceptible','resistant','non-susceptible', and 'not-defined' in line number %s"%(resistance_phenotype,line_number)
				return resistance_phenotype
		
		def val_platform(self,platform,line_number):
				return platform
				
		
