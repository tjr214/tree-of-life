# TreeOfLife Class Refactoring Project Progress

You can use the read tool to read in `new_tree.py` and `color_scales.md` whenever you need that information. The Python requirements are in `requirements.txt`.

## Phase 1: Setup and Planning

- [x] Review existing `new_tree.py` code
- [x] Define requirements for the `TreeOfLife` class
- [x] Create this task list document

## Phase 2: Basic Class Structure

- [x] Create `TreeOfLife` class with constructor and basic attributes

  - [x] Define class skeleton with appropriate imports
  - [x] Implement constructor with default parameters
  - [x] Set up default scaling and spacing parameters
  - [x] Initialize default color schemes

- [x] Define color scheme ENUMs

  - [x] Create ColorScheme enum with PLAIN, KING_SCALE, QUEEN_SCALE, PRINCE_SCALE, PRINCESS_SCALE
  - [x] Document enum values with descriptions

- [x] Create data structures to store Sephiroth and Paths information

  - [x] Define Sephirah class or namedtuple for storing Sephirah data
  - [x] Define Path class or namedtuple for storing path data
  - [x] Create structure to map Sephiroth numbers (1-10) to their data
  - [x] Create structure to map path numbers (11-32) to their data
  - [x] Store the coordinates and connections from original code

- [x] Implement basic setup methods
  - [x] Method to initialize Sephiroth positions and properties
  - [x] Method to initialize path connections and properties
  - [x] Method to handle Da'ath's special case

## Phase 3: Color Scheme Implementation

- [x] Parse color data from color scales

  - [x] Create parser for `color_scales.md` file
  - [x] Extract color definitions for each scheme
  - [x] Handle special effect colors (flecked, rayed, tinged)
  - [x] Create mapping from Sephiroth/path numbers to colors for each scheme

- [x] Implement plain/default color scheme

  - [x] Define default colors based on the original implementation
  - [x] Create method to apply default colors to all elements

- [x] Implement `set_sephiroth_color_scheme` method

  - [x] Create method to change the color scheme for all Sephiroth
  - [x] Handle validation and error cases
  - [x] Ensure Da'ath is handled correctly

- [x] Implement `set_path_color_scheme` method

  - [x] Create method to change the color scheme for all paths
  - [x] Handle validation and error cases

- [x] Create helper methods for specialized color effects
  - [x] Implement flecked color rendering helper
  - [x] Implement rayed color rendering helper
  - [x] Implement tinged color rendering helper
  - [x] Create color utility functions (blend, convert, etc.)

## Phase 4: Rendering Implementation

- [x] Implement base rendering logic

  - [x] Create core render method structure
  - [x] Set up plot parameters and configuration
  - [x] Implement Sephiroth drawing logic
  - [x] Implement path drawing logic
  - [x] Implement Da'ath drawing logic
  - [x] Handle special case for Kether's radiant effect

- [x] Implement selective Sephirah rendering

  - [x] Create method to focus on a specific Sephirah
  - [x] Implement zooming or framing logic for focus view
  - [x] Handle special layout adjustments for focused view

- [x] Create method to determine which paths to include when rendering a single Sephirah

  - [x] Implement path filtering logic
  - [x] Create mapping of Sephiroth to their connected paths
  - [x] Ensure all relevant paths are included

- [x] Implement logic to gray out connected Sephiroth

  - [x] Create method to modify colors for grayed out state
  - [x] Adjust opacity and saturation for connected Sephiroth
  - [x] Ensure visual hierarchy (focused Sephirah > paths > connected Sephiroth)

- [x] Implement special color effects rendering
  - [x] Integrate flecked color rendering
  - [x] Integrate rayed color rendering
  - [x] Integrate tinged color rendering
  - [x] Implement any other special color effects

## Phase 5: Output Methods

- [x] Implement method to display the tree in a window

  - [x] Create display method with appropriate parameters
  - [x] Handle matplotlib figure configuration
  - [x] Implement interactive elements if needed
  - [x] Add window title and metadata

- [x] Implement method to save the tree to a file

  - [x] Create save method with filename parameter
  - [x] Support multiple file formats (png, svg, pdf)
  - [x] Handle file path validation and error cases
  - [x] Set appropriate DPI and quality settings

- [x] Create a combined method to both display and save
  - [x] Implement method that calls both display and save
  - [x] Add parameter to control this behavior
  - [x] Ensure proper cleanup and resource management

## Phase 6: Testing and Refinement

- [ ] Test full tree rendering with different color schemes

  - [ ] Test with default/plain scheme
  - [ ] Test with King Scale
  - [ ] Test with Queen Scale
  - [ ] Test with Prince Scale
  - [ ] Test with Princess Scale
  - [ ] Compare output with expected results

- [ ] Test selective Sephirah rendering

  - [ ] Test rendering each individual Sephirah (1-10)
  - [ ] Verify correct paths are included
  - [ ] Verify connected Sephiroth are properly grayed out
  - [ ] Test boundary cases and error handling

- [ ] Test special color effects

  - [ ] Test flecked color rendering
  - [ ] Test rayed color rendering
  - [ ] Test tinged color rendering
  - [ ] Test combinations of effects

- [ ] Optimize and refine code

  - [ ] Identify and fix any performance bottlenecks
  - [ ] Refactor repeated code into utility functions
  - [ ] Optimize color rendering for performance
  - [ ] Clean up variable names and code structure

- [ ] Add detailed documentation
  - [ ] Add docstrings to all classes and methods
  - [ ] Document parameters and return values
  - [ ] Add usage examples in documentation
  - [ ] Create README with overview and examples

## Phase 7: Final Implementation

- [x] Write example usage code

  - [x] Basic usage example script
  - [x] Color scheme switching example
  - [x] Selective rendering example
  - [x] Complete demonstration of all features

- [ ] Create demonstration script

  - [ ] Create script that demonstrates all color schemes
  - [ ] Add examples of focused Sephirah rendering
  - [ ] Generate sample output files
  - [ ] Add explanatory comments

- [ ] Final review and testing

  - [ ] Code review for quality and style
  - [ ] Test on different platforms if applicable
  - [ ] Handle any edge cases or bugs
  - [ ] Verify all requirements are met

- [ ] Integration with any existing systems
  - [ ] Ensure compatibility with larger codebase if applicable
  - [ ] Create any necessary adapter methods
  - [ ] Document integration points

## Future Enhancements

- [ ] Add option for custom color schemes

  - [ ] Create interface for defining custom colors
  - [ ] Add save/load functionality for custom schemes

- [ ] Add option to adjust size and spacing

  - [ ] Create methods to customize layout parameters
  - [ ] Add presets for different aspect ratios

- [ ] Add text labels for Sephiroth names

  - [ ] Add support for displaying Hebrew names
  - [ ] Add support for displaying English names
  - [ ] Add customizable label positioning

- [ ] Add support for Hebrew letter and astrological symbol display options
  - [ ] Enhance path display with more symbol options
  - [ ] Add toggle for different symbol sets

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
