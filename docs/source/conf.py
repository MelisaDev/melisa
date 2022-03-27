# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

import sys
import os

sys.path.append(os.path.abspath("../.."))
sys.path.append(os.path.abspath('extensions'))


project = 'Melisa'
copyright = '2022, MelisaDev'
author = 'MelisaDev'

# The full version, including alpha/beta/rc tags
release = '0.0.1a'


# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx_design',
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.extlinks",
    "sphinxcontrib_trio",
    "attributable"
]


autodoc_default_options = {
    'members': True,
    'show-inheritance': True
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

add_module_names = False

exclude_patterns = []

intersphinx_mapping = {
    "py": ("https://docs.python.org/3", None),
    "aiohttp": ("https://docs.aiohttp.org/en/stable/", None),
}


# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'
html_theme_options = {
    "sidebar_hide_name": True,
}
pygments_style = 'monokai'
default_dark_mode = True
html_static_path = ['_static']
html_css_files = ["custom.css"]

rst_prolog = """
.. |coro| replace:: This function is a |coroutine_link|_.
.. |maybecoro| replace:: This function *could be a* |coroutine_link|_.
.. |coroutine_link| replace:: *coroutine*
.. _coroutine_link: https://docs.python.org/3/library/asyncio-task.html#coroutine
"""
