"""
The ``directive`` module
============================================================================

"""


import re
import collections
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx import addnodes
from sphinx.locale import _
from sphinx.util import texescape


#===========================================================================
# Node types

class latex_document(nodes.General, nodes.Element):
    pass


#===========================================================================
# Utility classes

class DefaultDict(dict):

    def __init__(self, default):
        dict.__init__(self)
        self.default = default

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return self.default

    def __bool__(self):
        return True

    __nonzero__ = __bool__


#===========================================================================
# Directives

class LatexDocumentDirective(Directive):

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = DefaultDict(lambda value: value)
    has_content = True

    latex_macro_name_re = re.compile(r"^[a-zA-Z]+$")

    def run(self):
        env = self.state.document.settings.env
        filename = self.arguments[0]

        node = latex_document()
        node["multilatex-filename"] = self.sanitize_filename(filename)
        node["multilatex-content"] = self.sanitize_content(self.content)
        options, variables = self.sanitize_options(self.options)
        node["multilatex-options"] = options
        node["multilatex-variables"] = variables
        return [node]

    def sanitize_filename(self, filename):
        return filename

    def sanitize_options(self, input):
        standard_option_defaults = {
            "title":    "Untitled document",
            "author":   "Unknown author",
            "docclass": "manual",
        }
        options = dict(input)
        standard_options = {}
        for name, default in standard_option_defaults.items():
            value = options.pop(name, default)
            standard_options[name] = value

        latex_variables = {}
        for name, value in options.items():
            # TeX macro names that are more than 1 character long consist
            # solely of lowercase and uppercase letters.
            # Source: http://www.tex.ac.uk/FAQ-whatmacros.html
            if not self.latex_macro_name_re.match(name):
                raise Exception("Invalid LaTeX macro name: {0!r}"
                                .format(name))
            latex_variables[name] = value.translate(texescape.tex_replace_map)

        return standard_options, latex_variables

    def sanitize_content(self, content):
        return content
