import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import re
from typing import List, Tuple, Dict, Optional, Union, NamedTuple, Literal, Any
from enum import Enum
from pathlib import Path as FilePath
import matplotlib.colors as mcolors

# Define type aliases for clarity
Coord = Tuple[float, float]
PathIndices = Tuple[int, int]
ColorEffect = Dict[str, Any]  # Stores special color effect information


class ColorScheme(Enum):
    """Enum defining the available color schemes for the Tree of Life."""
    PLAIN = "plain"  # Default color scheme from original implementation
    KING_SCALE = "king_scale"
    QUEEN_SCALE = "queen_scale"
    PRINCE_SCALE = "prince_scale"
    PRINCESS_SCALE = "princess_scale"


class Sephirah(NamedTuple):
    """Data structure to store information about a Sephirah."""
    number: int  # Sephirah number (1-10)
    name: str  # Name of the Sephirah (e.g., "Kether", "Chokmah", etc.)
    coord: Coord  # (x, y) coordinate for the Sephirah
    # Default color (will be overridden by color scheme)
    color: str = "#FFFFFF"
    # Special color effect (flecked, rayed, tinged)
    color_effect: Optional[ColorEffect] = None


class Path(NamedTuple):
    """Data structure to store information about a connecting path."""
    number: int  # Path number (11-32)
    # Tuple of the two Sephiroth indices it connects (0-based)
    connects: PathIndices
    # Default color (will be overridden by color scheme)
    color: str = "#FFFFFF"
    # Special color effect (flecked, rayed, tinged)
    color_effect: Optional[ColorEffect] = None


