Modules
=======

This section provides detailed documentation for all modules in the ord_rxn_converter package.

.. toctree::
   :maxdepth: 4
   :caption: Package Modules:

   ord_rxn_converter

Module Overview
---------------

The ord_rxn_converter package is organized into the following main modules:

**Core Processing Modules:**

* ``dataset_module`` - Main entry point for extracting entire datasets
* ``metadata_module`` - Dataset and reaction metadata extraction
* ``identifiers_module`` - Chemical identifiers (SMILES, InChI, etc.)
* ``inputs_module`` - Reactants, reagents, and solvents
* ``conditions_module`` - Temperature, pressure, and environmental conditions
* ``setup_module`` - Reaction vessels and automation setup
* ``workups_module`` - Post-reaction processing steps
* ``outcomes_module`` - Products and reaction analyses
* ``notes_observations_module`` - Experimental notes and observations

**Utility Modules:**

* ``utility_functions_module`` - Helper functions and enum extractors

Each module contains specialized functions for extracting and converting specific components of the ORD schema into pandas DataFrames.