# Kabbalistic Tree of Life Visualization

This project creates a visualization of the Kabbalistic Tree of Life using Python, networkx, and matplotlib.

## Description

The Kabbalistic Tree of Life is a diagram used in Kabbalah that represents the process of divine creation and the human journey to enlightenment. It consists of 10 nodes (Sephiroth) connected by 22 paths, organized in a specific pattern that represents different spiritual concepts.

This visualization includes:

- The 10 Sephiroth with their traditional names and colors
- The 22 connecting paths
- The three pillars (Mercy, Severity, and Balance)
- The four worlds (Atziluth, Briah, Yetzirah, and Assiah)

## Requirements

- Python 3.6+
- matplotlib
- networkx
- numpy

## Installation

1. Clone this repository or download the files
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the script to generate and display the Tree of Life visualization:

```bash
python tree_of_life.py
```

By default, the visualization will be displayed on screen and saved as `tree_of_life.png` in the current directory.

## Customization

You can modify the `TreeOfLife` class to customize various aspects of the visualization:

- Change the colors of the Sephiroth in the `sephiroth_colors` dictionary
- Adjust the positions in the `positions` dictionary
- Modify the paths in the `paths` list
- Customize the display by changing parameters in the `draw` method

## License

This project is open source and available for educational and personal use.

## References

- The Tree of Life structure is based on traditional Kabbalistic diagrams
- Colors and naming conventions follow common Hermetic and Western esoteric traditions
