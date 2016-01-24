# -*- coding: utf-8 -*-

import sys
import os
from glob import glob

# -------------------------------------------------------------------------
# Configure extensions

extensions = [
    'sphinx.ext.autodoc',
]

# -------------------------------------------------------------------------
# General configuration

project = u'sphinxcontrib.multilatex'
copyright = u'2015, Christo Butcher'
version = '0.1'                        # The short X.Y version.
release = '0.1'                        # The full version, incl alpha/beta/rc.

templates_path = ['_templates']
source_suffix = '.txt'                 # The suffix of source filenames.
master_doc = 'index'                   # The master toctree document.
today_fmt = '%Y-%m-%d'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
keep_warnings = True                   # Keep warnings in output documents.

# -------------------------------------------------------------------------
# Configure HTML output

html_theme = 'sphinx_rtd_theme'
html_show_sourcelink = True            # Link to source from pages.
