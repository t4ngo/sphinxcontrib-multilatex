
import directive
import builder


#===========================================================================
# Node visitor functions

def visit_passthrough(self, node):
    pass

def depart_passthrough(self, node):
    pass

passthrough = (visit_passthrough, depart_passthrough)


#===========================================================================
# Setup and register extension

def setup(app):
    app.add_node(directive.latex_document,
                 latex=passthrough,
                 html=passthrough)
    app.add_directive("latex-document", directive.LatexDocumentDirective)
    app.add_builder(builder.MultiLatexBuilder)

    return {"version": "0.0"}
