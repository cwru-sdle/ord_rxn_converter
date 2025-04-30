# import requirements: 
from ord_schema.proto import dataset_pb2, reaction_pb2
from google.protobuf.message import Message
from rdkit import Chem
from rdkit.Chem import AllChem
from ord_rxn_converter.utility_functions import extract_all_enums

#generate enums_data to be accessible here TODO - have importable object instead..?
enums_data = extract_all_enums(reaction_pb2)

def extract_reaction_identifiers(identifiers, reactionID: str) -> list:
    """ 
    Description: Takes in reaction identifiers and reaction ID and returns reaction identifiers:
        reactionID
        smiles
        cxsmiles
        rdfile
        rinchi
        reaction type
        unspecified
        custom
        details
        is mapped: True if the identifier is mapped atom-by-atom
   
    Algorithm: 
        1. Initialize an empty list to hold reaction identifiers (reaction_identifier)
        2. Loop through identifiers
        3. Extract and append identifier type, value, details, and is_mapped to reaction_identifier
   
    Args:
        identifiers: 
            Reaction identifiers of a reaction
        reactionID: 
            Unique ID of a reaction 
   
    Returns: 
        list: 
            A list containing reaction identifiers of a reaction
    """

    # Initiate empty lists to store identifier type, details, value, and is_mapped.
    identifier_type= []
    identifier_details = []
    identifier_value = []
    identifier_mapped = []

    for identifier in identifiers: 
        # append lists
        identifier_type.append(enums_data['ReactionIdentifier.ReactionIdentifierType'][identifier.type])
        identifier_value.append(identifier.value)
        identifier_details.append(identifier.details)
        identifier_mapped.append(identifier.is_mapped)

    # create a dictionary of identifier types and values and a dictionary of identifier types and details
    identifier_dict = dict(zip(identifier_type, identifier_value))
    details_dict = dict(zip(identifier_type, identifier_details))
    mapped_dict = dict(zip(identifier_type, identifier_mapped))

    # extract values
    unspecified = identifier_dict.get('UNSPECIFIED')
    custom = identifier_dict.get('CUSTOM')
    reaction_smiles = identifier_dict.get('REACTION_SMILES')
    reaction_cxsmiles = identifier_dict.get('REACTION_CXSMILES') 
    rdfile = identifier_dict.get('RDFILE')  
    rinchi = identifier_dict.get('RINCHI')
    reaction_type = identifier_dict.get('REACTION_TYPE')

    reaction_identifiers = [reactionID, reaction_smiles, reaction_cxsmiles, rdfile, rinchi, reaction_type, unspecified, custom, details_dict, mapped_dict]

    return reaction_identifiers

from rdkit import Chem

def extract_compound_identifiers(compound_identifiers):

    """ 
    Description: Takes in compound identifiers and returns compound identifiers:
        name
        smiles
        inchi
        inchi key
        cxsmiles
   
    Algorithm: 
        1. Initialize empty lists to hold compound identifier type, details, and value
        2. Loop through identifiers
        3. Extract and append identifier type, details, and value to corresponding lists
        4. Create a dictionary of identifier type and value
        5. Extract identifier type and value pairs from the dictionary
        6. Generate missing values from known values using RDKit
    
    Args:
        identifiers: 
            Compound identifiers of a reaction
   
    Returns: 
        list: 
            A list containing compound identifiers of a reaction
    """
    
    identifier_type_list = []
    identifier_details_list = []
    identifier_value_list = []

    for identifier in compound_identifiers:
        identifier_type = enums_data['CompoundIdentifier.CompoundIdentifierType'][identifier.type]
        identifier_type_list.append(identifier_type)
        identifier_value_list.append(identifier.value)
        identifier_details_list.append(identifier.details)

    identifier_dict = dict(zip(identifier_type_list, identifier_value_list))

    # Safely access keys - get() ensures they return None if they do not exist
    inchi_key = identifier_dict.get('INCHI_KEY')
    inchi = identifier_dict.get('INCHI')
    smiles = identifier_dict.get('SMILES')
    cxsmiles = identifier_dict.get('CXSMILES')

    if inchi_key is None and inchi:
        rdkit_mol = Chem.MolFromInchi(inchi)
        if rdkit_mol:
            identifier_dict['INCHI_KEY'] = Chem.MolToInchiKey(rdkit_mol)
            inchi_key = identifier_dict.get('INCHI_KEY')

    elif inchi_key is None and inchi is None and smiles:
        rdkit_mol = Chem.MolFromSmiles(smiles)
        if rdkit_mol:
            identifier_dict['INCHI'] = Chem.MolToInchi(rdkit_mol)
            identifier_dict['INCHI_KEY'] = Chem.MolToInchiKey(rdkit_mol)
            inchi_key = identifier_dict.get('INCHI_KEY')

    if smiles and cxsmiles is None:
        rdkit_mol = Chem.MolFromSmiles(smiles)
        identifier_dict['CXSMILES'] = Chem.MolToCXSmiles(rdkit_mol)
    
    else: pass

    return inchi_key, identifier_dict

