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

- [ ] 1. Create a utility function to detect color brightness
- [ ] 2. Modify the Sephiroth rendering code to use dynamic text colors
- [ ] 3. Modify the Path number rendering code to use dynamic text colors
- [ ] 4. Add tests to verify the functionality
- [ ] 5. Update documentation

## Implementation Details

### 1. Color Brightness Detection

We'll implement a function in `color_utils.py` to calculate the perceived brightness of a color and determine if it needs light or dark text:

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

    # Calculate perceived brightness using the common formula
    # (0.299*R + 0.587*G + 0.114*B)
    brightness = (0.299 * r + 0.587 * g + 0.114 * b)

    # Use white text on dark backgrounds, black text on light backgrounds
    # 128 is the mid-point on the 0-255 scale
    return "#FFFFFF" if brightness < 128 else "#000000"
```

### 2. Modify Sephiroth Rendering

In the `render` method of `TreeOfLife.py`, we'll update the text color logic (around line 690-698):

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

In the `_add_path_number` method, we'll update the text color logic:

```python
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

- The brightness threshold (128) might need adjustment based on testing results
- For colors with special effects (flecked, rayed, tinged), we'll use the base color for brightness calculation
- The current implementation doesn't account for color opacity (alpha), but all colors in the current system appear to use full opacity

## References

- Current text color implementation for Sephiroth: Around line 690 in TreeOfLife.py
- Current text color implementation for Paths: Around line 757 in TreeOfLife.py
- Color utility functions: color_utils.py
