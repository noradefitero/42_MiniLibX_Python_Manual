#!/usr/bin/env python3
"""Generate media/diagram-lifecycle.svg for the MiniLibX Python manual."""

import math
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
}

FONT = "Source Sans Pro, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
FONT_MONO = "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace"

BOX_RADIUS = 8
BOX_PADDING = 16
BOX_GAP = 24
STROKE_WIDTH = 2
ARROW_WIDTH = 2


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def box_width(label: str) -> int:
    """Approximate box width from label length (Source Sans Pro 14px)."""
    # Conservative estimate: ~8.2 px per average char for 14px Source Sans Pro.
    return int(len(label) * 8.5) + BOX_PADDING * 2


def rounded_rect(x: int, y: int, width: int, height: int, radius: int) -> str:
    return (
        f"M {x + radius},{y} "
        f"h {width - 2 * radius} "
        f"a {radius},{radius} 0 0 1 {radius},{radius} "
        f"v {height - 2 * radius} "
        f"a {radius},{radius} 0 0 1 {-radius},{radius} "
        f"h {-(width - 2 * radius)} "
        f"a {radius},{radius} 0 0 1 {-radius},{-radius} "
        f"v {-(height - 2 * radius)} "
        f"a {radius},{radius} 0 0 1 {radius},{-radius} z"
    )


