# Tree of Life Module

This module provides classes and utilities for creating, manipulating, and rendering the Kabbalistic Tree of Life diagram.

## Main Components

- `TreeOfLife`: The main class for creating and rendering Tree of Life diagrams
- `ColorScheme`: Enum for different color schemes (Plain, King Scale, Queen Scale, etc.)
- `SephirothTextMode`: Enum for different Sephiroth text display modes (Number, Trigram, Hebrew, Planet)
- `Sephirah`: NamedTuple representing a node (Sephirah) in the Tree of Life
- `Path`: NamedTuple representing a connecting path between Sephiroth
- Color utilities: Functions for handling color effects and manipulations

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

See `demonstration.py` in the root directory for a comprehensive usage example.
