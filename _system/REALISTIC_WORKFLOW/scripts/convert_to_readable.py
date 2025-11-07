#!/usr/bin/env python3
"""
Convert module content to human-readable format
Handles both XML and plain text, replacing visual elements with placeholders
"""
import re
from pathlib import Path


def xml_to_readable(content: str) -> str:
    """Convert XML content to human-readable text"""

    # Replace image tags with placeholder
    content = re.sub(r'<[Ii]mage[^>]*>.*?</[Ii]mage>', '[IMAGE]', content, flags=re.DOTALL)
    content = re.sub(r'<[Ii]mage[^>]*/>', '[IMAGE]', content)

    # Replace animation/video tags with placeholder
    content = re.sub(r'<[Aa]nimation[^>]*>.*?</[Aa]nimation>', '[ANIMATION]', content, flags=re.DOTALL)
    content = re.sub(r'<[Aa]nimation[^>]*/>', '[ANIMATION]', content)
    content = re.sub(r'<[Vv]ideo[^>]*>.*?</[Vv]ideo>', '[VIDEO]', content, flags=re.DOTALL)

    # Replace figure tags with placeholder
    content = re.sub(r'<[Ff]igure[^>]*>.*?</[Ff]igure>', '[FIGURE]', content, flags=re.DOTALL)

    # Replace common XML structural tags with readable text
    content = re.sub(r'<Module[^>]*>', '=== MODULE START ===\n', content)
    content = re.sub(r'</Module>', '\n=== MODULE END ===', content)

    content = re.sub(r'<title>', '\nTITLE: ', content)
    content = re.sub(r'</title>', '\n', content)

    content = re.sub(r'<description>', '\nDESCRIPTION: ', content)
    content = re.sub(r'</description>', '\n', content)

    # Math tags - preserve content but mark clearly
    content = re.sub(r'<m>', ' $', content)
    content = re.sub(r'</m>', '$ ', content)
    content = re.sub(r'<me>', '\n$$', content)
    content = re.sub(r'</me>', '$$\n', content)

    # Paragraph tags
    content = re.sub(r'<p>', '\n', content)
    content = re.sub(r'</p>', '\n', content)

    # List tags
    content = re.sub(r'<ul[^>]*>', '\n', content)
    content = re.sub(r'</ul>', '\n', content)
    content = re.sub(r'<ol[^>]*>', '\n', content)
    content = re.sub(r'</ol>', '\n', content)
    content = re.sub(r'<li>', '\n  • ', content)
    content = re.sub(r'</li>', '', content)

    # Remove all other XML tags but keep their content
    content = re.sub(r'<[^>]+>', ' ', content)

    # Clean up whitespace
    content = re.sub(r' +', ' ', content)  # Multiple spaces to single
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)  # Multiple newlines to double
    content = content.strip()

    return content


def process_module_content(file_path: Path) -> str:
    """Process module file and return human-readable content"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Detect if XML or plain text
    if file_path.suffix == '.xml' or content.strip().startswith('<'):
        return xml_to_readable(content)
    else:
        # Already plain text, just replace visual placeholders
        content = re.sub(r'\[IMAGE:.*?\]', '[IMAGE]', content)
        content = re.sub(r'\[ANIMATION:.*?\]', '[ANIMATION]', content)
        return content


if __name__ == "__main__":
    # Test with derivatives module
    input_path = Path("/Users/michaeljoyce/Desktop/LEARNVIA/REALISTIC_WORKFLOW/input/real_derivatives_module.txt")

    readable = process_module_content(input_path)

    output_path = input_path.parent / "derivatives_readable.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(readable)

    print(f"✓ Converted to readable format")
    print(f"  Input: {len(open(input_path).read())} chars")
    print(f"  Output: {len(readable)} chars")
    print(f"  Saved to: {output_path}")
