-- figure-center.lua -- centre standalone figures in the PDF.
--
-- Pandoc emits a standalone image as an ordinary paragraph, so LaTeX typesets
-- it like a line of text: flush left.  A screenshot wide enough to touch the
-- right margin hides that, but a diagram narrower than the text block
-- (uv-benchmark.svg, diagram-color-bytes.svg) stays glued to the left edge
-- with a large gap of white space on its right.
--
-- GFM has no `implicit_figures`, so there is no LaTeX `figure` environment
-- either and nothing centres the image.  This filter brackets every image-only
-- paragraph with the `pandocfigure` environment defined in pdf.tex, which
-- centres the image and drops the parfillskip, so that a wide image may use
-- the full \linewidth instead of bleeding into the right margin.
--
-- The bracketing blocks are *added around* the image paragraph, never in
-- place of it: pandoc decides whether the `graphics` template variable is
-- true by looking for images in the document, and the whole `$if(graphics)$`
-- block - which defines \pandocbounded - would otherwise be dropped.
--
-- Applied to the PDF target only: in the web/GFM targets a <figure> is
-- centred by the stylesheet, not by LaTeX.  It must run *after*
-- figure-captions.lua, which splits the image and its "Figure N:" caption
-- into two paragraphs: only the image is centred, the caption stays a normal
-- text paragraph.

function Para(el)
  if #el.content ~= 1 or el.content[1].t ~= "Image" then
    return nil
  end

  return {
    pandoc.RawBlock("latex", "\\begin{pandocfigure}"),
    el,
    pandoc.RawBlock("latex", "\\end{pandocfigure}"),
  }
end
