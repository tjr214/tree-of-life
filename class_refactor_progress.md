# TreeOfLife Class Refactoring Project Progress

## Phase 1: Setup and Planning

- [x] Review existing `new_tree.py` code
- [x] Define requirements for the `TreeOfLife` class
- [x] Create this task list document

## Phase 2: Basic Class Structure

- [ ] Create `TreeOfLife` class with constructor and basic attributes
- [ ] Define color scheme ENUMs
- [ ] Create data structures to store Sephiroth and Paths information
- [ ] Implement basic setup methods

## Phase 3: Color Scheme Implementation

- [ ] Parse color data from color scales
- [ ] Implement plain/default color scheme
- [ ] Implement `set_sephiroth_color_scheme` method
- [ ] Implement `set_path_color_scheme` method
- [ ] Create helper methods for specialized color effects (flecked, rayed, tinged)

## Phase 4: Rendering Implementation

- [ ] Implement base rendering logic
- [ ] Implement selective Sephirah rendering
- [ ] Create method to determine which paths to include when rendering a single Sephirah
- [ ] Implement logic to gray out connected Sephiroth
- [ ] Implement special color effects rendering

## Phase 5: Output Methods

- [ ] Implement method to display the tree in a window
- [ ] Implement method to save the tree to a file
- [ ] Create a combined method to both display and save

## Phase 6: Testing and Refinement

- [ ] Test full tree rendering with different color schemes
- [ ] Test selective Sephirah rendering
- [ ] Test special color effects
- [ ] Optimize and refine code
- [ ] Add detailed documentation

## Phase 7: Final Implementation

- [ ] Write example usage code
- [ ] Create demonstration script
- [ ] Final review and testing
- [ ] Integration with any existing systems

## Future Enhancements

- [ ] Add option for custom color schemes
- [ ] Add option to adjust size and spacing
- [ ] Add text labels for Sephiroth names
- [ ] Add support for Hebrew letter and astrological symbol display options

## Implementation Details and Notes

### Project Overview

- We are refactoring `new_tree.py` into a class-based implementation called `TreeOfLife.py`
- The original code creates a fixed diagram of the Kabbalistic Tree of Life
- The refactored code will provide a flexible class with customization options

### Key Requirements

1. Implement a `TreeOfLife` class with all functionality from the original code
2. Allow setting different color schemes for Sephiroth and Paths separately
3. Provide option to render only one Sephirah and its connected paths
4. Support both display and file output options

### Color Scheme Implementation

- 5 color schemes: King Scale, Queen Scale, Prince Scale, Princess Scale, and Plain (default)
- Use ENUMs for scheme selection (e.g., `KING_SCALE`, `QUEEN_SCALE`, etc.)
- Color definitions for all schemes are in `color_scales.md`
- Plain/default scheme uses the original colors from `new_tree.py`
- Special effects in color schemes include:
  - Flecked: dotted with particles of another color
  - Rayed: has rays of another color emanating from it
  - Tinged: slightly colored with another color

### Selective Rendering

- Default is to render the entire Tree of Life
- Option to render single Sephirah by number (1-10)
- When rendering single Sephirah:
  - Show the selected Sephirah in full color
  - Include all directly connected paths
  - Show connected Sephiroth but gray them out
  - The graying out should make them visible but less prominent

### Class Interface

- Constructor should initialize with default plain color scheme
- Methods for changing color schemes:
  - `set_sephiroth_color_scheme(scheme_enum)`
  - `set_path_color_scheme(scheme_enum)`
- Methods for output:
  - Method to display in window
  - Method to save to file
  - Combined method to both display and save
- Method to render specific Sephirah (by number 1-10)

### Technical Implementation Notes

- Use Python typing for all methods and parameters
- Maintain compatibility with matplotlib plotting
- Implement specialized rendering for special color effects
- Scale and layout should be customizable but have good defaults
- Da'ath (the hidden Sephirah) should be handled as a special case, but should be rendered by default along with the rest of the Sephiroth

### Implementation Specifics

- Color rendering effects:

  - For "flecked" colors: Implement using small dots or speckles of the secondary color
  - For "rayed" colors: Draw semi-transparent lines emanating from the center in the secondary color
  - For "tinged" colors: Slightly blend the base color with the tinge color

- Graying out connected Sephiroth:

  - When rendering a single Sephirah, connected Sephiroth should maintain their shape but appear in grayscale
  - Reduce opacity to approximately 50-60% to make them less prominent
  - Maintain enough visibility to show the structure of the tree

- Path numbering:

  - Preserve the path numbers from the original implementation (11-32)
  - Include astrological symbols with path numbers as in the original

- Method for focusing on a specific Sephirah:
  - Should take an integer parameter (1-10) indicating the Sephirah number
  - Should handle Da'ath appropriately when connected to focused Sephirah
  - Default parameter value should render the entire tree
