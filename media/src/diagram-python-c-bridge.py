#!/usr/bin/env python3
"""Generate diagram-python-c-bridge.svg for the MiniLibX Python manual.

This script is the editable source for the diagram.  Run it to regenerate the
exported SVG in media/.
"""

import os
import xml.etree.ElementTree as ET

# Style system palette
COLORS = {
    "python": "#306998",
    "wrapper": "#6340AC",
    "ctypes": "#10B981",
    "c_library": "#374151",
    "os": "#DC2626",
    "stroke": "#374151",
    "text_dark": "#1F2937",
    "text_light": "#FFFFFF",
    "bg": "#FFFFFF",
}

BOX_W = 150
BOX_H = 80
BOX_R = 8
SPACING = 24
MARGIN = 50
ARROW_LEN = SPACING
FONT_FAMILY = "Source Sans Pro, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
FONT_SIZE_LABEL = 14
FONT_SIZE_SUB = 11
STROKE_WIDTH = 2

BOXES = [
    {
        "label": "Python",
        "sublabel": "application",
        "fill": COLORS["python"],
        "text": COLORS["text_light"],
    },
    {
        "label": "Mlx class methods",
        "sublabel": "mlx_func wrapper",
        "fill": COLORS["wrapper"],
        "text": COLORS["text_light"],
    },
    {
        "label": "ctypes",
        "sublabel": "CDLL",
        "fill": COLORS["ctypes"],
        "text": COLORS["text_light"],
    },
    {
        "label": "libmlx.dylib / .so",
        "sublabel": "C library",
        "fill": COLORS["c_library"],
        "text": COLORS["text_light"],
    },
    {
        "label": "OS graphics subsystem",
        "sublabel": "display",
        "fill": COLORS["os"],
        "text": COLORS["text_light"],
    },
]


def add_text(parent, x, y, text, size, weight, color, anchor="middle"):
    """Add a single-line text element."""
    el = ET.SubElement(parent, "text")
    el.set("x", str(x))
    el.set("y", str(y))
    el.set("font-family", FONT_FAMILY)
    el.set("font-size", f"{size}px")
    el.set("font-weight", weight)
    el.set("fill", color)
    el.set("text-anchor", anchor)
    el.set("dominant-baseline", "middle")
    el.text = text
    return el


def add_rounded_rect(parent, x, y, w, h, r, fill, stroke):
    """Add a rounded rectangle."""
    el = ET.SubElement(parent, "rect")
    el.set("x", str(x))
    el.set("y", str(y))
    el.set("width", str(w))
    el.set("height", str(h))
    el.set("rx", str(r))
    el.set("ry", str(r))
    el.set("fill", fill)
    el.set("stroke", stroke)
    el.set("stroke-width", str(STROKE_WIDTH))
    return el


def add_arrow(parent, x1, y1, x2, y2, color):
    """Add a line with a filled arrowhead."""
    marker_id = "arrowhead"
    line = ET.SubElement(parent, "line")
    line.set("x1", str(x1))
    line.set("y1", str(y1))
    line.set("x2", str(x2))
    line.set("y2", str(y2))
    line.set("stroke", color)
    line.set("stroke-width", str(STROKE_WIDTH))
    line.set("marker-end", f"url(#{marker_id})")
    return line


def build_svg():
    n = len(BOXES)
    content_w = n * BOX_W + (n - 1) * SPACING
    width = content_w + 2 * MARGIN
    height = BOX_H + 2 * MARGIN

    svg = ET.Element("svg")
    svg.set("xmlns", "http://www.w3.org/2000/svg")
    svg.set("version", "1.1")
    svg.set("width", str(width))
    svg.set("height", str(height))
    svg.set("viewBox", f"0 0 {width} {height}")
    svg.set("role", "img")
    svg.set("aria-label", "The Python wrapper bridges Python method calls to the C MiniLibX library through ctypes, which then talks to the OS graphics subsystem.")

    # Background
    bg = ET.SubElement(svg, "rect")
    bg.set("width", "100%")
    bg.set("height", "100%")
    bg.set("fill", COLORS["bg"])

    # Arrow marker definition
    defs = ET.SubElement(svg, "defs")
    marker = ET.SubElement(defs, "marker")
    marker.set("id", "arrowhead")
    marker.set("markerWidth", "10")
    marker.set("markerHeight", "7")
    marker.set("refX", "9")
    marker.set("refY", "3.5")
    marker.set("orient", "auto")
    arrow_poly = ET.SubElement(marker, "polygon")
    arrow_poly.set("points", "0 0, 10 3.5, 0 7")
    arrow_poly.set("fill", COLORS["stroke"])

    # Draw boxes and arrows
    start_x = MARGIN
    center_y = MARGIN + BOX_H // 2

    for i, box in enumerate(BOXES):
        x = start_x + i * (BOX_W + SPACING)
        y = MARGIN

        add_rounded_rect(
            svg, x, y, BOX_W, BOX_H, BOX_R, box["fill"], COLORS["stroke"]
        )

        # Main label, centered
        add_text(
            svg,
            x + BOX_W // 2,
            center_y - 7,
            box["label"],
            FONT_SIZE_LABEL,
            "600",
            box["text"],
        )

        # Sub-label, centered below main label
        add_text(
            svg,
            x + BOX_W // 2,
            center_y + 12,
            box["sublabel"],
            FONT_SIZE_SUB,
            "400",
            box["text"],
        )

        # Arrow to next box
        if i < n - 1:
            arrow_x1 = x + BOX_W
            arrow_x2 = x + BOX_W + SPACING
            add_arrow(svg, arrow_x1, center_y, arrow_x2, center_y, COLORS["stroke"])

    return svg


def main():
    repo_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    output_path = os.path.join(repo_root, "media", "diagram-python-c-bridge.svg")

    svg = build_svg()
    tree = ET.ElementTree(svg)
    ET.indent(tree, space="  ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
