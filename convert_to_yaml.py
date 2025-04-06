#!/usr/bin/env python3
import re
import yaml
from typing import Dict, Any, List


def extract_color(text: str) -> str:
    """Extract hex color code from text."""
    match = re.search(r'#([A-Fa-f0-9]{6})', text)
    if match:
        return f"#{match.group(1)}"
    return "#FFFFFF"  # Default to white if no color found


def extract_effects(text: str) -> Dict[str, Any]:
    """Extract special effects (flecked, rayed, tinged) from text."""
    effects = {}

    # Check for flecked effect
    flecked_match = re.search(r'flecked\s+(.*?)(\s+with|\s+\(|\s*$)', text)
    if flecked_match:
        effects['type'] = 'flecked'
        effects['color2'] = flecked_match.group(1).strip()

        # Look for second color hex
        if "with" in text:
            second_part = text.split("with")[1]
            second_color = extract_color(second_part)
            if second_color != "#FFFFFF":  # If a color was found
                effects['color2_hex'] = second_color

    # Check for rayed effect
    rayed_match = re.search(r'rayed\s+(.*?)(\s+with|\s+\(|\s*$)', text)
    if rayed_match:
        effects['type'] = 'rayed'
        effects['color2'] = rayed_match.group(1).strip()

        # Look for second color hex
        if "with" in text:
            second_part = text.split("with")[1]
            second_color = extract_color(second_part)
            if second_color != "#FFFFFF":  # If a color was found
                effects['color2_hex'] = second_color

    # Check for tinged effect
    tinged_match = re.search(r'tinged\s+(.*?)(\s+with|\s+\(|\s*$)', text)
    if tinged_match:
        effects['type'] = 'tinged'
        effects['color2'] = tinged_match.group(1).strip()

    return effects if effects else None


def convert_md_to_yaml(md_file: str, yaml_file: str) -> None:
    """Convert color_scales.md to YAML format."""
    with open(md_file, 'r') as f:
        content = f.read()

    # Initialize result dictionary
    result = {
        'king_scale': {'sephiroth': {}, 'paths': {}},
        'queen_scale': {'sephiroth': {}, 'paths': {}},
        'prince_scale': {'sephiroth': {}, 'paths': {}},
        'princess_scale': {'sephiroth': {}, 'paths': {}}
    }

    # Split content by scale sections
    sections = content.split('# ')[1:]  # Skip the first empty section

    for section in sections:
        lines = section.strip().split('\n')
        scale_name = lines[0].lower().replace(' ', '_')

        if scale_name not in result:
            continue  # Skip unexpected sections

        # Find the sephiroth and paths subsections
        sephiroth_idx = -1
        paths_idx = -1

        for i, line in enumerate(lines):
            if "## The " in line and "Sephiroth" in line:
                sephiroth_idx = i
            elif "## The " in line and "Paths" in line:
                paths_idx = i

        # Parse Sephiroth
        if sephiroth_idx >= 0:
            end_idx = paths_idx if paths_idx > sephiroth_idx else len(lines)
            sephiroth_lines = lines[sephiroth_idx+1:end_idx]

            for line in sephiroth_lines:
                line = line.strip()
                if not line or line.startswith('##') or not line.startswith('-'):
                    continue

                # Extract sephirah data
                seph_match = re.match(
                    r'-\s+(\d+|Daath),\s+(\w+)\s+=\s+(.*)', line)
                if seph_match:
                    num_str, name, desc = seph_match.groups()

                    # Handle special case for Da'ath
                    if num_str == "Daath":
                        num = 0  # Use 0 for Da'ath
                    else:
                        num = int(num_str)

                    # Extract color and effects
                    color = extract_color(desc)
                    effects = extract_effects(desc)

                    # Store the result
                    result[scale_name]['sephiroth'][num] = {
                        'name': name,
                        'color': color,
                        'effects': effects
                    }

        # Parse Paths
        if paths_idx >= 0:
            path_lines = lines[paths_idx+1:]

            for line in path_lines:
                line = line.strip()
                if not line or line.startswith('##') or not line.startswith('-'):
                    continue

                # Extract path data
                path_match = re.match(r'-\s+(\d+)\s+=\s+(.*)', line)
                if path_match:
                    num_str, desc = path_match.groups()
                    num = int(num_str)

                    # Extract color and effects
                    color = extract_color(desc)
                    effects = extract_effects(desc)

                    # Store the result
                    result[scale_name]['paths'][num] = {
                        'color': color,
                        'effects': effects
                    }

    # Write the result to YAML file
    with open(yaml_file, 'w') as f:
        yaml.dump(result, f, default_flow_style=False, sort_keys=False)

    print(f"Converted {md_file} to {yaml_file}")


if __name__ == '__main__':
    convert_md_to_yaml('color_scales.md', 'color_scales.yaml')
