
import os
from xml.etree import ElementTree
from utils import with_app, pretty_print_xml


#=============================================================================
# Tests

@with_app(buildername="xml", srcdir="directive", warningiserror=True)
def test_directive(app, status, warning):
    app.build()
    tree = ElementTree.parse(app.outdir / "index.xml")
    pretty_print_xml(tree.getroot())

    # Verify that a latex_document node is present.
    assert len(tree.findall(".//latex_document")) == 1

    # Verify latex_document options.
    node = tree.findall(".//latex_document")[0]
    assert node.attrib["multilatex-filename"] == "sagitta"
    assert "'title': 'Sagitta'" in node.attrib["multilatex-options"]
    assert (node.attrib["multilatex-content"]
            == "[u'Content of Sagitta directive']")
