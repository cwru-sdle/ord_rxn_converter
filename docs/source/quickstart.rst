Quick Start Guide 
=================

This guide will get you up and running with ord_rxn_converter in minutes 

Installation
------------

.. code-block:: bash

    pip install ord_rxn_converter

Basic Usage
------------

Extract Complete Dataset
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ord_rxn_converter.dataset_module import extract_dataset

    # Load and extract all reaction data 
    data = extract_dataset("reactions.pb")

    # View available data components
    print("Available data keys:", list(data.keys()))

    # Check number of reactions
    print(f"Number of reactions: {len(data['reaction_metadata'])}")

Extract Individual components
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ord_schema.proto import dataset_pb2
    from ord_schema.message_helpers import load_message
    from ord_rxn_converter.conditions_module import extract_reaction_conditions

    # Load dataset
    dataset = load_message("reactions.pb", dataset_pb2.Dataset)

    # Extract conditions from first reaction
    conditions = extract_reaction_conditions(dataset.reactions[0].conditions)
    print(conditions.head())

Export Results
~~~~~~~~~~~~~~

.. code-block:: python

    # Save all components as CSV files
    for component, df in data.items():
        df.to_csv(f"{component}.csv", index = False)
        print(f"Saved {component}.csv with {len(df)} rows")

Next Steps
----------

* Read the full :doc: 'ord_rxn_converter' documentation
* Browse the :doc: 'modules' for detailed API reference
* Check out more examples in the main documentation