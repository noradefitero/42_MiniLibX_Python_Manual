-- yeti.lua — hand pandoc's plain HTML to Yeti's own components.
--
-- Applied to the web target only. Things pandoc writes as bare HTML that
-- Yeti already has a component for, so the stylesheet does not have to style
-- them by hand:
--
--   * a GFM table arrives as a bare <table>; Yeti's is .table, whose cell
--     padding and row rules come from the component and whose stripes come
--     from data-striped.
--
--   * a GFM alert arrives as <div class="note"> with a <div class="title">
--     header ("Note", "Tip", ...); Yeti's is .alert with a data-variant hue.
--     Yeti's alert is one message in a flex row, so the title folds into the
--     body as a bold lead rather than sitting in a block of its own — the
--     words stay, the hue carries the kind.

local alert_variant = {
	note = "primary",
	tip = "success",
	important = "danger",
	warning = "warning",
}

function Table(t)
	t.attr = pandoc.Attr("", { "table" }, { ["data-size"] = "sm", ["data-striped"] = "" })
	return t
end

function Div(el)
	local variant = nil
	for name, hue in pairs(alert_variant) do
		if el.classes:includes(name) then
			variant = hue
			break
		end
	end
	if not variant then
		return nil
	end

	-- The title becomes a bold lead on the body paragraph.
	local label = nil
	if #el.content > 0
		and el.content[1].t == "Div"
		and el.content[1].classes:includes("title")
	then
		label = pandoc.utils.stringify(el.content[1])
		el.content:remove(1)
	end
	if label and #el.content > 0 and el.content[1].t == "Para" then
		local lead = pandoc.Inlines({ pandoc.Strong({ pandoc.Str(label) }), pandoc.Space() })
		el.content[1].content = lead .. el.content[1].content
	end

	el.classes = pandoc.List({ "alert" })
	el.attributes["data-variant"] = variant
	return el
end
