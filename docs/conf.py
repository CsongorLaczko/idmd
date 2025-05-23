import os
import sys

# -- Path setup -----------------------------------------------------
sys.path.insert(0, os.path.abspath(".."))  # project root

# -- Project information --------------------------------------------
project = "idmd"
author = "Bence Gercuj, Csongor Loránd Laczkó, Richárd Bence Rózsa"
release = "0.0.2"

# -- General configuration ------------------------------------------
extensions = [
    "sphinx.ext.autodoc",  # Core Sphinx library for auto html doc generation from docstrings
    "sphinx.ext.autosummary",  # Create neat summary tables for modules/classes/methods etc
    "sphinx.ext.viewcode",  # Add a link to the Python source code for classes, functions etc.
    "sphinx_autodoc_typehints",  # Automatically document param types (less noise in class signature)
    "myst_parser",
]

autosummary_generate = True  # Turn on sphinx.ext.autosummary
autoclass_content = "both"  # Add __init__ doc (ie. params) to class summaries
set_type_checking_flag = True  # Enable 'expensive' imports for sphinx_autodoc_typehints

templates_path = ["_templates"]
html_extra_path = ["images"]

# -- Options for HTML output ----------------------------------------
# on_rtd is whether on readthedocs.org, this line of code grabbed from docs.readthedocs.org...

# on_rtd = os.environ.get("READTHEDOCS", None) == "True"
# if not on_rtd:  # only import and set the theme if we're building docs locally
#     import sphinx_rtd_theme
#     html_theme = "sphinx_rtd_theme"
#     html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
# html_css_files = ["readthedocs-custom.css"] # Override some CSS settings

html_theme = "sphinx_rtd_theme"

html_logo = "images/idmd_icon.png"
html_theme_options = {
    "logo_only": True,
}
