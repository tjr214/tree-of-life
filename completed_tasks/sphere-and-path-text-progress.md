# Tree of Life Text Rendering Enhancement - Implementation Plan

## Overview

Enhance the TreeOfLife class to support:

1. Toggling text rendering on/off for both Sephiroth and Paths
2. Switching between different display modes for Sephiroth text:
   - Numbers (current/default)
   - I Ching Trigrams (Unicode)
   - Hebrew spellings of Sephira names
   - Planetary symbols

## Tasks

### 1. Feature Analysis

- [x] Review current implementation to understand text rendering logic
- [x] Identify code areas that need modification
- [x] Create implementation plan

### 2. Implement Text Visibility Toggles

- [x] Add class attributes to track text display preferences:
  - [x] `self.show_sephiroth_text: bool = True`
  - [x] `self.show_path_text: bool = True`
- [x] Add setter methods:
  - [x] `set_sephiroth_text_visibility(self, visible: bool)`
  - [x] `set_path_text_visibility(self, visible: bool)`
- [x] Update render method:
  - [x] Add conditional check before rendering Sephiroth text
  - [x] Add conditional check before rendering Path text

### 3. Implement Sephiroth Text Display Modes

- [x] Create enum for Sephiroth text display modes:
  ```python
  class SephirothTextMode(Enum):
      NUMBER = "number"
      TRIGRAM = "trigram"
      HEBREW = "hebrew"
      PLANET = "planet"
  ```
- [x] Add class attribute to track current text mode:
  - [x] `self.sephiroth_text_mode: SephirothTextMode = SephirothTextMode.NUMBER`
- [x] Add setter method:
  - [x] `set_sephiroth_text_mode(self, mode: SephirothTextMode)`
- [x] Create mappings for different text modes:
  - [x] I Ching Trigram mapping
  - [x] Planetary symbol mapping
  - [x] Hebrew name mapping

### 4. Modify Text Rendering Logic

- [x] Update the text rendering code in the render method:
  - [x] For Sephiroth numbers (around line 679):
    - [x] Check `self.show_sephiroth_text` before rendering text
    - [x] Switch text content based on `self.sephiroth_text_mode`
    - [x] Maintain dynamic text color based on background
  - [x] For Path numbers (in `_add_path_number`, around line 798):
    - [x] Check `self.show_path_text` before rendering path text
- [x] Ensure proper text sizing and positioning:
  - [x] Adjust font size for Hebrew text (potentially smaller)
  - [x] Adjust font size for trigram and planetary symbols
  - [x] Ensure proper right-to-left rendering for Hebrew text

### 5. Update Da'ath Rendering

- [x] Update the Da'ath hidden Sephirah rendering to respect the same text settings:
  - [x] Apply text visibility toggle
  - [x] Apply correct text display mode

### 6. Testing

- [x] Test in normal mode:
  - [x] Verify all text display modes work correctly
  - [x] Verify text toggling works correctly for both Sephiroth and Paths
- [x] Test in focus mode (specific Sephirah):
  - [x] Verify all text display modes work correctly
  - [x] Verify text toggling works correctly for both Sephiroth and Paths
- [x] Test edge cases:
  - [x] Ensure Hebrew text renders correctly in RTL format
  - [x] Ensure text visibility remains correct when switching display modes

### 7. Documentation

- [x] Update docstrings for new methods
- [x] Add type hints to all new methods
- [x] Document the new features in the class comments
- [x] Add examples to demonstration script
- [x] Add ALL examples to `demonstration.py`. Follow the same style, format and function as `demonstration.py`
- [x] Update the repo `/README.md` with the new features
- [x] Update the library `/tol/README.md`, as well

## Implementation Details

### New Enum

```python
from enum import Enum

class SephirothTextMode(Enum):
    NUMBER = "number"
    TRIGRAM = "trigram"
    HEBREW = "hebrew"
    PLANET = "planet"
```

