# Tree of Life Generator CLI Tool - Progress

## Overview

This document tracks our progress on implementing a command-line utility tool (`treegen.py`) for the Tree of Life visualization project. The tool allows users to generate and save Tree of Life diagrams using the `TreeOfLife` class with a rich, interactive interface.

## Project Requirements

- Create a command-line utility that uses the `rich` library for colorful output
- Display 80s/90s-style ASCII art for the tool name at startup
- Allow configuration of all TreeOfLife parameters
- Support three operation modes:
  - Interactive configuration and save to YAML when run without arguments
  - Interactive configuration and save to specified YAML when given a non-existent filename
  - Load config from YAML and render to PNG (or display with --display flag) when given an existing filename
- Always create a TreeOfLife object to validate settings

## Implementation Plan

### 1. Overall Structure and Flow

```
1. Parse command-line arguments
2. Display ASCII art banner
3. If no config file exists:
   - Run interactive configuration
   - Save config to YAML
4. If config file exists:
   - Load config from YAML
   - Create TreeOfLife object and configure it
   - Render to PNG or display
5. In all cases, validate settings with TreeOfLife object
```

### 2. Required Libraries

- os
- sys
- yaml
- argparse
- rich (console, panel, prompt, table, text)
- tol (TreeOfLife, ColorScheme)

### 3. Command-Line Interface Design

```python
parser = argparse.ArgumentParser(description="Tree of Life visualization generator")
parser.add_argument("config_file", nargs="?", help="YAML configuration file path")
parser.add_argument("--display", action="store_true", help="Display the visualization instead of saving to file")
```

### 4. Interactive Configuration Flow

1. **Basic Parameters**

   - sphere_scale_factor (float): Default 1.75
   - spacing_factor (float): Default 1.5

2. **Color Schemes**

   - sephiroth_color_scheme: Choose from ColorScheme enum
   - path_color_scheme: Choose from ColorScheme enum

3. **Text Display Options**

   - sephiroth_text_mode: Choose from SephirothTextMode enum
   - sephiroth_text_visibility: Boolean
   - path_text_visibility: Boolean

4. **Rendering Options**
   - focus_sephirah: Optional[int] (1-10)
   - figsize: Tuple[float, float]
   - dpi: int
   - show_title: Boolean

### 5. YAML Configuration Structure

```yaml
# Tree of Life Generator Configuration
basic:
  sphere_scale_factor: 1.75
  spacing_factor: 1.5
color_schemes:
  sephiroth: "KING_SCALE"
  path: "QUEEN_SCALE"
text_display:
  sephiroth_mode: "HEBREW"
  sephiroth_visible: true
  path_visible: true
rendering:
  focus_sephirah: null # or 1-10
  figsize: [7.5, 11]
  dpi: 300
  show_title: false
```

### 6. ASCII Art Banner

Create a colorful 80s/90s-style ASCII art banner using `rich` library styling

## Tasks

- [x] Set up basic script structure and argument parsing
- [x] Create ASCII art banner function
- [x] Implement interactive configuration prompts
- [x] Add YAML configuration saving functionality
- [x] Add YAML configuration loading functionality
- [x] Implement TreeOfLife object creation and validation
- [x] Add rendering logic (display or save to file)
- [x] Add comprehensive error handling
- [x] Polish user experience with rich styling
- [x] Test all operation modes and edge cases
- [x] Document the code thoroughly with comments
- [x] Complete implementation with proper typing

## Implementation Notes

We have successfully implemented the TreeOfLife Generator CLI tool with the following features:

1. **Colorful Interface**: Used the `rich` library to create a visually appealing interface with colorful text, panels, tables, and interactive prompts.

2. **ASCII Art Banner**: Implemented an eye-catching 80s/90s-style ASCII art banner for the tool name.

3. **Command-Line Argument Handling**: Added support for optional config file path and --display flag.

4. **Interactive Configuration**: Created a comprehensive interactive configuration flow with tables and descriptions for all options.

5. **YAML Configuration**: Implemented saving and loading of configuration files in YAML format with proper comments and structure.

6. **TreeOfLife Integration**: Seamless integration with the TreeOfLife class, properly passing all configuration parameters.

7. **Intelligent File Naming**: Output files now use the configuration filename as their base, with suffixes for specific configurations (e.g., focus on specific Sephirah).

8. **Error Handling**: Added robust error handling throughout the application for graceful failure.

9. **Three Operation Modes**:

   - Interactive mode with custom filename when no arguments
   - Interactive mode saving to specified file when non-existent filename is given
   - Load and render mode when existing file is provided

10. **Comprehensive Documentation**: Added detailed documentation throughout the code, including descriptive function docstrings, section comments, and explanations for each major component.

The implementation follows proper Python typing and provides a rich, user-friendly interface for working with the Tree of Life visualization library.
