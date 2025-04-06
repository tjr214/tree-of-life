from enum import Enum
from typing import Dict, Optional, Any
import matplotlib.colors as mcolors
import yaml
import numpy as np
import matplotlib.patches as patches


class ColorScheme(Enum):
    """Enum defining the available color schemes for the Tree of Life."""
    PLAIN = "plain"  # Default color scheme from original implementation
    KING_SCALE = "king"
    QUEEN_SCALE = "queen"
    PRINCE_SCALE = "prince"
    PRINCESS_SCALE = "princess"


# Define type aliases for clarity
ColorEffect = Dict[str, Any]  # Stores special color effect information


class ColorParser:
    """
    A utility class to parse color scales from the color_scales.yaml file.
    """

    @staticmethod
    def parse_color_scales(file_path: str) -> Dict[str, Dict[str, Dict[int, Dict[str, Any]]]]:
        """
        Parse the color_scales.yaml file to extract color information.

        Args:
            file_path: Path to the color_scales.yaml file

        Returns:
            Dictionary with structure:
            {
                'king': {
                    'sephiroth': {1: {'color': '#FFFFFF', 'effects': {...}}, ...},
                    'paths': {11: {'color': '#FFFFC0', 'effects': {...}}, ...}
                },
                'queen': {...},
                ...
            }
        """
        try:
            with open(file_path, 'r') as f:
                yaml_data = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Color scales file not found at {file_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return {}

        # Initialize result dictionary
        result = {
            'king': {'sephiroth': {}, 'paths': {}},
            'queen': {'sephiroth': {}, 'paths': {}},
            'prince': {'sephiroth': {}, 'paths': {}},
            'princess': {'sephiroth': {}, 'paths': {}}
        }

        # Process each scale from the YAML file
        if 'scales' in yaml_data:
            for scale_name, scale_data in yaml_data['scales'].items():
                if scale_name not in result:
                    continue  # Skip unexpected scales

                # Process sephiroth
                if 'sephiroth' in scale_data:
                    for sephirah in scale_data['sephiroth']:
                        number = sephirah['number']
                        color_info = {
                            'color': sephirah['hex'],
                            'effects': None
                        }

                        # Handle special effects
                        if 'effect' in sephirah:
                            effect_type = sephirah['effect'].get('type')
                            if effect_type:
                                effects = {'type': effect_type}

                                if 'color' in sephirah['effect'] and 'hex' in sephirah['effect']:
                                    effects['color2'] = sephirah['effect']['color']
                                    effects['color2_hex'] = sephirah['effect']['hex']
                                elif 'colors' in sephirah['effect']:
                                    # Handle multiple fleck colors
                                    effects['colors'] = sephirah['effect']['colors']

                                color_info['effects'] = effects

                        result[scale_name]['sephiroth'][number] = color_info

                # Process paths
                if 'paths' in scale_data:
                    for path in scale_data['paths']:
                        number = path['number']
                        color_info = {
                            'color': path['hex'],
                            'effects': None
                        }

                        # Handle special effects
                        if 'effect' in path:
                            effect_type = path['effect'].get('type')
                            if effect_type:
                                effects = {'type': effect_type}

                                if 'color' in path['effect'] and 'hex' in path['effect']:
                                    effects['color2'] = path['effect']['color']
                                    effects['color2_hex'] = path['effect']['hex']
                                elif 'colors' in path['effect']:
                                    # Handle multiple fleck colors
                                    effects['colors'] = path['effect']['colors']

                                color_info['effects'] = effects

                        result[scale_name]['paths'][number] = color_info

        return result


# Default colors for sephiroth and paths
DEFAULT_SEPHIROTH_COLORS = {
    0: "#FFFFFF",   # Da'ath - Lavender
    1: "#FFFFFF",   # Kether - White
    2: "#FFFFFF",   # Chokmah - Pale Blue
    3: "#FFFFFF",   # Binah - Crimson
    4: "#FFFFFF",   # Chesed - Deep Violet
    5: "#FFFFFF",   # Geburah - Orange
    6: "#FFFFFF",   # Tiphereth - Pink
    7: "#FFFFFF",   # Netzach - Amber
    8: "#FFFFFF",   # Hod - Lavender
    9: "#FFFFFF",   # Yesod - Indigo
    10: "#FFFFFF"   # Malkuth - Yellow
}

DEFAULT_PATH_COLORS = {
    # Use a neutral color for all paths in the default scheme
    # This will be overridden by specific color schemes
    i: "#FFFFFF" for i in range(11, 33)
}


def blend_colors(color1: str, color2: str, ratio: float = 0.8) -> str:
    """
    Blend two colors together with the given ratio.

    Args:
        color1: First color (as hex string)
        color2: Second color (as hex string)
        ratio: Ratio of the first color (0.0 to 1.0)

    Returns:
        Blended color as hex string
    """
    # Convert hex strings to RGB
    rgb1 = mcolors.to_rgb(color1)
    rgb2 = mcolors.to_rgb(color2)

    # Blend the colors
    blended_rgb = tuple(c1 * ratio + c2 * (1 - ratio)
                        for c1, c2 in zip(rgb1, rgb2))

    # Convert back to hex
    return mcolors.to_hex(blended_rgb)


def apply_color_effect(ax, element_type: str, number: int, x: float, y: float,
                       color: str, effect: Optional[ColorEffect], radius: float = None) -> None:
    """
    Apply special color effects (flecked, rayed, tinged) to a Sephirah or Path.

    Args:
        ax: Matplotlib axis to draw on
        element_type: Type of element ('sephirah' or 'path')
        number: Element number (1-10 for Sephiroth, 11-32 for Paths)
        x, y: Center coordinates
        color: Base color
        effect: Special color effect data
        radius: Radius (for Sephiroth only)
    """
    if not effect:
        return

    effect_type = effect.get('type')

    if effect_type == 'flecked':
        # Get the second color for flecking - adapt to YAML structure
        if 'color2_hex' in effect:
            color2 = effect['color2_hex']
        elif 'colors' in effect and len(effect['colors']) > 0:
            # Use the first color in the colors list if available
            color2 = effect['colors'][0].get('hex', '#FFFFFF')
        else:
            color2 = '#FFFFFF'  # Default

        if element_type == 'sephirah' and radius:
            # Draw small circles randomly distributed within the Sephirah
            num_flecks = 50  # Number of flecks
            # Use element number as seed for reproducibility
            np.random.seed(number)

            for _ in range(num_flecks):
                # Random position within the circle
                angle = np.random.uniform(0, 2 * np.pi)
                # Stay within 90% of radius
                r = np.random.uniform(0, radius * 0.9)
                fleck_x = x + r * np.cos(angle)
                fleck_y = y + r * np.sin(angle)

                # Random size for the fleck, proportional to the main circle
                fleck_size = np.random.uniform(0.02, 0.05) * radius

                # Draw the fleck
                fleck = patches.Circle(
                    (fleck_x, fleck_y),
                    fleck_size,
                    facecolor=color2,
                    edgecolor=None,
                    alpha=0.8,
                    zorder=5  # Above the main circle
                )
                ax.add_patch(fleck)

        elif element_type == 'path':
            # For paths, this will need to be implemented differently when drawing paths
            pass

    elif effect_type == 'rayed':
        # Get the second color for rays - adapt to YAML structure
        if 'color2_hex' in effect:
            color2 = effect['color2_hex']
        elif 'colors' in effect and len(effect['colors']) > 0:
            # Use the first color in the colors list if available
            color2 = effect['colors'][0].get('hex', '#FFFFFF')
        else:
            color2 = '#FFFFFF'  # Default

        if element_type == 'sephirah' and radius:
            # Draw rays emanating from the center
            num_rays = 12  # Number of rays
            ray_length = radius * 1.5  # Rays extend beyond the circle

            for i in range(num_rays):
                angle = i * (2 * np.pi / num_rays)
                end_x = x + ray_length * np.cos(angle)
                end_y = y + ray_length * np.sin(angle)

                # Draw the ray as a line
                ax.plot(
                    [x, end_x],
                    [y, end_y],
                    color=color2,
                    linewidth=radius * 0.1,
                    alpha=0.6,
                    zorder=2  # Below the main circle but above background
                )

        elif element_type == 'path':
            # For paths, this will need to be implemented differently when drawing paths
            pass

    elif effect_type == 'tinged':
        # For tinged, we slightly blend the color with another
        # Get the tinge color - adapt to YAML structure
        if 'color2_hex' in effect:
            tinge_color = effect['color2_hex']
        elif 'colors' in effect and len(effect['colors']) > 0:
            # Use the first color in the colors list if available
            tinge_color = effect['colors'][0].get('hex', '#FFFFFF')
        else:
            tinge_color = '#FFFFFF'  # Default

        # Blend the colors with a subtle tinge
        blended_color = blend_colors(color, tinge_color, 0.7)

        # This is typically applied by giving the main color a slight tint
        # The actual implementation will happen when drawing the elements
        pass


def apply_path_effect(ax, path_num: int, x1: float, y1: float, x2: float, y2: float,
                      color: str, effect: Optional[ColorEffect], sphere_scale_factor: float) -> None:
    """
    Apply special color effects to a path.

    Args:
        ax: Matplotlib axis
        path_num: Path number (11-32)
        x1, y1: Coordinates of the first endpoint
        x2, y2: Coordinates of the second endpoint
        color: Base color of the path
        effect: Special color effect data
        sphere_scale_factor: Scale factor for spheres (used for proportional sizing)
    """
    if not effect:
        return

    effect_type = effect.get('type')

    if effect_type == 'flecked':
        # Get the second color for flecking - adapt to YAML structure
        if 'color2_hex' in effect:
            color2 = effect['color2_hex']
        elif 'colors' in effect and len(effect['colors']) > 0:
            # Use the first color in the colors list if available
            color2 = effect['colors'][0].get('hex', '#FFFFFF')
        else:
            color2 = '#FFFFFF'  # Default

        # Calculate the path length and angle
        dx = x2 - x1
        dy = y2 - y1
        path_length = np.sqrt(dx*dx + dy*dy)
        angle = np.arctan2(dy, dx)

        # Draw flecks along the path
        # Scale number of flecks with path length
        num_flecks = int(path_length * 15)
        # Use path number as seed for reproducibility
        np.random.seed(path_num)

        for _ in range(num_flecks):
            # Random position along the path
            t = np.random.uniform(0.1, 0.9)  # Avoid endpoints
            # Random offset perpendicular to the path
            offset = np.random.uniform(-0.05, 0.05)

            fleck_x = x1 + t * dx + offset * np.sin(angle)
            fleck_y = y1 + t * dy - offset * np.cos(angle)

            # Random size for the fleck
            fleck_size = np.random.uniform(0.01, 0.03) * sphere_scale_factor

            # Draw the fleck
            fleck = patches.Circle(
                (fleck_x, fleck_y),
                fleck_size,
                facecolor=color2,
                edgecolor=None,
                alpha=0.8,
                zorder=3  # Above the path
            )
            ax.add_patch(fleck)

    elif effect_type == 'rayed':
        # Get the second color for rays - adapt to YAML structure
        if 'color2_hex' in effect:
            color2 = effect['color2_hex']
        elif 'colors' in effect and len(effect['colors']) > 0:
            # Use the first color in the colors list if available
            color2 = effect['colors'][0].get('hex', '#FFFFFF')
        else:
            color2 = '#FFFFFF'  # Default

        # Calculate the midpoint
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        # Draw rays emanating perpendicular to the path
        num_rays = 8  # Number of rays
        ray_length = 0.2 * sphere_scale_factor  # Length of rays

        # Calculate path direction vector
        dx = x2 - x1
        dy = y2 - y1
        path_length = np.sqrt(dx*dx + dy*dy)

        # Normalize direction vector
        if path_length > 0:
            dx /= path_length
            dy /= path_length

            # Calculate perpendicular vector
            perp_dx = -dy
            perp_dy = dx

            # Draw rays along the path
            for t in np.linspace(0.2, 0.8, num_rays):
                # Position along the path
                ray_x = x1 + t * dx * path_length
                ray_y = y1 + t * dy * path_length

                # Draw rays in perpendicular directions
                ax.plot(
                    [ray_x, ray_x + perp_dx * ray_length],
                    [ray_y, ray_y + perp_dy * ray_length],
                    color=color2,
                    linewidth=1.5,
                    alpha=0.7,
                    zorder=2.5
                )

                ax.plot(
                    [ray_x, ray_x - perp_dx * ray_length],
                    [ray_y, ray_y - perp_dy * ray_length],
                    color=color2,
                    linewidth=1.5,
                    alpha=0.7,
                    zorder=2.5
                )

    elif effect_type == 'tinged':
        # For tinged paths, we'd normally blend the colors
        # Get the tinge color - adapt to YAML structure
        if 'color2_hex' in effect:
            tinge_color = effect['color2_hex']
        elif 'colors' in effect and len(effect['colors']) > 0:
            # Use the first color in the colors list if available
            tinge_color = effect['colors'][0].get('hex', '#FFFFFF')
        else:
            tinge_color = '#FFFFFF'  # Default

        # The blended color would be used to draw the path
        # This is handled during the main path drawing
        pass


def get_contrasting_text_color(background_color: str) -> str:
    """
    Determine whether to use light or dark text based on background color brightness.

    Args:
        background_color: Hex color string (e.g., "#RRGGBB")

    Returns:
        Text color as hex string ("#FFFFFF" for white or "#000000" for black)
    """
    # Convert hex color to RGB values
    bg_color = background_color.lstrip('#')
    r, g, b = int(bg_color[0:2], 16), int(
        bg_color[2:4], 16), int(bg_color[4:6], 16)

    # Special case for bright green (#00FF00) which should use black text
    if r == 0 and g > 240 and b == 0:
        return "#000000"

    # Calculate perceived brightness using the common formula
    # (0.299*R + 0.587*G + 0.114*B)
    brightness = (0.299 * r + 0.587 * g + 0.114 * b)

    # Use white text on dark backgrounds, black text on light backgrounds
    # Use a higher threshold (150) for better readability with gray colors
    return "#FFFFFF" if brightness < 150 else "#000000"
