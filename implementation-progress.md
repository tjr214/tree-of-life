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

- [ ] Add class attributes to track text display preferences:
  - [ ] `self.show_sephiroth_text: bool = True`
  - [ ] `self.show_path_text: bool = True`
- [ ] Add setter methods:
  - [ ] `set_sephiroth_text_visibility(self, visible: bool)`
  - [ ] `set_path_text_visibility(self, visible: bool)`
- [ ] Update render method:
  - [ ] Add conditional check before rendering Sephiroth text
  - [ ] Add conditional check before rendering Path text

### 3. Implement Sephiroth Text Display Modes

- [ ] Create enum for Sephiroth text display modes:
  ```python
  class SephirothTextMode(Enum):
      NUMBER = "number"
      TRIGRAM = "trigram"
      HEBREW = "hebrew"
      PLANET = "planet"
  ```
- [ ] Add class attribute to track current text mode:
  - [ ] `self.sephiroth_text_mode: SephirothTextMode = SephirothTextMode.NUMBER`
- [ ] Add setter method:
  - [ ] `set_sephiroth_text_mode(self, mode: SephirothTextMode)`
- [ ] Create mappings for different text modes:
  - [ ] I Ching Trigram mapping:
    ```python
    self._trigram_map = {
        1: "☯",  # The Supreme Ultimate (Kether)
        2: "⚊",  # Solid Line (Chokmah)
        3: "⚋",  # Broken Line (Binah)
        0: "☰",  # Heaven (Da'ath)
        4: "☱",  # Lake (Chesed)
        5: "☳",  # Thunder (Geburah)
        6: "☲",  # Fire/Sun (Tiphereth)
        7: "☶",  # Mountain (Netzach)
        8: "☴",  # Wind (Hod)
        9: "☵",  # Water/Moon (Yesod)
        10: "☷"  # Earth (Malkuth)
    }
    ```
  - [ ] Planetary symbol mapping:
    ```python
    self._planet_map = {
        1: "♇",  # Pluto (Kether)
        2: "⛢",  # Uranus (Chokmah)
        3: "♄",  # Saturn (Binah)
        0: "♆",  # Neptune (Da'ath)
        4: "♃",  # Jupiter (Chesed)
        5: "♂",  # Mars (Geburah)
        6: "☉",  # Sun (Tiphereth)
        7: "♀",  # Venus (Netzach)
        8: "☿",  # Mercury (Hod)
        9: "☽",  # Moon (Yesod)
        10: "⊕"  # Earth (Malkuth)
    }
    ```
  - [ ] Hebrew name mapping:
    ```python
    self._hebrew_map = {
        1: "כתר",       # Kether
        2: "חכמה",      # Chokmah
        3: "בינה",      # Binah
        0: "דעת",       # Da'ath
        4: "חסד",       # Chesed
        5: "גבורה",     # Geburah
        6: "תפארת",     # Tiphereth
        7: "נצח",       # Netzach
        8: "הוד",       # Hod
        9: "יסוד",      # Yesod
        10: "מלכות"     # Malkuth
    }
    ```

### 4. Modify Text Rendering Logic

- [ ] Update the text rendering code in the render method:
  - [ ] For Sephiroth numbers (around line 679):
    - [ ] Check `self.show_sephiroth_text` before rendering text
    - [ ] Switch text content based on `self.sephiroth_text_mode`
    - [ ] Maintain dynamic text color based on background
  - [ ] For Path numbers (in `_add_path_number`, around line 798):
    - [ ] Check `self.show_path_text` before rendering path text
- [ ] Ensure proper text sizing and positioning:
  - [ ] Adjust font size for Hebrew text (potentially smaller)
  - [ ] Adjust font size for trigram and planetary symbols
  - [ ] Ensure proper right-to-left rendering for Hebrew text

### 5. Update Da'ath Rendering

- [ ] Update the Da'ath hidden Sephirah rendering to respect the same text settings:
  - [ ] Apply text visibility toggle
  - [ ] Apply correct text display mode

### 6. Testing

- [ ] Test in normal mode:
  - [ ] Verify all text display modes work correctly
  - [ ] Verify text toggling works correctly for both Sephiroth and Paths
- [ ] Test in focus mode (specific Sephirah):
  - [ ] Verify all text display modes work correctly
  - [ ] Verify text toggling works correctly for both Sephiroth and Paths
- [ ] Test edge cases:
  - [ ] Ensure Hebrew text renders correctly in RTL format
  - [ ] Ensure text visibility remains correct when switching display modes

### 7. Documentation

- [ ] Update docstrings for new methods
- [ ] Add type hints to all new methods
- [ ] Document the new features in the class comments
- [ ] Add examples to demonstration script
- [ ] Update the repo README.md with the new features
- [ ] Update the library README.md, as well

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
