class antibiogram:
    
    global antibiotic_file
    
    antibiotic_file="antibiotics.txt"

    def __init__(self,biosample_id,species,antibiotic_name,ast_standard,breakpoint_version,laboratory_typing_method,measurement,measurement_units,measurement_sign,resistance_phenotype,platform):
	    self.biosample_id = self.val_biosample_id(biosample_id) 
	    self.species=self.val_species(species)
	    self.antibiotic_name=self.val_antibiotic_name(antibiotic_name,antibiotic_file)
	    self.ast_standard=self.val_ast_standard(ast_standard)
	    self.breakpoint_version=self.val_breakpoint_version(breakpoint_version)
	    self.laboratory_typing_method=self.val_laboratory_typing_method(laboratory_typing_method)
	    self.measurement=self.val_measurement(measurement,laboratory_typing_method)
	    self.measurement_units=self.val_measurement_units(measurement_units,laboratory_typing_method)
	    self.measurement_sign=self.val_measurement_sign(measurement_sign)
	    self.resistance_phenotype=self.val_resistance_phenotype(resistance_phenotype)
	    self.platform=self.val_platform(platform)
        
    def val_biosample_id(self,biosample_id):
        if not biosample_id.startswith("SAM"):
            print "ERROR: %s is not a valid biosample accession"%biosample_id
        return biosample_id
        
    def val_species(self,species):
        return species
    
    def val_antibiotic_name(self,antibiotic_name,antibiotic_file):
        with open(antibiotic_file) as f:
             antibiotics = f.read().splitlines() 
        if antibiotic_name not in antibiotics:
           print "ERROR: %s is not a valid antibiotic_name name"%antibiotic_name
        return antibiotic_name
        
    def val_ast_standard(self,ast_standard):
        accepted_ast_standards=['CLSI','EUCAST','CA-SFM','BSAC','DIN','SIR','WRG']
        if ast_standard not in accepted_ast_standards:
           print "ERROR: %s is not a valid ast_standard"%ast_standard
        return ast_standard
        
    def val_breakpoint_version(self,breakpoint_version):
        return breakpoint_version
        
    def val_laboratory_typing_method(self,laboratory_typing_method):
        laboratory_typing_methods=['broth dilution','microbroth dilution','agar dilution','disc-diffusion','neo-sensitabs','etest']
        if laboratory_typing_method not in laboratory_typing_methods:
           print "ERROR: %s is not a valid laboratory_typing_method"%laboratory_typing_method
        return laboratory_typing_method
    
    def val_measurement(self,measurement,laboratory_typing_method):
        dilution_methods=['broth dilution','microbroth dilution','agar dilution']
        diffusion_methods=['disc-diffusion','neo-sensitabs','etest']
          
        if laboratory_typing_method in dilution_methods:
           if measurement > 2048 or measurement < 0.01:
              print "ERROR: %s is not a valid measurement, accepted one is between 0.01 and 2048 for dilution methods."%measurement
        elif laboratory_typing_method in diffusion_methods:
           if measurement > 99 or measurement < 6:
              print "ERROR: %s is not a valid measurement, accepted one is between 6 and 99 for diffusion methods."%measurement
        else:
            print "ERROR: measurement can't be validated as laboratory_typing_method needs to be valid to validate the measurement."
            
        return measurement
        
    def val_measurement_units(self,measurement_units,laboratory_typing_method):
        dilution_methods=['broth dilution','microbroth dilution','agar dilution']
        diffusion_methods=['disc-diffusion','neo-sensitabs','etest']
          
        if laboratory_typing_method in dilution_methods:
           if measurement_units !='mg/L':
              print "ERROR: %s is not a valid measurement unit, accepted one is 'mg/L' for dilution methods."%measurement_units
        elif laboratory_typing_method in diffusion_methods:
           if measurement_units !='mm':
              print "ERROR: %s is not a valid measurement unit, accepted one is 'mm' for dilution methods."%measurement_units
        else:
            print "ERROR: measurement unit can't be validated as laboratory_typing_method needs to be valid to validate the measurement unit."
            
        return measurement_units
        
    def val_measurement_sign(self,measurement_sign):
        accepted_val_measurement_signs=['>','<','=']
        if measurement_sign not in accepted_val_measurement_signs:
            print "ERROR: %s is not a valid measurement sign. Valid ones are '>','<',and '='."%measurement_sign
        return measurement_sign
    
    def val_resistance_phenotype(self,resistance_phenotype):
        accepted_resistance_phenotype=['intermediate','susceptible','resistant','non-susceptible','not-defined']
        if resistance_phenotype not in accepted_resistance_phenotype:
            print "ERROR: %s is not a valid resistance phenotype. Valid ones are 'intermediate','susceptible','resistant','non-susceptible', and 'not-defined'"%resistance_phenotype
        return resistance_phenotype
    
    def val_platform(self,platform):
        return platform
        
    