def generate_compound_table (compound_identifiers):

    """ 
    Description: Takes in compound identifiers and returns all compound identifier types and values:
        inchi key
        smiles
        inchi
        upac_name
        name
        cas number
        pubchem cid
        chemspider id
        cxsmiles
        unspecified
        custom
        molblock
        xyz
        uniprot id
        pdb_id
        amino acid sequence
        helm
        mdl
        details
   
    Algorithm: 
        1. Initialize empty lists to hold compound identifier type, details, and value
        2. Loop through identifiers
        3. Extract and append identifier type, details, and value to corresponding lists
        4. Create a dictionary of identifier type and value
        5. Create a dictionary of identifier type and details
        6. Check for inchi key and generate if not present
        7. Extract comopund identifier values and add to list
    
    Args:
        identifiers: 
            Compound identifiers of a reaction
   
    Returns: 
        list: 
            A list containing compound identifiers of a reaction
    """

    identifier_type_list = []
    identifier_details_list = []
    identifier_value_list = []

    for identifier in compound_identifiers:
        identifier_type = enums_data['CompoundIdentifier.CompoundIdentifierType'][identifier.type]

        identifier_type_list.append(identifier_type)
        identifier_value_list.append(identifier.value)
        identifier_details_list.append(identifier.details)

    identifier_dict = dict(zip(identifier_type_list, identifier_value_list))
    details_dict = dict(zip(identifier_type_list, identifier_details_list))

    if identifier_dict.get('INCHI_KEY') is None and identifier_dict.get('INCHI'): 
        inchi = identifier_dict.get('INCHI')
        rdkit_mol = Chem.MolFromInchi(inchi)
        identifier_dict['INCHI_KEY'] = Chem.MolToInchiKey(rdkit_mol)
    
    elif identifier_dict.get('INCHI_KEY') is None and identifier_dict.get('INCHI') is None:
        smiles_string = identifier_dict.get('SMILES')
        rdkit_mol = None
        identifier_dict['INCHI'] = None
        identifier_dict['INCHI_KEY'] = None
        if smiles_string:  #Chem.MolFromSmiles errors if passed None
            rdkit_mol = Chem.MolFromSmiles(smiles_string)
            identifier_dict['INCHI'] = Chem.MolToInchi(rdkit_mol)
            identifier_dict['INCHI_KEY'] = Chem.MolToInchiKey(rdkit_mol)

    else: pass

    if identifier_dict.get('SMILES') and identifier_dict.get('CXSMILES') is None: 
        smiles_string = identifier_dict.get('SMILES')
        rdkit_mol = None
        if smiles_string:  #Chem.MolFromSmiles errors if passed None
            rdkit_mol = Chem.MolFromSmiles(smiles_string)
        identifier_dict['CXSMILES'] = Chem.MolToCXSmiles(rdkit_mol) 
    
    else: pass

    # extract values
    inchi_key = identifier_dict.get('INCHI_KEY')
    smiles = identifier_dict.get('SMILES')
    inchi = identifier_dict.get('INCHI')
    iupac_name = identifier_dict.get('IUPAC_NAME')
    name = identifier_dict.get('NAME')
    cas_number = identifier_dict.get('CAS_NUMBER')
    pubchem_cid = identifier_dict.get('PUBCHEM_CID')
    chemspider_id = identifier_dict.get('CHEMSPIDER_ID')
    cxsmiles = identifier_dict.get('CXSMILES')
    unspecified = identifier_dict.get('UNSPECIFIED')
    custom = identifier_dict.get('CUSTOM')
    molblock = identifier_dict.get('MOLBLOCK')
    xyz = identifier_dict.get('XYZ')
    uniprot_id = identifier_dict.get('UNIPROT_ID')
    pdb_id = identifier_dict.get('PDB_ID')
    amino_acid_sequence = identifier_dict.get('AMINO_ACID_SEQUENCE')
    helm = identifier_dict.get('HELM')
    mdl = identifier_dict.get('MDL')

    compound_identifiers = [inchi_key, smiles, inchi, iupac_name, name, cas_number, pubchem_cid, chemspider_id, cxsmiles, unspecified, custom, molblock, xyz, uniprot_id, pdb_id, amino_acid_sequence, helm, mdl]

    #TODO - figure out what to do with details_dict

    return compound_identifiers
