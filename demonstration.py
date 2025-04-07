#!/usr/bin/env python
"""
Tree of Life Visualization - Comprehensive Demonstration
-------------------------------------------------------

This script demonstrates all features of the TreeOfLife class, including:
1. All color schemes
2. Focused rendering for each Sephirah
3. Special color effects
4. Text rendering options and visibility toggles
"""

import os
import matplotlib.pyplot as plt
from tol import TreeOfLife, ColorScheme


def main():
    """Run a comprehensive demonstration of the TreeOfLife class."""
    # Create output directory if it doesn't exist
    output_dir = "sample-output"
    os.makedirs(output_dir, exist_ok=True)

    # Create a Tree of Life instance
    tree = TreeOfLife()

    # Part 1: Generate the full tree with each color scheme
    print("Part 1: Generating full tree with all color schemes...")

    schemes = [
        (ColorScheme.PLAIN, "Plain"),
        (ColorScheme.KING_SCALE, "King Scale"),
        (ColorScheme.QUEEN_SCALE, "Queen Scale"),
        (ColorScheme.PRINCE_SCALE, "Prince Scale"),
        (ColorScheme.PRINCESS_SCALE, "Princess Scale")
    ]

    for scheme, name in schemes:
        print(f"  Rendering with {name} color scheme...")
        tree.set_sephiroth_color_scheme(scheme)
        tree.set_path_color_scheme(scheme)
        tree.render(
            display=False,  # Don't display to avoid interrupting the script
            save_to_file=os.path.join(
                output_dir, f"full_tree_{scheme.value}.png")
        )

    # Part 2: Generate focused views of each Sephirah using King Scale
    print("\nPart 2: Generating focused views of each Sephirah using King Scale...")

    # Use King Scale for this part
    tree.set_sephiroth_color_scheme(ColorScheme.KING_SCALE)
    tree.set_path_color_scheme(ColorScheme.KING_SCALE)

    # Render each Sephirah (1-10)
    sephiroth_names = [
        "Kether", "Chokmah", "Binah", "Chesed", "Geburah",
        "Tiphereth", "Netzach", "Hod", "Yesod", "Malkuth"
    ]

    for num in range(1, 11):
        name = sephiroth_names[num-1]
        print(f"  Rendering focus on {name} (Sephirah {num})...")
        tree.render(
            focus_sephirah=num,
            display=False,
            save_to_file=os.path.join(
                output_dir, f"focus_{num}_{name.lower()}.png"),
            show_title=True  # Enable titles for focused views
        )

    # Part 3: Generate a color scheme comparison grid
    print("\nPart 3: Generating color scheme comparison grid...")

    # We'll create a grid of renderings with different combinations of color schemes
    # This will be a 5x5 grid where rows are Sephiroth schemes and columns are Path schemes

    print("  This will create 25 different combinations of color schemes...")

    # Create figure with 5x5 grid of subplots
    fig, axes = plt.subplots(5, 5, figsize=(15, 15))
    fig.suptitle("Color Scheme Combinations", fontsize=16)

    # Add row and column labels
    for i, (_, name) in enumerate(schemes):
        axes[i, 0].set_ylabel(f"{name}\nSephiroth",
                              fontsize=10, rotation=90, labelpad=15)
        axes[0, i].set_title(f"{name}\nPaths", fontsize=10)

    # Generate all combinations of color schemes
    for i, (seph_scheme, _) in enumerate(schemes):
        for j, (path_scheme, _) in enumerate(schemes):
            print(
                f"  Rendering combination: {seph_scheme.value} Sephiroth, {path_scheme.value} Paths...")

            # Set color schemes
            tree.set_sephiroth_color_scheme(seph_scheme)
            tree.set_path_color_scheme(path_scheme)

            # Render to a temporary file
            temp_file = os.path.join(
                output_dir, f"temp_{seph_scheme.value}_{path_scheme.value}.png")
            tree.render(display=False, save_to_file=temp_file)

            # Load the image and display it in the grid
            img = plt.imread(temp_file)
            axes[i, j].imshow(img)
            axes[i, j].axis('off')

            # Clean up temporary file
            os.remove(temp_file)

    # Save the grid
    # Adjust layout to make room for title
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    grid_file = os.path.join(output_dir, "color_scheme_grid.png")
    plt.savefig(grid_file, dpi=150)
    print(f"  Color scheme grid saved to {grid_file}")
    plt.close(fig)

    # Part 4: Special Effect Demonstration
    print("\nPart 4: Demonstrating special color effects...")

    # First, let's see if we can find Sephiroth with special effects in each scale
    for scheme, name in schemes:
        if scheme == ColorScheme.PLAIN:
            continue  # Skip plain scheme as it doesn't have special effects

        print(f"  Rendering special effects in {name} color scheme...")
        tree.set_sephiroth_color_scheme(scheme)
        tree.set_path_color_scheme(scheme)
        tree.render(
            display=False,
            save_to_file=os.path.join(
                output_dir, f"special_effects_{scheme.value}.png")
        )

    # Part 5: Text Rendering Options
    print("\nPart 5: Demonstrating text rendering options...")

    # Use King Scale for this part
    tree.set_sephiroth_color_scheme(ColorScheme.KING_SCALE)
    tree.set_path_color_scheme(ColorScheme.KING_SCALE)

    # 5.1: Text Display Modes
    print("  Demonstrating different Sephiroth text display modes...")

    # Demonstrate each text mode
    display_modes = [
        (tree.SephirothTextMode.NUMBER, "numbers"),
        (tree.SephirothTextMode.TRIGRAM, "trigrams"),
        (tree.SephirothTextMode.HEBREW, "hebrew"),
        (tree.SephirothTextMode.PLANET, "planets")
    ]

    for mode, name in display_modes:
        print(f"    Rendering with {name} text mode...")
        tree.set_sephiroth_text_mode(mode)
        tree.render(
            display=False,
            save_to_file=os.path.join(output_dir, f"text_mode_{name}.png")
        )

    # 5.2: Text Visibility Options
    print("  Demonstrating text visibility options...")

    # Reset to number mode for visibility demos
    tree.set_sephiroth_text_mode(tree.SephirothTextMode.NUMBER)

    # No Sephiroth text
    print("    Rendering with Sephiroth text hidden...")
    tree.set_sephiroth_text_visibility(False)
    tree.set_path_text_visibility(True)
    tree.render(
        display=False,
        save_to_file=os.path.join(output_dir, "text_no_sephiroth.png")
    )

    # No Path text
    print("    Rendering with Path text hidden...")
    tree.set_sephiroth_text_visibility(True)
    tree.set_path_text_visibility(False)
    tree.render(
        display=False,
        save_to_file=os.path.join(output_dir, "text_no_paths.png")
    )

    # No text at all
    print("    Rendering with all text hidden...")
    tree.set_sephiroth_text_visibility(False)
    tree.set_path_text_visibility(False)
    tree.render(
        display=False,
        save_to_file=os.path.join(output_dir, "text_none.png")
    )

    # Reset text visibility for future use
    tree.set_sephiroth_text_visibility(True)
    tree.set_path_text_visibility(True)

    # 5.3: Text Modes in Focused View
    print("  Demonstrating text modes in focused view...")

    # Focus on Tiphereth with each text mode
    for mode, name in display_modes:
        print(f"    Rendering focused view with {name} text mode...")
        tree.set_sephiroth_text_mode(mode)
        tree.render(
            focus_sephirah=6,  # Tiphereth
            display=False,
            save_to_file=os.path.join(output_dir, f"focus_text_{name}.png"),
            show_title=True
        )

    print("\nAll demonstrations complete! Generated images saved to the 'output' directory.")
    print("\nSummary of generated files:")
    for file in sorted(os.listdir(output_dir)):
        print(f"  - {file}")


if __name__ == "__main__":
    main()
