sphinxcontrib-multilatex
==============================================================================

|pypi-version| |pypi-downloads| |docs-status| |build-status|
|coverage-status| |pypi-license|

A Sphinx extension that allows LaTeX/PDF documents to be declared and
parameterized within reStructuredText source files.

`Sphinx`_ offers a built-in `LaTeX builder <sphinx-latex-builder>`_ which
can produce pretty PDF documents. It requires PDF documents to be declared
in the ``conf.py`` file, see the
`latex_documents setting <sphinx-latexdocs-confval>`_. That works for
simple projects, but is not flexible enough for projects which create
multiple PDFs with varying templates and parameterization.

This extension provides a new LaTeX builder which determines which PDFs
to generate from declarations in line in the reStructuredText source.
Those declarations, in the form of reST directives, allow various
parameters to be set in the LaTeX output, such as which document class
to use, custom parameters, etc.

More information is available here:

- Documentation: https://sphinxcontrib-multilatex.readthedocs.org/en/latest/
- Download: https://pypi.python.org/pypi/sphinxcontrib-multilatex
- Development: https://github.com/t4ngo/sphinxcontrib-multilatex

.. _Sphinx: http://sphinx-doc.org/

.. _sphinx-latex-builder:
   http://www.sphinx-doc.org/en/stable/builders.html#sphinx.builders.latex.LaTeXBuilder

.. _sphinx-latexdocs-confval:
   http://www.sphinx-doc.org/en/stable/config.html#confval-latex_documents

.. |docs-status| image:: https://readthedocs.org/projects/sphinxcontrib-multilatex/badge/?version=latest
    :alt: Documentation status
    :scale: 100%
    :target: https://sphinxcontrib-multilatex.readthedocs.org/en/latest/?badge=latest

.. |build-status| image:: https://travis-ci.org/t4ngo/sphinxcontrib-multilatex.svg
    :alt: Build status
    :target: https://travis-ci.org/t4ngo/sphinxcontrib-multilatex

.. |coverage-status| image:: https://coveralls.io/repos/t4ngo/sphinxcontrib-multilatex/badge.svg?branch=master&service=github
    :alt: Test coverage status
    :target: https://coveralls.io/github/t4ngo/sphinxcontrib-multilatex?branch=master

.. |pypi-version| image:: https://img.shields.io/pypi/v/sphinxcontrib-multilatex.svg
    :alt: Latest version at PyPI
    :target: https://pypi.python.org/pypi/sphinxcontrib-multilatex

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/sphinxcontrib-multilatex.svg
    :alt: Downloads from PyPI last month
    :target: https://pypi.python.org/pypi/sphinxcontrib-multilatex

.. |pypi-license| image:: https://img.shields.io/pypi/l/sphinxcontrib-multilatex.svg
    :alt: License specified at PyPI
    :target: https://pypi.python.org/pypi/sphinxcontrib-multilatex
