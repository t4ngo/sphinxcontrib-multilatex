"""
The ``builder`` module
============================================================================

"""


import re
import os.path
from docutils.io import FileOutput
from docutils.frontend import OptionParser
from sphinx import addnodes
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

        self.settings = document.settings
        lines = []

        variables = self.settings.multilatex_variables
        for name, value in variables.items():
            lines.append("\\newcommand{{\\{0}}}{{{1}}}"
                         .format(name, value))

        for node in self.settings.multilatex_all_latex_document_nodes:
            filename = node["multilatex-filename"]
            if filename != self.settings.multilatex_output_filename:
                lines.append("\\externaldocument{{{0}}}".format(filename))

        self.elements["preamble"] += "\n" + "\n".join(lines)

    inter_doc_re = re.compile("^%(?P<short_uri>%(?P<docname>[^#]+).*)$")
    exdoc_ref_prefix = ""
    exdoc_ref_suffix = " on page \\pageref*{{{ref}}} in \\autoref*{{{ref}}} of {title}"
    unknown_exdoc_ref_prefix = ""
    unknown_exdoc_ref_suffix = " (in unknown external document)"

    def visit_reference(self, node):
        uri = node.get("refuri", "")
        match = self.inter_doc_re.match(uri)
        if match:
            target_docname = match.group("docname")
            short_uri = match.group("short_uri")

            for latex_document in \
                self.settings.multilatex_all_latex_document_nodes:
                docnames = latex_document["multilatex-docnames"]
                if target_docname in docnames:
                    target_latex_document = latex_document
                    break
            else:
                target_latex_document = None

            if target_latex_document:
                options = target_latex_document["multilatex-options"]
                parameters = {
                    "ref": short_uri[1:].replace("#", ":"),
                    "title": options.get("title", "unknown external document"),
                }
                prefix = self.exdoc_ref_prefix.format(**parameters)
                suffix = self.exdoc_ref_suffix.format(**parameters)
            else:
                prefix = self.unknown_exdoc_ref_prefix
                suffix = self.unknown_exdoc_ref_suffix
            self.body.append(prefix)
            self.context.append(suffix)

            node["refuri"] = short_uri
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
            return "%%" + docname
        else:
            return '%' + docname

    def get_relative_uri(self, from_, to, typ=None):
        return self.get_target_uri(to, typ)

    def write(self, *ignored):
        # Collect all latex_document nodes.
        all_latex_document_nodes = []
        for docname in self.env.all_docs.keys():
            local_doctree = self.env.get_doctree(docname)
            for node in local_doctree.traverse(latex_document):
                node["multilatex-docname"] = docname

                # Assemble doctrees of latex_document nodes.
                doctree = self.assemble_doctree(docname, False, [])
                node["multilatex-doctree"] = doctree

                # Determine which source files went into which
                # latex_document nodes.
                docnames = [docname]
                for sof_node in doctree.traverse(addnodes.start_of_file):
                    docnames.append(sof_node["docname"])
                node["multilatex-docnames"] = docnames

                all_latex_document_nodes.append(node)

        all_output_filenames = []
        for node in all_latex_document_nodes:
            all_output_filenames.append(node["multilatex-filename"])

        # Generate latex files.
        for node in all_latex_document_nodes:
            self.write_latex_document(node, all_latex_document_nodes)

    def write_latex_document(self, latex_document_node,
                             all_latex_document_nodes):
        output_filename = latex_document_node["multilatex-filename"]
        variables       = latex_document_node["multilatex-variables"]
        content         = latex_document_node["multilatex-content"]
        options         = latex_document_node["multilatex-options"]
        docname         = latex_document_node["multilatex-docname"]
        doctree         = latex_document_node["multilatex-doctree"]

        if not output_filename.endswith(".tex"):
            output_filename += ".tex"
        self.info("processing {0}...".format(output_filename), nonl=1)

#        for node in doctree.traverse(latex_document):
#            node.parent.remove(node)
#        parent_node = latex_document_node.parent
#        parent_node.remove(latex_document_node)

        self.post_process_images(doctree)

        self.info("writing...", nonl=1)
        docwriter = LaTeXWriter(self)
        option_parser = OptionParser(
            defaults=self.env.settings,
            components=(docwriter,),
            read_config_files=True)

        doctree.settings = option_parser.get_default_values()
        settings = doctree.settings
        settings.contentsname = None
        settings.docname = docname
        for name, value in options.items():
            setattr(settings, name, value)
        settings.multilatex_options = options
        settings.multilatex_variables = variables
        settings.multilatex_content = content
        settings.multilatex_output_filename = output_filename
        settings.multilatex_all_latex_document_nodes = all_latex_document_nodes

        destination = FileOutput(
            destination_path=os.path.join(self.outdir, output_filename),
            encoding="utf-8")

        docwriter.write(doctree, destination)
        self.info("done")
