#!/usr/bin/env python
"""
Tree of Life Generator - Command Line Utility
---------------------------------------------

A CLI tool to configure, save, load, and render Tree of Life visualizations.
This tool provides a rich, interactive interface for working with the TreeOfLife class.
"""

import os
import sys
import argparse
import yaml
from typing import Dict, Any, Optional, Tuple, List, Union

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt
from rich.table import Table
from rich.text import Text
from rich import print as rprint

from tol import TreeOfLife, ColorScheme


# Initialize Rich console
console = Console()


def display_banner() -> None:
    """Display an 80s/90s style ASCII art banner for the application."""
    # ASCII art created with FIGlet (font: slant)
    banner = r"""
    ___________                     ________   ___      .__ _______
    \__    ___/______   ____   ____ \_____  \  \  \     |  |\      \
      |    |  \_  __ \_/ __ \_/ __ \ /   |   \  \  \    |  |/   |   \
      |    |   |  | \/\  ___/\  ___//    |    \  \  \   |  /    |    \
      |____|   |__|    \___  >\___  >_______  /   \__\_/  /\____|__  /
                           \/     \/        \/           \/         \/
     _____________   ____   __________              __
    /  _____/\   \ /   /   \______   \__ __   ____ |  | ______
   /   \  ___ \   Y   /     |     ___/  |  \_/ __ \|  |/ /  _ \
   \    \_\  \ \     /      |    |   |  |  /\  ___/|    <  <_> )
    \______  /  \___/ /\ /\ |____|   |____/  \___  >__|_ \____/
           \/         \/ \/                       \/     \/
    """

    # Display the banner with a colorful panel
    console.print(Panel(
        Text(banner, style="bold bright_magenta"),
        border_style="bright_cyan",
        title="[bold bright_yellow]Tree of Life Generator[/]",
        subtitle="[italic bright_green]Interactive CLI Tool[/]"
    ))


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Tree of Life visualization generator",
        epilog="Run without arguments for interactive mode"
    )

    parser.add_argument(
        "config_file",
        nargs="?",
        help="YAML configuration file path (optional)"
    )

    parser.add_argument(
        "--display",
        action="store_true",
        help="Display the visualization instead of saving to file"
    )

    return parser.parse_args()


def run_interactive_config() -> Dict[str, Any]:
    """
    Run interactive configuration prompts to configure a Tree of Life visualization.

    Returns:
        Dict[str, Any]: Configuration dictionary with all TreeOfLife parameters.
    """
    config = {
        "basic": {},
        "color_schemes": {},
        "text_display": {},
        "rendering": {}
    }

    console.print("\n[bold cyan]===== Tree of Life Configuration =====[/]")
    console.print("[dim]Enter values or press Enter for defaults[/]")

    # --- Basic Parameters ---
    console.print("\n[bold green]Basic Parameters:[/]")

    config["basic"]["sphere_scale_factor"] = FloatPrompt.ask(
        "Sphere scale factor [cyan](controls size of Sephiroth)[/]",
        default=1.75
    )

    config["basic"]["spacing_factor"] = FloatPrompt.ask(
        "Spacing factor [cyan](controls distance between Sephiroth)[/]",
        default=1.5
    )

    # --- Color Schemes ---
    console.print("\n[bold green]Color Schemes:[/]")

    # Create color scheme choices table
    scheme_table = Table(title="Available Color Schemes")
    scheme_table.add_column("Number", justify="center", style="cyan")
    scheme_table.add_column("Scheme Name", style="green")
    scheme_table.add_column("Description", style="yellow")

    schemes = [
        (1, "PLAIN", "Simple default colors"),
        (2, "KING_SCALE", "Elemental/planetary associations in Atziluth"),
        (3, "QUEEN_SCALE", "Elemental/planetary associations in Briah"),
        (4, "PRINCE_SCALE", "Elemental/planetary associations in Yetzirah"),
        (5, "PRINCESS_SCALE", "Elemental/planetary associations in Assiah")
    ]

    for num, name, desc in schemes:
        scheme_table.add_row(str(num), name, desc)

    console.print(scheme_table)

    # Prompt for Sephiroth color scheme
    sephiroth_scheme = IntPrompt.ask(
        "Sephiroth color scheme (1-5)",
        default=2,  # KING_SCALE
        choices=[str(i) for i in range(1, 6)]
    )
    config["color_schemes"]["sephiroth"] = schemes[sephiroth_scheme-1][1]

    # Prompt for Path color scheme
    path_scheme = IntPrompt.ask(
        "Path color scheme (1-5)",
        default=2,  # KING_SCALE
        choices=[str(i) for i in range(1, 6)]
    )
    config["color_schemes"]["path"] = schemes[path_scheme-1][1]

    # --- Text Display Options ---
    console.print("\n[bold green]Text Display Options:[/]")

    # Create text mode choices table
    text_mode_table = Table(title="Sephiroth Text Display Modes")
    text_mode_table.add_column("Number", justify="center", style="cyan")
    text_mode_table.add_column("Mode", style="green")
    text_mode_table.add_column("Description", style="yellow")

    text_modes = [
        (1, "NUMBER", "Traditional enumeration (1-10)"),
        (2, "TRIGRAM", "I Ching trigrams corresponding to each Sephirah"),
        (3, "HEBREW", "Hebrew names of the Sephiroth"),
        (4, "PLANET", "Planetary symbols corresponding to each Sephirah")
    ]

    for num, name, desc in text_modes:
        text_mode_table.add_row(str(num), name, desc)

    console.print(text_mode_table)

    # Prompt for text display mode
    text_mode = IntPrompt.ask(
        "Sephiroth text mode (1-4)",
        default=1,  # NUMBER
        choices=[str(i) for i in range(1, 5)]
    )
    config["text_display"]["sephiroth_mode"] = text_modes[text_mode-1][1]

    # Prompt for text visibility
    config["text_display"]["sephiroth_visible"] = Confirm.ask(
        "Show Sephiroth text?",
        default=True
    )

    config["text_display"]["path_visible"] = Confirm.ask(
        "Show Path text and symbols?",
        default=True
    )

    # --- Rendering Options ---
    console.print("\n[bold green]Rendering Options:[/]")

    # Prompt for focus Sephirah
    focus_choice = Confirm.ask(
        "Focus on a specific Sephirah?",
        default=False
    )

    if focus_choice:
        sephiroth_names = [
            "1: Kether", "2: Chokmah", "3: Binah", "4: Chesed", "5: Geburah",
            "6: Tiphereth", "7: Netzach", "8: Hod", "9: Yesod", "10: Malkuth"
        ]

        for name in sephiroth_names:
            console.print(f"  [cyan]{name}[/]")

        focus_num = IntPrompt.ask(
            "Enter Sephirah number to focus on (1-10)",
            default=6,  # Tiphereth
            choices=[str(i) for i in range(1, 11)]
        )
        config["rendering"]["focus_sephirah"] = focus_num
    else:
        config["rendering"]["focus_sephirah"] = None

    # Prompt for figure size
    console.print("[dim]Figure size in inches (width, height)[/]")
    width = FloatPrompt.ask("Width", default=7.5)
    height = FloatPrompt.ask("Height", default=11.0)
    config["rendering"]["figsize"] = [width, height]

    # Prompt for DPI
    config["rendering"]["dpi"] = IntPrompt.ask(
        "DPI (dots per inch) [cyan](higher = better quality, larger file)[/]",
        default=300
    )

    # Prompt for title
    config["rendering"]["show_title"] = Confirm.ask(
        "Show title on the diagram?",
        default=False
    )

    return config


