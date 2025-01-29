# HWMom

An ultra-lightweight hardware monitoring application for Windows that displays system performance metrics through an elegant dashboard with live-updating widgets. Designed to not look like ass.

## Features
- Real-time monitoring of system metrics (CPU, RAM, etc.)
- Customizable and sleek dashboard with various widget types
- Modern, minimal dark/light theme interface
- Low resource footprint

## Installation
Just install bro.


# How to create a layout

When the app is lauched, it loads the layout defined in the `default_layout.txt` text file.

In it, widgets are created with the following syntax: 
`[{widget_type} {metric} {height}x{width} {color_scheme}]` 
(without brackets), where:

- `widget_type`: The type of widget to create.
    - Must be one of `graph`, `circle`, `text`, `separator`.
- `metric`: The metric to display.
    - Must be one of `cpu`, `gpu`, `ping`, `gpu temp`.
- `height` and `width`: The height and width of the widget. 
    -  Must be integers.
- `color_scheme`: The color scheme of the widget.
    - Must be one of `color a`, `color b`, `color c`.

Layouts are created by placing widgets next to each other, separated by `[]` brackets. Use new lines to indicate the end of a row and empty brackets (`[ ]`) to reserve space in case a widget spans more than one row. See examples below.

The default theme can be specified by adding either `theme: dark` or `theme: light` to the beginning of the text file.

**Example 1:**
```
theme: dark
[gpu circle 2x2 color a][ping text 1x1][separator 2x1][gpu temp circle 2x2 color b]
[                      ][ping text 1x1][             ][                           ]
[cpu graph 2x6 color b]
[                     ]
[separator 1x6]
```
This will create a layout with 5 rows (since there are 5 rows of text) and 6 columns (since the maximum sum of widths over all rows is 6).

**Example 2:**
```
```

