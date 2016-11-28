from amr import antibiogram
import sys



def get_antibiogram_data(tsv_file):
    with open(tsv_file) as f:
        lines = f.readlines()
    print lines[0]
    print lines[1]
   
    #if not lines[0].startswith("#"):
    #   print "ERROR: header line (line number 0) shall start with #."
        
    values = lines[0].strip().split("\t")
    header_len=len(values)
    print values
        
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
        if i>1:
            if len(columns)!=header_len:
                print "ERROR: Line number:%s has wrong number of column"%i
                
            else:
                biosample_id=columns[biosample_id_index]
                species=columns[species_index]
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
                                    resistance_phenotype,platform)

                antibiograms.append(antibio)
        i += 1
    
    return antibiograms



if __name__ == '__main__':
    print sys.argv[0]
    antibiograms=get_antibiogram_data(sys.argv[1])
    print antibiograms
    