def make_svg() -> str:
    boxes = [
        ("Mlx()", COLORS["wrapper"], COLORS["text_light"]),
        ("mlx_init()", COLORS["c_library"], COLORS["text_light"]),
        ("mlx_new_window()", COLORS["c_library"], COLORS["text_light"]),
        ("draw + register hooks", COLORS["python"], COLORS["text_light"]),
        ("mlx_loop()", COLORS["c_library"], COLORS["text_light"]),
        ("mlx_loop_exit()", COLORS["c_library"], COLORS["text_light"]),
        ("mlx_destroy_*() + mlx_release()", COLORS["c_library"], COLORS["text_light"]),
    ]

    box_heights = [46] * len(boxes)
    box_widths = [box_width(label) for label, _, _ in boxes]

    total_width = sum(box_widths) + BOX_GAP * (len(boxes) - 1)
    margin_x = 60
    margin_y_top = 70
    canvas_width = total_width + margin_x * 2

    start_x = margin_x
    box_y = margin_y_top
    box_positions = []
    x = start_x
    for w, h in zip(box_widths, box_heights):
        box_positions.append((x, box_y, w, h))
        x += w + BOX_GAP

    # Display server / GPU box (wide, centered under the main flow)
    display_label = "Display server / GPU"
    display_width = box_width(display_label)
    display_height = 46
    display_x = (canvas_width - display_width) // 2
    display_y = box_y + box_heights[0] + 90
    # The canvas must also cover the display box, which sits below the flow.
    canvas_height = display_y + display_height + 24

    # Arrow marker
    marker = (
        '<marker id="arrowhead" markerWidth="10" markerHeight="7" '
        'refX="9" refY="3.5" orient="auto">\n'
        f'      <polygon points="0 0, 10 3.5, 0 7" fill="{COLORS["stroke"]}" />\n'
        '    </marker>'
    )

    parts = []
    parts.append('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
    parts.append('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">')
    parts.append(
        f'<svg width="100%" height="100%" viewBox="0 0 {canvas_width} {canvas_height}" '
        'version="1.1" xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" '
        'style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:1.5;">'
    )
    parts.append('  <defs>')
    parts.append(f'    {marker}')
    parts.append('  </defs>')
    # Background
    parts.append(f'  <rect x="0" y="0" width="{canvas_width}" height="{canvas_height}" fill="{COLORS["background"]}" />')

    # Main sequential arrows
    for i in range(len(box_positions) - 1):
        x1 = box_positions[i][0] + box_positions[i][2]
        y1 = box_positions[i][1] + box_positions[i][3] // 2
        x2 = box_positions[i + 1][0]
        y2 = y1
        parts.append(
            f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{COLORS["stroke"]}" stroke-width="{ARROW_WIDTH}" marker-end="url(#arrowhead)" />'
        )

    # Self-return arrow on mlx_loop() (index 4)
    lp_x, lp_y, lp_w, lp_h = box_positions[4]
    loop_mid_y = lp_y + lp_h // 2
    arc_left = lp_x + 12
    arc_right = lp_x + lp_w - 12
    arc_top = lp_y - 36
    parts.append(
        f'  <path d="M {arc_right},{loop_mid_y} '
        f'C {arc_right + 30},{loop_mid_y} {arc_right + 30},{arc_top} {arc_right},{arc_top} '
        f'H {arc_left} '
        f'C {arc_left - 30},{arc_top} {arc_left - 30},{loop_mid_y} {arc_left},{loop_mid_y}" '
        f'fill="none" stroke="{COLORS["stroke"]}" stroke-width="{ARROW_WIDTH}" '
        f'marker-end="url(#arrowhead)" />'
    )
    parts.append(
        f'  <text x="{(arc_left + arc_right) // 2}" y="{arc_top - 6}" '
        f'text-anchor="middle" font-family="{FONT}" font-size="12px" fill="{COLORS["text_dark"]}">'
        'events &amp; frames</text>'
    )

    # Annotation under mlx_loop()
    annotation_y = lp_y + lp_h + 16
    parts.append(
        f'  <text x="{lp_x + lp_w // 2}" y="{annotation_y}" '
        f'text-anchor="middle" font-family="{FONT}" font-size="12px" fill="{COLORS["text_dark"]}">'
        'never returns on its own</text>'
    )

    # Draw main boxes
    for (x, y, w, h), (label, fill, text_color) in zip(box_positions, boxes):
        parts.append(
            f'  <path d="{rounded_rect(x, y, w, h, BOX_RADIUS)}" '
            f'fill="{fill}" stroke="{COLORS["stroke"]}" stroke-width="{STROKE_WIDTH}" />'
        )
        # Code-like labels use mono font, otherwise regular sans
        family = FONT_MONO if any(c in label for c in "()_") else FONT
        weight = "600" if text_color == COLORS["text_light"] else "500"
        parts.append(
            f'  <text x="{x + w // 2}" y="{y + h // 2 + 5}" '
            f'text-anchor="middle" font-family="{family}" font-size="14px" '
            f'font-weight="{weight}" fill="{text_color}">{escape(label)}</text>'
        )

    # Display server / GPU box
    parts.append(
        f'  <path d="{rounded_rect(display_x, display_y, display_width, display_height, BOX_RADIUS)}" '
        f'fill="{COLORS["os_display"]}" stroke="{COLORS["stroke"]}" stroke-width="{STROKE_WIDTH}" />'
    )
    parts.append(
        f'  <text x="{display_x + display_width // 2}" y="{display_y + display_height // 2 + 5}" '
        f'text-anchor="middle" font-family="{FONT}" font-size="14px" font-weight="600" '
        f'fill="{COLORS["text_light"]}">{escape(display_label)}</text>'
    )

    # Bidirectional arrows from mlx_init() and mlx_loop() to display box
    for idx in (1, 4):
        bx, by, bw, bh = box_positions[idx]
        top_x = bx + bw // 2
        top_y = by + bh
        disp_x = display_x + display_width // 2
        disp_y = display_y
        # Small vertical line from box to a clear routing point, then elbow
        mid_y = (top_y + disp_y) // 2
        if idx == 1:
            # left-ish connection point on display box
            target_x = display_x + display_width // 4
        else:
            target_x = display_x + 3 * display_width // 4
        parts.append(
            f'  <polyline points="{top_x},{top_y} {top_x},{mid_y} {target_x},{mid_y} {target_x},{disp_y}" '
            f'fill="none" stroke="{COLORS["stroke"]}" stroke-width="{ARROW_WIDTH}" '
            f'marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />'
        )

    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(root, "diagram-lifecycle.svg")
    svg = make_svg()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {out_path} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
