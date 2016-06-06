
import os
from utils import with_app


#=============================================================================
# Tests

@with_app(buildername="multilatex", srcdir="builder", warningiserror=True)
def test_builder(app, status, warning):
    app.build()
    output = (app.outdir / "sagitta.tex").text()
    assert "Lorem ipsum for the first chapter..." in output
    assert "Lorem ipsum for the second chapter..." in output
    print output
