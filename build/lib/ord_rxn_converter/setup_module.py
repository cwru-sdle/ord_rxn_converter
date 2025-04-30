# import requirements: 
from ord_schema.proto import dataset_pb2, reaction_pb2
from google.protobuf.message import Message
import pandas as pd
from ord_rxn_converter.utility_functions import extract_all_enums

#generate enums_data to be accessible here TODO - have importable object instead..?
enums_data = extract_all_enums(reaction_pb2)

def extract_reaction_setup(setup, reactionID):

    """
    Description: 
        Takes in a reaction and returns reaction setup:
            vessel
            vessel material
            vessel volume
            vessel volume unit
            vessel preparation
            vessel attachment
            is automated?
            automation platform
            automation code
            reaction environment
    Algorithm:
        1. Initialize an empty list to hold reaction provenance
        3. Extract reaction setup
        4. From setup, preparation, and attachment, extract reaction setup data
        5. Append these values to the reaction provenance list
        6. Create a dataframe placing each reaction provenance into its corresponding column
    Args: 
        reaction:
            A reaction from ORD
    Returns: 
        dataframe:
            Dataframe containing the reaction provenance of a reaction
    """
    
    vessel = enums_data['Vessel.VesselType'][setup.vessel.type]
    vessel_material = enums_data['VesselMaterial.VesselMaterialType'][setup.vessel.material.type]
    attach_dict = {} 
    prep_dict = {}
    if hasattr(setup.vessel, 'preparation') and setup.vessel.preparations:
        for preparation in setup.vessel.preparations: 
            vessel_preparation = enums_data['VesselPreparation.VesselPreparationType'][preparation.type]
            prep_dict.update([(vessel_preparation, preparation.details)])
    else: prep_dict = None
    
    if setup.vessel.attachments:
        for attachment in setup.vessel.attachments:  
            vessel_attachment = enums_data['VesselAttachment.VesselAttachmentType'][attachment.type]
            attach_dict.update(zip(vessel_attachment, attachment.details))
    else: attach_dict = None

    if setup.vessel.volume:
        vessel_volume = setup.vessel.volume.value
        volume_unit = enums_data['Volume.VolumeUnit'][setup.vessel.volume.units]
    else: 
        vessel_volume = None   
        volume_unit = None

    is_automated = setup.is_automated if setup.is_automated else None
    automation_platform = setup.automation_platform if setup.automation_platform else None
    automation_code = ", ".join(f"{key}: {value}" for key, value in setup.automation_code.items()) 
    
    reaction_environment = enums_data['VesselAttachment.VesselAttachmentType'][setup.environment.type] if setup.environment else None

    reaction_setup = [reactionID, vessel, vessel_material, vessel_volume, volume_unit, prep_dict, attach_dict, is_automated, automation_platform, automation_code, reaction_environment]

    return reaction_setup