def save_config_to_yaml(config: Dict[str, Any], filename: str) -> None:
    """
    Save configuration dictionary to a YAML file.

    Args:
        config: Configuration dictionary with TreeOfLife parameters.
        filename: Path to save the YAML file.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

    # Add comment header to YAML file
    with open(filename, 'w') as file:
        file.write("# Tree of Life Generator Configuration\n")
        file.write("# Generated by treegen.py\n\n")
        yaml.dump(config, file, default_flow_style=False, sort_keys=False)

    console.print(
        f"\n[bold green]Configuration saved to:[/] [cyan]{filename}[/]")


def load_config_from_yaml(filename: str) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.

    Args:
        filename: Path to the YAML configuration file.

    Returns:
        Dict[str, Any]: Configuration dictionary with TreeOfLife parameters.
    """
    try:
        with open(filename, 'r') as file:
            config = yaml.safe_load(file)

        console.print(
            f"\n[bold green]Loaded configuration from:[/] [cyan]{filename}[/]")
        return config
    except Exception as e:
        console.print(f"[bold red]Error loading configuration:[/] {e}")
        sys.exit(1)


def create_tree_from_config(config: Dict[str, Any]) -> TreeOfLife:
    """
    Create a TreeOfLife object from configuration dictionary.

    Args:
        config: Configuration dictionary with TreeOfLife parameters.

    Returns:
        TreeOfLife: Configured TreeOfLife object.
    """
    try:
        # Create Tree of Life with basic parameters
        tree = TreeOfLife(
            sphere_scale_factor=config["basic"]["sphere_scale_factor"],
            spacing_factor=config["basic"]["spacing_factor"]
        )

        # Set color schemes
        sephiroth_scheme = getattr(
            ColorScheme, config["color_schemes"]["sephiroth"])
        path_scheme = getattr(ColorScheme, config["color_schemes"]["path"])

        tree.set_sephiroth_color_scheme(sephiroth_scheme)
        tree.set_path_color_scheme(path_scheme)

        # Set text display options
        sephiroth_mode = getattr(
            tree.SephirothTextMode, config["text_display"]["sephiroth_mode"])
        tree.set_sephiroth_text_mode(sephiroth_mode)

        tree.set_sephiroth_text_visibility(
            config["text_display"]["sephiroth_visible"])
        tree.set_path_text_visibility(config["text_display"]["path_visible"])

        return tree
    except Exception as e:
        console.print(f"[bold red]Error creating Tree of Life:[/] {e}")
        sys.exit(1)