class ColorParser:
    """
    A utility class to parse color scales from the color_scales.md file.
    """

    # Regex patterns to extract color information
    SEPHIROTH_PATTERN = re.compile(
        r"(\d+|Daath),\s+(\w+)\s+=\s+(.*?)(\(.*?\))")
    PATH_PATTERN = re.compile(r"(\d+)\s+=\s+(.*?)(\(.*?\))")
    COLOR_HEX_PATTERN = re.compile(r"\(\s*#([A-Fa-f0-9]{6})\s*\)")
    FLECKED_PATTERN = re.compile(r"flecked\s+(.*?)\s+\(")
    RAYED_PATTERN = re.compile(r"rayed\s+(.*?)\s+\(")
    TINGED_PATTERN = re.compile(r"tinged\s+(.*?)\s+\(")

    @staticmethod
    def parse_color_scales(file_path: str) -> Dict[str, Dict[str, Dict[int, Dict[str, Any]]]]:
        """
        Parse the color_scales.md file to extract color information.

        Args:
            file_path: Path to the color_scales.md file

        Returns:
            Dictionary with structure:
            {
                'king_scale': {
                    'sephiroth': {1: {'color': '#FFFFFF', 'effects': {...}}, ...},
                    'paths': {11: {'color': '#FFFFC0', 'effects': {...}}, ...}
                },
                'queen_scale': {...},
                ...
            }
        """
        try:
            with open(file_path, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Color scales file not found at {file_path}")
            return {}

        # Initialize result dictionary
        result = {
            'king_scale': {'sephiroth': {}, 'paths': {}},
            'queen_scale': {'sephiroth': {}, 'paths': {}},
            'prince_scale': {'sephiroth': {}, 'paths': {}},
            'princess_scale': {'sephiroth': {}, 'paths': {}}
        }

        # Split content by scale sections
        sections = content.split('# ')[1:]  # Skip the first empty section

        for section in sections:
            lines = section.strip().split('\n')
            scale_name = lines[0].lower().replace(' ', '_')

            if scale_name not in result:
                continue  # Skip unexpected sections

            # Find the sephiroth and paths subsections
            sephiroth_idx = -1
            paths_idx = -1

            for i, line in enumerate(lines):
                if "## The " in line and "Sephiroth" in line:
                    sephiroth_idx = i
                elif "## The " in line and "Paths" in line:
                    paths_idx = i

            # Parse Sephiroth
            if sephiroth_idx >= 0:
                end_idx = paths_idx if paths_idx > sephiroth_idx else len(
                    lines)
                sephiroth_lines = lines[sephiroth_idx+1:end_idx]

                for line in sephiroth_lines:
                    line = line.strip()
                    if not line or line.startswith('##'):
                        continue

                    match = ColorParser.SEPHIROTH_PATTERN.search(line)
                    if match:
                        num_str, name, desc, hex_part = match.groups()

                        # Handle special case for Da'ath
                        if num_str == "Daath":
                            num = 0  # Use 0 for Da'ath
                        else:
                            num = int(num_str)

                        # Extract the hex color
                        hex_match = ColorParser.COLOR_HEX_PATTERN.search(
                            hex_part)
                        if hex_match:
                            color = f"#{hex_match.group(1)}"
                        else:
                            color = "#FFFFFF"  # Default white if no color found

                        # Check for special effects
                        effects = {}

                        flecked_match = ColorParser.FLECKED_PATTERN.search(
                            desc)
                        if flecked_match:
                            effects['type'] = 'flecked'
                            effects['color2'] = flecked_match.group(1)
                            # Look for the second color's hex in the description
                            if "flecked" in line and "with" in line and "#" in line.split("with")[1]:
                                fleck_hex = re.search(
                                    r'#([A-Fa-f0-9]{6})', line.split("with")[1])
                                if fleck_hex:
                                    effects['color2_hex'] = f"#{fleck_hex.group(1)}"

                        rayed_match = ColorParser.RAYED_PATTERN.search(desc)
                        if rayed_match:
                            effects['type'] = 'rayed'
                            effects['color2'] = rayed_match.group(1)
                            # Look for the second color's hex
                            if "rayed" in line and "with" in line and "#" in line.split("with")[1]:
                                ray_hex = re.search(
                                    r'#([A-Fa-f0-9]{6})', line.split("with")[1])
                                if ray_hex:
                                    effects['color2_hex'] = f"#{ray_hex.group(1)}"

                        tinged_match = ColorParser.TINGED_PATTERN.search(desc)
                        if tinged_match:
                            effects['type'] = 'tinged'
                            effects['color2'] = tinged_match.group(1)
                            # Tinged typically doesn't have a second hex specified

                        # Store the result
                        result[scale_name]['sephiroth'][num] = {
                            'color': color,
                            'effects': effects if effects else None
                        }

            # Parse Paths
            if paths_idx >= 0:
                path_lines = lines[paths_idx+1:]

                for line in path_lines:
                    line = line.strip()
                    if not line or line.startswith('##'):
                        continue

                    match = ColorParser.PATH_PATTERN.search(line)
                    if match:
                        num_str, desc, hex_part = match.groups()
                        num = int(num_str)

                        # Extract the hex color
                        hex_match = ColorParser.COLOR_HEX_PATTERN.search(
                            hex_part)
                        if hex_match:
                            color = f"#{hex_match.group(1)}"
                        else:
                            color = "#FFFFFF"  # Default white if no color found

                        # Check for special effects
                        effects = {}

                        flecked_match = ColorParser.FLECKED_PATTERN.search(
                            desc)
                        if flecked_match:
                            effects['type'] = 'flecked'
                            effects['color2'] = flecked_match.group(1)
                            # Look for the second color's hex in the description
                            if "flecked" in line and "with" in line and "#" in line.split("with")[1]:
                                fleck_hex = re.search(
                                    r'#([A-Fa-f0-9]{6})', line.split("with")[1])
                                if fleck_hex:
                                    effects['color2_hex'] = f"#{fleck_hex.group(1)}"

                        rayed_match = ColorParser.RAYED_PATTERN.search(desc)
                        if rayed_match:
                            effects['type'] = 'rayed'
                            effects['color2'] = rayed_match.group(1)
                            # Look for the second color's hex
                            if "rayed" in line and "with" in line and "#" in line.split("with")[1]:
                                ray_hex = re.search(
                                    r'#([A-Fa-f0-9]{6})', line.split("with")[1])
                                if ray_hex:
                                    effects['color2_hex'] = f"#{ray_hex.group(1)}"

                        tinged_match = ColorParser.TINGED_PATTERN.search(desc)
                        if tinged_match:
                            effects['type'] = 'tinged'
                            effects['color2'] = tinged_match.group(1)
                            # Tinged typically doesn't have a second hex specified

                        # Store the result
                        result[scale_name]['paths'][num] = {
                            'color': color,
                            'effects': effects if effects else None
                        }

        return result


class TreeOfLife:
    """Class to create, manipulate and render the Kabbalistic Tree of Life diagram."""

    # Default plain colors for sephiroth and paths based on the original implementation
    DEFAULT_SEPHIROTH_COLORS = {
        0: "#E6E6FA",   # Da'ath - Lavender
        1: "#FFFFFF",   # Kether - White
        2: "#AACCFF",   # Chokmah - Pale Blue
        3: "#DC143C",   # Binah - Crimson
        4: "#9400D3",   # Chesed - Deep Violet
        5: "#FF7F00",   # Geburah - Orange
        6: "#FFB6C1",   # Tiphereth - Pink
        7: "#FFBF00",   # Netzach - Amber
        8: "#E6E6FA",   # Hod - Lavender
        9: "#4B0082",   # Yesod - Indigo
        10: "#FFFF00"   # Malkuth - Yellow
    }

    DEFAULT_PATH_COLORS = {
        # Use a neutral color for all paths in the default scheme
        # This will be overridden by specific color schemes
        i: "#FFFFFF" for i in range(11, 33)
    }

    def __init__(self,
                 sphere_scale_factor: float = 1.75,
                 spacing_factor: float = 1.5,
                 sephiroth_color_scheme: ColorScheme = ColorScheme.PLAIN,
                 path_color_scheme: ColorScheme = ColorScheme.PLAIN,
                 color_scales_file: str = "color_scales.md"):
        """
        Initialize the Tree of Life with configurable parameters.

        Args:
            sphere_scale_factor: Scale factor for spheres (sephiroth)
            spacing_factor: Factor to adjust spacing between spheres
            sephiroth_color_scheme: Color scheme to use for Sephiroth
            path_color_scheme: Color scheme to use for Paths
            color_scales_file: Path to the color scales file
        """
        # Store scaling parameters
        self.sphere_scale_factor = sphere_scale_factor
        self.spacing_factor = spacing_factor

        # Calculate derived values
        self.base_radius = 0.5
        self.circle_radius = self.base_radius * self.sphere_scale_factor
        self.vertical_shift = -0.5 * self.spacing_factor

        # Initialize color schemes
        self.sephiroth_color_scheme = sephiroth_color_scheme
        self.path_color_scheme = path_color_scheme

        # Initialize collections to store Sephiroth and Path data
        # Maps sephirah number (1-10) to its data
        self.sephiroth: Dict[int, Sephirah] = {}
        # Maps path number (11-32) to its data
        self.paths: Dict[int, Path] = {}

        # Initialize special case for Da'ath (the hidden Sephirah)
        self.daath = None

        # Parse the color scales file
        self.color_scales_file = color_scales_file
        self.color_data = self._load_color_data()

        # Initialize the Sephiroth and Paths
        self._init_sephiroth()
        self._init_paths()
        self._init_daath()

        # Apply the initial color schemes
        self.set_sephiroth_color_scheme(sephiroth_color_scheme)
        self.set_path_color_scheme(path_color_scheme)

    def _load_color_data(self) -> Dict[str, Dict[str, Dict[int, Dict[str, Any]]]]:
        """Load color data from the color scales file."""
        if FilePath(self.color_scales_file).exists():
            return ColorParser.parse_color_scales(self.color_scales_file)
        else:
            print(
                f"Warning: Color scales file '{self.color_scales_file}' not found. Using default colors.")
            return {}

    def _init_sephiroth(self) -> None:
        """Initialize the positions and properties of the Sephiroth."""
        # Define the coordinates for the Sephiroth with adjusted spacing
        sephiroth_data = [
            # number, name, (x, y) coordinates
            (1, "Kether", (0 * self.spacing_factor, 9 * self.spacing_factor)),
            (2, "Chokmah", (2.0 * self.spacing_factor, 8.0 *
             self.spacing_factor + self.vertical_shift)),
            (3, "Binah", (-2.0 * self.spacing_factor, 8.0 *
             self.spacing_factor + self.vertical_shift)),
            (4, "Chesed", (2.0 * self.spacing_factor, 5.5 *
             self.spacing_factor + self.vertical_shift)),
            (5, "Geburah", (-2.0 * self.spacing_factor, 5.5 *
             self.spacing_factor + self.vertical_shift)),
            (6, "Tiphereth", (0 * self.spacing_factor, 4.25 *
             self.spacing_factor + self.vertical_shift)),
            (7, "Netzach", (2.0 * self.spacing_factor, 3.0 *
             self.spacing_factor + self.vertical_shift)),
            (8, "Hod", (-2.0 * self.spacing_factor, 3.0 *
             self.spacing_factor + self.vertical_shift)),
            (9, "Yesod", (0 * self.spacing_factor, 1.75 *
             self.spacing_factor + self.vertical_shift)),
            (10, "Malkuth", (0 * self.spacing_factor, -
             0.7 * self.spacing_factor + self.vertical_shift))
        ]

        # Create Sephirah objects and store them in the dictionary
        for number, name, coord in sephiroth_data:
            self.sephiroth[number] = Sephirah(
                number=number,
                name=name,
                coord=coord,
                color=self.DEFAULT_SEPHIROTH_COLORS[number]
            )

    def _init_paths(self) -> None:
        """Initialize the paths connecting the Sephiroth."""
        # Define the paths connecting the Sephiroth
        # Each entry maps a 1-based path number (11-32) to a tuple of 1-based Sephiroth numbers
        path_connections = [
            # Path number, (from_sephirah, to_sephirah)
            (11, (1, 2)),  # Kether to Chokmah
            (12, (1, 3)),  # Kether to Binah
            (13, (1, 6)),  # Kether to Tiphereth
            (14, (2, 3)),  # Chokmah to Binah
            (15, (2, 6)),  # Chokmah to Tiphereth
            (16, (2, 4)),  # Chokmah to Chesed
            (17, (3, 6)),  # Binah to Tiphereth
            (18, (3, 5)),  # Binah to Geburah
            (19, (4, 5)),  # Chesed to Geburah
            (20, (4, 6)),  # Chesed to Tiphereth
            (21, (4, 7)),  # Chesed to Netzach
            (22, (5, 6)),  # Geburah to Tiphereth
            (23, (5, 8)),  # Geburah to Hod
            (24, (6, 7)),  # Tiphereth to Netzach
            (25, (6, 9)),  # Tiphereth to Yesod
            (26, (6, 8)),  # Tiphereth to Hod
            (27, (7, 8)),  # Netzach to Hod
            (28, (7, 9)),  # Netzach to Yesod
            (29, (7, 10)),  # Netzach to Malkuth
            (30, (8, 9)),  # Hod to Yesod
            (31, (8, 10)),  # Hod to Malkuth
            (32, (9, 10))   # Yesod to Malkuth
        ]

        # Create Path objects and store them in the dictionary
        for number, (from_sephirah, to_sephirah) in path_connections:
            # Convert from 1-based to 0-based indices for internal path representation
            connects = (from_sephirah - 1, to_sephirah - 1)
            self.paths[number] = Path(
                number=number,
                connects=connects,
                color=self.DEFAULT_PATH_COLORS[number]
            )

    def _init_daath(self) -> None:
        """Initialize the hidden Sephirah Da'ath."""
        # Da'ath is positioned at the geometric center of Chokmah, Binah, Chesed, and Geburah
        daath_coord = (0 * self.spacing_factor, 6.75 *
                       self.spacing_factor + self.vertical_shift)
        self.daath = Sephirah(
            number=0,
            name="Da'ath",
            coord=daath_coord,
            color=self.DEFAULT_SEPHIROTH_COLORS[0]
        )

    def set_sephiroth_color_scheme(self, scheme: ColorScheme) -> None:
        """
        Set the color scheme for all Sephiroth.

        Args:
            scheme: The color scheme to apply to Sephiroth
        """
        self.sephiroth_color_scheme = scheme

        # Dictionary to store updated Sephiroth with new colors
        updated_sephiroth = {}

        if scheme == ColorScheme.PLAIN:
            # Use default colors for the plain scheme
            for number, sephirah in self.sephiroth.items():
                color = self.DEFAULT_SEPHIROTH_COLORS[number]
                updated_sephiroth[number] = Sephirah(
                    number=sephirah.number,
                    name=sephirah.name,
                    coord=sephirah.coord,
                    color=color
                )

            # Update Da'ath separately
            self.daath = Sephirah(
                number=self.daath.number,
                name=self.daath.name,
                coord=self.daath.coord,
                color=self.DEFAULT_SEPHIROTH_COLORS[0]
            )
        else:
            # Use colors from the parsed color scales file
            scheme_name = scheme.value

            if not self.color_data or scheme_name not in self.color_data:
                print(
                    f"Warning: Color scheme '{scheme_name}' not found. Using default colors.")
                return

            for number, sephirah in self.sephiroth.items():
                # Get color data for this sephirah in the selected scheme
                seph_data = self.color_data[scheme_name]['sephiroth'].get(
                    number)

                if seph_data:
                    color = seph_data['color']
                    effects = seph_data['effects']

                    updated_sephiroth[number] = Sephirah(
                        number=sephirah.number,
                        name=sephirah.name,
                        coord=sephirah.coord,
                        color=color,
                        color_effect=effects
                    )
                else:
                    # If no color data found, keep the current color
                    updated_sephiroth[number] = sephirah

            # Handle Da'ath separately
            daath_data = self.color_data[scheme_name]['sephiroth'].get(0)
            if daath_data:
                self.daath = Sephirah(
                    number=self.daath.number,
                    name=self.daath.name,
                    coord=self.daath.coord,
                    color=daath_data['color'],
                    color_effect=daath_data['effects']
                )

        # Update the sephiroth dictionary with the new colors
        self.sephiroth = updated_sephiroth

    def set_path_color_scheme(self, scheme: ColorScheme) -> None:
        """
        Set the color scheme for all paths.

        Args:
            scheme: The color scheme to apply to paths
        """
        self.path_color_scheme = scheme

        # Dictionary to store updated paths with new colors
        updated_paths = {}

        if scheme == ColorScheme.PLAIN:
            # Use default colors for the plain scheme
            for number, path in self.paths.items():
                color = self.DEFAULT_PATH_COLORS[number]
                updated_paths[number] = Path(
                    number=path.number,
                    connects=path.connects,
                    color=color
                )
        else:
            # Use colors from the parsed color scales file
            scheme_name = scheme.value

            if not self.color_data or scheme_name not in self.color_data:
                print(
                    f"Warning: Color scheme '{scheme_name}' not found. Using default colors.")
                return

            for number, path in self.paths.items():
                # Get color data for this path in the selected scheme
                path_data = self.color_data[scheme_name]['paths'].get(number)

                if path_data:
                    color = path_data['color']
                    effects = path_data['effects']

                    updated_paths[number] = Path(
                        number=path.number,
                        connects=path.connects,
                        color=color,
                        color_effect=effects
                    )
                else:
                    # If no color data found, keep the current color
                    updated_paths[number] = path

        # Update the paths dictionary with the new colors
        self.paths = updated_paths

    def _apply_color_effect(self, ax, element_type: str, number: int, x: float, y: float,
                            color: str, effect: Optional[ColorEffect], radius: float = None) -> None:
        """
        Apply special color effects (flecked, rayed, tinged) to a Sephirah or Path.

        Args:
            ax: Matplotlib axis to draw on
            element_type: Type of element ('sephirah' or 'path')
            number: Element number (1-10 for Sephiroth, 11-32 for Paths)
            x, y: Center coordinates
            color: Base color
            effect: Special color effect data
            radius: Radius (for Sephiroth only)
        """
        if not effect:
            return

        effect_type = effect.get('type')

        if effect_type == 'flecked':
            # Get the second color for flecking
            color2 = effect.get('color2_hex', '#FFFFFF')

            if element_type == 'sephirah' and radius:
                # Draw small circles randomly distributed within the Sephirah
                num_flecks = 50  # Number of flecks
                # Use element number as seed for reproducibility
                np.random.seed(number)

                for _ in range(num_flecks):
                    # Random position within the circle
                    angle = np.random.uniform(0, 2 * np.pi)
                    # Stay within 90% of radius
                    r = np.random.uniform(0, radius * 0.9)
                    fleck_x = x + r * np.cos(angle)
                    fleck_y = y + r * np.sin(angle)

                    # Random size for the fleck, proportional to the main circle
                    fleck_size = np.random.uniform(0.02, 0.05) * radius

                    # Draw the fleck
                    fleck = patches.Circle(
                        (fleck_x, fleck_y),
                        fleck_size,
                        facecolor=color2,
                        edgecolor=None,
                        alpha=0.8,
                        zorder=5  # Above the main circle
                    )
                    ax.add_patch(fleck)

            elif element_type == 'path':
                # For paths, this will need to be implemented differently when drawing paths
                pass

        elif effect_type == 'rayed':
            # Get the second color for rays
            color2 = effect.get('color2_hex', '#FFFFFF')

            if element_type == 'sephirah' and radius:
                # Draw rays emanating from the center
                num_rays = 12  # Number of rays
                ray_length = radius * 1.5  # Rays extend beyond the circle

                for i in range(num_rays):
                    angle = i * (2 * np.pi / num_rays)
                    end_x = x + ray_length * np.cos(angle)
                    end_y = y + ray_length * np.sin(angle)

                    # Draw the ray as a line
                    ax.plot(
                        [x, end_x],
                        [y, end_y],
                        color=color2,
                        linewidth=radius * 0.1,
                        alpha=0.6,
                        zorder=2  # Below the main circle but above background
                    )

            elif element_type == 'path':
                # For paths, this will need to be implemented differently when drawing paths
                pass

        elif effect_type == 'tinged':
            # For tinged, we slightly blend the color with another
            # This is typically applied by giving the main color a slight tint
            # The actual implementation will happen when drawing the elements
            pass

    def _blend_colors(self, color1: str, color2: str, ratio: float = 0.8) -> str:
        """
        Blend two colors together with the given ratio.

        Args:
            color1: First color (as hex string)
            color2: Second color (as hex string)
            ratio: Ratio of the first color (0.0 to 1.0)

        Returns:
            Blended color as hex string
        """
        # Convert hex strings to RGB
        rgb1 = mcolors.to_rgb(color1)
        rgb2 = mcolors.to_rgb(color2)

        # Blend the colors
        blended_rgb = tuple(c1 * ratio + c2 * (1 - ratio)
                            for c1, c2 in zip(rgb1, rgb2))

        # Convert back to hex
        return mcolors.to_hex(blended_rgb)

    def render(self,
               focus_sephirah: Optional[int] = None,
               display: bool = True,
               save_to_file: Optional[str] = None) -> None:
        """
        Render the Tree of Life diagram.

        Args:
            focus_sephirah: If provided, render only this Sephirah (1-10) and its connected paths
            display: Whether to display the diagram in a window
            save_to_file: If provided, save the diagram to this filename
        """
        # TODO: Implement rendering logic
        # This will be done in Phase 4
        pass
