#!/usr/bin/env python
# Example usage of the TreeOfLife class

import os
from TreeOfLife import TreeOfLife, ColorScheme


def main():
    """Demonstrate the usage of the TreeOfLife class."""
    print("Tree of Life Visualization Examples")
    print("----------------------------------")

    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Create a Tree of Life instance with default settings
    tree = TreeOfLife()

    # 1. Render the complete tree with the default (plain) color scheme
    print("\n1. Rendering the complete tree with the default color scheme...")
    tree.render(
        display=True,
        save_to_file=os.path.join(output_dir, "tree_plain.png")
    )

    # 2. Render with King Scale colors
    print("\n2. Rendering with King Scale colors...")
    tree.set_sephiroth_color_scheme(ColorScheme.KING_SCALE)
    tree.set_path_color_scheme(ColorScheme.KING_SCALE)
    tree.render(
        display=True,
        save_to_file=os.path.join(output_dir, "tree_king_scale.png")
    )

    # 3. Render with mixed color schemes
    print("\n3. Rendering with mixed color schemes (Queen Scale Sephiroth, Prince Scale Paths)...")
    tree.set_sephiroth_color_scheme(ColorScheme.QUEEN_SCALE)
    tree.set_path_color_scheme(ColorScheme.PRINCE_SCALE)
    tree.render(
        display=True,
        save_to_file=os.path.join(output_dir, "tree_mixed_scales.png")
    )

    # 4. Render focusing on Tiphereth (6)
    print("\n4. Rendering with focus on Tiphereth (Sephirah 6)...")
    tree.render(
        focus_sephirah=6,
        display=True,
        save_to_file=os.path.join(output_dir, "tree_focus_tiphereth.png")
    )

    # 5. Render focusing on Kether (1) with Princess Scale
    print("\n5. Rendering with focus on Kether (Sephirah 1) using Princess Scale...")
    tree.set_sephiroth_color_scheme(ColorScheme.PRINCESS_SCALE)
    tree.set_path_color_scheme(ColorScheme.PRINCESS_SCALE)
    tree.render(
        focus_sephirah=1,
        display=True,
        save_to_file=os.path.join(output_dir, "tree_focus_kether_princess.png")
    )

    # 6. Render focusing on Malkuth (10) with Queen Scale
    print("\n6. Rendering with focus on Malkuth (Sephirah 10) using Queen Scale...")
    tree.set_sephiroth_color_scheme(ColorScheme.QUEEN_SCALE)
    tree.set_path_color_scheme(ColorScheme.QUEEN_SCALE)
    tree.render(
        focus_sephirah=10,
        display=True,
        save_to_file=os.path.join(output_dir, "tree_focus_malkuth_queen.png")
    )

    print("\nAll renderings complete! Images saved to the 'output' directory.")


if __name__ == "__main__":
    main()
