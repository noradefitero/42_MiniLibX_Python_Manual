"""Minify the generated HTML in place; called by `make web`."""

import pathlib
import sys

import minify_html

for name in sys.argv[1:]:
    path = pathlib.Path(name)
    path.write_text(
        minify_html.minify(
            path.read_text(encoding="utf-8"),
            allow_removing_spaces_between_attributes=True,
            keep_comments=False,
            keep_ssi_comments=False,
            minify_js=True,
            minify_css=True,
            minify_doctype=True,
            remove_processing_instructions=True,
        ),
        encoding="utf-8",
    )
