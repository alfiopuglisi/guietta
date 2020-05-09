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

import os
import sys
import re


# -- Project information -----------------------------------------------------

project = 'guietta'
copyright = '2020, Alfio Timothy Puglisi'
author = 'Alfio Timothy Puglisi'

# -- General configuration ---------------------------------------------------

# Mock the PyQt5 module
# Otherwise the build on readthedocs.io fails!

class QtWidgets:
    QPushButton = QLabel = QLineEdit = QCheckBox = None
    QRadioButton = QSlider = QWidget = QGridLayout = None
    QAbstractSlider = QAbstractButton = QMessageBox = None
    class QFrame:
        HLine = VLine = Sunken = None
        def setFrameShadow(self, a): pass
        def setFrameShape(self, a): pass
        def setMinimumWidth(self, a): pass
        def setFixedHeight(self, a): pass
    class QApplication:
        @staticmethod
        def instance():
            return 1    # With this, the main file will not trty
                        # to create a new one.

sys.modules['PyQt5.QtWidgets'] = QtWidgets

sys.path.insert(0, os.path.abspath('..'))
from guietta.__version__ import __version__

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.coverage',
              'sphinx.ext.napoleon',
              'sphinx.ext.napoleon',
              "sphinx.ext.intersphinx",
              ]
intersphinx_mapping = {
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None),
    # 'matplotlib': ('http://matplotlib.org/', None),
    'astropy': ('https://docs.astropy.org/en/stable/', None),
    }

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

master_doc = 'index'

# General substitutions.

# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
version = re.sub(r'\.dev-.*$', r'.dev', __version__)
release = __version__

print("%s (VERSION %s)" % (project, version))

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = "sphinx_rtd_theme"
# html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme = 'nature'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = 'py:obj'
