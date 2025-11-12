#!/usr/bin/env python3
"""
Strip animation code from module content to focus on pedagogical text
"""
from pathlib import Path
import re


def strip_animation_code(content: str) -> str:
    """Remove animation code blocks while preserving pedagogical content"""

    lines = content.split('\n')
    cleaned_lines = []
    in_animation_block = False
    skip_line = False

    for i, line in enumerate(lines):
        # Check for base64/encoded animation blocks
        if line.strip().startswith('CgovLy') or 'Canvas(windows:' in line:
            in_animation_block = True
            continue

        # Check for animation script blocks
        if any(marker in line for marker in ['Scene()', 'Animate()', 'Init(', 'Question(id:']):
            in_animation_block = True
            continue

        # Check for end of animation block (usually ==)
        if in_animation_block and line.strip() == '==':
            in_animation_block = False
            continue

        # Skip lines that are clearly animation code
        if any(marker in line for marker in [
            'play("https://',
            '.show(',
            '.hide(',
            'wait(',
            '.position.',
            '.opacity',
            '.color.blend',
            'Rule(Vec2',
            'Text(content:',
            'Image(source:',
            'blocking:',
            'duration:',
            'window:',
        ]):
            continue

        # Skip if we're inside an animation block
        if in_animation_block:
            continue

        # Keep this line
        cleaned_lines.append(line)

    # Join lines back together
    cleaned = '\n'.join(cleaned_lines)

    # Clean up excessive whitespace
    cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)

    return cleaned


def main():
    input_path = Path("/Users/michaeljoyce/Desktop/LEARNVIA/modules/module_3.5_readable.txt")
    output_path = Path("/Users/michaeljoyce/Desktop/LEARNVIA/modules/module_3.5_pedagogical_only.txt")

    print(f"Reading {input_path.name}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_lines = len(content.splitlines())
    original_chars = len(content)

    print(f"Stripping animation code...")
    cleaned = strip_animation_code(content)

    cleaned_lines = len(cleaned.splitlines())
    cleaned_chars = len(cleaned)

    print(f"Saving to {output_path.name}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)

    print(f"\n✓ Animation code stripped successfully!")
    print(f"  Original: {original_lines} lines, {original_chars} characters")
    print(f"  Cleaned:  {cleaned_lines} lines, {cleaned_chars} characters")
    print(f"  Removed:  {original_lines - cleaned_lines} lines ({100*(original_lines-cleaned_lines)/original_lines:.1f}%)")


if __name__ == "__main__":
    main()
