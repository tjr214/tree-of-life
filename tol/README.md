# Tree of Life Module

This module provides classes and utilities for creating, manipulating, and rendering the Kabbalistic Tree of Life diagram.

## Main Components

- `TreeOfLife`: The main class for creating and rendering Tree of Life diagrams
- `ColorScheme`: Enum for different color schemes (Plain, King Scale, Queen Scale, etc.)
- `SephirothTextMode`: Enum for different Sephiroth text display modes (Number, Trigram, Hebrew, Planet)
- `Sephirah`: NamedTuple representing a node (Sephirah) in the Tree of Life
- `Path`: NamedTuple representing a connecting path between Sephiroth
- `ColorEffect`: Dictionary type for handling special color effects
- `ColorParser`: Utility class for parsing color scales from YAML

## API Reference

### Constructor Parameters

The `TreeOfLife` class accepts the following parameters during initialization:

```python
def __init__(self,
             sphere_scale_factor: float = 1.75,
             spacing_factor: float = 1.5,
             sephiroth_color_scheme: ColorScheme = ColorScheme.PLAIN,
             path_color_scheme: ColorScheme = ColorScheme.PLAIN,
             color_scales_file: str = "color_scales.yaml"):
```

| Parameter                | Type        | Default             | Description                              |
| ------------------------ | ----------- | ------------------- | ---------------------------------------- |
| `sphere_scale_factor`    | float       | 1.75                | Scale factor for spheres (Sephiroth)     |
| `spacing_factor`         | float       | 1.5                 | Factor to adjust spacing between spheres |
| `sephiroth_color_scheme` | ColorScheme | PLAIN               | Color scheme for Sephiroth               |
| `path_color_scheme`      | ColorScheme | PLAIN               | Color scheme for Paths                   |
| `color_scales_file`      | str         | "color_scales.yaml" | Path to color scales file                |

### Key Methods

#### Rendering

```python
def render(self,
           focus_sephirah: Optional[int] = None,
           display: bool = True,
           save_to_file: Optional[str] = None,
           figsize: Tuple[float, float] = (7.5, 11),
           dpi: int = 300,
           show_title: bool = False) -> None:
```

Renders the Tree of Life diagram with the specified options.

#### Color Schemes

```python
def set_sephiroth_color_scheme(self, scheme: ColorScheme) -> None
def set_path_color_scheme(self, scheme: ColorScheme) -> None
```

Set the color scheme for Sephiroth or Paths.

#### Text Rendering

```python
def set_sephiroth_text_mode(self, mode: SephirothTextMode) -> None
def set_sephiroth_text_visibility(self, visible: bool) -> None
def set_path_text_visibility(self, visible: bool) -> None
```

Configure the text display options.

## Color Effects

The module supports special color effects common in traditional Kabbalistic color scales:

1. **Flecked**: Colors with small particles or dots of another color

   - Implementation: Random dots of the secondary color overlaid on the primary color

2. **Rayed**: Colors with rays of another color emanating from the center

   - Implementation: Lines of the secondary color radiating from the center

3. **Tinged**: Colors with a subtle tint of another color
   - Implementation: Blending of the primary color with a small amount of the secondary color

These effects can be applied to both Sephiroth and Paths through the `color_scales.yaml` file.

## Path Text and Symbols

Each path (numbered 11-32) is associated with:

1. A numerical, or "Key Scale" identifier (11-32)
2. An astrological or elemental symbol corresponding to the Hebrew letter traditionally associated with the path

The symbols are automatically positioned along the paths with correct orientation for readability. The module handles special cases for vertical, horizontal, and diagonal paths to ensure proper text placement.

## Usage

Basic usage example:

```python
from tol import TreeOfLife, ColorScheme

# Create a Tree of Life with default settings
tree = TreeOfLife()

# Set color schemes
tree.set_sephiroth_color_scheme(ColorScheme.KING_SCALE)
tree.set_path_color_scheme(ColorScheme.QUEEN_SCALE)

# Render the full tree
tree.render(display=True)

# Render a focused view of a specific Sephirah
tree.render(focus_sephirah=6, display=True)  # Focus on Tiphereth

# Save to file
tree.render(save_to_file="tree_of_life.png")

# Customize text display mode
tree.set_sephiroth_text_mode(tree.SephirothTextMode.HEBREW)  # Show Hebrew names
tree.render(display=True)

# Control text visibility
tree.set_sephiroth_text_visibility(False)  # Hide Sephiroth text
tree.set_path_text_visibility(False)       # Hide Path text
tree.render(display=True)
```

### Command Line Interface

For interactive configuration and generation of Tree of Life visualizations, see the `treegen.py` script in the root directory. This CLI tool provides a user-friendly interface for configuring all aspects of the Tree of Life renderer and saving configurations for reuse.

## Text Rendering Options

The TreeOfLife class provides several ways to customize text rendering:

### Text Display Modes

Choose from multiple display modes for Sephiroth text:

- `NUMBER`: Traditional enumeration (1-10)
- `TRIGRAM`: I Ching trigrams corresponding to each Sephirah
- `HEBREW`: Hebrew names of the Sephiroth (כתר, חכמה, etc.)
- `PLANET`: Planetary symbols corresponding to each Sephirah

### Text Visibility Controls

Control the visibility of text elements:

- `set_sephiroth_text_visibility(bool)`: Show/hide Sephiroth text
- `set_path_text_visibility(bool)`: Show/hide Path text and symbols

## Extending the Module

### Adding New Color Schemes

1. Add a new value to the `ColorScheme` enum in `color_utils.py`
2. Add corresponding entries in the `color_scales.yaml` file
3. Follow the existing format for Sephiroth and Path color definitions

### Adding New Color Effects

1. Update the `apply_color_effect` function in `color_utils.py` to handle the new effect
2. Add corresponding entries in the `color_scales.yaml` file with the new effect type
3. Update the rendering code if necessary

### Adding New Text Display Modes

1. Add a new value to the `SephirothTextMode` enum in `TreeOfLife.py`
2. Create a new mapping dictionary in the `_init_text_mappings` method
3. Update the rendering code in the `render` method to handle the new mode

See `demonstration.py` in the root directory for a comprehensive usage example.
