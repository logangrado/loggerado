# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath(".."))  # Ensure Sphinx finds your package


project = "loggerado"
copyright = "2025, Logan Grado"
author = "Logan Grado"
release = "0.3.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # Auto-generate API docs from docstrings
    "sphinx.ext.napoleon",  # Support Google/NumPy-style docstrings
    "sphinx.ext.autosummary",  # Auto-generate function/method summaries
    "sphinx.ext.viewcode",  # Add links to source code
    "sphinx_autodoc_typehints",  # Show type hints in docs
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = []


autosummary_generate = True
autodoc_member_order = "bysource"  # Preserve function order
napoleon_google_docstring = True  # Support Google-style docstrings
napoleon_numpy_docstring = False  # Disable NumPy-style docstrings


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
