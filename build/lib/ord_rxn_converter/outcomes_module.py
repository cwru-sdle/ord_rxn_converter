# import requirements:
from ord_schema.proto import dataset_pb2, reaction_pb2
from google.protobuf.message import Message
from uuid import uuid4
from ord_rxn_converter.utility_functions import extract_all_enums
from ord_rxn_converter.identifiers_module import extract_compound_identifiers, generate_compound_table

#generate enums_data to be accessible here TODO - have importable object instead..?
enums_data = extract_all_enums(reaction_pb2)

def extract_reaction_outcomes(reactionID, outcomes): 

    """
    Description: 
        Takes a reaction outcome object (in Google Protobuf message type based on ORD structure schema) & return a list of outcomes: 
            reaction time: for flow, equivalent to residence time or spacetime
            reaction time unit
            percentage conversion
            product information:
                identifiers
                measurements
                texture
                features, etc.
            analyses

    Algorithm:
        1. Initialize empty lists to hold reaction outcomes
        2. Loop through each outcome
        3. For each product in an outcome, extract product data
        4. For each product, extract analysis data
        5. If analysis data exists, append all values to reaction outcomes list
        6. Otherwise, append all values to reaction outcomes list and analysis values to 'None' 
    
    Args: 
        outcomes:
            Outcomes from a reaction 

    Returns: 
        list:
            A list of outcome information from a reaction
    """
    outcomes_list = []
    outcome_identifiers = []
    outcome_measurements = []
    
    for index, outcome in enumerate(outcomes, start=1):
        outcomeKey = f"outcomeKey_{index}_{reactionID}"
        
        # reaction_time = 1
        time_unit = enums_data['Time.TimeUnit'][outcome.reaction_time.units]
        
        # conversion = 2

        # products = 3
        if outcome.products:
            products = outcome.products 
            products_list, compound_table = extract_product(products)
            outcome_identifiers.extend(compound_table)
        else:
            products_list = None
            outcome_identifiers = None
          
        # analyses = 4  
        if outcome.analyses:
            analyses = outcome.analyses
            analyses_list = extract_analyses(analyses)
        else: analyses_list = None
            
        outcomes_list.append([reactionID, outcomeKey, outcome.reaction_time.value , time_unit, outcome.conversion.value, products_list, analyses_list])
    
    return outcomes_list, outcome_identifiers

def extract_product (products):
    """"
    Description: Takes in products and outcome key and extracts products and measurents of a reaction outcome and compounds in a reaction: 
        product measurements
        products_list: 
            outcomeKey
            identifier list
            is desired product
            measurement keys  
            isolated color,
            texture
            feature dict
            reaction role
        compound table

    Algorithm: 
        1. Initialize products_list to store all of the products 
        2. Initialize products_measurements to store measurements of all of the products 
        3. Initialize compound_table to hold compound information
        4. Iterate through each product in products: 
            a. Extract all of the identifiers into a list # TODO: somehow need to add the product identifiers into the compound table 
            b. Append compound identifiers to compound_table
            c. Extract the measurements by calling the extract_product_measurements function with measurements as the argument
                - This returns a list of measurement_keys to cross-refernce between the two tables (outcome vs measurements)
            d. Append all of the measurement lists into a list for ALL of the products' measurements (products_measurements)
            e. Extract texture, features, and reaction role
        5. Append of all of the fields into products_list
        6. Return the products_list, the products_measurements and the compound_table

    Args: 
        products: 
            Products of a reaction
        outcomeKey:
            Unique key of a reaction outcome

    Returns: 
        list:
            A list of reaction products, measurements, and compounds 
    """
    products_list = []
    products_measurements = []
    compound_identifiers = []
    
    for product in products:
        # identifiers = 1
        if product.identifiers:
            identifiers = product.identifiers
            inchi_key, identifier_list = extract_compound_identifiers(identifiers)
            compound_identifiers.append(generate_compound_table(identifiers))
        else: 
            identifier_list = None
            inchi_key = None

        # TODO: need to generate the InChIKey from SMILES or InChI & use the InChI to update the COMPOUND TABLE should this be in the identifiers function? 

        # is_desired_product = 2

        # measurements = 3 
        if product.measurements:
            measurements = product.measurements 
            measurement_list = extract_product_measurements(measurements)
            products_measurements.append(measurement_list)
        else: 
            measurement_list = None
            products_measurements.append(measurement_list)   

        # isolated_color = 4
        
        # texture = 5
        if product.texture:
            texture = enums_data['Texture.TextureType'][product.texture.type]
            product_texture = {texture:product.texture.details}
        else: product_texture = None
        
        # features = 6 
        feature_dict = {feature_key: feature for feature_key, feature in product.features} if product.features else None
        #for feature_key, feature in product.features.items():
        #    feature_list.append(dict(zip(feature_key, feature)))

        # reaction_role = 7
        reaction_role = enums_data['ReactionRole.ReactionRoleType'].get(product.reaction_role, 'UNKNOWN')
        
        products_list.append([inchi_key, product.is_desired_product, products_measurements, 
            product.isolated_color, product_texture, feature_dict, reaction_role])
    
    return products_list, compound_identifiers

