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
        # 0: Kether (כתר) - Crown - Sephirah #1 - Divine Will/Light
        (0 * spacing_factor, 9 * spacing_factor),
        # 1: Chokmah (חכמה) - Wisdom - Sephirah #2 - Creative Force
        (2.0 * spacing_factor, 8.0 * spacing_factor + vertical_shift),
        # 2: Binah (בינה) - Understanding - Sephirah #3 - Divine Understanding
        (-2.0 * spacing_factor, 8.0 * spacing_factor + vertical_shift),
        # 3: Chesed (חסד) - Mercy/Kindness - Sephirah #4 - Loving Grace
        (2.0 * spacing_factor, 5.5 * spacing_factor + vertical_shift),
        # 4: Geburah (גבורה) - Severity/Strength - Sephirah #5 - Divine Judgment
        (-2.0 * spacing_factor, 5.5 * spacing_factor + vertical_shift),
        # 5: Tiphereth (תפארת) - Beauty/Harmony - Sephirah #6 - Balance & Truth
        (0 * spacing_factor, 4.25 * spacing_factor + vertical_shift),
        # 6: Netzach (נצח) - Victory/Eternity - Sephirah #7 - Divine Emotion
        (2.0 * spacing_factor, 3.0 * spacing_factor + vertical_shift),
        # 7: Hod (הוד) - Splendor/Glory - Sephirah #8 - Divine Intellect
        (-2.0 * spacing_factor, 3.0 * spacing_factor + vertical_shift),
        # 8: Yesod (יסוד) - Foundation - Sephirah #9 - Divine Connection
        (0 * spacing_factor, 1.75 * spacing_factor + vertical_shift),
        # 9: Malkuth (מלכות) - Kingdom - Sephirah #10 - Physical Manifestation
        (0 * spacing_factor, -0.7 * spacing_factor + vertical_shift)
    ]

    # Coordinate for the hidden Sephirah, Da'ath (דעת) - Knowledge
    # Positioned at the geometric center of Chokmah, Binah, Chesed, and Geburah
    daath_coord: Coord = (0 * spacing_factor, 6.75 *
                          spacing_factor + vertical_shift)

    # 2. Define the Paths connecting the Sephirot
    #    Each tuple contains the 0-based indices of the two Sephirot it connects.
    #    There are 22 paths in total, corresponding to the 22 Hebrew letters.

    # We'll use this refined path list based on visual evidence in standard diagrams
    paths_from_image: List[PathIndices] = [
        # Paths from Kether (0)
        (0, 1),  # Kether to Chokmah (Path 11, Diagonal, א, The Fool, Air)
        (0, 2),  # Kether to Binah (Path 12, Diagonal, ב, The Magus, Mercury)
        (0, 5),  # Kether to Tiphereth (Path 13, Middle Pillar, ג, The Priestess, Moon)

        # Paths from Chokmah (1)
        (1, 2),  # Chokmah to Binah (Path 14, Horizontal Path, ד, The Empress, Venus)
        (1, 5),  # Chokmah to Tiphereth (Path 15, Diagonal, ה, The Star, Aquarius)
        (1, 3),  # Chokmah to Chesed (Path 16, Right Pillar, ו, The Hierophant, Taurus)


        # Paths from Binah (2)
        (2, 5),  # Binah to Tiphereth (Path 17, Diagonal, ז, The Lovers, Gemini)
        (2, 4),  # Binah to Geburah (Path 18, Left Pillar, ח, The Chariot, Cancer)


        # Paths from Chesed (3)
        (3, 4),  # Chesed to Geburah (Path 19, Horizontal Path, ט, Lust, Leo)
        (3, 5),  # Chesed to Tiphereth (Path 20, Diagonal, י, The Hermit, Virgo)
        (3, 6),  # Chesed to Netzach (Path 21, Diagonal, כ, The Wheel of Fortune, Jupiter)

        # Paths from Geburah (4)
        (4, 5),  # Geburah to Tiphereth (Path 22, Diagonal, ל, Justice, Libra)
        (4, 7),  # Geburah to Hod (Path 23, Diagonal, מ, The Hanged Man, Water)

        # Paths from Tiphereth (5)
        (5, 6),  # Tiphereth to Netzach (Path 24, Diagonal, נ, Death, Scorpio)
        (5, 8),  # Tiphereth to Yesod (Path 25, Middle Pillar, ס, Art / Temperance, Sagittarius)
        (5, 7),  # Tiphereth to Hod (Path 26, Diagonal, ע, The Devil, Capricorn)


        # Paths from Netzach (6)
        (6, 7),  # Netzach to Hod (Path 27, Horizontal Path, פ, The Tower, Mars)
        (6, 8),  # Netzach to Yesod (Path 28, Diagonal, צ, The Emperor, Aries)
        (6, 9),  # Netzach to Malkuth (Path 29, Diagonal, ק, The Moon, Pisces)

        # Paths from Hod (7)
        (7, 8),  # Hod to Yesod (Path 30, Diagonal, ר, The Sun, Sun)
        (7, 9),  # Hod to Malkuth (Path 31, Diagonal, ש, The Vision & The Voice, Fire/Spirit)

        # Path from Yesod (8)
        (8, 9)   # Yesod to Malkuth (Path 32, Middle Pillar, ת, The World, Saturn, Earth)
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
    # Adjusted to center the diagram vertically
    ax.set_ylim(-3.5, 15.0)

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
            num_rays = 12  # 12 rays of the crown...
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
