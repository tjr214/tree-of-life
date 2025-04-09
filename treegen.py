#!/usr/bin/env python
"""
Tree of Life Generator - Command Line Utility
---------------------------------------------

A CLI tool to configure, save, load, and render Tree of Life visualizations.
This tool provides a rich, interactive interface for working with the TreeOfLife class.

Features:
- Interactive configuration with colorful prompts and tables
- Save/load configurations as YAML files
- Render visualizations to PNG files or display on screen
- Multiple operation modes based on command-line arguments
- Comprehensive validation of all Tree of Life parameters
- Graceful handling of keyboard interrupts (Ctrl+C) and EOF signals (Ctrl+D)

Usage:
    # Display help screen
    ./treegen.py
    
    # Interactive configuration mode (prompts for saving location)
    ./treegen.py --new
    
    # Interactive configuration mode (saves to specified file)
    ./treegen.py --new my_config.yaml
    
    # Load existing configuration and render
    ./treegen.py existing_config.yaml
    
    # Load existing configuration and display instead of saving
    ./treegen.py existing_config.yaml --display
"""

import os
import sys
import argparse
import yaml
import signal
from typing import Dict, Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt
from rich.table import Table
from rich.text import Text
from rich import print as rprint
from rich.columns import Columns
from rich.box import ROUNDED

from tol import TreeOfLife, ColorScheme


# Initialize Rich console
console = Console()


def handle_exit(signal_received=None, frame=None) -> None:
    """
    Handles clean exit when the user presses Ctrl+C or Ctrl+D.

    Args:
        signal_received: Signal that triggered this handler (if called from signal handler)
        frame: Current stack frame (if called from signal handler)
    """
    console.print(
        "\n[bold yellow]Program interrupted by user. Exiting gracefully...[/]")
    sys.exit(0)


def display_banner() -> None:
    """
    Display an 80s/90s style ASCII art banner for the application.

    This function creates a visually appealing header with the application name
    using ASCII art and Rich library styling features including colors and panels.
    """
    # ASCII art created with FIGlet (font: slant)
    banner = r"""
     _____                        __     __ _  __                                     
    /__   \_ __ ___  ___    ___  / _|   / /(_)/ _| ___                                
      / /\/ '__/ _ \/ _ \  / _ \| |_   / / | | |_ / _ \                               
     / /  | | |  __/  __/ | (_) |  _| / /__| |  _|  __/                               
     \/   |_|  \___|\___|  \___/|_|   \____/_|_|  \___|                               
                                                                                  
      _____                                ___                          _             
      \_   \_ __ ___   __ _  __ _  ___    / _ \___ _ __   ___ _ __ __ _| |_ ___  _ __ 
       / /\/ '_ ` _ \ / _` |/ _` |/ _ \  / /_\/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
    /\/ /_ | | | | | | (_| | (_| |  __/ / /_\\  __/ | | |  __/ | | (_| | || (_) | |   
    \____/ |_| |_| |_|\__,_|\__, |\___| \____/\___|_| |_|\___|_|  \__,_|\__\___/|_|   
                            |___/                                                     
    """

    # Display the banner with a colorful panel
    console.print(Panel(
        Text(banner, style="bold bright_magenta"),
        border_style="bright_cyan",
        title="[bold bright_yellow]Tree of Life Image Generator[/]",
        subtitle="[italic bright_green]Interactive CLI Tool[/]"
    ))


