# Real-Time Hardware Monitor Application

## Project Overview
Create a Windows desktop application that displays real-time system performance metrics in a modern, intuitive interface. The application should monitor and visualize CPU usage, memory consumption, and other relevant system metrics through an elegant UI with live-updating graphs and numbers. The application should be designed as a dashboard, where users can add or remove widgets to fit their own preference.

## Core Requirements

### Functionality
- Dashboard where users can add or remove widgets of different types
- Real-time monitoring of system metrics (CPU, RAM usage, etc.)
- Live-updating graphs showing performance over time

### Widgets
- Number widget
    * Display a number with a label
    * Example numbers: Temperatures, CPU Usage, RAM Usage, Disk Usage, etc.
    * Option to display instantaneus values or average values over a period of time
- Bar chart widget
    * Display a bar chart showing a number relative to a maximum value (e.g. a percentage)
    * Supports multiple bars in a single widget
    * Supports both horizontal and vertical bars
    * Example bar charts: CPU Usage, RAM Usage, Disk Usage, etc.
- Circle widget
    * Displays a number in the middle, encircled by a thin bar chart
    * Example circle widgets: CPU Usage, RAM Usage, Disk Usage, etc.
- Graph widget
    * Display a graph showing the evolution of a number over time
    * Supports multiple graphs in a single widget
    * Example graphs: CPU Usage, RAM Usage, Disk Usage, etc.

### User Interface
- Overall design: modern, minimalisc
- Layout: Card-based/widget-based
- Style: Smooth, modern rounded edges, similar to Skillex UI-UX from HALO LAB
- Color scheme: professional dark theme color scheme, with option to use light theme
- Responsive and dynamic window sizing

### Technical Specifications
- Should work for Windows
- Implementation in Python using Qt framework or similar
- Real-time data visualization using PyQtGraph or similar
- System metrics collection via psutil or similar
- Packaged as standalone Windows executable
- Data sampling at 1-second intervals
- Options for both 60-seconds and 360-seconds historical data window

## Suggested project structure
```
hw-mom/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── app.py
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── base_widget.py
│   │   ├── number_widget.py
│   │   ├── bar_widget.py
│   │   ├── circle_widget.py
│   │   └── graph_widget.py
│   ├── collectors/
│   │   ├── __init__.py
│   │   └── system_metrics.py
│   └── utils/
│       ├── __init__.py
│       └── themes.py
├── requirements.txt
└── README.md
```

## Additional Considerations
- As much as possible, minimal CPU/memory footprint
- Clean error handling
- Graceful startup and shutdown

