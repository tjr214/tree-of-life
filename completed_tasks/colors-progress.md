# Dynamic Text Color Implementation for Tree of Life Visualization

## Problem Statement

Currently, the text color for both Sephiroth numbers and Path numbers/symbols is hardcoded:

- For Sephiroth: Text color is either '#AAAAAA' (gray) for non-focused Sephiroth or 'black' as the default
- For Paths: Text color is hardcoded to 'black'

This causes readability issues when Sephiroth or Paths have dark background colors, as black text becomes difficult to read against dark backgrounds.

## Solution Approach

Implement a dynamic text color system that:

1. Keeps black as the default text color
2. Automatically switches to white (or light-colored) text when the background is detected to be too dark
3. Maintains the current behavior for non-focused elements (which are already grayed out)

## Implementation Tasks

- [x] 1. Create a utility function to detect color brightness
- [x] 2. Modify the Sephiroth rendering code to use dynamic text colors
- [x] 3. Modify the Path number rendering code to use dynamic text colors
- [x] 4. Add tests to verify the functionality
- [x] 5. Update documentation
- [x] 6. Fix special case for bright green in King Scale (paths 14 and 22)

## Implementation Details

### 1. Color Brightness Detection

We've implemented a function in `color_utils.py` to calculate the perceived brightness of a color and determine if it needs light or dark text:

```python
def get_contrasting_text_color(background_color: str) -> str:
    """
    Determine whether to use light or dark text based on background color brightness.

    Args:
        background_color: Hex color string (e.g., "#RRGGBB")

    Returns:
        Text color as hex string ("#FFFFFF" for white or "#000000" for black)
    """
    # Convert hex color to RGB values
    bg_color = background_color.lstrip('#')
    r, g, b = int(bg_color[0:2], 16), int(bg_color[2:4], 16), int(bg_color[4:6], 16)

    # Special case for bright green (#00FF00) which should use black text
    if r == 0 and g > 240 and b == 0:
        return "#000000"

    # Calculate perceived brightness using the common formula
    # (0.299*R + 0.587*G + 0.114*B)
    brightness = (0.299 * r + 0.587 * g + 0.114 * b)

    # Use white text on dark backgrounds, black text on light backgrounds
    # Use a higher threshold (150) for better readability with gray colors
    return "#FFFFFF" if brightness < 150 else "#000000"
```

### 2. Modify Sephiroth Rendering

In the `render` method of `TreeOfLife.py`, we've updated the text color logic:

```python
# If focusing on a specific sephirah, gray out all except the focused one
if focus_sephirah is not None and seph_num != focus_sephirah:
    # Gray out connected sephiroth without reducing opacity
    alpha = 1.0
    circle_face_color = '#E0E0E0'  # Slightly darker gray for non-focused sephiroth
    circle_edge_color_override = '#AAAAAA'  # Border is slightly darker gray
    text_color = '#AAAAAA'  # Match number to darker gray
else:
    alpha = 1.0
    circle_face_color = color  # Use the sephirah's color
    circle_edge_color_override = circle_edge_color  # Use default border color
    # Dynamically determine text color based on background brightness
    text_color = get_contrasting_text_color(circle_face_color)
```

### 3. Modify Path Number Rendering

In the `_add_path_number` method, we've updated the text color logic:

```python
# Get the path color from the paths dictionary
path = self.paths.get(path_num)
path_color = path.color if path else '#888888'

# Dynamic text color based on path color
text_color = 'black'  # Default
if path_color != '#888888':  # Only change for focused paths (non-gray)
    text_color = get_contrasting_text_color(path_color)

# Draw text without background or border
ax.text(
    mid_x, mid_y + special_offset_y,
    path_label,
    fontsize=9 * self.sphere_scale_factor * 0.55,
    fontweight='bold',
    ha='center',
    va='center',
    color=text_color,  # Use the dynamic text color
    rotation=rotation,
    rotation_mode='anchor',
    zorder=zorder
)
```

### 4. Testing

We've created a test file `test_color_contrast.py` that tests the brightness detection function with various colors:

```python
import unittest
from color_utils import get_contrasting_text_color


class TestColorContrast(unittest.TestCase):
    """Test cases for the color contrast utility function."""

    def test_get_contrasting_text_color(self):
        """Test that dark backgrounds get white text and light backgrounds get black text."""
        # Dark colors should return white text
        self.assertEqual(get_contrasting_text_color("#000000"), "#FFFFFF")  # Black
        self.assertEqual(get_contrasting_text_color("#0000FF"), "#FFFFFF")  # Blue
        # ... more test cases ...

    def test_with_actual_color_schemes(self):
        """Test with colors that might be used in the Tree of Life visualization."""
        # Test with sample colors from Tree of Life color schemes
        # ... color scheme test cases ...
```

### 5. Documentation

We've updated the README.md file to include information about the dynamic text color feature:

```markdown
## Overview

This library provides a flexible, object-oriented implementation for rendering the Kabbalistic Tree of Life. It supports:

- Multiple color schemes (Plain, King Scale, Queen Scale, Prince Scale, Princess Scale)
- Focusing on individual Sephiroth with connected paths
- Special color effects (flecked, rayed, tinged)
- Dynamic text coloring for optimal readability
- High-quality output for both display and saving to file
- Modular architecture with separation of concerns

...

### Dynamic Text Color

The visualization automatically adjusts text colors based on the background brightness:

- For light-colored backgrounds, black text is used
- For dark-colored backgrounds, white text is used
- This ensures optimal readability regardless of the background color

This feature works for both Sephiroth numbers and Path numbers/symbols, and maintains the current behavior for non-focused elements (which are grayed out).
```

## Testing Strategy

1. **Manual Testing**:

   - Render the Tree of Life with different color schemes
   - Verify text readability on all Sephiroth and Paths
   - Specifically check dark-colored elements to ensure text is visible

2. **Edge Cases to Test**:
   - Very dark colors (near black)
   - Very light colors (near white)
   - Colors with high saturation but low brightness
   - Special color effects (flecked, rayed, tinged)

## Notes

- The brightness threshold has been set to 150 (instead of the mid-point 128) for better handling of gray tones
- A special case was added for bright green (#00FF00), which always uses black text for better readability in the King Scale paths 14 and 22
- For colors with special effects (flecked, rayed, tinged), we'll use the base color for brightness calculation
- The current implementation doesn't account for color opacity (alpha), but all colors in the current system appear to use full opacity

## References

- Current text color implementation for Sephiroth: Around line 690 in TreeOfLife.py
- Current text color implementation for Paths: Around line 757 in TreeOfLife.py
- Color utility functions: color_utils.py
- Project Readme File: README.md
