# This is the README for the ord_rxn_converter package

## Introduction

`ord_rxn_converter` is a Python package designed to streamline the transformation of chemical reaction data from the Open Reaction Database (ORD) format into structured datasets suitable for downstream machine learning and data analysis tasks. It provides modular tools for parsing, extracting, and converting complex reaction schema into interpretable tables, lists, and dictionaries that can be easily ingested by models or used in exploratory chemical data analysis.

The library is organized into specialized modules that handle different components of the reaction schema — including identifiers, inputs, conditions, setup, workups, outcomes, and notes/observations — as well as utility functions for key operations and dataset generation. The package is structured for clarity and extendibility, enabling researchers to adapt it to varying needs in computational chemistry or cheminformatics pipelines.

The codebase is written in Python 3 and supports integration into Jupyter notebooks, standalone scripts, or larger ML pipelines for tasks such as property prediction, reaction classification, or synthesis planning.

## Motivation

Chemical reaction data is often stored in highly nested or semi-structured formats that are difficult to work with directly in data science workflows. The Open Reaction Database provides a valuable standardized format, but researchers and developers often require a flat, structured format with clean fields to build models or perform analysis.

`ord_rxn_converter` was developed to automate and standardize this transformation process. It allows users to systematically convert the complex data in ORD protobuf files into simplified Python structures (lists, dictionaries, Pandas DataFrames), reducing time spent on preprocessing and improving reproducibility in ML workflows. By modularizing the conversion process, the package promotes clarity, flexibility, and easier debugging.

The project originated as part of a broader effort to accelerate machine learning-driven synthesis planning by improving the usability of publicly available chemical data.

## Limitations

- The package currently assumes that input ORD data conforms closely to the expected schema. It may require modification or additional error handling for incomplete or non-standard records.

- Complex reaction pathways involving multi-step synthesis or overlapping outcomes may not be fully supported in this version.

- The current modules focus primarily on extraction rather than validation or correction of chemical information. Users are advised to preprocess or sanitize their data before applying the conversion tools if needed.

- While the package is modular, it is not yet fully abstracted for plug-and-play use in non-ORD schemas. Adapting it to other chemical data formats (e.g., USPTO, Reaxys) would require extension.

- The project is in active development, and interface or function-level changes may occur in future versions.

## ord_rxn_converter
### This is a package repo.

## Repo Owner: Quynh D. Tran
### Purpose of this repo: Extract chemical reaction data from ORD schema (serialized in Google Protocol Buffers) into RDB and RDF triples

[Case Western Reserve University, SDLElab] [1]

[1]: http://sdle.case.edu

# Python package documentation
https://sphinx-rtd-tutorial.readthedocs.io/en/latest/index.html

Testing CI/CD