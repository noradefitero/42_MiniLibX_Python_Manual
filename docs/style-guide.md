<!-- markdownlint-disable MD013 MD024 -->

# MiniLibX Python Manual — Visual Style Guide

This guide keeps the manual's diagrams, callouts, and figure captions consistent
across the GitHub readme, the dist Markdown file, and the PDF.

## Figure style system

All diagrams should share the same visual family so the manual feels cohesive.

### Palette

Use these colors for diagrams:

| Role             | Hex       | Usage                                                   |
| ---------------- | --------- | ------------------------------------------------------- |
| Python layer     | `#306998` | Boxes that represent Python code or the application     |
| Wrapper / bridge | `#6340AC` | The `Mlx` wrapper, `mlx_func`, or any translation layer |
| ctypes / CDLL    | `#10B981` | Foreign-function interface boxes                        |
| C library        | `#374151` | `libmlx.dylib` / `libmlx.so`                            |
| OS / display     | `#DC2626` | Graphics subsystem, display, compositor                 |
| Stroke / arrows  | `#374151` | Box borders and connecting arrows                       |
| Text dark        | `#1F2937` | Labels on light boxes                                   |
| Text light       | `#FFFFFF` | Labels on dark boxes                                    |
| Background       | `#FFFFFF` | Diagram canvas                                          |

### Shapes and line work

- Boxes: rounded rectangles with a `8 px` corner radius.
- Stroke width: `2 px`, color `#374151`.
- Arrows: `2 px` stroke with a filled triangular arrowhead.
- Direction: left-to-right for sequential diagrams; top-to-bottom for hierarchies.
- Spacing: `24 px` between boxes; `16 px` padding inside boxes.
- Shadows: none; keep diagrams flat and clean.

### Typography

- Font family: `Source Sans Pro, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`.
- Box labels: `14 px`, `font-weight: 600` on dark boxes, `500` on light boxes.
- Annotation text: `12 px`, regular.
- Code fragments inside boxes: monospaced, `13 px`.

### File formats

- Editable source: keep it under `media/src/` (for example a Python script that
  generates the SVG).
- Exported diagram: place the final SVG in `media/`.
- Screenshots and photos: JPG.
- Charts: SVG when possible.

## Callout convention

Source syntax uses GitHub Flavored Markdown alerts:

```markdown
> [!NOTE]
> Useful extra information that is not essential to the main point.

> [!TIP]
> A helpful suggestion or recommended practice.

> [!WARNING]
> Something that may cause problems if ignored.

> [!IMPORTANT]
> Critical information the reader must not miss.
```

### Rendering

- **README.md and dist/manual.md**: rendered as native GFM alerts by GitHub / GFM.
- **dist/manual.pdf**: rendered as colored `mdframed` boxes with a bold title
  and a tinted background. The title matches the alert type (Note, Tip,
  Warning, Important).

Do not use plain blockquotes for callouts; reserve them for actual quotations.

## Figure and caption convention

Use a standalone image paragraph. The alt text becomes the caption.

```markdown
![The Python wrapper bridges Python method calls to the C MiniLibX library through ctypes, which then talks to the OS graphics subsystem.](media/diagram-python-c-bridge.svg)
```

The build adds the literal `Figure N:` prefix automatically in all three outputs:

- **README.md / dist/manual.md**: a Lua filter appends `*Figure N: <alt text>*`
  beneath the image.
- **dist/manual.pdf**: LaTeX handles automatic figure numbering and the List of
  Figures (enabled with `lof: true` in the YAML frontmatter).

Reference a figure in the prose like this:

```markdown
As shown in Figure 1, the wrapper loads the C library through ctypes.
```

Keep the alt text descriptive enough to work as a caption on its own.
