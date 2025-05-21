ORD Reaction Converter
======================

Overview
--------
The package automatically extracts all of the reactions in a dataset in Open Reaction Database to a dictionary of Pandas DataFrames which can be saved as csv files to make a relational database. 

The structure of the Pandas DataFrames is according to the ORD schema: 

    1. dataset & reaction metadata (provenance)
    2. reaction identifiers
    3. reaction inputs
    4. reaction setup
    5. reaction conditions
    6. reaction notes & observations
    7. reaction workups
    8. reaction outcomes 

The package also includes a utility_function_module to conveniently extract all of the enum types stored in the .proto file. All of the columns are named according to the ORD schema. 

Installation
------------

.. code-block:: bash

   pip install ord_rxn_converter

Usage
-----

Brief examples of how to use the package.

.. code-block:: python

   from ord_schema.proto import reaction_pb2
   from ord_schema.proto import dataset_pb2
   from ord_schema.message_helpers import load_message

   from ord_rxn_converter.identifiers_module import extract_reaction_identifiers
   from ord_rxn_converter.conditions_module import extract_reaction_conditions

   # Assume file_list is a list of input .pb files
   file_list = ['example1.pb', 'example2.pb']

   # Load a Dataset message from file
   dataset = load_message(file_list[1], dataset_pb2.Dataset)

   # Access first reaction in dataset
   reaction = dataset.reactions[0]

   # View reaction identifiers
   extract_reaction_identifiers(reaction.identifiers)

   # View reaction conditions
   extract_reaction_conditions(reaction.conditions)

API Reference
-------------

Main Module
~~~~~~~~~~~

.. automodule:: ord_rxn_converter
   :members:
   :undoc-members:
   :show-inheritance:

Utility Functions Module
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: ord_rxn_converter.utility_functions_module
   :members: 
   :undoc-members:
   :show-inheritance:

Dataset Module
~~~~~~~~~~~~~~

.. automodule:: ord_rxn_converter.dataset_module
   :members: extract_dataset
   :undoc-members:
   :show-inheritance:

Metadata Module
~~~~~~~~~~~~~~~

.. automodule:: ord_rxn_converter.metadata_module
   :members:
   :undoc-members:
   :show-inheritance:

Identifiers Module
~~~~~~~~~~~~~~~~~~

.. automodule:: ord_rxn_converter.identifiers_module
   :members:
   :undoc-members:
   :show-inheritance:

Inputs Module
~~~~~~~~~~~~~

.. automodule:: ord_rxn_converter.inputs_module
   :members:
   :undoc-members:
   :show-inheritance:

Setup Module
~~~~~~~~~~~~

.. automodule:: ord_rxn_converter.setup_module
   :members:
   :undoc-members:
   :show-inheritance:

Conditons Module
~~~~~~~~~~~~~~~~

.. automodule:: ord_rxn_converter.conditions_module
   :members:
   :undoc-members:
   :show-inheritance:

Notes & Observations Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: ord_rxn_converter.notes_observations_module
   :members:
   :undoc-members:
   :show-inheritance:

Workups Module
~~~~~~~~~~~~~~

.. automodule:: ord_rxn_converter.workups_module
   :members:
   :undoc-members:
   :show-inheritance:

Outcomes Module
~~~~~~~~~~~~~~~
.. automodule:: ord_rxn_converter.outcomes_module
   :members:
   :undoc-members:
   :show-inheritance: