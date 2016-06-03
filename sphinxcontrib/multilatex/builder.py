"""
The ``builder`` module
============================================================================

"""


import re
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

        self.elements["passoptionstopackages"] += "\n\\usepackage{xr}"
        self.elements["passoptionstopackages"] += "\n\\usepackage{xr-hyper}"

        settings = document.settings
        lines = []

        variables = settings.multilatex_variables
        for name, value in variables.items():
            lines.append("\\newcommand{{\\{0}}}{{{1}}}"
                         .format(name, value))

        for filename in settings.multilatex_all_output_filenames:
            if filename != settings.multilatex_output_filename:
                lines.append("\\externaldocument{{{0}}}".format(filename))

        self.elements["preamble"] += "\n" + "\n".join(lines)

    inter_doc_re = re.compile("^%%([^%]+)(%.*)$")

    def visit_reference(self, node):
        uri = node.get("refuri", "")
        match = self.inter_doc_re.match(uri)
        if match:
            other_doc = match.group(1)
            short_uri = match.group(2)
            node["refuri"] = short_uri
            self.context.append(" (in external document {0})".format(other_doc))
            try:
                LaTeXTranslator.visit_reference(self, node)
            finally:
                node["refuri"] = uri

        else:
            self.context.append("")
            LaTeXTranslator.visit_reference(self, node)

    def depart_reference(self, node):
        LaTeXTranslator.depart_reference(self, node)
        self.body.append(self.context.pop())


#===========================================================================
# Builder class

class MultiLatexBuilder(LaTeXBuilder):

    name = "multilatex"
    format = "latex"

    def init(self):
        self.translator_class = MultiLatexTranslator
        super(MultiLatexBuilder, self).init()

    def get_target_uri(self, docname, typ=None):
        if docname not in self.docnames:
            return "%%xyz%" + docname
        else:
            return '%' + docname

    def get_relative_uri(self, from_, to, typ=None):
        return self.get_target_uri(to, typ)

    def write(self, *ignored):
        print "All docs:", self.env.all_docs

        # Collect info on all latex_document nodes in the docs.
        output_document_node_pairs = []
        all_output_filenames = []
        for docname in self.env.all_docs.keys():
            doctree = self.env.get_doctree(docname)
            for node in doctree.traverse(latex_document):
                output_document_node_pairs.append((node, docname))
                all_output_filenames.append(node["multilatex-filename"])

        # Generate latex files.
        for (node, docname) in output_document_node_pairs:
            self.write_latex_document(node, docname, all_output_filenames)

    def write_latex_document(self, latex_document_node, docname, all_output_filenames):
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
        doctree.settings.multilatex_output_filename = output_filename
        doctree.settings.multilatex_all_output_filenames = all_output_filenames

        destination = FileOutput(
            destination_path=os.path.join(self.outdir, output_filename),
            encoding="utf-8")

        docwriter.write(doctree, destination)
        self.info("done")
