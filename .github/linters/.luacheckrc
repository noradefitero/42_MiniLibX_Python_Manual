-- Pandoc Lua filters run inside Pandoc's runtime, which injects the global
-- `pandoc` table. The filter entry points (Div, Para, Table, ...) are global
-- functions that Pandoc calls by name, so they are expected to be global.
std = "max"
globals = {
  "pandoc",
  "Div",
  "Para",
  "Table",
}
