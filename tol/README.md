# Tree of Life Module

This module provides classes and utilities for creating, manipulating, and rendering the Kabbalistic Tree of Life diagram.

## Main Components

- `TreeOfLife`: The main class for creating and rendering Tree of Life diagrams
- `ColorScheme`: Enum for different color schemes (Plain, King Scale, Queen Scale, etc.)
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
```

See `demonstration.py` in the root directory for a comprehensive usage example.
