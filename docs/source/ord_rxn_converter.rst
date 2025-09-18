ORD Reaction Converter
======================

Overview
--------
The package automatically extracts all of the reactions in a dataset in Open Reaction Database to a dictionary of Pandas DataFrames which can be saved as CSV files to make a relational database. 

The structure of the Pandas DataFrames follows the ORD schema: 

1. **Dataset & reaction metadata** (provenance)
2. **Reaction identifiers** (SMILES, InChI, etc.)
3. **Reaction inputs** (reactants, reagents, solvents)
4. **Reaction setup** (vessels, automation)
5. **Reaction conditions** (temperature, pressure, stirring)
6. **Reaction notes & observations** (experimental notes)
7. **Reaction workups** (post-reaction processing)
8. **Reaction outcomes** (products and analyses)

The package also includes a utility functions module to conveniently extract all of the enum types stored in the ``.proto`` file. All columns are named according to the ORD schema. 

Installation
------------

Install from PyPI:

.. code-block:: bash

   pip install ord_rxn_converter

Or install from source:

.. code-block:: bash

   git clone https://github.com/cwru-sdle/ord_rxn_converter.git
   cd ord_rxn_converter
   pip install -e .

Quick Start
-----------

Extract an entire dataset:

.. code-block:: python

   from ord_rxn_converter.dataset_module import extract_dataset
   
   # Extract all data from a dataset file
   data = extract_dataset("example_dataset.pb")
   
   # Access different components
   print(f"Available data: {list(data.keys())}")
   print(f"Number of reactions: {len(data['reaction_metadata'])}")
   
   # Export to CSV files
   for key, df in data.items():
       df.to_csv(f"{key}.csv", index=False)

Extract individual reaction components:

.. code-block:: python

   from ord_schema.proto import dataset_pb2
   from ord_schema.message_helpers import load_message
   from ord_rxn_converter.identifiers_module import extract_reaction_identifiers
   from ord_rxn_converter.conditions_module import extract_reaction_conditions

   # Load a Dataset message from file
   dataset = load_message("example1.pb", dataset_pb2.Dataset)

   # Access first reaction in dataset
   reaction = dataset.reactions[0]

   # Extract specific components
   identifiers_df = extract_reaction_identifiers(reaction.identifiers)
   conditions_df = extract_reaction_conditions(reaction.conditions)
   
   print("Reaction identifiers:")
   print(identifiers_df.head())
   
   print("\nReaction conditions:")
   print(conditions_df.head())

API Reference
-------------

Main Functions
~~~~~~~~~~~~~~

.. autofunction:: ord_rxn_converter.dataset_module.extract_dataset

Core Modules
~~~~~~~~~~~~

Utility Functions Module
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: ord_rxn_converter.utility_functions_module
   :members: 
   :undoc-members:
   :show-inheritance:

Dataset Module
^^^^^^^^^^^^^^

.. automodule:: ord_rxn_converter.dataset_module
   :members:
   :undoc-members:
   :show-inheritance:

Metadata Module
^^^^^^^^^^^^^^^

.. automodule:: ord_rxn_converter.metadata_module
   :members:
   :undoc-members:
   :show-inheritance:

Identifiers Module
^^^^^^^^^^^^^^^^^^

.. automodule:: ord_rxn_converter.identifiers_module
   :members:
   :undoc-members:
   :show-inheritance:

Inputs Module
^^^^^^^^^^^^^

.. automodule:: ord_rxn_converter.inputs_module
   :members:
   :undoc-members:
   :show-inheritance:

Setup Module
^^^^^^^^^^^^

.. automodule:: ord_rxn_converter.setup_module
   :members:
   :undoc-members:
   :show-inheritance:

Conditions Module
^^^^^^^^^^^^^^^^^

.. automodule:: ord_rxn_converter.conditions_module
   :members:
   :undoc-members:
   :show-inheritance:

Notes & Observations Module
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: ord_rxn_converter.notes_observations_module
   :members:
   :undoc-members:
   :show-inheritance:

Workups Module
^^^^^^^^^^^^^^

.. automodule:: ord_rxn_converter.workups_module
   :members:
   :undoc-members:
   :show-inheritance:

Outcomes Module
^^^^^^^^^^^^^^^

.. automodule:: ord_rxn_converter.outcomes_module
   :members:
   :undoc-members:
   :show-inheritance:

Examples
--------

Working with Multiple Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   from ord_rxn_converter.dataset_module import extract_dataset
   
   # Process multiple dataset files
   file_list = ['dataset1.pb', 'dataset2.pb', 'dataset3.pb']
   all_data = {}
   
   for file_path in file_list:
       data = extract_dataset(file_path)
       
       # Combine data from multiple files
       for key, df in data.items():
           if key in all_data:
               all_data[key] = pd.concat([all_data[key], df], ignore_index=True)
           else:
               all_data[key] = df
   
   print(f"Total reactions processed: {len(all_data['reaction_metadata'])}")

Filtering and Analysis
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Load dataset
   data = extract_dataset("reactions.pb")
   
   # Filter reactions by temperature
   conditions = data['reaction_conditions']
   temp_conditions = conditions[conditions['condition_type'] == 'temperature']
   high_temp_reactions = temp_conditions[temp_conditions['value'] > 100]
   
   # Analyze outcomes
   outcomes = data['reaction_outcomes']
   successful_reactions = outcomes[outcomes['conversion'] > 0.8]
   
   print(f"High temperature reactions: {len(high_temp_reactions)}")
   print(f"High conversion reactions: {len(successful_reactions)}")

Notes
-----

- The package automatically handles both compressed (``.pb.gz``) and uncompressed (``.pb``) files
- Large datasets may require significant memory for processing
- All DataFrames follow consistent naming conventions based on the ORD schema
- Missing or optional fields are handled gracefully with appropriate default values

See Also
--------

- `Open Reaction Database <https://open-reaction-database.org/>`_
- `ORD Schema Documentation <https://github.com/open-reaction-database/ord-schema>`_
- `Pandas Documentation <https://pandas.pydata.org/docs/>`_