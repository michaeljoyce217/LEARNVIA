#!/usr/bin/env python3
"""
Convert XML module to readable text format
"""
import xml.etree.ElementTree as ET
import re
from pathlib import Path


def strip_xml_tags(text):
    """Remove XML tags but preserve content"""
    if not text:
        return ""
    # Remove XML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode common HTML entities
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    text = text.replace('&apos;', "'")
    return text


def parse_xml_module(xml_path):
    """Parse XML module and extract readable text"""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    output_lines = []

    # Try to extract the main content
    # This will vary depending on XML structure, so we'll be flexible

    def extract_text(element, indent=0):
        """Recursively extract text from XML elements"""
        prefix = "  " * indent

        # Get element tag name (without namespace)
        tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag

        # Get text content
        text = (element.text or "").strip()
        tail = (element.tail or "").strip()

        # Add element text if present
        if text:
            output_lines.append(f"{prefix}{text}")

        # Process children
        for child in element:
            extract_text(child, indent)

        # Add tail text if present
        if tail:
            output_lines.append(f"{prefix}{tail}")

    # Extract all text
    extract_text(root)

    # Join and clean up
    content = "\n".join(output_lines)

    # Clean up excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)

    return content


def main():
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python3 convert_xml_to_text.py <input_xml> <output_txt>")
        sys.exit(1)
    
    xml_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    print(f"Converting {xml_path.name} to readable text...")

    content = parse_xml_module(xml_path)

    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Converted to: {output_path}")
    print(f"  Length: {len(content)} characters")
    print(f"  Lines: {len(content.splitlines())}")


if __name__ == "__main__":
    main()
