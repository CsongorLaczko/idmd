# Configuration file for the Sphinx documentation builder.

# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath("../idmd"))


# -- Project information -----------------------------------------------------

project = "idmd"
author = "Bence Gercuj, Csongor Loránd Laczkó, Richárd Bence Rózsa"


# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    'sphinx.ext.autosummary',
]

autosummary_generate = True

def run_apidoc(_):
    from sphinx.ext.apidoc import main
    import os
    import shutil

    src_dir = os.path.abspath('../idmd')
    output_dir = os.path.abspath('./generated')

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    main([
        '--force',
        '--no-toc',
        '--separate',
        '-o', output_dir, src_dir, 
        '**/tests/*',  # optionally exclude tests
    ])

def setup(app):
    app.connect('builder-inited', run_apidoc)

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
