from TreeOfLife import TreeOfLife, ColorScheme


def main():
    """
    Test script to demonstrate the focused rendering functionality of the Tree of Life.
    """
    # Create a Tree of Life instance with default settings
    tree = TreeOfLife(
        sphere_scale_factor=1.75,
        spacing_factor=1.5,
        sephiroth_color_scheme=ColorScheme.QUEEN_SCALE,
        path_color_scheme=ColorScheme.QUEEN_SCALE
    )

    # Render the full tree
    print("Rendering full Tree of Life...")
    tree.render(save_to_file="full_tree.png", display=False)

    # Render focused views for different Sephiroth
    focus_sephiroth = [1, 6, 9]  # Kether, Tiphereth, Yesod

    for sephirah_num in focus_sephiroth:
        print(f"Rendering focused view for Sephirah {sephirah_num}...")
        tree.render(
            focus_sephirah=sephirah_num,
            save_to_file=f"focused_sephirah_{sephirah_num}.png",
            display=False,
            show_title=True
        )

    print("All renderings completed!")


if __name__ == "__main__":
    main()