def render_tree(tree: TreeOfLife, config: Dict[str, Any], display: bool, config_filename: Optional[str] = None) -> None:
    """
    Render the Tree of Life visualization.

    Args:
        tree: Configured TreeOfLife object.
        config: Configuration dictionary with rendering parameters.
        display: Whether to display the visualization instead of saving to file.
        config_filename: Optional name of the config file, used as base for output filename.
    """
    # Extract rendering parameters
    focus_sephirah = config["rendering"]["focus_sephirah"]
    figsize = tuple(config["rendering"]["figsize"])
    dpi = config["rendering"]["dpi"]
    show_title = config["rendering"]["show_title"]

    # Generate output filename if not displaying
    if not display:
        if config_filename:
            # Use the config filename base for the output file
            base_name = os.path.splitext(os.path.basename(config_filename))[0]

            # Determine suffix based on configuration
            if focus_sephirah:
                sephirah_names = [
                    "kether", "chokmah", "binah", "chesed", "geburah",
                    "tiphereth", "netzach", "hod", "yesod", "malkuth"
                ]
                suffix = f"_focus_{focus_sephirah}_{sephirah_names[focus_sephirah-1]}"
            else:
                suffix = ""

            output_file = f"{base_name}{suffix}.png"
        else:
            # Fallback to the old method if no config filename is provided
            if focus_sephirah:
                sephirah_names = [
                    "kether", "chokmah", "binah", "chesed", "geburah",
                    "tiphereth", "netzach", "hod", "yesod", "malkuth"
                ]
                output_file = f"tree_focus_{focus_sephirah}_{sephirah_names[focus_sephirah-1]}.png"
            else:
                seph_scheme = config["color_schemes"]["sephiroth"]
                path_scheme = config["color_schemes"]["path"]
                output_file = f"tree_{seph_scheme.lower()}_{path_scheme.lower()}.png"
    else:
        output_file = None

    # Show rendering information
    console.print("\n[bold green]Rendering Tree of Life:[/]")
    if focus_sephirah:
        console.print(f"  Focus: [cyan]Sephirah {focus_sephirah}[/]")
    else:
        console.print("  Focus: [cyan]None (full tree)[/]")

    console.print(
        f"  Sephiroth Color Scheme: [cyan]{config['color_schemes']['sephiroth']}[/]")
    console.print(
        f"  Path Color Scheme: [cyan]{config['color_schemes']['path']}[/]")
    console.print(f"  Figure Size: [cyan]{figsize} inches[/]")
    console.print(f"  DPI: [cyan]{dpi}[/]")

    if display:
        console.print("  Output: [cyan]Display window[/]")
    else:
        console.print(f"  Output: [cyan]{output_file}[/]")

    # Render the tree
    try:
        tree.render(
            focus_sephirah=focus_sephirah,
            display=display,
            save_to_file=output_file,
            figsize=figsize,
            dpi=dpi,
            show_title=show_title
        )

        if not display:
            console.print(
                f"\n[bold green]Visualization saved to:[/] [cyan]{output_file}[/]")
    except Exception as e:
        console.print(f"[bold red]Error rendering Tree of Life:[/] {e}")
        sys.exit(1)


def main() -> None:
    """Main function for the Tree of Life Generator CLI tool."""
    # Parse command-line arguments
    args = parse_arguments()

    # Display the banner
    display_banner()

    # Determine mode of operation
    if args.config_file is None:
        # No config file provided - run interactive mode and ask for filename
        console.print(
            "[bold blue]Running in interactive configuration mode[/]")
        config = run_interactive_config()

        # Ask for config filename
        console.print("\n[bold cyan]Configuration File:[/]")
        default_filename = "tree_of_life_config.yaml"
        config_filename = Prompt.ask(
            "Enter filename to save configuration",
            default=default_filename
        )

        save_config_to_yaml(config, config_filename)

        # Create Tree of Life object
        tree = create_tree_from_config(config)

        # Ask if the user wants to render now
        if Confirm.ask("\nRender the Tree of Life now?", default=True):
            render_tree(tree, config, args.display, config_filename)

    elif not os.path.exists(args.config_file):
        # Non-existent config file - run interactive mode and save to specified file
        console.print(
            f"[bold yellow]Config file not found:[/] [cyan]{args.config_file}[/]")
        console.print(
            "[bold blue]Running in interactive configuration mode[/]")

        config = run_interactive_config()
        save_config_to_yaml(config, args.config_file)

        # Create Tree of Life object
        tree = create_tree_from_config(config)

        # Ask if the user wants to render now
        if Confirm.ask("\nRender the Tree of Life now?", default=True):
            render_tree(tree, config, args.display, args.config_file)

    else:
        # Existing config file - load and render
        console.print(
            f"[bold blue]Loading configuration from:[/] [cyan]{args.config_file}[/]")

        config = load_config_from_yaml(args.config_file)

        # Create Tree of Life object
        tree = create_tree_from_config(config)

        # Render the Tree of Life
        render_tree(tree, config, args.display, args.config_file)


if __name__ == "__main__":
    main()
