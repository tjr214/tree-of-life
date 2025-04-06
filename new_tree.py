import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np  # Required for the glow effect
from typing import List, Tuple, Dict

# Define type aliases for clarity
Coord = Tuple[float, float]
PathIndices = Tuple[int, int]


def draw_tree_of_life(output_filename: str = None) -> None:
    """
    Generates and displays or saves a diagram of the Kabbalistic Tree of Life.

    Args:
        output_filename (str, optional): If provided, saves the plot to this
                                         filename. Otherwise, displays the plot.
                                         Defaults to None.
    """

    # Define parameters for scaling
    sphere_scale_factor: float = 1.75  # Scale factor for spheres (sephirot)
    spacing_factor: float = 1.5        # Factor to adjust spacing between spheres

    # Original base radius
    base_radius: float = 0.5
    # Calculate the increased radius
    circle_radius: float = base_radius * sphere_scale_factor

    # Define a shift value to move everything down
    # Shift value for moving everything below Kether down
    vertical_shift: float = -0.5 * spacing_factor

    # 1. Define Coordinates for the Sephirot with adjusted spacing
    # We apply the spacing factor to spread out the coordinates
    sephirot_coords: List[Coord] = [
        # 0: Kether (Top center) - kept in original position
        (0 * spacing_factor, 9 * spacing_factor),
        # 1: Chokmah (Top right) - shifted down
        (2.0 * spacing_factor, 8.0 * spacing_factor + vertical_shift),
        # 2: Binah (Top left) - shifted down
        (-2.0 * spacing_factor, 8.0 * spacing_factor + vertical_shift),
        # 3: Chesed (Mid right) - shifted down
        (2.0 * spacing_factor, 5.0 * spacing_factor + vertical_shift),
        # 4: Geburah (Mid left) - shifted down
        (-2.0 * spacing_factor, 5.0 * spacing_factor + vertical_shift),
        # 5: Tiphereth (Center) - shifted down
        (0 * spacing_factor, 3.5 * spacing_factor + vertical_shift),
        # 6: Netzach (Bottom right) - shifted down
        (2.0 * spacing_factor, 2.0 * spacing_factor + vertical_shift),
        # 7: Hod (Bottom left) - shifted down
        (-2.0 * spacing_factor, 2.0 * spacing_factor + vertical_shift),
        # 8: Yesod (Bottom center) - shifted down
        (0 * spacing_factor, 1.0 * spacing_factor + vertical_shift),
        # 9: Malkuth (Bottom) - shifted down
        (0 * spacing_factor, -1.3 * spacing_factor + vertical_shift)
    ]

    # Coordinate for the hidden Sephirah, Da'ath - also shifted down
    daath_coord: Coord = (0 * spacing_factor, 6.5 *
                          spacing_factor + vertical_shift)

    # 2. Define the Paths connecting the Sephirot
    #    Each tuple contains the 0-based indices of the two Sephirot it connects.
    #    There are 22 paths in total.
    paths: List[PathIndices] = [
        # Vertical Paths (Pillars)
        (0, 5), (5, 8), (8, 9),  # Middle Pillar
        (1, 3), (3, 6),          # Right Pillar
        (2, 4), (4, 7),          # Left Pillar

        # Horizontal Paths
        (1, 2), (3, 4), (6, 7),

        # Diagonal Paths
        (0, 1), (0, 2),          # Kether connections
        # Chokmah connections (Note: 1-4 is debated, but present in many diagrams like the source)
        (1, 5), (1, 4),
        # Binah connections (Note: 2-3 is debated, but present in many diagrams like the source)
        (2, 5), (2, 3),
        (3, 5), (3, 8),          # Chesed connections
        (4, 5), (4, 6),          # Geburah connections
        (5, 6), (5, 7),          # Tiphereth connections
        (6, 8),                  # Netzach connection
        (7, 8),                  # Hod connection
        (6, 9),                  # Netzach to Malkuth (Added based on source image)
        (7, 9),                  # Hod to Malkuth (Added based on source image)
    ]

    # Ensure path list consistency with standard diagrams and the source image.
    # Standard diagrams often omit 1-4, 2-3, 6-9, 7-9. However, the *provided source image* clearly shows these paths.
    # Let's refine the path list strictly based on the *visual evidence* in the provided image.
    paths_from_image: List[PathIndices] = [
        # From Kether (0)
        (0, 1), (0, 2), (0, 5),
        # From Chokmah (1)
        (1, 2), (1, 3), (1, 5),
        # From Binah (2)
        (2, 4), (2, 5),
        # From Chesed (3)
        (3, 4), (3, 5), (3, 6),
        # From Geburah (4)
        (4, 5), (4, 7),
        # From Tiphereth (5)
        (5, 6), (5, 7), (5, 8),
        # From Netzach (6)
        (6, 7), (6, 8), (6, 9),
        # From Hod (7)
        (7, 8), (7, 9),
        # From Yesod (8)
        (8, 9)
        # This list has 22 paths and matches the visual connections exactly. We'll use this one.
    ]

    # 3. Setup the Plot
    # Adjust figsize for better aspect ratio
    # Adjusted from original (6, 9) based on spacing factor
    fig, ax = plt.subplots(figsize=(7.5, 11))
    fig.patch.set_facecolor('#EAEAEA')  # Set background color of the figure
    ax.set_facecolor('#EAEAEA')      # Set background color of the axes area

    # Set plot limits with some padding to accommodate the larger spheres and adjusted spacing
    # Expanded to accommodate wider sephirot positioning
    ax.set_xlim(-4.0, 4.0)
    # Extended lower limit to accommodate Malkuth's new position
    ax.set_ylim(-4.0, 14.5)

    # Ensure aspect ratio is equal so circles are not distorted
    ax.set_aspect('equal', adjustable='box')

    # Hide the axes
    ax.axis('off')

    # Define visual parameters
    line_color_outer: str = 'black'
    line_color_inner: str = 'white'
    # Further increased thickness for paths to accommodate future text/symbols
    line_width_outer: float = 11.5 * \
        (sphere_scale_factor * 0.7)  # Even thicker than before
    # Further increased thickness while maintaining the outer/inner ratio
    line_width_inner: float = 8.0 * (sphere_scale_factor * 0.7)
    circle_edge_color: str = 'black'
    circle_face_color: str = 'white'
    circle_line_width: float = 1.5 * \
        (sphere_scale_factor * 0.6)  # Adjusted for visual balance
    zorder_paths_outer: int = 1  # Draw black lines first
    zorder_paths_inner: int = 2  # Draw white lines on top
    zorder_circles: int = 3     # Draw circles on top of lines
    # Draw Daath outline above outer paths, potentially below inner paths/circles
    zorder_daath: int = 2

    # 4. Draw the Paths
    # Draw the thicker black lines first (as outlines)
    for i, j in paths_from_image:
        x1, y1 = sephirot_coords[i]
        x2, y2 = sephirot_coords[j]
        ax.plot([x1, x2], [y1, y2],
                color=line_color_outer,
                linewidth=line_width_outer,
                solid_capstyle='round',  # Use round caps for smoother joins
                zorder=zorder_paths_outer)

    # Draw the slightly thinner white lines on top to create the filled effect
    for i, j in paths_from_image:
        x1, y1 = sephirot_coords[i]
        x2, y2 = sephirot_coords[j]
        ax.plot([x1, x2], [y1, y2],
                color=line_color_inner,
                linewidth=line_width_inner,
                solid_capstyle='round',
                zorder=zorder_paths_inner)

    # 5. Draw the Sephirot (Circles)
    for i, (x, y) in enumerate(sephirot_coords):
        # Special effect for Kether (index 0)
        if i == 0:  # Kether
            # Create a radiant/emanating effect for Kether
            # First draw a series of concentric circles with decreasing opacity
            num_rings = 12
            max_radius = circle_radius * 1.25  # Reduced from 1.8 to make halo smaller
            base_alpha = 0.8  # Increased slightly for better visibility with smaller halo

            # Create white glow effect with multiple circles
            for r in np.linspace(max_radius, circle_radius, num_rings):
                alpha = base_alpha * \
                    ((r - circle_radius) / (max_radius - circle_radius))
                glow = patches.Circle((x, y), radius=r,
                                      facecolor='#FFFFFF',  # Pure white color
                                      edgecolor='none',
                                      alpha=alpha,
                                      zorder=zorder_circles - 1)  # Below the main circle
                ax.add_patch(glow)

            # Add rays of light emanating from Kether (shorter rays)
            num_rays = 12
            ray_length = circle_radius * 1.4  # Reduced from 2.2 to make rays shorter
            for angle in np.linspace(0, 2*np.pi, num_rays, endpoint=False):
                dx = ray_length * np.cos(angle)
                dy = ray_length * np.sin(angle)
                # Draw a line from just outside the circle to the ray endpoint
                ax.plot([x + np.cos(angle)*circle_radius*1.05, x + dx],  # Start closer to the circle
                        [y + np.sin(angle)*circle_radius*1.05, y + dy],
                        color='#FFFFFF',     # Pure white
                        alpha=0.7,           # Slightly more opaque for better visibility
                        linewidth=1.2,       # Slightly thinner lines
                        zorder=zorder_circles - 1)  # Below the main circle

            # Now draw the main Kether circle with a slightly brighter color
            circle = patches.Circle((x, y), radius=circle_radius,
                                    facecolor='#FFFFFF',  # Pure white for Kether
                                    edgecolor=circle_edge_color,
                                    linewidth=circle_line_width,
                                    zorder=zorder_circles)
        else:  # All other Sephirot
            circle = patches.Circle((x, y), radius=circle_radius,
                                    facecolor=circle_face_color,
                                    edgecolor=circle_edge_color,
                                    linewidth=circle_line_width,
                                    zorder=zorder_circles)  # Ensure circles are on top
        ax.add_patch(circle)

    # Add the traditional numbering (1-10) to each Sephirah
    for i, (x, y) in enumerate(sephirot_coords):
        # Traditional numbering starts at 1, so add 1 to the 0-based index
        number = i + 1
        ax.text(x, y, str(number),
                fontsize=12 * sphere_scale_factor * 0.55,  # Adjusted for visual balance
                fontweight='bold',
                ha='center',
                va='center',
                color='black',
                zorder=zorder_circles + 1)  # Make text appear above circles

    # 6. Draw Da'ath (Dotted Circle)
    daath_circle = patches.Circle(daath_coord, radius=circle_radius,
                                  facecolor='none',  # No fill
                                  edgecolor=circle_edge_color,  # Black outline
                                  linewidth=circle_line_width,
                                  linestyle=':',  # Dotted line style
                                  zorder=zorder_daath)  # Place appropriately in stack order
    ax.add_patch(daath_circle)

    # 7. Finalize and Show/Save Plot
    plt.tight_layout()  # Adjust layout to prevent clipping

    if output_filename:
        plt.savefig(output_filename, facecolor=fig.get_facecolor(), dpi=300)
        print(f"Tree of Life diagram saved to {output_filename}")
    else:
        plt.show()


# --- Execute the function ---
if __name__ == "__main__":
    # To display the plot:
    # draw_tree_of_life()

    # To save the plot to a file (e.g., tree_of_life.png):
    draw_tree_of_life(output_filename="tree_of_life.png")
