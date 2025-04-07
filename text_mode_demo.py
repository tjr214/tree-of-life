#!/usr/bin/env python
"""
TreeOfLife Text Rendering Demo

This script demonstrates the new text rendering options for the Tree of Life diagram.
"""

import matplotlib.pyplot as plt
from tol import TreeOfLife, ColorScheme


def main():
    """Run demonstrations of TreeOfLife text rendering options."""

    # Create figure for multiple trees
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle("Tree of Life Text Display Options", fontsize=16)

    # Use a 2x3 subplot grid
    grid = plt.GridSpec(2, 3, fig, hspace=0.3, wspace=0.1)

    # Demo 1: Default (Numbers)
    ax1 = fig.add_subplot(grid[0, 0])
    tree1 = TreeOfLife(
        sphere_scale_factor=1.2,
        spacing_factor=1.2,
        sephiroth_color_scheme=ColorScheme.KING_SCALE
    )
    tree1.render(display=False, show_title=False)
    ax1.set_title("Default: Number Mode", fontsize=12)

    # Demo 2: I Ching Trigrams
    ax2 = fig.add_subplot(grid[0, 1])
    tree2 = TreeOfLife(
        sphere_scale_factor=1.2,
        spacing_factor=1.2,
        sephiroth_color_scheme=ColorScheme.KING_SCALE
    )
    tree2.set_sephiroth_text_mode(TreeOfLife.SephirothTextMode.TRIGRAM)
    tree2.render(display=False, show_title=False)
    ax2.set_title("I Ching Trigram Mode", fontsize=12)

    # Demo 3: Hebrew Names
    ax3 = fig.add_subplot(grid[0, 2])
    tree3 = TreeOfLife(
        sphere_scale_factor=1.2,
        spacing_factor=1.2,
        sephiroth_color_scheme=ColorScheme.KING_SCALE
    )
    tree3.set_sephiroth_text_mode(TreeOfLife.SephirothTextMode.HEBREW)
    tree3.render(display=False, show_title=False)
    ax3.set_title("Hebrew Names Mode", fontsize=12)

    # Demo 4: Planetary Symbols
    ax4 = fig.add_subplot(grid[1, 0])
    tree4 = TreeOfLife(
        sphere_scale_factor=1.2,
        spacing_factor=1.2,
        sephiroth_color_scheme=ColorScheme.KING_SCALE
    )
    tree4.set_sephiroth_text_mode(TreeOfLife.SephirothTextMode.PLANET)
    tree4.render(display=False, show_title=False)
    ax4.set_title("Planetary Symbols Mode", fontsize=12)

    # Demo 5: No Sephiroth Text
    ax5 = fig.add_subplot(grid[1, 1])
    tree5 = TreeOfLife(
        sphere_scale_factor=1.2,
        spacing_factor=1.2,
        sephiroth_color_scheme=ColorScheme.KING_SCALE
    )
    tree5.set_sephiroth_text_visibility(False)
    tree5.render(display=False, show_title=False)
    ax5.set_title("No Sephiroth Text", fontsize=12)

    # Demo 6: No Path Text
    ax6 = fig.add_subplot(grid[1, 2])
    tree6 = TreeOfLife(
        sphere_scale_factor=1.2,
        spacing_factor=1.2,
        sephiroth_color_scheme=ColorScheme.KING_SCALE
    )
    tree6.set_path_text_visibility(False)
    tree6.render(display=False, show_title=False)
    ax6.set_title("No Path Text", fontsize=12)

    # Display the figure
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust for the figure title
    plt.show()

    # Focused view demonstrations
    print("\nGenerating focused view demonstrations...")

    # Create a focused view with different text modes
    for mode in TreeOfLife.SephirothTextMode:
        tree = TreeOfLife(
            sphere_scale_factor=1.5,
            spacing_factor=1.3,
            sephiroth_color_scheme=ColorScheme.KING_SCALE
        )
        tree.set_sephiroth_text_mode(mode)
        tree.render(focus_sephirah=6, display=True, show_title=True)

    print("Demo complete!")


if __name__ == "__main__":
    main()
