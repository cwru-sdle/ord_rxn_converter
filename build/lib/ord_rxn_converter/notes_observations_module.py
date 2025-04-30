from ord_schema.proto import dataset_pb2, reaction_pb2
from google.protobuf.message import Message
from ord_rxn_converter.utility_functions import extract_all_enums

#generate enums_data to be accessible here TODO - have importable object instead..?
enums_data = extract_all_enums(reaction_pb2)

# TODO: notes are available but observations sometimes are not available, how to make notes or observations optional? 
def extract_notes_observations(reactionID, notes, observations=None):

    """
    Description: 
        Takes in a reactionID, notes, and observations if available and returns reaction notes:
            reactionID
            is heterogeneous
            forms precipitate
            is exothermic
            offgasses,
            is sensitive to moisture
            is sensitive to oxygen
            is sensitive to light 
            safety notes
            procedure details
            and observations (if available):
            time value
            time unit 
            comment 
            image kind
            image description
            image format

    Algorithm:
        1. Check if observations are present and extract time value and unit
        2. Extract image kind from observations
        3. Add notes and observation values to a list (reaction_notes_observations)
   
    Args: 
        reactionID:
            Unique ID of a reaction 
        notes:
            Notes of a reaction
        observations:
            Observations of a reaction
    
    Returns: 
        list:
            A list containing reaction notes and observations
    """

    # optional bool is_heterogeneous = 1 
    
    # optional bool forms_precipitate = 2 

    # optional bool is_exothermic = 3 

    # optional bool offgasses = 4

    # optional bool is_sensitive_to_moisture = 5

    # optional bool is_sensitive_to_oxygen = 6

    # optional bool is_sensitive_to_light = 7

    # string safety_notes = 8 

    # string procedure_details = 9; 

    observation_list = []
    if observations: 
        for observation in observations:
            # get reaction_observation_time if exists:
            time_observation = observation.time.value 
            time_unit = enums_data['Time.TimeUnit'][observation.time.units] 
            
            # get reaction_observation_comments if exists: 
            comment = observation.comment

            # get reaction_observation_image if exists:
            if observation.image and isinstance(observation.image.WhichOneof('kind'), str): 
                image_kind = getattr(observation.image, observation.image.WhichOneof('kind'))
                description = observation.image.description
                image_format = observation.image.format
                observation_list.append({'time':time_observation, 
                                        'timeUnit':time_unit, 
                                        'commonet':observation.comment, 
                                        'imageKind':image_kind, 
                                        'imageDescription':observation.image.description, 
                                        'imageFormat':observation.image.format})
            else: pass
    else: 
        observation_list = None

    reaction_notes_observations = [reactionID, notes.is_heterogeneous, notes.forms_precipitate, notes.is_exothermic , 
        notes.offgasses, notes.is_sensitive_to_moisture, notes.is_sensitive_to_oxygen, notes.is_sensitive_to_light, 
        notes.safety_notes, notes.procedure_details, observation_list
    ]
    
    return reaction_notes_observations
