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
from typing import Dict, Any, Optional, Tuple, List

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text

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


def main() -> None:
    """Main function for the Tree of Life Generator CLI tool."""
    # Parse command-line arguments
    args = parse_arguments()

    # Display the banner
    display_banner()

    # TO DO:
    # 1. Check if a config file was provided and exists
    # 2. If no config or non-existent file, run interactive configuration
    # 3. If existing config file, load and render
    # 4. In all cases, validate with TreeOfLife object

    console.print("\n[bold yellow]Not yet fully implemented![/] Stay tuned...",
                  justify="center")


if __name__ == "__main__":
    main()
