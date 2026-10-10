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

  -- Render the remaining content back to LaTeX.
  local body = pandoc.write(pandoc.Pandoc(el.content), "latex")
  body = body:gsub("^%s+", ""):gsub("%s+$", "")

  local env = "ml" .. atype
  local latex = "\\begin{" .. env .. "}[frametitle={" .. title .. "}]\n" .. body .. "\n\\end{" .. env .. "}"

  return pandoc.RawBlock("latex", latex)
end