def extract_product_measurements(measurements):
    """
    Description: Takes in measurements and extracts the measurements of reaction outcomes:
        measurement key
        analysis key
        measurement type
        measurement details
        measurement uses internal standard,
        measurement is normalized
        measurement uses authentic standard
        compound authentic
        measurement value
        retention time
        time unit
        mass spec type
        mass spec details
        tic minimum
        tic maximum
        eic masses 
        selectivity
        wavelength
        wavelength unit

    Algorithm:
        1. Create empty lists for measurements and measurement keys
        2. Loop through each measurement
        3. Set unique measurement keys and append to key list
        4. Extract measurement information if available 
        5. Append measurement information to measurement list

    Args: 
        measurements:
            Measurements of reaction 
    
    Returns:
        list:
            A list of measurment information for reaction outcomes

    """
    measurement_list = []
    
    for measurement in measurements:        
        # analysis_key =1 
        analysis_key = measurement.analysis_key if measurement.analysis_key else None
        
        # type = 2
        measurement_type = enums_data['ProductMeasurement.ProductMeasurementType'][measurement.type]

        # details = 3

        # uses_internal_standard = 4

        # is_normalized = 5

        # uses_authentic_standard = 6

        # authentic_standard = 6
        # TODO: call compound function here
        compound_authentic = measurement.authentic_standard if measurement.authentic_standard else None

        if measurement.WhichOneof('value'):
            measurement_value = getattr(measurement, measurement.WhichOneof('value'))
        else:
            measurement_value = None
        
        # percentage = 8
        if measurement_value == 'percentage': 
            measurement_value = measurement.percentage.value
            
        # float_value = 9
        elif measurement_value == 'float_vlaue':
            measurement_value = measurement.float_value
        
        # string_value = 10
        elif measurement_value == 'string_value':
            measurement_value = measurement.string_value
        
        # amount = 11 
        elif measurement_value == 'amount':
            amount_value, amount_unit = extract_amount(measurement)
            measurement_value = {'amount':amount_value, 'unit':amount_unit}
        
        else: measurement_value = None

        # retention_time = 12 
        if measurement.retention_time:
            retention_time = measurement.retention_time.value
            time_unit = enums_data['Time.TimeUnit'][measurement.retention_time.units]
        else: 
            retention_time = None
            time_unit = None

        # mass_spec_details = 13
        if measurement.mass_spec_details:
            mass_spec_type = enums_data['ProductMeasurement.MassSpecMeasurementDetails.MassSpecMeasurementType'][measurement.mass_spec_details.type]
            mass_spec_details = measurement.mass_spec_details.details 
            tic_minimum = measurement.mass_spec_details.tic_minimum_mz 
            tic_maximum = measurement.mass_spec_details.tic_maximum_mz 
            eic_masses = []
            for eic_mass in measurement.mass_spec_details.eic_masses:
                eic_masses.append(eic_mass)
        else: 
            mass_spec_type = None
            mass_spec_details = None
            tic_minimum = None
            tic_maximum = None
            eic_masses = None

        # selectivity = 14
        if measurement.selectivity:
            select_type = enums_data['ProductMeasurement.Selectivity.SelectivityType'][measurement.selectivity.type]
            selectivity = {select_type:measurement.selectivity.details}
        else: selectivity = None
        
        # wavelength = 15
        if measurement.wavelength:
            wavelength = measurement.wavelength.value
            wavelength_unit = enums_data['Wavelength.WavelengthUnit'][measurement.wavelength.units]
        else: 
            wavelength = None
            wavelength_unit = None
        
        measurement_list.append([analysis_key, measurement_type, measurement.details, measurement.uses_internal_standard, 
            measurement.is_normalized, measurement.uses_authentic_standard, compound_authentic, measurement_value, retention_time, time_unit, 
            mass_spec_type, mass_spec_details, tic_minimum, tic_maximum, eic_masses,
            selectivity, wavelength, wavelength_unit])
        
    return measurement_list

def extract_analyses(analyses):
    """
    Description: 
        Takes in a analyses and returns reaction analyses info:
            key
            type
            details 
            chmo id
            is of isolated species
            data dict
            nstrument manufacturer
            instrument last calibrated

    Algorithm:
        1. Create an empty list to hold analyses info (analyses_list)
        2. Loop through each analysis
        3. Extract and append analysis info to analyses_list
   
    Args: 
        analyses:
            Analyses of a reaction
    
    Returns: 
        list:
            A list containing reaction analyses
    """
    analyses_list = []
    data_dict = {}
    for analysis_key, analysis in analyses.items():
        analysis_type = enums_data['Analysis.AnalysisType'].get(analysis.type, 'UNKNOWN')
        for data_key, data in analysis.data.items(): 
            value = getattr(data, data.WhichOneof('kind'))
            dict_value = [value, data.description]
            data_dict.update([(data_key, dict_value)])
        analyses_list.append(
            ({'analysisKey':analysis_key,
            'analysisType':analysis_type,
            'Details':analysis.details,
            'CHMO_ID':analysis.chmo_id,
            'IsolatedSpecies':analysis.is_of_isolated_species, 
            'data':data_dict, 
            'instrumentManufacturer':analysis.instrument_manufacturer, 
            'lastCalibrated':analysis.instrument_last_calibrated
            })
        )
    return analyses_list