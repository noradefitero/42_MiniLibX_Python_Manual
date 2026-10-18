-- Render GFM-style alert callouts (> [!NOTE], > [!TIP], > [!WARNING],
-- > [!IMPORTANT]) as styled mdframed boxes in LaTeX/PDF output.
-- This filter is applied ONLY to the PDF target.

local function alert_type(classes)
  for _, cls in ipairs(classes) do
    local lower = cls:lower()
    if lower == "note" or lower == "tip" or lower == "warning" or lower == "important" then
      return lower
    end
  end
  return nil
end

-- Split any paragraph that mixes text with inline images into separate
-- blocks, so an image inside an alert never ends up typeset inline next to
-- (or wrapped around) text.  This keeps the layout sane no matter whether
-- the source markdown puts blank ">" lines around the image or not.
local function normalize_blocks(blocks)
  local out = {}
  for _, block in ipairs(blocks) do
    if block.t == "Para" or block.t == "Plain" then
      local has_img = false
      for _, inl in ipairs(block.content) do
        if inl.t == "Image" then
          has_img = true
          break
        end
      end
      if not has_img then
        out[#out + 1] = block
      else
        local seg = {}
        local flush = function()
          if #seg > 0 then
            out[#out + 1] = pandoc[block.t](seg)
            seg = {}
          end
        end
        for _, inl in ipairs(block.content) do
          if inl.t == "Image" then
            flush()
            out[#out + 1] = pandoc[block.t]({ inl })
          else
            seg[#seg + 1] = inl
          end
        end
        flush()
      end
    else
      out[#out + 1] = block
    end
  end
  return out
end

function Div(el)
  local atype = alert_type(el.classes)
  if not atype then
    return nil
  end

  -- Pandoc with -f markdown+alerts wraps alerts in a Div whose first child
  -- is the title Div; with -f gfm the title is also the first child.
  local title = atype:gsub("^%l", string.upper)
  if #el.content > 0 and el.content[1].t == "Div" then
    local first_classes = el.content[1].classes
    if first_classes and first_classes:includes("title") then
      local title_text = pandoc.utils.stringify(el.content[1].content)
      if title_text ~= "" then
        title = title_text
      end
      table.remove(el.content, 1)
    end
  end

  local env = "ml" .. atype

  -- Emit only the environment delimiters as raw LaTeX and let the alert's
  -- content pass through pandoc's normal writer.  Rendering the body here
  -- with pandoc.write(..., "latex") would bake in LaTeX image commands
  -- (e.g. \includesvg) that the PDF pipeline never post-processes: for PDF
  -- output pandoc converts SVG images itself and does NOT load the svg
  -- package, so a baked-in \includesvg ends up undefined.
  local blocks = {
    pandoc.RawBlock("latex", "\\begin{" .. env .. "}[frametitle={" .. title .. "}]"),
  }
  for _, block in ipairs(normalize_blocks(el.content)) do
    blocks[#blocks + 1] = block
  end
  blocks[#blocks + 1] = pandoc.RawBlock("latex", "\\end{" .. env .. "}")

  return blocks
end
