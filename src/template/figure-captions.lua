-- Number standalone figure images and add a literal "Figure N: <caption>"
-- caption beneath them.  This filter is applied ONLY to GFM targets
-- (README.md and dist/manual.md); LaTeX handles its own figure numbering.

local figcounter = 0

function Para(el)
  -- Only act on paragraphs that contain exactly one standalone image.
  if #el.content ~= 1 or el.content[1].t ~= "Image" then
    return nil
  end

  local img = el.content[1]
  local caption = pandoc.utils.stringify(img.caption)

  -- No alt text means no caption/number.
  if caption == "" then
    return nil
  end

  figcounter = figcounter + 1
  local numbered = "Figure " .. figcounter .. ": " .. caption
  local caption_para = pandoc.Para(pandoc.Emph(pandoc.Str(numbered)))

  return { el, caption_para }
end
