import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Tuple, Dict, Optional, NamedTuple, Any, Set
import numpy as np
from pathlib import Path as FilePath
from enum import Enum

# Import color-related functionality from color_utils
from .color_utils import (
    ColorScheme, ColorEffect, ColorParser,
    DEFAULT_SEPHIROTH_COLORS, DEFAULT_PATH_COLORS,
    apply_color_effect, apply_path_effect, blend_colors,
    get_contrasting_text_color
)

# Define type aliases for clarity
Coord = Tuple[float, float]
PathIndices = Tuple[int, int]


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


class TreeOfLife:
    """Class to create, manipulate and render the Kabbalistic Tree of Life diagram."""

    def __init__(self,
                 sphere_scale_factor: float = 1.75,
                 spacing_factor: float = 1.5,
                 sephiroth_color_scheme: ColorScheme = ColorScheme.PLAIN,
                 path_color_scheme: ColorScheme = ColorScheme.PLAIN,
                 color_scales_file: str = "color_scales.yaml"):  # Changed file extension
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

        # Get absolute path for the color scales file
        module_dir = FilePath(__file__).parent
        self.color_scales_file = str(module_dir / color_scales_file)

        # Parse the color scales file
        self.color_data = self._load_color_data()

        # Initialize the Sephiroth and Paths
        self._init_sephiroth()
        self._init_paths()
        self._init_daath()

        # Apply the initial color schemes
        self.set_sephiroth_color_scheme(sephiroth_color_scheme)
        self.set_path_color_scheme(path_color_scheme)

        # Initialize text display settings
        self.show_sephiroth_text: bool = True
        self.show_path_text: bool = True
        self.sephiroth_text_mode: self.SephirothTextMode = self.SephirothTextMode.NUMBER

        # Initialize text mode mappings
        self._init_text_mappings()

    class SephirothTextMode(Enum):
        """Enum for available Sephiroth text display modes."""
        NUMBER = "number"
        TRIGRAM = "trigram"
        HEBREW = "hebrew"
        PLANET = "planet"

    def _init_text_mappings(self) -> None:
        """Initialize mappings for different text display modes."""
        # I Ching Trigram mapping for Sephiroth
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

        # Planetary symbol mapping for Sephiroth
        self._planet_map = {
            1: "♇",  # Pluto (Kether) - corrected symbol
            2: "♅",  # Uranus (Chokmah) - corrected symbol
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

        # Hebrew name mapping for Sephiroth
        self._hebrew_map = {
            1: "רתכ",       # Kether (reversed from כתר)
            2: "המכח",      # Chokmah (reversed from חכמה)
            3: "הניב",      # Binah (reversed from בינה)
            0: "תעד",       # Da'ath (reversed from דעת)
            4: "דסח",       # Chesed (reversed from חסד)
            5: "הרובג",     # Geburah (reversed from גבורה)
            6: "תראפת",     # Tiphereth (reversed from תפארת)
            7: "חצנ",       # Netzach (reversed from נצח)
            8: "דוה",       # Hod (reversed from הוד)
            9: "דוסי",      # Yesod (reversed from יסוד)
            10: "תוכלמ"     # Malkuth (reversed from מלכות)
        }

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

    def set_sephiroth_text_mode(self, mode: 'SephirothTextMode') -> None:
        """
        Set the display mode for Sephiroth text.

        Args:
            mode: The text display mode (NUMBER, TRIGRAM, HEBREW, PLANET)
        """
        self.sephiroth_text_mode = mode

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
                color=DEFAULT_SEPHIROTH_COLORS[number]
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
                color=DEFAULT_PATH_COLORS[number]
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
            color=DEFAULT_SEPHIROTH_COLORS[0]
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
                color = DEFAULT_SEPHIROTH_COLORS[number]
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
                color=DEFAULT_SEPHIROTH_COLORS[0]
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
                color = DEFAULT_PATH_COLORS[number]
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

    def _calculate_focus_bounds(self, sephiroth_to_draw: set, paths_to_draw: set) -> Tuple[float, float, float, float]:
        """
        Calculate the appropriate bounds for a focused diagram.

        Args:
            sephiroth_to_draw: Set of sephirah numbers (1-10) to be displayed
            paths_to_draw: Set of path numbers (11-32) to be displayed

        Returns:
            Tuple of (min_x, max_x, min_y, max_y) for the plot limits
        """
        # Initialize with extreme values
        min_x, max_x = float('inf'), float('-inf')
        min_y, max_y = float('inf'), float('-inf')

        # Check coordinates of all sephiroth to be drawn
        for seph_num in sephiroth_to_draw:
            if seph_num in self.sephiroth:
                x, y = self.sephiroth[seph_num].coord
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

        # Check if we should include Da'ath
        if 1 in sephiroth_to_draw or 6 in sephiroth_to_draw:
            x, y = self.daath.coord
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        # Consider midpoints of paths for path numbers/labels
        for path_num in paths_to_draw:
            if path_num in self.paths:
                path = self.paths[path_num]
                i, j = path.connects
                # Convert from 0-based to 1-based
                if i+1 in self.sephiroth and j+1 in self.sephiroth:
                    x1, y1 = self.sephiroth[i+1].coord
                    x2, y2 = self.sephiroth[j+1].coord
                    # Path midpoint
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2

                    # Special cases for paths with offset labels
                    special_offset_y = 0
                    if path_num == 13:  # Kether to Tiphereth
                        special_offset_y = 1.6 * self.spacing_factor
                    elif path_num == 25:  # Tiphereth to Yesod
                        special_offset_y = 0.38 * self.spacing_factor

                    mid_y += special_offset_y

                    min_x = min(min_x, mid_x)
                    max_x = max(max_x, mid_x)
                    min_y = min(min_y, mid_y)
                    max_y = max(max_y, mid_y)

        # Add padding (proportional to the circle radius and spacing factor)
        padding_x = self.circle_radius * 2.5
        padding_y = self.circle_radius * 2.5

        width = max_x - min_x + padding_x * 2
        height = max_y - min_y + padding_y * 2

        # Ensure the aspect ratio is balanced
        if width > height:
            # If width is greater, increase height to match aspect ratio
            height_diff = (width - height) / 2
            min_y -= height_diff
            max_y += height_diff
        else:
            # If height is greater, increase width to match aspect ratio
            width_diff = (height - width) / 2
            min_x -= width_diff
            max_x += width_diff

        return (
            min_x - padding_x,
            max_x + padding_x,
            min_y - padding_y,
            max_y + padding_y
        )

    def render(self,
               focus_sephirah: Optional[int] = None,
               display: bool = True,
               save_to_file: Optional[str] = None,
               figsize: Tuple[float, float] = (7.5, 11),
               dpi: int = 300,
               show_title: bool = False) -> None:
        """
        Render the Tree of Life diagram.

        Args:
            focus_sephirah: If provided, render only this Sephirah (1-10) and its connected paths
            display: Whether to display the diagram in a window
            save_to_file: If provided, save the diagram to this filename
            figsize: Size of the figure (width, height) in inches
            dpi: Resolution in dots per inch for saving the figure
            show_title: Whether to display the title on the diagram
        """
        # Determine which paths and Sephiroth to draw based on focus
        if focus_sephirah is not None and 1 <= focus_sephirah <= 10:
            paths_to_draw = self._get_connected_paths(focus_sephirah)
            sephiroth_to_draw = self._get_connected_sephiroth(focus_sephirah)
            # Always include the focus sephirah
            sephiroth_to_draw.add(focus_sephirah)

            # Calculate plot limits for the focused view
            min_x, max_x, min_y, max_y = self._calculate_focus_bounds(
                sephiroth_to_draw, paths_to_draw)

            # Adjust figure size for focused view to maintain aspect ratio
            width = max_x - min_x
            height = max_y - min_y
            aspect_ratio = width / height if height != 0 else 1.0

            # Use a more appropriate figsize for the focused view
            # Maintain the same figure area but adjust dimensions based on content aspect ratio
            fig_area = figsize[0] * figsize[1]  # Original figure area

            if aspect_ratio > 1.0:  # Wider than tall
                new_height = (fig_area / aspect_ratio) ** 0.5
                new_width = new_height * aspect_ratio
            else:  # Taller than wide
                new_width = (fig_area * aspect_ratio) ** 0.5
                new_height = new_width / aspect_ratio

            # Cap maximum dimension
            max_dimension = max(figsize)
            if new_width > max_dimension or new_height > max_dimension:
                scale_factor = max_dimension / max(new_width, new_height)
                new_width *= scale_factor
                new_height *= scale_factor

            adjusted_figsize = (new_width, new_height)
        else:
            # Draw all paths and Sephiroth
            paths_to_draw = set(self.paths.keys())
            sephiroth_to_draw = set(self.sephiroth.keys())
            adjusted_figsize = figsize

        # Setup the plot with potentially adjusted figure size
        fig, ax = plt.subplots(figsize=adjusted_figsize)

        # Set background color of the figure
        fig.patch.set_facecolor('#EAEAEA')
        ax.set_facecolor('#EAEAEA')  # Set background color of the axes area

        if focus_sephirah is not None and 1 <= focus_sephirah <= 10:
            # Set the plot limits for the focused view
            ax.set_xlim(min_x, max_x)
            ax.set_ylim(min_y, max_y)
        else:
            # Set plot limits with padding to accommodate the larger spheres and adjusted spacing
            ax.set_xlim(-4.0, 4.0)
            ax.set_ylim(-3.5, 15.0)

        # Ensure aspect ratio is equal so circles are not distorted
        ax.set_aspect('equal', adjustable='box')

        # Hide the axes
        ax.axis('off')

        # Define visual parameters
        line_color_outer = 'black'
        line_color_inner = 'white'
        # Increased thickness for path numbers
        line_width_outer = 14.0 * (self.sphere_scale_factor * 0.7)
        line_width_inner = 10.0 * (self.sphere_scale_factor * 0.7)
        circle_edge_color = 'black'
        # Increased for thicker sephiroth borders
        circle_line_width = 3.0 * (self.sphere_scale_factor * 0.6)
        zorder_paths_outer = 1  # Draw black lines first
        zorder_paths_inner = 2  # Draw white lines on top
        zorder_circles = 3     # Draw circles on top of lines
        # Draw Daath outline above outer paths, potentially below inner paths/circles
        zorder_daath = 2
        zorder_path_numbers = 4  # Draw path numbers on top of everything

        # Identify special paths that need different z-ordering
        path13_num = 13  # Kether to Tiphereth
        path14_num = 14  # Chokmah to Binah
        path15_num = 15  # Chokmah to Tiphereth
        path17_num = 17  # Binah to Tiphereth
        path19_num = 19  # Chesed to Geburah
        path25_num = 25  # Tiphereth to Yesod
        path27_num = 27  # Netzach to Hod

        # Create lists of special paths
        paths_underneath = {path13_num, path15_num, path17_num, path25_num}
        paths_special = {path14_num, path19_num,
                         path27_num}  # Horizontal paths

        # Draw paths
        # First handle normal paths
        for path_num, path in self.paths.items():
            if path_num not in paths_to_draw:
                continue

            # Skip special paths for now
            if path_num in paths_underneath or path_num in paths_special:
                continue

            # Get sephiroth coordinates
            i, j = path.connects
            # Convert from 0-based to 1-based
            x1, y1 = self.sephiroth[i+1].coord
            # Convert from 0-based to 1-based
            x2, y2 = self.sephiroth[j+1].coord

            # Determine path color
            path_color = path.color

            # Check if we're focusing on a specific sephirah
            if focus_sephirah is not None:
                # Get 0-based indices for the focused sephirah
                focus_idx = focus_sephirah - 1

                # If path connects to focused sephirah, use normal color
                # Otherwise gray it out
                if focus_idx not in path.connects:
                    path_color = '#888888'  # Use gray for non-focused paths

            # Draw the outer black line
            ax.plot([x1, x2], [y1, y2],
                    color=line_color_outer,
                    linewidth=line_width_outer,
                    solid_capstyle='round',
                    zorder=zorder_paths_outer)

            # Draw the inner colored line
            ax.plot([x1, x2], [y1, y2],
                    color=path_color if path_color != '#888888' else line_color_inner,
                    linewidth=line_width_inner,
                    solid_capstyle='round',
                    zorder=zorder_paths_inner)

            # Apply special effects if any
            if path.color_effect and path_color != '#888888':
                apply_path_effect(
                    ax, path_num, x1, y1, x2, y2, path.color, path.color_effect, self.sphere_scale_factor)

            # Add path number at the midpoint
            self._add_path_number(ax, path_num, x1, y1,
                                  x2, y2, zorder_path_numbers)

        # Draw paths that should appear underneath
        for path_num in paths_underneath:
            if path_num not in paths_to_draw or path_num not in self.paths:
                continue

            path = self.paths[path_num]
            i, j = path.connects
            x1, y1 = self.sephiroth[i+1].coord
            x2, y2 = self.sephiroth[j+1].coord

            # Determine path color
            path_color = path.color

            # Check if we're focusing on a specific sephirah
            if focus_sephirah is not None:
                focus_idx = focus_sephirah - 1
                if focus_idx not in path.connects:
                    path_color = '#888888'  # Use gray for non-focused paths

            # Draw with lower zorder to ensure it appears underneath
            ax.plot([x1, x2], [y1, y2],
                    color=line_color_outer,
                    linewidth=line_width_outer,
                    solid_capstyle='round',
                    zorder=zorder_paths_outer-1)  # Even lower zorder

            ax.plot([x1, x2], [y1, y2],
                    color=path_color if path_color != '#888888' else line_color_inner,
                    linewidth=line_width_inner,
                    solid_capstyle='round',
                    zorder=zorder_paths_inner-1)  # Even lower zorder

            # Apply special effects if any
            if path.color_effect and path_color != '#888888':
                apply_path_effect(
                    ax, path_num, x1, y1, x2, y2, path.color, path.color_effect, self.sphere_scale_factor)

            # Add path number at the midpoint
            self._add_path_number(ax, path_num, x1, y1,
                                  x2, y2, zorder_path_numbers)

        # Draw special horizontal paths
        for path_num in paths_special:
            if path_num not in paths_to_draw or path_num not in self.paths:
                continue

            path = self.paths[path_num]
            i, j = path.connects
            x1, y1 = self.sephiroth[i+1].coord
            x2, y2 = self.sephiroth[j+1].coord

            # Determine path color
            path_color = path.color

            # Check if we're focusing on a specific sephirah
            if focus_sephirah is not None:
                focus_idx = focus_sephirah - 1
                if focus_idx not in path.connects:
                    path_color = '#888888'  # Use gray for non-focused paths

            # Draw with different zorder to handle horizontal paths correctly
            ax.plot([x1, x2], [y1, y2],
                    color=line_color_outer,
                    linewidth=line_width_outer,
                    solid_capstyle='round',
                    zorder=zorder_paths_outer)

            ax.plot([x1, x2], [y1, y2],
                    color=path_color if path_color != '#888888' else line_color_inner,
                    linewidth=line_width_inner,
                    solid_capstyle='round',
                    zorder=zorder_paths_inner)

            # Apply special effects if any
            if path.color_effect and path_color != '#888888':
                apply_path_effect(
                    ax, path_num, x1, y1, x2, y2, path.color, path.color_effect, self.sphere_scale_factor)

            # Add path number at the midpoint
            self._add_path_number(ax, path_num, x1, y1,
                                  x2, y2, zorder_path_numbers)

        # Draw Sephiroth
        for seph_num, sephirah in self.sephiroth.items():
            if seph_num not in sephiroth_to_draw:
                continue

            x, y = sephirah.coord
            color = sephirah.color

            # If focusing on a specific sephirah, gray out all except the focused one
            if focus_sephirah is not None and seph_num != focus_sephirah:
                # Gray out connected sephiroth without reducing opacity
                alpha = 1.0  # Changed from 0.6 to make fully opaque
                circle_face_color = '#E0E0E0'  # Slightly darker gray for non-focused sephiroth
                circle_edge_color_override = '#AAAAAA'  # Border is slightly darker gray
                text_color = '#AAAAAA'  # Match number to darker gray
            else:
                alpha = 1.0
                circle_face_color = color  # Use the sephirah's color
                circle_edge_color_override = circle_edge_color  # Use default border color
                # Dynamically determine text color based on background brightness
                text_color = get_contrasting_text_color(circle_face_color)

            # Draw the circle
            circle = patches.Circle(
                (x, y),
                self.circle_radius,
                facecolor=circle_face_color,
                edgecolor=circle_edge_color_override,
                linewidth=circle_line_width,
                alpha=alpha,
                zorder=zorder_circles
            )
            ax.add_patch(circle)

            # Apply special color effects if any
            if sephirah.color_effect and (focus_sephirah is None or seph_num == focus_sephirah):
                apply_color_effect(
                    ax, 'sephirah', seph_num, x, y, color,
                    sephirah.color_effect, self.circle_radius
                )

            # Add sephirah text in the center (if enabled)
            if self.show_sephiroth_text:
                # Get text to display based on current mode
                if self.sephiroth_text_mode == self.SephirothTextMode.NUMBER:
                    display_text = str(seph_num)
                    fontsize = 12 * self.sphere_scale_factor
                elif self.sephiroth_text_mode == self.SephirothTextMode.TRIGRAM:
                    display_text = self._trigram_map[seph_num]
                    fontsize = 14 * self.sphere_scale_factor  # Slightly larger for symbols
                elif self.sephiroth_text_mode == self.SephirothTextMode.HEBREW:
                    display_text = self._hebrew_map[seph_num]
                    fontsize = 10 * self.sphere_scale_factor  # Slightly smaller for Hebrew
                elif self.sephiroth_text_mode == self.SephirothTextMode.PLANET:
                    display_text = self._planet_map[seph_num]
                    fontsize = 14 * self.sphere_scale_factor  # Slightly larger for symbols
                else:
                    # Default to number if mode is invalid
                    display_text = str(seph_num)
                    fontsize = 12 * self.sphere_scale_factor

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

            # Special case for Kether (1) - Add radiant effect
            if seph_num == 1:
                self._add_kether_radiant_effect(ax, x, y)

        # Draw Da'ath (the hidden Sephirah) if it should be included
        # (either showing all sephiroth or if Kether or Tiphareth is focused)
        if focus_sephirah is None or focus_sephirah == 1 or focus_sephirah == 6:
            x, y = self.daath.coord
            color = self.daath.color

            # If focusing on a specific sephirah, gray out Da'ath unless it's directly connected
            if focus_sephirah is not None:
                # Use gray for Da'ath when in focus mode
                daath_border_color = '#AAAAAA'

                # Da'ath isn't directly connected to any nodes, but logically appears
                # in the vertical pillar between Kether and Tiphereth
                if focus_sephirah not in [1, 6]:  # If not Kether or Tiphereth
                    color = '#E0E0E0'  # Use a grayish color for Da'ath's background
            else:
                daath_border_color = circle_edge_color

            # Da'ath is typically drawn with a dashed line
            circle = patches.Circle(
                (x, y),
                self.circle_radius,
                facecolor=color,  # Use actual color instead of transparent fill
                edgecolor=daath_border_color,
                linewidth=circle_line_width * 0.7,
                linestyle='dashed',
                alpha=0.8,
                zorder=zorder_daath
            )
            ax.add_patch(circle)

            # Apply special color effects if any
            if self.daath.color_effect and (focus_sephirah is None or focus_sephirah in [1, 6]):
                apply_color_effect(
                    ax, 'sephirah', 0, x, y, color,
                    self.daath.color_effect, self.circle_radius
                )

            # Add Da'ath text if enabled
            if self.show_sephiroth_text:
                # Get text to display based on current mode
                if self.sephiroth_text_mode == self.SephirothTextMode.NUMBER:
                    # For NUMBER mode, Da'ath should display no text (blank)
                    display_text = ""  # Empty string for Da'ath in NUMBER mode
                    fontsize = 12 * self.sphere_scale_factor
                elif self.sephiroth_text_mode == self.SephirothTextMode.TRIGRAM:
                    display_text = self._trigram_map[0]  # Use Da'ath trigram
                    fontsize = 14 * self.sphere_scale_factor
                elif self.sephiroth_text_mode == self.SephirothTextMode.HEBREW:
                    display_text = self._hebrew_map[0]  # Use Hebrew for Da'ath
                    fontsize = 10 * self.sphere_scale_factor
                elif self.sephiroth_text_mode == self.SephirothTextMode.PLANET:
                    # Use planet symbol for Da'ath
                    display_text = self._planet_map[0]
                    fontsize = 14 * self.sphere_scale_factor
                else:
                    display_text = ""  # Default to blank if mode is invalid
                    fontsize = 12 * self.sphere_scale_factor

                # Determine text color based on whether we're in focus mode
                if focus_sephirah is not None:
                    # In focus mode, always use the gray text color to match other non-focused spheres
                    text_color = '#AAAAAA'
                else:
                    # In normal mode, use contrasting color based on background
                    text_color = get_contrasting_text_color(color)

                ax.text(
                    x, y,
                    display_text,
                    color=text_color,
                    fontsize=fontsize,
                    ha='center',
                    va='center',
                    fontweight='bold',
                    alpha=0.8,
                    zorder=zorder_daath + 1
                )

        # Add title if enabled
        if show_title:
            if focus_sephirah is not None:
                sephirah_name = self.sephiroth[focus_sephirah].name
                title = f"Focus on {sephirah_name} (Sephirah {focus_sephirah})"
                fig.suptitle(title, fontsize=14)
            else:
                pass

        # Save the figure if a filename is provided
        if save_to_file:
            plt.savefig(save_to_file, dpi=dpi, bbox_inches='tight')
            print(f"Diagram saved to {save_to_file}")

        # Display the figure if requested
        if display:
            plt.show()
        else:
            plt.close(fig)

    def _get_connected_paths(self, sephirah_num: int) -> set:
        """
        Get the set of path numbers that connect to the given sephirah.

        Args:
            sephirah_num: The sephirah number (1-10)

        Returns:
            Set of path numbers (11-32) that connect to the sephirah
        """
        connected_paths = set()
        sephirah_idx = sephirah_num - 1  # Convert to 0-based index

        for path_num, path in self.paths.items():
            if sephirah_idx in path.connects:
                connected_paths.add(path_num)

        return connected_paths

    def _get_connected_sephiroth(self, sephirah_num: int) -> set:
        """
        Get the set of sephiroth that are directly connected to the given sephirah.

        Args:
            sephirah_num: The sephirah number (1-10)

        Returns:
            Set of sephirah numbers (1-10) that are connected to the given sephirah
        """
        connected_sephiroth = set()
        sephirah_idx = sephirah_num - 1  # Convert to 0-based index

        for path in self.paths.values():
            if sephirah_idx in path.connects:
                # Get the other sephirah connected by this path
                other_idx = path.connects[0] if path.connects[1] == sephirah_idx else path.connects[1]
                # Convert back to 1-based
                connected_sephiroth.add(other_idx + 1)

        # Check if Da'ath (0) should be included
        # For simplicity, consider Da'ath connected to Sephiroth 1-6
        if 1 <= sephirah_num <= 6:
            connected_sephiroth.add(0)  # Add Da'ath

        return connected_sephiroth

    def _add_path_number(self, ax, path_num: int, x1: float, y1: float, x2: float, y2: float, zorder: int) -> None:
        """
        Add the path number at the midpoint of the path, including astrological/elemental symbols.

        Args:
            ax: Matplotlib axis
            path_num: Path number (11-32)
            x1, y1: Coordinates of the first endpoint
            x2, y2: Coordinates of the second endpoint
            zorder: Z-order for drawing
        """
        # Only proceed if path text should be shown
        if not self.show_path_text:
            return

        # Calculate midpoint
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        # Define astrological and elemental symbols for each path (ordered by path number 11-32)
        path_symbols = {
            11: '△̵',  # Air - Kether to Chokmah
            12: '☿',   # Mercury - Kether to Binah
            13: '☽',   # Moon - Kether to Tiphereth
            14: '♀',   # Venus - Chokmah to Binah
            15: '♒',   # Aquarius - Chokmah to Tiphereth
            16: '♉',   # Taurus - Chokmah to Chesed
            17: '♊',   # Gemini - Binah to Tiphereth
            18: '♋',   # Cancer - Binah to Geburah
            19: '♌',   # Leo - Chesed to Geburah
            20: '♍',   # Virgo - Chesed to Tiphereth
            21: '♃',   # Jupiter - Chesed to Netzach
            22: '♎',   # Libra - Geburah to Tiphereth
            23: '▽',   # Water - Geburah to Hod
            24: '♏',   # Scorpio - Tiphereth to Netzach
            25: '♐',   # Sagittarius - Tiphereth to Yesod
            26: '♑',   # Capricorn - Tiphereth to Hod
            27: '♂',   # Mars - Netzach to Hod
            28: '♈',   # Aries - Netzach to Yesod
            29: '♓',   # Pisces - Netzach to Malkuth
            30: '☉',   # Sun - Hod to Yesod
            31: '△ ⊙',  # Fire & Spirit - Hod to Malkuth
            32: '♄\n▽̵'  # Saturn & Earth - Yesod to Malkuth
        }

        # Define paths needing orientation fixes (appearing upside down)
        paths_needing_orientation_fix = [12, 15, 20, 26, 28, 29]

        # Define special path offsets for paths that need custom positioning
        special_offset_y = 0

        # Path 13 (Kether to Tiphereth) needs to be higher
        if path_num == 13:
            special_offset_y = 1.6 * self.spacing_factor

        # Path 25 (Tiphereth to Yesod) needs to be raised a bit
        if path_num == 25:
            special_offset_y = 0.38 * self.spacing_factor

        # Calculate the angle of the path for text rotation
        angle_rad = np.arctan2(y2 - y1, x2 - x1)
        angle_deg = np.degrees(angle_rad)

        # Adjust angle for readability - text should be right-side up
        if 90 < angle_deg < 270:
            angle_deg -= 180

        # Force flip for specific paths that are rendering upside down
        if path_num in paths_needing_orientation_fix:
            angle_deg += 180

        # Determine if the path is vertical or horizontal
        # within 5 degrees of vertical
        is_vertical = abs(abs(angle_deg) - 90) < 5
        is_horizontal = abs(angle_deg) < 5 or abs(
            abs(angle_deg) - 180) < 5  # within 5 degrees of horizontal

        # Set final rotation angle
        if is_vertical or is_horizontal:
            rotation = 0  # Keep horizontal for vertical and horizontal paths
        else:
            rotation = angle_deg  # Rotate text to match path angle

        # Create combined label with path number and symbol
        if path_num == 32 or is_vertical:
            # For path 32 and vertical paths, stack number and symbol
            path_label = f"{path_num}\n{path_symbols[path_num]}"
        else:
            # For horizontal and diagonal paths, put symbol next to number
            path_label = f"{path_num} {path_symbols[path_num]}"

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
            fontsize=9 * self.sphere_scale_factor * 0.55,  # Slightly smaller font
            fontweight='bold',
            ha='center',
            va='center',
            color=text_color,
            rotation=rotation,
            rotation_mode='anchor',
            zorder=zorder
        )

    def _add_kether_radiant_effect(self, ax, x: float, y: float) -> None:
        """
        Add a radiant effect around Kether (first Sephirah).

        Args:
            ax: Matplotlib axis
            x, y: Center coordinates of Kether
        """
        # Create a radiant glow effect
        for i in range(20, 0, -2):
            # Decrease alpha and increase size as we move outward
            alpha = i / 40.0  # 0.5 to 0.025
            size = self.circle_radius * (1 + (20 - i) / 10.0)  # 1.0r to 3.0r

            glow = patches.Circle(
                (x, y),
                size,
                facecolor='white',
                edgecolor='none',
                alpha=alpha,
                zorder=1  # Below the main circle
            )
            ax.add_patch(glow)
