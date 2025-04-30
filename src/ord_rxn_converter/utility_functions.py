from ord_schema.proto import dataset_pb2, reaction_pb2
from google.protobuf.message import Message

# =============================================================================
#               FUNCTIONS TO EXTRACT ENUMS FROM ALL MESSAGE TYPES
# =============================================================================

# Get all of enum field names and numbers: 

def extract_enums_from_message(descriptor, parent_name=''):
    """Recursively extract enums from messages and nested messages."""

    #ensure descriptor is not None
    if not descriptor:
        return {}

    enums = {}

    # Get enums within this message
    for enum_type in descriptor.enum_types:
        full_enum_name = f'{parent_name}.{enum_type.name}' if parent_name else enum_type.name
        enums[full_enum_name] = {v.number: v.name for v in enum_type.values}

    # Recursively check nested messages
    for nested_type in descriptor.nested_types:
        nested_enums = extract_enums_from_message(nested_type, f"{parent_name}.{nested_type.name}" if parent_name else nested_type.name)
        enums.update(nested_enums)

    return enums

#should be called by public - gets full enums_data set from proto_module
def extract_all_enums(proto_module):
    """Extract enums from all message types in the proto module."""
    all_enums = {}

    for name in dir(proto_module):
        obj = getattr(proto_module, name)

        # Check if it's a message type
        if isinstance(obj, type) and hasattr(obj, 'DESCRIPTOR'):
            descriptor = obj.DESCRIPTOR
            message_enums = extract_enums_from_message(descriptor, descriptor.name)
            
            if message_enums:
                all_enums.update(message_enums)

    return all_enums