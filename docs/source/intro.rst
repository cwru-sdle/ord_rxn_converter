Introduction
============

``ord_rxn_converter`` is a Python package designed to streamline the transformation of chemical reaction data from the Open Reaction Database (ORD) format into structured datasets suitable for downstream machine learning and data analysis tasks. It provides modular tools for parsing, extracting, and converting complex reaction schema into interpretable tables, lists, and dictionaries that can be easily ingested by models or used in exploratory chemical data analysis.

The library is organized into specialized modules that handle different components of the reaction schema — including identifiers, inputs, conditions, setup, workups, outcomes, and notes/observations — as well as utility functions for key operations and dataset generation. The package is structured for clarity and extendibility, enabling researchers to adapt it to varying needs in computational chemistry or cheminformatics pipelines.

The codebase is written in Python 3 and supports integration into Jupyter notebooks, standalone scripts, or larger ML pipelines for tasks such as property prediction, reaction classification, or synthesis planning.

Key Features
************

* **Comprehensive Data Extraction**: Converts all major ORD schema components into pandas DataFrames
* **Modular Design**: Each reaction component handled by specialized modules for clarity and maintainability  
* **Batch Processing**: Process entire datasets or individual reactions as needed
* **ML-Ready Output**: Structured tabular data suitable for machine learning pipelines
* **Schema Compliance**: Column names and structure follow ORD schema conventions
* **Format Flexibility**: Handles both compressed (``.pb.gz``) and uncompressed (``.pb``) protobuf files

Workflow Overview
*****************

The typical workflow with ''ord_rxn_converter'' involves: 

1. **Loading**: Import ORD dataset files in protobuf format
2. **Extraction**: Use the main ``extract_dataset()`` function or individual module functions
3. **Processing**: Work with the resulting pandas DataFrames for analysis or ML
4. **Export**: Save structured data as CSV files for use in other tools

.. code-block:: python

   from ord_rxn_converter.dataset_module import extract_dataset
   
   # Extract entire dataset
   data = extract_dataset("my_reactions.pb")
   
   # Access specific components
   conditions = data["reaction_conditions"]
   outcomes = data["reaction_outcomes"]
   
   # Export for further analysis
   conditions.to_csv("conditions.csv")

Motivation
**********

Chemical reaction data is often stored in highly nested or semi-structured formats that are difficult to work with directly in data science workflows. The Open Reaction Database provides a valuable standardized format, but researchers and developers often require a flat, structured format with clean fields to build models or perform analysis.

``ord_rxn_converter`` was developed to automate and standardize this transformation process. It allows users to systematically convert the complex data in ORD protobuf files into simplified Python structures (lists, dictionaries, Pandas DataFrames), reducing time spent on preprocessing and improving reproducibility in ML workflows. By modularizing the conversion process, the package promotes clarity, flexibility, and easier debugging.

The project originated as part of a broader effort to accelerate machine learning-driven synthesis planning by improving the usability of publicly available chemical data.

Use Cases
*********

This package is particularly useful for:

* **Machine Learning Practitioners** building models for reaction prediction or optimization
* **Cheminformatics Researchers** analyzing large-scale reaction datasets  
* **Chemical Engineers** studying reaction conditions and outcomes across datasets
* **Data Scientists** working with chemical reaction data in exploratory analysis
* **Software Developers** building tools that consume ORD data


Limitations
***********

- The package currently assumes that input ORD data conforms closely to the expected schema. It may require modification or additional error handling for incomplete or non-standard records.

- Complex reaction pathways involving multi-step synthesis or overlapping outcomes may not be fully supported in this version.

- The current modules focus primarily on extraction rather than validation or correction of chemical information. Users are advised to preprocess or sanitize their data before applying the conversion tools if needed.

- While the package is modular, it is not yet fully abstracted for plug-and-play use in non-ORD schemas. Adapting it to other chemical data formats (e.g., USPTO, Reaxys) would require extension.

- The project is in active development, and interface or function-level changes may occur in future versions.

Getting Started
***************

To get started with ``ord_rxn_converter``, check out the :doc:`ord_rxn_converter` page for installation instructions and usage examples, or browse the :doc:`modules` section for detailed API documentation.

For a quick start, try:

.. code-block:: bash

   pip install ord_rxn_converter

.. code-block:: python

   from ord_rxn_converter.dataset_module import extract_dataset
   result = extract_dataset("your_dataset.pb")
   print(f"Extracted {len(result)} data components")