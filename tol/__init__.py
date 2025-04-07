"""
Tree of Life Package

This package provides classes and utilities for creating, manipulating,
and rendering the Kabbalistic Tree of Life diagram.
"""

# Import TreeOfLife class and ColorScheme enum to expose at package level
from .TreeOfLife import TreeOfLife, ColorScheme, Sephirah, Path
from .color_utils import (
    ColorEffect, ColorParser, apply_color_effect,
    apply_path_effect, blend_colors, get_contrasting_text_color
)

# Define what's accessible when doing "from tol import *"
__all__ = [
    'TreeOfLife',
    'ColorScheme',
    'Sephirah',
    'Path',
    'ColorEffect',
    'ColorParser',
    'apply_color_effect',
    'apply_path_effect',
    'blend_colors',
    'get_contrasting_text_color'
]
