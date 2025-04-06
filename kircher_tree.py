#!/usr/bin/env python3
"""
Kircher Tree of Life Visualization

This program creates a visual representation of Athanasius Kircher's version of the
Kabbalistic Tree of Life, featuring the 10 Sephirot (nodes) and the paths connecting them.
The visualization is designed to be accurate to the traditional representation with paths
that look like actual paths rather than simple lines.

"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch, FancyArrowPatch
from matplotlib.path import Path
import matplotlib.colors as mcolors
from typing import Dict, List, Tuple, Optional


class KircherTreeOfLife:
    """
    A class to generate and visualize Athanasius Kircher's version of the Tree of Life.

    This implementation emphasizes accurate path representation and proper positioning
    of the Sephirot according to the traditional Kircher layout.
    """

    def __init__(self, figsize: Tuple[int, int] = (10, 15), dpi: int = 100):
        """
        Initialize the Kircher Tree of Life visualization.

        Args:
            figsize: Tuple specifying the figure size (width, height)
            dpi: Resolution of the figure
        """
        self.figsize = figsize
        self.dpi = dpi
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        # Define colors
        self.sephirot_colors = {
            'Keter': '#FFFFFF',        # White
            'Chokmah': '#808080',      # Grey
            'Binah': '#000000',        # Black
            'Chesed': '#0000FF',       # Blue
            'Geburah': '#FF0000',      # Red
            'Tiferet': '#FFFF00',      # Yellow
            'Netzach': '#00FF00',      # Green
            'Hod': '#FFA500',          # Orange
            'Yesod': '#800080',        # Purple
            'Malkuth': '#A52A2A',      # Brown
        }

        # Define coordinates for the sephirot (traditional Kircher layout)
        # Using relative positioning (0-1) for flexibility
        self.sephirot_positions = {
            'Keter':    (0.5, 0.95),   # Crown - top center
            'Chokmah':  (0.25, 0.85),  # Wisdom - upper right
            'Binah':    (0.75, 0.85),  # Understanding - upper left
            'Chesed':   (0.25, 0.70),  # Mercy - middle right
            'Geburah':  (0.75, 0.70),  # Severity - middle left
            'Tiferet':  (0.5, 0.60),   # Beauty - middle center
            'Netzach':  (0.25, 0.45),  # Victory - lower right
            'Hod':      (0.75, 0.45),  # Splendor - lower left
            'Yesod':    (0.5, 0.30),   # Foundation - lower center
            'Malkuth':  (0.5, 0.10),   # Kingdom - bottom
        }

        # Define the paths connecting the sephirot
        # Each tuple contains (start_sephirah, end_sephirah)
        self.paths = [
            ('Keter', 'Chokmah'),      # Path 1
            ('Keter', 'Binah'),        # Path 2
            ('Chokmah', 'Binah'),      # Path 3
            ('Chokmah', 'Chesed'),     # Path 4
            ('Binah', 'Geburah'),      # Path 5
            ('Chesed', 'Geburah'),     # Path 6
            ('Chesed', 'Tiferet'),     # Path 7
            ('Geburah', 'Tiferet'),    # Path 8
            ('Chokmah', 'Tiferet'),    # Path 9
            ('Binah', 'Tiferet'),      # Path 10
            ('Chesed', 'Netzach'),     # Path 11
            ('Tiferet', 'Netzach'),    # Path 12
            ('Tiferet', 'Hod'),        # Path 13
            ('Geburah', 'Hod'),        # Path 14
            ('Netzach', 'Hod'),        # Path 15
            ('Netzach', 'Yesod'),      # Path 16
            ('Hod', 'Yesod'),          # Path 17
            ('Tiferet', 'Yesod'),      # Path 18
            ('Yesod', 'Malkuth'),      # Path 19
            ('Netzach', 'Malkuth'),    # Path 20
            ('Hod', 'Malkuth'),        # Path 21
            ('Binah', 'Chesed'),       # Path 22 (according to Kircher's version)
        ]

    def _create_curved_path(self,
                            start: Tuple[float, float],
                            end: Tuple[float, float],
                            curvature: float = 0.2) -> np.ndarray:
        """
        Create a curved path between two points.

        Args:
            start: Starting coordinates (x, y)
            end: Ending coordinates (x, y)
            curvature: Amount of curve (0 = straight line)

        Returns:
            Array of path vertices
        """
        # Calculate midpoint
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2

        # Calculate perpendicular direction for control point
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        # Perpendicular vector
        perp_x = -dy
        perp_y = dx

        # Normalize
        length = np.sqrt(perp_x**2 + perp_y**2)
        if length > 0:
            perp_x /= length
            perp_y /= length

        # Control point
        control_x = mid_x + curvature * perp_x
        control_y = mid_y + curvature * perp_y

        # Create path
        verts = [
            (start[0], start[1]),              # Starting point
            (control_x, control_y),            # Control point
            (end[0], end[1]),                  # Ending point
        ]

        # Create path codes
        codes = [
            Path.MOVETO,
            Path.CURVE3,
            Path.CURVE3,
        ]

        return Path(verts, codes)

    def draw(self, title: Optional[str] = None,
             save_path: Optional[str] = None) -> None:
        """
        Draw the Tree of Life visualization.

        Args:
            title: Title of the figure (None for no title)
            save_path: Path to save the figure (if None, figure is displayed)
        """
        # Set up the figure
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        # Only add title if one is provided
        if title:
            self.fig.suptitle(title, fontsize=16)

        # Draw the paths first (so spheres appear on top)
        for start_name, end_name in self.paths:
            start_pos = self.sephirot_positions[start_name]
            end_pos = self.sephirot_positions[end_name]

            # Determine appropriate curvature based on geometry
            # Horizontal paths should have more curvature
            dx = abs(start_pos[0] - end_pos[0])
            dy = abs(start_pos[1] - end_pos[1])

            # Default curvature for vertical paths
            curvature = 0.0

            # Adjust curvature for diagonal or horizontal paths
            if dx > 0.1 and dy > 0.1:
                # Diagonal path
                curvature = 0.1
            elif dx > 0.3:
                # Horizontal path
                curvature = 0.2

            # Special case for paths that need opposite curvature
            # In Kircher's version, some paths curve differently
            special_paths = [
                ('Chokmah', 'Tiferet'),
                ('Binah', 'Tiferet'),
                ('Binah', 'Chesed')
            ]

            if (start_name, end_name) in special_paths:
                curvature = -curvature

            # Create and draw the path
            path = self._create_curved_path(start_pos, end_pos, curvature)
            path_patch = PathPatch(path, facecolor='none',
                                   edgecolor='gold', linewidth=2, alpha=0.7)
            self.ax.add_patch(path_patch)

        # Draw sephirot (nodes)
        for name, pos in self.sephirot_positions.items():
            # Create circle
            circle = Circle(pos, 0.05, facecolor=self.sephirot_colors[name],
                            edgecolor='black', linewidth=2, alpha=0.8)
            self.ax.add_patch(circle)

            # Add text label
            self.ax.text(pos[0], pos[1], name,
                         ha='center', va='center',
                         fontsize=10, fontweight='bold',
                         color='black' if name not in ['Binah', 'Malkuth'] else 'white')

        # Add the "Flaming Sword" path - the lightning flash that connects the sephirot
        # in order of their emanation
        flaming_sword_order = ['Keter', 'Chokmah', 'Binah', 'Chesed',
                               'Geburah', 'Tiferet', 'Netzach', 'Hod',
                               'Yesod', 'Malkuth']
        flaming_sword_points = [self.sephirot_positions[s]
                                for s in flaming_sword_order]

        # Create zigzag path for the flaming sword
        verts = []
        codes = []

        for i, point in enumerate(flaming_sword_points):
            if i == 0:
                codes.append(Path.MOVETO)
            else:
                codes.append(Path.LINETO)
            verts.append(point)

        flaming_sword_path = Path(verts, codes)
        flaming_sword_patch = PathPatch(flaming_sword_path,
                                        facecolor='none',
                                        edgecolor='red',
                                        linewidth=3,
                                        alpha=0.7,
                                        linestyle='--')
        self.ax.add_patch(flaming_sword_patch)

        # Add the three columns (pillars)
        # Left pillar - Severity
        left_pillar = Path(
            [(0.75, 0.95), (0.75, 0.10)],
            [Path.MOVETO, Path.LINETO]
        )
        left_pillar_patch = PathPatch(left_pillar,
                                      facecolor='none',
                                      edgecolor='black',
                                      linewidth=3,
                                      alpha=0.3)
        self.ax.add_patch(left_pillar_patch)
        self.ax.text(0.75, 0.02, "Pillar of Severity",
                     ha='center', va='center', fontsize=10)

        # Middle pillar - Balance
        middle_pillar = Path(
            [(0.5, 0.95), (0.5, 0.10)],
            [Path.MOVETO, Path.LINETO]
        )
        middle_pillar_patch = PathPatch(middle_pillar,
                                        facecolor='none',
                                        edgecolor='black',
                                        linewidth=3,
                                        alpha=0.3)
        self.ax.add_patch(middle_pillar_patch)
        self.ax.text(0.5, 0.02, "Pillar of Balance",
                     ha='center', va='center', fontsize=10)

        # Right pillar - Mercy
        right_pillar = Path(
            [(0.25, 0.95), (0.25, 0.10)],
            [Path.MOVETO, Path.LINETO]
        )
        right_pillar_patch = PathPatch(right_pillar,
                                       facecolor='none',
                                       edgecolor='black',
                                       linewidth=3,
                                       alpha=0.3)
        self.ax.add_patch(right_pillar_patch)
        self.ax.text(0.25, 0.02, "Pillar of Mercy",
                     ha='center', va='center', fontsize=10)

        # Add the "Veil of the Abyss" - horizontal line between upper and lower sephirot
        abyss_veil = Path(
            [(0.1, 0.77), (0.9, 0.77)],
            [Path.MOVETO, Path.LINETO]
        )
        abyss_veil_patch = PathPatch(abyss_veil,
                                     facecolor='none',
                                     edgecolor='black',
                                     linewidth=1,
                                     alpha=0.5,
                                     linestyle=':')
        self.ax.add_patch(abyss_veil_patch)
        self.ax.text(0.95, 0.77, "Abyss",
                     ha='center', va='center', fontsize=8, alpha=0.7)

        # Add a background glow to enhance the visual appearance
        self.fig.patch.set_facecolor('#f0f0e8')  # Light beige background

        # Save or display the figure
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=self.dpi)
            print(f"Tree of Life image saved to {save_path}")
        else:
            plt.tight_layout()
            plt.show()

    def save(self, filepath: str) -> None:
        """
        Save the visualization to a file.

        Args:
            filepath: Path where the image should be saved
        """
        plt.savefig(filepath, bbox_inches='tight', dpi=self.dpi)
        print(f"Tree of Life image saved to {filepath}")


def main():
    """Main function to create and display the Kircher Tree of Life."""
    # Create Tree of Life visualization
    tree = KircherTreeOfLife(figsize=(10, 15), dpi=150)

    # Set output filename
    output_file = "kircher_tree_of_life.png"

    # Draw and save in one operation without a title
    tree.draw(title=None, save_path=output_file)

    print(f"Tree of Life visualization created and saved to {output_file}")


if __name__ == "__main__":
    main()
