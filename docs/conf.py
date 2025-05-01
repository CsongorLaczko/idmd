import os
import sys
import shutil
import subprocess

# -- Path setup -----------------------------------------------------
sys.path.insert(0, os.path.abspath(".."))  # project root
sys.path.insert(0, os.path.abspath("../idmd"))  # your package

# -- Project information --------------------------------------------
project = "idmd"
author = "Bence Gercuj, Csongor Loránd Laczkó, Richárd Bence Rózsa"

# -- General configuration ------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
]

autosummary_generate = True  # Needed for autosummary

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output ----------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Autodoc: include both class docstring and __init__ docstring ---
autoclass_content = "both"

# -- Sphinx-apidoc automation ---------------------------------------

def run_apidoc(app):
    """Generate .rst files from source modules using sphinx-apidoc."""
    src_dir = os.path.abspath("../idmd")
    output_dir = os.path.abspath("generated")

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # Run sphinx-apidoc using subprocess for RTD compatibility
    subprocess.run([
        sys.executable,
        "-m",
        "sphinx.ext.apidoc",
        "-f",             # overwrite
        "-o", output_dir, # output dir
        src_dir           # source dir
    ], check=True)

def setup(app):
    app.connect("builder-inited", run_apidoc)