def display_help_screen() -> None:
    """
    Display a colorful help screen with emojis explaining how to use the program.

    This function creates an engaging, user-friendly guide to the Tree of Life Generator
    using rich formatting, colors, and emojis for a positive user experience.
    """
    # Display the banner first
    display_banner()

    # Main title
    console.print(
        "\n[bold cyan]✨ Welcome to the Tree of Life Image Generator! ✨[/]\n")

    # Introduction
    intro_text = (
        "This tool helps you create beautiful Tree of Life visualizations with "
        "customizable colors, text, and rendering options. Here's how to use it:"
    )
    console.print(Panel(intro_text, border_style="green", expand=False))

    # Create a table for command examples
    commands_table = Table(
        title="🚀 Command Examples",
        box=ROUNDED,
        title_style="bold yellow",
        border_style="bright_blue",
        highlight=True,
        header_style="bold cyan"
    )

    # Define the columns
    commands_table.add_column("Command", style="cyan")
    commands_table.add_column("Description", style="green")
    commands_table.add_column("✨", justify="center")

    # Add rows with examples
    commands_table.add_row(
        "./treegen.py --new",
        "Start interactive configuration mode",
        "🧙"
    )
    commands_table.add_row(
        "./treegen.py --new my_config.yaml",
        "Create new configuration and save to file",
        "💾"
    )
    commands_table.add_row(
        "./treegen.py existing_config.yaml",
        "Load and render a saved configuration",
        "🎨"
    )
    commands_table.add_row(
        "./treegen.py existing_config.yaml --display",
        "Load configuration and display (don't save)",
        "🖼️"
    )
    commands_table.add_row(
        "./treegen.py -h",
        "Show this help screen",
        "❓"
    )

    # Display the command examples table
    console.print(commands_table)

    # Create feature highlights panels
    features = [
        (
            "✨ Interactive Configuration",
            "Step-by-step process with colorful prompts to create your perfect visualization"
        ),
        (
            "🎨 Multiple Color Schemes",
            "Choose from traditional color scales for Sephiroth and paths"
        ),
        (
            "🔤 Text Display Options",
            "Show numbers, Hebrew names, trigrams, or planetary symbols"
        ),
        (
            "🔍 Focus Mode",
            "Zoom in on a specific Sephirah to highlight its connections"
        ),
        (
            "💾 Save & Load",
            "Store your configurations as YAML files for future use"
        )
    ]

    # Convert features to panels
    feature_panels = []
    for title, desc in features:
        feature_panels.append(
            Panel(
                desc,
                title=title,
                border_style="magenta",
                title_align="left"
            )
        )

    # Display features in columns
    console.print(Columns(feature_panels, equal=True, expand=True))

    # Footer with get started tip
    console.print(
        "\n[bold green]💫 Get Started:[/] Run [cyan]./treegen.py --new[/] to create your first Tree of Life visualization!"
    )
    console.print(
        "[dim]For more information about the Tree of Life in Kabbalah, visit https://en.wikipedia.org/wiki/Tree_of_life_(Kabbalah)[/]"
    )


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the application.

    Returns:
        argparse.Namespace: Parsed command-line arguments with the following attributes:
            - config_file: Optional path to a YAML configuration file
            - display: Boolean flag indicating whether to display the visualization
            - new: Boolean flag indicating whether to start a new configuration
    """
    parser = argparse.ArgumentParser(
        description="Tree of Life visualization generator",
        epilog="Run without arguments for a helpful guide",
        add_help=False  # We'll provide our own help
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

    parser.add_argument(
        "--new",
        action="store_true",
        help="Start interactive mode to create a new configuration"
    )

    parser.add_argument(
        "-h", "--help",
        action="store_true",
        help="Show this help message and exit"
    )

    return parser.parse_args()


def run_interactive_config() -> Dict[str, Any]:
    """
    Run interactive configuration prompts to configure a Tree of Life visualization.

    This function presents a series of user-friendly prompts for configuring all
    aspects of the Tree of Life, organized into logical sections:
    - Basic parameters (scale and spacing)
    - Color schemes (for Sephiroth and paths)
    - Text display options (mode and visibility)
    - Rendering options (focus, size, quality, title)

    Each section includes helpful explanations and tables where appropriate.

    Returns:
        Dict[str, Any]: Nested configuration dictionary with all TreeOfLife parameters
        structured in sections for basic, color schemes, text display, and rendering.

    Note:
        Handles EOFError and KeyboardInterrupt for graceful exit.
    """
    config = {
        "basic": {},
        "color_schemes": {},
        "text_display": {},
        "rendering": {}
    }

    console.print("\n[bold cyan]===== Tree of Life Configuration =====[/]")
    console.print("[dim]Enter values or press Enter for defaults[/]")

    try:
        # --- Basic Parameters Section ---
        console.print("\n[bold green]Basic Parameters:[/]")

        config["basic"]["sphere_scale_factor"] = FloatPrompt.ask(
            "Sphere scale factor [cyan](controls size of Sephiroth)[/]",
            default=1.75
        )

        config["basic"]["spacing_factor"] = FloatPrompt.ask(
            "Spacing factor [cyan](controls distance between Sephiroth)[/]",
            default=1.5
        )

        # --- Color Schemes Section ---
        console.print("\n[bold green]Color Schemes:[/]")

        # Create color scheme choices table for visual clarity
        scheme_table = Table(title="Available Color Schemes")
        scheme_table.add_column("Number", justify="center", style="cyan")
        scheme_table.add_column("Scheme Name", style="green")
        scheme_table.add_column("Description", style="yellow")

        # Define available color schemes with descriptions
        schemes = [
            (1, "PLAIN", "Simple default colors"),
            (2, "KING_SCALE", "Elemental/planetary associations in Atziluth"),
            (3, "QUEEN_SCALE", "Elemental/planetary associations in Briah"),
            (4, "PRINCE_SCALE", "Elemental/planetary associations in Yetzirah"),
            (5, "PRINCESS_SCALE", "Elemental/planetary associations in Assiah")
        ]

        # Populate the table with color scheme information
        for num, name, desc in schemes:
            scheme_table.add_row(str(num), name, desc)

        # Display the color scheme table
        console.print(scheme_table)

        # Prompt for Sephiroth color scheme selection
        sephiroth_scheme = IntPrompt.ask(
            "Sephiroth color scheme (1-5)",
            default=2,  # KING_SCALE as default
            choices=[str(i) for i in range(1, 6)]
        )
        config["color_schemes"]["sephiroth"] = schemes[sephiroth_scheme-1][1]

        # Prompt for Path color scheme selection
        path_scheme = IntPrompt.ask(
            "Path color scheme (1-5)",
            default=2,  # KING_SCALE as default
            choices=[str(i) for i in range(1, 6)]
        )
        config["color_schemes"]["path"] = schemes[path_scheme-1][1]

        # --- Text Display Options Section ---
        console.print("\n[bold green]Text Display Options:[/]")

        # Create text mode choices table for visual clarity
        text_mode_table = Table(title="Sephiroth Text Display Modes")
        text_mode_table.add_column("Number", justify="center", style="cyan")
        text_mode_table.add_column("Mode", style="green")
        text_mode_table.add_column("Description", style="yellow")

        # Define available text modes with descriptions
        text_modes = [
            (1, "NUMBER", "Traditional enumeration (1-10)"),
            (2, "TRIGRAM", "I Ching trigrams corresponding to each Sephirah"),
            (3, "HEBREW", "Hebrew names of the Sephiroth"),
            (4, "PLANET", "Planetary symbols corresponding to each Sephirah")
        ]

        # Populate the table with text mode information
        for num, name, desc in text_modes:
            text_mode_table.add_row(str(num), name, desc)

        # Display the text mode table
        console.print(text_mode_table)

        # Prompt for text display mode selection
        text_mode = IntPrompt.ask(
            "Sephiroth text mode (1-4)",
            default=1,  # NUMBER as default
            choices=[str(i) for i in range(1, 5)]
        )
        config["text_display"]["sephiroth_mode"] = text_modes[text_mode-1][1]

        # Prompt for text visibility settings
        config["text_display"]["sephiroth_visible"] = Confirm.ask(
            "Show Sephiroth text?",
            default=True
        )

        config["text_display"]["path_visible"] = Confirm.ask(
            "Show Path text and symbols?",
            default=True
        )

        # --- Rendering Options Section ---
        console.print("\n[bold green]Rendering Options:[/]")

        # Prompt for focus Sephirah setting
        focus_choice = Confirm.ask(
            "Focus on a specific Sephirah?",
            default=False
        )

        if focus_choice:
            # Display list of Sephiroth names for selection
            sephiroth_names = [
                "1: Kether", "2: Chokmah", "3: Binah", "4: Chesed", "5: Geburah",
                "6: Tiphereth", "7: Netzach", "8: Hod", "9: Yesod", "10: Malkuth"
            ]

            for name in sephiroth_names:
                console.print(f"  [cyan]{name}[/]")

            # Prompt for specific Sephirah to focus on
            focus_num = IntPrompt.ask(
                "Enter Sephirah number to focus on (1-10)",
                default=6,  # Tiphereth (central Sephirah) as default
                choices=[str(i) for i in range(1, 11)]
            )
            config["rendering"]["focus_sephirah"] = focus_num
        else:
            config["rendering"]["focus_sephirah"] = None

        # Prompt for figure size dimensions
        console.print("[dim]Figure size in inches (width, height)[/]")
        width = FloatPrompt.ask("Width", default=7.5)  # Default width
        # Default height (letter paper)
        height = FloatPrompt.ask("Height", default=11.0)
        config["rendering"]["figsize"] = [width, height]

        # Prompt for DPI (image quality)
        config["rendering"]["dpi"] = IntPrompt.ask(
            "DPI (dots per inch) [cyan](higher = better quality, larger file)[/]",
            default=300  # Standard print quality
        )

        # Prompt for title display
        config["rendering"]["show_title"] = Confirm.ask(
            "Show title on the diagram?",
            default=False
        )

    except (KeyboardInterrupt, EOFError):
        handle_exit()

    return config


def save_config_to_yaml(config: Dict[str, Any], filename: str) -> None:
    """
    Save configuration dictionary to a YAML file with descriptive comments.

    Args:
        config: Configuration dictionary with TreeOfLife parameters.
        filename: Path to save the YAML file.

    The function ensures the target directory exists and adds helpful
    header comments to the YAML file.
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
    Load configuration from a YAML file with error handling.

    Args:
        filename: Path to the YAML configuration file.

    Returns:
        Dict[str, Any]: Configuration dictionary with TreeOfLife parameters.

    Raises:
        SystemExit: If there is an error loading the configuration file.
    """
    try:
        # Open and parse the YAML file
        with open(filename, 'r') as file:
            config = yaml.safe_load(file)

        # Confirm successful load to user
        console.print(
            f"\n[bold green]Loaded configuration from:[/] [cyan]{filename}[/]")
        return config
    except Exception as e:
        # Handle any errors (file not found, parse errors, etc.)
        console.print(f"[bold red]Error loading configuration:[/] {e}")
        sys.exit(1)


def create_tree_from_config(config: Dict[str, Any]) -> TreeOfLife:
    """
    Create a TreeOfLife object from configuration dictionary.

    This function maps configuration dictionary values to the appropriate
    TreeOfLife parameters and method calls.

    Args:
        config: Configuration dictionary with TreeOfLife parameters.

    Returns:
        TreeOfLife: Configured TreeOfLife object ready for rendering.

    Raises:
        SystemExit: If there is an error creating the TreeOfLife object.
    """
    try:
        # Create Tree of Life with basic parameters
        tree = TreeOfLife(
            sphere_scale_factor=config["basic"]["sphere_scale_factor"],
            spacing_factor=config["basic"]["spacing_factor"]
        )

        # Set color schemes by looking up enum values from string names
        sephiroth_scheme = getattr(
            ColorScheme, config["color_schemes"]["sephiroth"])
        path_scheme = getattr(ColorScheme, config["color_schemes"]["path"])

        tree.set_sephiroth_color_scheme(sephiroth_scheme)
        tree.set_path_color_scheme(path_scheme)

        # Set text display options by looking up enum values from string names
        sephiroth_mode = getattr(
            tree.SephirothTextMode, config["text_display"]["sephiroth_mode"])
        tree.set_sephiroth_text_mode(sephiroth_mode)

        # Set visibility options
        tree.set_sephiroth_text_visibility(
            config["text_display"]["sephiroth_visible"])
        tree.set_path_text_visibility(config["text_display"]["path_visible"])

        return tree
    except Exception as e:
        # Handle any errors during TreeOfLife creation
        console.print(f"[bold red]Error creating Tree of Life:[/] {e}")
        sys.exit(1)


def render_tree(tree: TreeOfLife, config: Dict[str, Any], display: bool, config_filename: Optional[str] = None) -> None:
    """
    Render the Tree of Life visualization to a file or display it on screen.

    This function handles the final rendering step, setting up appropriate filenames
    based on the configuration and handling either display or file output.

    Args:
        tree: Configured TreeOfLife object.
        config: Configuration dictionary with rendering parameters.
        display: Whether to display the visualization instead of saving to file.
        config_filename: Optional name of the config file, used as base for output filename.

    Raises:
        SystemExit: If there is an error during rendering.
    """
    # Extract rendering parameters from configuration
    focus_sephirah = config["rendering"]["focus_sephirah"]
    figsize = tuple(config["rendering"]["figsize"])
    dpi = config["rendering"]["dpi"]
    show_title = config["rendering"]["show_title"]

    # Generate output filename if not displaying
    if not display:
        if config_filename:
            # Use the config filename base for the output file (intelligent naming)
            base_name = os.path.splitext(os.path.basename(config_filename))[0]

            # Determine suffix based on configuration
            if focus_sephirah:
                # List of Sephiroth names for filename generation
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
                # Use color schemes in filename if no focus
                seph_scheme = config["color_schemes"]["sephiroth"]
                path_scheme = config["color_schemes"]["path"]
                output_file = f"tree_{seph_scheme.lower()}_{path_scheme.lower()}.png"
    else:
        # No output file if displaying
        output_file = None

    # Show rendering information to user
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
        # Call the TreeOfLife render method with appropriate parameters
        tree.render(
            focus_sephirah=focus_sephirah,
            display=display,
            save_to_file=output_file,
            figsize=figsize,
            dpi=dpi,
            show_title=show_title
        )

        # Confirm successful save if not displaying
        if not display:
            console.print(
                f"\n[bold green]Visualization saved to:[/] [cyan]{output_file}[/]")
    except Exception as e:
        # Handle rendering errors
        console.print(f"[bold red]Error rendering Tree of Life:[/] {e}")
        sys.exit(1)


def main() -> None:
    """
    Main function for the Tree of Life Generator CLI tool.

    This function implements the core workflow of the application:
    1. Parse command-line arguments
    2. Determine mode of operation:
       - Display help screen (no arguments or --help)
       - Interactive configuration (--new flag)
       - Load and render (existing config file)
    3. Create TreeOfLife object and render visualization when applicable

    The function handles keyboard interrupts (Ctrl+C) and EOF signals (Ctrl+D)
    gracefully, ensuring a clean exit with a friendly message.
    """
    # Set up signal handler for keyboard interrupts (Ctrl+C)
    signal.signal(signal.SIGINT, handle_exit)

    try:
        # Parse command-line arguments
        args = parse_arguments()

        # Determine mode of operation based on arguments

        # Show help screen if no arguments or help flag
        if args.help or (args.config_file is None and not args.new):
            display_help_screen()
            sys.exit(0)

        # Display the banner for non-help operations
        display_banner()

        # Handle interactive mode with --new flag
        if args.new:
            console.print(
                "[bold blue]Running in interactive configuration mode[/]")

            # Run interactive configuration
            config = run_interactive_config()

            # Determine where to save the config
            if args.config_file:
                config_filename = args.config_file
            else:
                # Ask for config filename to save
                console.print("\n[bold cyan]Configuration File:[/]")
                default_filename = "tree_of_life_config.yaml"
                try:
                    config_filename = Prompt.ask(
                        "Enter filename to save configuration",
                        default=default_filename
                    )
                except (KeyboardInterrupt, EOFError):
                    handle_exit()

            # Save configuration to file
            save_config_to_yaml(config, config_filename)

            # Create Tree of Life object
            tree = create_tree_from_config(config)

            # Ask if the user wants to render now
            try:
                if Confirm.ask("\nRender the Tree of Life now?", default=True):
                    render_tree(tree, config, args.display, config_filename)
            except (KeyboardInterrupt, EOFError):
                handle_exit()

        # Handle existing config file (with or without --display)
        elif args.config_file and os.path.exists(args.config_file):
            console.print(
                f"[bold blue]Loading configuration from:[/] [cyan]{args.config_file}[/]")

            # Load configuration from file
            config = load_config_from_yaml(args.config_file)

            # Create Tree of Life object
            tree = create_tree_from_config(config)

            # Render the Tree of Life
            render_tree(tree, config, args.display, args.config_file)

        # Handle non-existent config file (without --new)
        elif args.config_file:
            console.print(
                f"[bold yellow]Config file not found:[/] [cyan]{args.config_file}[/]")
            console.print(
                "[yellow]Use --new flag to create a new configuration.[/]")
            console.print(
                "[yellow]Run without arguments to see help screen.[/]")
            sys.exit(1)

    except (KeyboardInterrupt, EOFError):
        handle_exit()
    except Exception as e:
        console.print(f"\n[bold red]An unexpected error occurred:[/] {e}")
        sys.exit(1)


# Entry point when script is run directly
if __name__ == "__main__":
    main()