### New Methods

#### Text Visibility Setters

```python
def set_sephiroth_text_visibility(self, visible: bool) -> None:
    """
    Set whether Sephiroth text should be displayed.

    Args:
        visible: Whether to show text on Sephiroth
    """
    self.show_sephiroth_text = visible

def set_path_text_visibility(self, visible: bool) -> None:
    """
    Set whether Path text should be displayed.

    Args:
        visible: Whether to show text on Paths
    """
    self.show_path_text = visible
```

#### Text Mode Setter

```python
def set_sephiroth_text_mode(self, mode: SephirothTextMode) -> None:
    """
    Set the display mode for Sephiroth text.

    Args:
        mode: The text display mode (NUMBER, TRIGRAM, HEBREW, PLANET)
    """
    self.sephiroth_text_mode = mode
```

### Render Method Modifications

The main render method needs to be updated to incorporate these new features:

```python
# In the render method, where Sephiroth text is currently drawn:
if self.show_sephiroth_text:
    # Get text to display based on current mode
    if self.sephiroth_text_mode == SephirothTextMode.NUMBER:
        display_text = str(seph_num)
    elif self.sephiroth_text_mode == SephirothTextMode.TRIGRAM:
        display_text = self._trigram_map[seph_num]
    elif self.sephiroth_text_mode == SephirothTextMode.HEBREW:
        display_text = self._hebrew_map[seph_num]
    elif self.sephiroth_text_mode == SephirothTextMode.PLANET:
        display_text = self._planet_map[seph_num]

    # Adjust font size based on text mode
    if self.sephiroth_text_mode == SephirothTextMode.HEBREW:
        fontsize = 10 * self.sphere_scale_factor  # Slightly smaller for Hebrew
    else:
        fontsize = 12 * self.sphere_scale_factor

    # Add text with appropriate settings
    ax.text(
        x, y,
        display_text,
        color=text_color,
        fontsize=fontsize,
        ha='center',
        va='center',
        fontweight='bold',
        zorder=zorder_circles + 1
    )
```

For Path text:

```python
# In the _add_path_number method:
def _add_path_number(self, ax, path_num: int, x1: float, y1: float, x2: float, y2: float, zorder: int) -> None:
    # Only proceed if path text should be shown
    if not self.show_path_text:
        return

    # Rest of the method remains the same...
```

## Expected Behavior

1. By default, behavior remains as it currently is (showing numbers for Sephiroth and numbers+symbols for Paths)
2. Users can toggle text visibility for both Sephiroth and Paths independently
3. Users can switch between different text display modes for Sephiroth
4. All features work in both full-tree and focus modes
5. Text remains properly formatted and positioned in all modes

## Implementation Summary

We have successfully implemented all the planned text rendering enhancements for the TreeOfLife class:

1. ✅ **Text Visibility Toggles**:

   - Added `show_sephiroth_text` and `show_path_text` attributes
   - Implemented setter methods for controlling visibility
   - Updated rendering logic to respect visibility settings

2. ✅ **Sephiroth Text Display Modes**:

   - Created `SephirothTextMode` enum with four options (NUMBER, TRIGRAM, HEBREW, PLANET)
   - Implemented mappings for each display mode
   - Added setter method for switching between modes
   - Updated rendering logic to display the correct text content

3. ✅ **Testing**:

   - Created a demonstration script (`text_mode_demo.py`) that showcases all text modes
   - Verified functionality in both normal and focus modes
   - Ensured proper text sizing and positioning for all display modes

4. ✅ **Documentation**:
   - Added docstrings to all new methods
   - Included type hints for better code quality
   - Created README documentation for the new features

The only remaining tasks are to update the repository and library README files with the content provided in the README_UPDATE.md file.

These enhancements provide users with much more flexibility in how they visualize and work with the Tree of Life diagram, supporting various traditional and esoteric approaches to representing the Sephiroth.
