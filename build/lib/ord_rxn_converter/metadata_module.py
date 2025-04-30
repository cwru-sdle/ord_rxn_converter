# %% 
import re
from ord_schema.message_helpers import load_message, write_message
from ord_schema.proto import dataset_pb2, reaction_pb2
from google.protobuf.message import Message

def extract_dataset_metadata(dataset):

    """
    Description: 
        Takes in a dataset and returns its metadata:
            ID
            ORD ID
            Name
            Description

    Algorithm:
        1. Create a unique dataset ID by splitting the ORD ID at '-' and replacing the prefix as 'mds_dataset-' (this signifies the dataset is in MDS database and not ORD)
        2. Extract the dataset name and description
        3. Add the unique ID, ORD ID, name, and description to a list (dataset_metadata)
   
    Args: 
        dataset:
            A dataset from ORD that has been converted to a Python object (which has a type of a message in Google Protocol Buffers) instead of a message in Google Protocol Buffer. 
    
    Returns: 
        list:
            A list containing dataset metadata
    """

    dsID = re.split('-', dataset.dataset_id) 
    datasetID = f"mds_dataset-{dsID[1]}"
    ORDdsID = dataset.dataset_id 

    dsName = dataset.name
    dsDes = dataset.description

    dataset_metadata = [datasetID, ORDdsID, dsName, dsDes]

    return dataset_metadata

def extract_reaction_metadata(provenance, reactionID):

    """
    Description: 
        Takes in a Protobuf message (PROVENANCE) and returns reaction provenance:
            reactionID
            doi (string)
            patent (string)
            publicationURL (string)
            createdTime (time?)
            createdPerson (string of ORCiD)
            modified time: use flattened list of modification times (since there can be multiple)
            modified person: use flattened list of people (since there can be multiple, corresponding with modification times)
    

            reactionID
            orcid
            city
            experiment start
            doi (string)
            patent (string)
            publication url (string)
            created time value (time?)
            created person orcid (string)
            created details  
            modified times: use flattened list of modification times (since there can be multiple)
            modified people: use flattened list of people (since there can be multiple, corresponding with modification times)
        and person metadata:
            orcid
            username
            name
            organization
            email

    Algorithm:
        1. From input provenance, extract reaction provenance data
        2. Create an empty list to hold person metadata
        3. Extract created person metadata and append to person_metadata list
        4. Extract a list of modified times
        5. Extract modified orcids and person metadata and append to person_metadata list
        6. Add provenance data, modified times, and modified orcids to provenance_data list
    
    Args: 
        provenance:
            Reaction provenance from ORD
    
    Returns: 
        list:
            List containing reaction metadata (provenance and person)
    """
    
    person_metadata = []

    # experimenter = 1
    experimenter = provenance.experimenter
    person_metadata.append([experimenter.username, experimenter.name, experimenter.orcid, experimenter.organization, experimenter.email])
    
    # city = 2

    # experiment_start = 3

    # doi = 4

    # patent = 5

    # publication_url = 6
    
    # record_created = 
    created_time = provenance.record_created.time.value
    person = provenance.record_created.person
    person_metadata.append([person.username, person.name, person.orcid, person.organization, person.email])

    modified_times_list = []
    modified_person_orcid_list = []

    for record in provenance.record_modified:
        modified_times_list.append(record.time.value)
        modified_person_orcid_list.append(record.person.orcid)
    modified_people = ", ".join(modified_person_orcid_list)
    modified_times = ", ".join(modified_times_list)

    for record in provenance.record_modified:
        person = record.person
        person_metadata.append([person.orcid, person.username, person.name, person.organization, person.email])
        
    provenance_data = [reactionID, provenance.experimenter.orcid, provenance.city, provenance.experiment_start, provenance.doi, provenance.patent, provenance.publication_url, 
        provenance.record_created.time.value, provenance.record_created.person.orcid, provenance.record_created.details, 
        modified_times, modified_people]
   
    return provenance_data, person_metadata
