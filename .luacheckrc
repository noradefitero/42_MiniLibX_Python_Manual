-- Pandoc Lua filters run inside pandoc: the `pandoc` global is provided by the
-- host, and filter handlers (Para, Table, Div, ...) are globals by design.
globals = { "pandoc" }
allow_defined_top = true
