#!/usr/bin/env python3
"""Generate media/diagram-stride.svg for the MiniLibX Python manual."""

import os

# ---------------------------------------------------------------------------
# Style constants (from docs/style-guide.md)
# ---------------------------------------------------------------------------
COLORS = {
    "python": "#306998",
    "wrapper": "#6340AC",
    "ctypes": "#10B981",
    "c_library": "#374151",
    "os_display": "#DC2626",
    "stroke": "#374151",
    "text_dark": "#1F2937",
    "text_light": "#FFFFFF",
    "background": "#FFFFFF",
    "padding_fill": "#D1D5DB",  # light tint of #374151
    "accent": "#10B981",
}

FONT = "Source Sans Pro, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
FONT_MONO = "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace"

CELL_SIZE = 50
ROWS = 3
COLS = 6
PADDING_CELLS = 2  # 8 bytes = 2 cells of 4 bytes each
STROKE_WIDTH = 2


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def make_svg() -> str:
    grid_w = COLS * CELL_SIZE
    grid_h = ROWS * CELL_SIZE
    padding_w = PADDING_CELLS * CELL_SIZE
    total_w = grid_w + padding_w
    margin_x = 70
    margin_y_top = 90
    margin_y_bottom = 110
    # The offset annotation sits to the right of the padding column; the
    # canvas has to be wide enough for it (measured: 233 px at 13 px mono).
    ANNOTATION_WIDTH = 240
    ann_x = margin_x + total_w + 16
    canvas_width = ann_x + ANNOTATION_WIDTH + 24
    canvas_height = grid_h + margin_y_top + margin_y_bottom

    grid_x = margin_x
    grid_y = margin_y_top

    parts = []
    parts.append('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
    parts.append('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">')
    parts.append(
        f'<svg width="100%" height="100%" viewBox="0 0 {canvas_width} {canvas_height}" '
        'version="1.1" xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" '
        'style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:1.5;">'
    )
    parts.append(f'  <rect x="0" y="0" width="{canvas_width}" height="{canvas_height}" fill="{COLORS["background"]}" />')

    # Draw padding blocks first (behind cell borders)
    for row in range(ROWS):
        px = grid_x + grid_w
        py = grid_y + row * CELL_SIZE
        parts.append(
            f'  <rect x="{px}" y="{py}" width="{padding_w}" height="{CELL_SIZE}" '
            f'fill="{COLORS["padding_fill"]}" stroke="{COLORS["stroke"]}" stroke-width="{STROKE_WIDTH}" />'
        )
        # Diagonal hatch to emphasize padding
        parts.append(
            f'  <line x1="{px}" y1="{py}" x2="{px + padding_w}" y2="{py + CELL_SIZE}" '
            f'stroke="{COLORS["stroke"]}" stroke-width="1" opacity="0.25" />'
        )
        parts.append(
            f'  <line x1="{px}" y1="{py + CELL_SIZE}" x2="{px + padding_w}" y2="{py}" '
            f'stroke="{COLORS["stroke"]}" stroke-width="1" opacity="0.25" />'
        )
        parts.append(
            f'  <text x="{px + padding_w // 2}" y="{py + CELL_SIZE // 2 + 4}" '
            f'text-anchor="middle" font-family="{FONT}" font-size="12px" '
            f'font-weight="600" fill="{COLORS["text_dark"]}">8 bytes</text>'
        )

    # Draw pixel grid cells
    highlight_col = 2
    highlight_row = 1
    for row in range(ROWS):
        for col in range(COLS):
            cx = grid_x + col * CELL_SIZE
            cy = grid_y + row * CELL_SIZE
            is_highlight = (row == highlight_row and col == highlight_col)
            fill = COLORS["accent"] if is_highlight else COLORS["background"]
            stroke_w = STROKE_WIDTH + 1 if is_highlight else STROKE_WIDTH
            stroke_col = COLORS["accent"] if is_highlight else COLORS["stroke"]
            parts.append(
                f'  <rect x="{cx}" y="{cy}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
                f'fill="{fill}" stroke="{stroke_col}" stroke-width="{stroke_w}" />'
            )
            parts.append(
                f'  <text x="{cx + CELL_SIZE // 2}" y="{cy + CELL_SIZE // 2 - 2}" '
                f'text-anchor="middle" font-family="{FONT}" font-size="12px" '
                f'font-weight="{600 if is_highlight else 500}" fill="{COLORS["text_light"] if is_highlight else COLORS["text_dark"]}">pixel</text>'
            )
            parts.append(
                f'  <text x="{cx + CELL_SIZE // 2}" y="{cy + CELL_SIZE // 2 + 14}" '
                f'text-anchor="middle" font-family="{FONT}" font-size="10px" '
                f'fill="{COLORS["text_light"] if is_highlight else COLORS["text_dark"]}" opacity="0.9">4 bytes</text>'
            )

    # Labels
    label_y_base = grid_y - 30
    parts.append(
        f'  <text x="{grid_x + grid_w // 2}" y="{label_y_base}" '
        f'text-anchor="middle" font-family="{FONT}" font-size="14px" font-weight="600" '
        f'fill="{COLORS["text_dark"]}">width = 6 px</text>'
    )
    parts.append(
        f'  <text x="{grid_x + grid_w + padding_w // 2}" y="{label_y_base}" '
        f'text-anchor="middle" font-family="{FONT}" font-size="12px" '
        f'fill="{COLORS["text_dark"]}">padding</text>'
    )

    parts.append(
        f'  <text x="{grid_x + total_w // 2}" y="{label_y_base - 22}" '
        f'text-anchor="middle" font-family="{FONT}" font-size="12px" '
        f'fill="{COLORS["text_dark"]}">size_line = 32 bytes (24 useful + 8 padding)</text>'
    )

    # Highlight annotation pointing to pixel (2,1)
    hx = grid_x + highlight_col * CELL_SIZE + CELL_SIZE // 2
    hy = grid_y + highlight_row * CELL_SIZE + CELL_SIZE // 2
    ann_y = grid_y + grid_h // 2 + 10
    parts.append(
        f'  <line x1="{hx}" y1="{hy}" x2="{ann_x - 6}" y2="{ann_y}" '
        f'stroke="{COLORS["accent"]}" stroke-width="2" marker-end="url(#arrowhead-accent)" />'
    )
    parts.append(
        f'  <text x="{ann_x}" y="{ann_y - 6}" font-family="{FONT_MONO}" font-size="13px" '
        f'fill="{COLORS["text_dark"]}">offset = y · size_line + x · 4</text>'
    )
    parts.append(
        f'  <text x="{ann_x}" y="{ann_y + 14}" font-family="{FONT_MONO}" font-size="13px" '
        f'fill="{COLORS["text_dark"]}">= 1·32 + 2·4 = 40</text>'
    )

    # Bottom annotations
    parts.append(
        f'  <text x="{grid_x}" y="{grid_y + grid_h + 26}" font-family="{FONT}" font-size="12px" '
        f'fill="{COLORS["text_dark"]}">Each row: 6 pixels × 4 bytes = 24 useful bytes + 8 padding bytes.</text>'
    )

    # Accent arrow marker
    parts.append('  <defs>')
    parts.append(
        f'    <marker id="arrowhead-accent" markerWidth="10" markerHeight="7" '
        f'refX="9" refY="3.5" orient="auto">\n'
        f'      <polygon points="0 0, 10 3.5, 0 7" fill="{COLORS["accent"]}" />\n'
        f'    </marker>'
    )
    parts.append('  </defs>')

    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(root, "diagram-stride.svg")
    svg = make_svg()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {out_path} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
