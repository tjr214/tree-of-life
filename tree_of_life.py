#!/usr/bin/env python3
"""
Kabbalistic Tree of Life Visualization

This script creates a visualization of the Kabbalistic Tree of Life
using networkx for graph representation and matplotlib for rendering.
"""

import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Tuple, List, Optional
import numpy as np


class TreeOfLife:
    """Class representing the Kabbalistic Tree of Life."""

    def __init__(self) -> None:
        """Initialize the Tree of Life with Sephiroth and paths."""
        # Create a directed graph
        self.graph = nx.DiGraph()

        # Define the Sephiroth (nodes)
        self.sephiroth_names: Dict[int, str] = {
            1: "Keter (Crown)",
            2: "Chokmah (Wisdom)",
            3: "Binah (Understanding)",
            4: "Chesed (Mercy)",
            5: "Geburah (Severity)",
            6: "Tiferet (Beauty)",
            7: "Netzach (Victory)",
            8: "Hod (Splendor)",
            9: "Yesod (Foundation)",
            10: "Malkuth (Kingdom)"
        }

        # Define colors for each Sephirah
        self.sephiroth_colors: Dict[int, str] = {
            1: "#FFFFFF",  # White
            2: "#C0C0C0",  # Gray
            3: "#FFFF00",  # Yellow
            4: "#0000FF",  # Blue
            5: "#FF0000",  # Red
            6: "#FFCC99",  # Gold
            7: "#00FF00",  # Green
            8: "#FF69B4",  # Pink
            9: "#9932CC",  # Purple
            10: "#8B4513"  # Brown
        }

        # Define positions for each Sephirah
        # These coordinates create the traditional Tree of Life arrangement
        self.positions: Dict[int, Tuple[float, float]] = {
            # Keter (moved up to maintain position above Chokmah and Binah)
            1: (0, 12),
            2: (2, 10),    # Chokmah (moved from y=8 to y=10)
            3: (-2, 10),   # Binah (moved from y=8 to y=10)
            4: (2, 6),     # Chesed
            5: (-2, 6),    # Geburah
            6: (0, 4),     # Tiferet
            7: (2, 2),     # Netzach
            8: (-2, 2),    # Hod
            9: (0, 0),     # Yesod
            10: (0, -2)    # Malkuth
        }

        # Add nodes (Sephiroth) to the graph
        for i in range(1, 11):
            self.graph.add_node(
                i, name=self.sephiroth_names[i], color=self.sephiroth_colors[i])

        # Define the paths (edges) between Sephiroth
        # These are the 22 traditional paths in the Tree of Life
        self.paths: List[Tuple[int, int]] = [
            (1, 2), (1, 3), (1, 6),  # Paths from Keter
            (2, 3), (2, 4), (2, 6),  # Paths from Chokmah
            (3, 5), (3, 6),          # Paths from Binah
            (4, 5), (4, 6), (4, 7),  # Paths from Chesed
            (5, 6), (5, 8),          # Paths from Geburah
            (6, 7), (6, 8), (6, 9),  # Paths from Tiferet
            (7, 8), (7, 9), (7, 10),  # Paths from Netzach
            (8, 9), (8, 10),         # Paths from Hod
            (9, 10),                 # Path from Yesod
            # The additional Hebrew letter path
            (5, 7)
        ]

        # Add edges to the graph
        for source, target in self.paths:
            self.graph.add_edge(source, target)

    def draw(self, node_size: int = 11250, edge_width: float = 2.0,
             figsize: Tuple[int, int] = (12, 15),
             save_path: Optional[str] = None,
             display: bool = False) -> None:
        """
        Draw the Tree of Life.

        Args:
            node_size: Size of the Sephiroth nodes
            edge_width: Width of the paths
            figsize: Size of the figure
            save_path: If provided, save the figure to this path
            display: Whether to display the visualization in a window
        """
        # Create figure with explicitly defined margins to avoid tight_layout warnings
        fig = plt.figure(figsize=figsize)
        # Set larger figure margins manually instead of using tight_layout
        plt.subplots_adjust(left=0.15, right=0.85, top=0.95, bottom=0.05)

        # Extract node colors
        node_colors = [self.sephiroth_colors[node]
                       for node in self.graph.nodes()]

        # Draw the graph
        nx.draw(
            self.graph,
            pos=self.positions,
            with_labels=True,
            labels={node: data['name']
                    for node, data in self.graph.nodes(data=True)},
            node_color=node_colors,
            node_size=node_size,
            width=edge_width,
            edge_color='black',
            arrows=False,
            font_size=10,
            font_weight='bold'
        )

        # Set title
        plt.title("The Kabbalistic Tree of Life",
                  fontsize=16, fontweight='bold', pad=20)

        # Add the three pillars as background columns
        self._draw_pillars()

        # Add the four worlds
        self._draw_worlds()

        # Remove the tight_layout call that was causing warnings
        # plt.tight_layout()

        # Save the figure if a path is provided
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        # Only show the visualization if display is True
        if display:
            plt.show()
        else:
            plt.close(fig)  # Close the figure to free memory

    def _draw_pillars(self) -> None:
        """Draw the three pillars of the Tree of Life."""
        # Pillar of Mercy (right side in traditional depiction, left side when facing the tree)
        plt.axvspan(1, 3, alpha=0.1, color='blue', zorder=-1)

        # Pillar of Severity (left side in traditional depiction, right side when facing the tree)
        plt.axvspan(-3, -1, alpha=0.1, color='red', zorder=-1)

        # Middle Pillar
        plt.axvspan(-1, 1, alpha=0.1, color='purple', zorder=-1)

        # Add text labels for pillars
        plt.text(2.5, 13, "Pillar of Mercy", ha='center', fontsize=12)
        plt.text(0, 13, "Middle Pillar", ha='center', fontsize=12)
        plt.text(-2.5, 13, "Pillar of Severity", ha='center', fontsize=12)

    def _draw_worlds(self) -> None:
        """Draw the four worlds of the Tree of Life."""
        worlds = [
            # Updated to include Keter at y=12
            ("Atziluth (Emanation)", 11, 13, "#FFEEEE"),
            # Updated to include Chokmah/Binah at y=10
            ("Briah (Creation)", 7, 11, "#EEFFEE"),
            # Updated to include Chesed/Geburah at y=6
            ("Yetzirah (Formation)", 1, 7, "#EEEEFF"),
            ("Assiah (Action)", -3, 1, "#FFFFEE")         # Unchanged
        ]

        for name, y_min, y_max, color in worlds:
            plt.axhspan(y_min-0.5, y_max+0.5, alpha=0.1,
                        color=color, zorder=-2)


def main() -> None:
    """Main function to create and display the Tree of Life."""
    tree = TreeOfLife()
    tree.draw(node_size=13500, save_path="tree_of_life.png", display=False)
    print("Tree of Life visualization complete. Image saved to 'tree_of_life.png'.")


if __name__ == "__main__":
    main()
