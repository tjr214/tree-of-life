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

- [ ] Set up basic script structure and argument parsing
- [ ] Create ASCII art banner function
- [ ] Implement interactive configuration prompts
- [ ] Add YAML configuration saving functionality
- [ ] Add YAML configuration loading functionality
- [ ] Implement TreeOfLife object creation and validation
- [ ] Add rendering logic (display or save to file)
- [ ] Add comprehensive error handling
- [ ] Polish user experience with rich styling
- [ ] Test all operation modes and edge cases
- [ ] Document the code thoroughly with comments
- [ ] Complete implementation with proper typing

## Testing Strategy

- [ ] Test with no arguments (interactive mode)
- [ ] Test with non-existent filename
- [ ] Test with existing filename
- [ ] Test with --display flag
- [ ] Test with invalid configurations
- [ ] Test each feature of the TreeOfLife class

## Implementation Notes

_To be updated as we make progress_
