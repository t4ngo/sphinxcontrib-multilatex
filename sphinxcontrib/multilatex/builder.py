"""
The ``builder`` module
============================================================================

"""


import os.path
from docutils.io import FileOutput
from docutils.frontend import OptionParser
from sphinx.builders.latex import LaTeXBuilder
from sphinx.writers.latex import LaTeXWriter, LaTeXTranslator
from .directive import latex_document


#===========================================================================
# Translator class

class MultiLatexTranslator(LaTeXTranslator):

    def __init__(self, document, builder):
        LaTeXTranslator.__init__(self, document, builder)

        variables = document.settings.multilatex_variables
        lines = []
        for name, value in variables.items():
            lines.append("\\newcommand{{\\{0}}}{{{1}}}"
                         .format(name, value))
        self.elements["preamble"] += "\n".join(lines)
        print "----------------------------------------"
        print self.elements["preamble"]



#===========================================================================
# Builder class

class MultiLatexBuilder(LaTeXBuilder):

    name = "multilatex"
    format = "latex"

    def init(self):
        self.translator_class = MultiLatexTranslator
        super(MultiLatexBuilder, self).init()

    def write(self, *ignored):
        print "All docs:", self.env.all_docs
        for docname in self.env.all_docs.keys():
            doctree = self.env.get_doctree(docname)
            for node in doctree.traverse(latex_document):
                self.write_latex_document(node, docname)

    def write_latex_document(self, latex_document_node, docname):
        print latex_document_node
        output_filename   = latex_document_node["multilatex-filename"]
        if not output_filename.endswith(".tex"):
            output_filename += ".tex"
        self.info("processing {0}...".format(output_filename), nonl=1)

        variables         = latex_document_node["multilatex-variables"]
        content           = latex_document_node["multilatex-content"]
        options           = latex_document_node["multilatex-options"]

        parent_node = latex_document_node.parent
        parent_node.remove(latex_document_node)

#        from sphinx import addnodes
#        from sphinx.util.nodes import inline_all_toctrees
#        from sphinx.util.console import darkgreen
#        print; print; print "**********"
#        doctree = self.env.get_doctree(docname)
#        print self.env.get_doctree(u"examplereport/content")
#        print self.env.all_docs.keys()
#        largetree = inline_all_toctrees(self, [docname], docname, doctree, darkgreen)
#        print; print; print "%%%%%%%%%%"
#        for pendingnode in largetree.traverse(addnodes.pending_xref):
#            self.warning("Pending xref: {0} ({1})"
#                         .format(pendingnode, pendingnode["refdocname"]))
#            print ("Pending xref: {0} ({1})"
#                   .format(pendingnode, pendingnode["refdocname"]))
#            print
#        print; print; print "%%%%%%%%%%"

        doctree = self.assemble_doctree(docname, False, [])
        for node in doctree.traverse(latex_document):
            node.parent.remove(node)

        self.post_process_images(doctree)
        self.info("writing...", nonl=1)

        docwriter = LaTeXWriter(self)
        option_parser = OptionParser(
            defaults=self.env.settings,
            components=(docwriter,),
            read_config_files=True)

        doctree.settings = option_parser.get_default_values()
        doctree.settings.contentsname = None
        doctree.settings.docname = docname
        for name, value in options.items():
            setattr(doctree.settings, name, value)
        doctree.settings.multilatex_options = options
        doctree.settings.multilatex_variables = variables
        doctree.settings.multilatex_content = content

        destination = FileOutput(
            destination_path=os.path.join(self.outdir, output_filename),
            encoding="utf-8")

        docwriter.write(doctree, destination)
        self.info("done")
