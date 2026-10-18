-- table-widths.lua -- keep every table inside the text block.
--
-- Pandoc's LaTeX writer normally declares table columns as `l` (natural
-- width), so a table that is naturally wider than the text block runs off
-- the right margin and, on A4 with 2.5cm margins, straight onto the page
-- edge (Troubleshooting, Function index, the keysym appendices, ...).
--
-- This filter estimates the natural width of every table.  Tables that fit
-- are left alone, so short tables keep their compact ragged-right look.
-- Tables that would overflow get explicit relative column widths, which
-- makes the LaTeX writer emit wrapping `p{...}` columns instead.

local TEXT_WIDTH_PT = 453.5  -- A4 width minus the 2.5cm margins

-- Natural width of a cell, in points, at the body font size (10.95pt Source
-- Sans Pro) and the code font size (10.9pt Source Code Pro).
local SANS_CHAR_PT = 5.0
local MONO_CHAR_PT = 6.6
local SPACE_PT = 2.4
-- Column separators (\tabcolsep on both sides of every column).
local PADDING_PT = 12.0
-- Estimation is approximate: treat a table as overflowing a bit early.
local TOLERANCE = 0.97

-- Characters of the longest unbreakable run: a run ends at whitespace and,
-- because the template lets code tokens break after an underscore, at "_".
local function longest_token(text)
  local best = 0
  for word in text:gmatch("%S+") do
    for run in word:gmatch("[^_]+") do
      if #run > best then best = #run end
    end
  end
  return best
end

local function inline_width(el)
  if el.t == "Code" or el.t == "Math" then
    return #el.text * MONO_CHAR_PT
  elseif el.t == "Space" or el.t == "SoftBreak" or el.t == "LineBreak" then
    return SPACE_PT
  elseif el.t == "Str" then
    return #el.text * SANS_CHAR_PT
  elseif el.content then
    return #pandoc.utils.stringify(el) * SANS_CHAR_PT
  end
  return 0
end

local function blocks_width(blocks)
  local width = 0
  for _, blk in ipairs(blocks) do
    if blk.content then
      for _, el in ipairs(blk.content) do
        width = width + inline_width(el)
      end
    end
  end
  return width
end

local function rows(tbl)
  local all = {}
  local function add(list)
    for _, row in ipairs(list or {}) do
      all[#all + 1] = row
    end
  end
  add(tbl.head.rows)
  for _, body in ipairs(tbl.bodies) do
    add(body.head)
    add(body.body)
    add(body.foot)
  end
  add(tbl.foot.rows)
  return all
end

-- Assign relative widths: proportional to the content, but never narrower
-- than the longest unbreakable token a column has to hold.
local function fit(widths)
  local n = #widths
  local total = 0
  for i = 1, n do total = total + widths[i] end
  local share = {}
  for i = 1, n do share[i] = widths[i] / total end
  local sum = 0
  for i = 1, n do sum = sum + share[i] end
  for i = 1, n do
    widths[i] = share[i] / sum * 0.999
  end
  return widths
end

function Table(tbl)
  local n = #tbl.colspecs
  if n == 0 then return nil end

  local demand, token = {}, {}
  for i = 1, n do demand[i], token[i] = 1.0, 0 end
  local natural = 0
  for _, row in ipairs(rows(tbl)) do
    local row_width = (n - 1) * PADDING_PT
    for i = 1, math.min(n, #row.cells) do
      local cell = row.cells[i]
      local text = pandoc.utils.stringify(cell.contents)
      row_width = row_width + blocks_width(cell.contents)
      demand[i] = math.max(demand[i], #text)
      token[i] = math.max(token[i], longest_token(text))
    end
    natural = math.max(natural, row_width)
  end

  local debug = pandoc.system.environment().TABLE_WIDTHS_DEBUG
  if debug then
    io.stderr:write(string.format("table[%dcols] natural=%.0fpt %s\n",
      n, natural, natural > TOLERANCE * TEXT_WIDTH_PT and "OVERFLOW" or "fits"))
  end

  if natural <= TOLERANCE * TEXT_WIDTH_PT then
    return nil
  end

  -- A column must be wide enough for its longest unbreakable token, with a
  -- little room to spare so a token never touches the column edge.
  local floor = {}
  for i = 1, n do
    floor[i] = token[i] * MONO_CHAR_PT * 1.1 / TEXT_WIDTH_PT
  end

  local total = 0
  for i = 1, n do total = total + demand[i] end
  local widths = {}
  for i = 1, n do widths[i] = demand[i] / total end

  -- Shrink the columns that still have room above their floor, so that the
  -- widths of the code-heavy columns can stay above theirs.
  local sum = 0
  for i = 1, n do sum = sum + math.max(widths[i], floor[i]) end
  if sum > 1 then
    local slack = 0
    for i = 1, n do slack = slack + math.max(widths[i] - floor[i], 0) end
    if slack > 0 then
      local excess = sum - 1
      for i = 1, n do
        local room = widths[i] - floor[i]
        if room > 0 then widths[i] = widths[i] - excess * room / slack end
      end
    end
    for i = 1, n do widths[i] = math.max(widths[i], floor[i]) end
  end

  widths = fit(widths)
  for i = 1, n do
    tbl.colspecs[i] = { tbl.colspecs[i][1], widths[i] }
  end
  return tbl
end
