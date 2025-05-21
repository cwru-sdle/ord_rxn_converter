# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add the source code directory to the Python path
sys.path.insert(0, os.path.abspath('/home/hls92/CSE_MSE_RXF131/cradle-members/mds3/hls92/kg_chem_synthesis/ord_rxn_converter/src'))

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ORD Reaction Converter'
copyright = '2025, Quynh D. Tran, Ethan Tobey, Holly Schreiber, Laura S. Bruckman, Roger H. French'
author = 'Quynh D. Tran, Ethan Tobey, Holly Schreiber, Laura S. Bruckman, Roger H. French'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',          # ESSENTIAL: This enables automodule directives
    'sphinx.ext.viewcode',         # Add source code links
    'sphinx.ext.napoleon',         # Support for Google/NumPy style docstrings
    'sphinx.ext.autosummary',      # Generate summary tables
]

# Autodoc configuration
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Napoleon settings for your docstring style
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
