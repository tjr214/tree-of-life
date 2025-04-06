import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import List, Tuple, Dict, Optional, Union, NamedTuple, Literal
from enum import Enum

# Define type aliases for clarity
Coord = Tuple[float, float]
PathIndices = Tuple[int, int]


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


class Path(NamedTuple):
    """Data structure to store information about a connecting path."""
    number: int  # Path number (11-32)
    # Tuple of the two Sephiroth indices it connects (0-based)
    connects: PathIndices
    # Default color (will be overridden by color scheme)
    color: str = "#FFFFFF"


class TreeOfLife:
    """Class to create, manipulate and render the Kabbalistic Tree of Life diagram."""

    def __init__(self,
                 sphere_scale_factor: float = 1.75,
                 spacing_factor: float = 1.5,
                 sephiroth_color_scheme: ColorScheme = ColorScheme.PLAIN,
                 path_color_scheme: ColorScheme = ColorScheme.PLAIN):
        """
        Initialize the Tree of Life with configurable parameters.

        Args:
            sphere_scale_factor: Scale factor for spheres (sephiroth)
            spacing_factor: Factor to adjust spacing between spheres
            sephiroth_color_scheme: Color scheme to use for Sephiroth
            path_color_scheme: Color scheme to use for Paths
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

        # Initialize the Sephiroth and Paths
        self._init_sephiroth()
        self._init_paths()
        self._init_daath()

        # Apply the initial color schemes
        self.set_sephiroth_color_scheme(sephiroth_color_scheme)
        self.set_path_color_scheme(path_color_scheme)

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
                number=number, name=name, coord=coord)

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
            self.paths[number] = Path(number=number, connects=connects)

    def _init_daath(self) -> None:
        """Initialize the hidden Sephirah Da'ath."""
        # Da'ath is positioned at the geometric center of Chokmah, Binah, Chesed, and Geburah
        daath_coord = (0 * self.spacing_factor, 6.75 *
                       self.spacing_factor + self.vertical_shift)
        self.daath = Sephirah(number=0, name="Da'ath", coord=daath_coord)

    def set_sephiroth_color_scheme(self, scheme: ColorScheme) -> None:
        """
        Set the color scheme for all Sephiroth.

        Args:
            scheme: The color scheme to apply to Sephiroth
        """
        self.sephiroth_color_scheme = scheme
        # TODO: Implement color scheme application logic based on the chosen scheme
        # This will be done in Phase 3

    def set_path_color_scheme(self, scheme: ColorScheme) -> None:
        """
        Set the color scheme for all paths.

        Args:
            scheme: The color scheme to apply to paths
        """
        self.path_color_scheme = scheme
        # TODO: Implement color scheme application logic based on the chosen scheme
        # This will be done in Phase 3

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
