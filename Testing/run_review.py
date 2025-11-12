#!/usr/bin/env python3
"""
30-Agent Content Review System - Generic Rule-Based Version

This script simulates the multi-agent content review process using rule-based detection
instead of hardcoded findings. It can work on ANY module by applying pattern matching
based on the style and authoring guides.

⚠️ CRITICAL: INPUT FILES MUST NEVER BE MODIFIED ⚠️
- This script is READ-ONLY for input XML and readable text files
- ALL writes go to the output/ subdirectory only
- The "Original Input" tab in HTML reports MUST show the source faithfully
- Any text extraction is for ANALYSIS only, never for replacement

Usage:
  python run_review.py <module_folder> <xml_file>

Example:
  python run_review.py Power_Series power_series_original.xml
  python run_review.py Fund_Thm_of_Calculus module_5_6.xml
"""

import xml.etree.ElementTree as ET
import json
import re
import math
import html as html_module
import random
import hashlib
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any, Tuple

# Base configuration paths (config is shared across all reviews)
LEARNVIA_PATH = Path("/Users/michaeljoyce/Desktop/LEARNVIA")
CONFIG_PATH = LEARNVIA_PATH / "config"
PROMPTS_PATH = CONFIG_PATH / "prompts"
RUBRICS_PATH = CONFIG_PATH / "rubrics"
TESTING_PATH = LEARNVIA_PATH / "Testing"

# Module-specific paths set by command-line arguments
TEST_MODULE_PATH = None
OUTPUT_PATH = None

# Agent configuration based on agent_configuration.xml
AGENT_CONFIG = {
    "authoring": {
        "total": 15,
        "rubric_focused": 9,  # 60%
        "generalist": 6,  # 40%
        "competencies": [
            "Pedagogical Flow",
            "Structural Integrity",
            "Student Engagement",
            "Conceptual Clarity",
            "Assessment Quality"
        ]
    },
    "style": {
        "total": 15,
        "rubric_focused": 9,  # 60%
        "generalist": 6,  # 40%
        "competencies": [
            "Mechanical Compliance",
            "Mathematical Formatting",
            "Punctuation & Grammar",
            "Accessibility",
            "Consistency"
        ]
    }
}


def load_prompt_file(filename: str) -> str:
    """Load a prompt file from the prompts directory."""
    filepath = PROMPTS_PATH / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def load_rubric_file(filename: str) -> str:
    """Load a rubric XML file from the rubrics directory."""
    filepath = RUBRICS_PATH / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def load_module_content(filepath: Path) -> str:
    """Load the module content to be reviewed."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def extract_text_from_module(xml_content: str) -> str:
    """Extract human-readable text from module XML for line-based review, PRESERVING <m> and <me> LaTeX tags."""
    lines = []
    try:
        root = ET.fromstring(xml_content)

        # Extract text recursively, preserving <m> and <me> tags
        def extract_text_with_latex(element):
            """Recursively extract text, preserving <m> and <me> tags as strings."""
            result = element.text or ''

            for child in element:
                # Preserve LaTeX tags
                if child.tag in ['m', 'me']:
                    result += f'<{child.tag}>'
                    result += (child.text or '')
                    result += f'</{child.tag}>'
                else:
                    # Recursively process other elements
                    result += extract_text_with_latex(child)

                # Add tail text
                result += (child.tail or '')

            return result

        # Extract all text content
        full_text = extract_text_with_latex(root)

        # Normalize whitespace WITHIN LaTeX tags (keep them on one line)
        # Replace newlines inside <m> and <me> tags with spaces
        def normalize_latex_tags(text):
            import re
            # Match <m>...</m> and <me>...</me> including content with newlines
            def replace_newlines(match):
                return match.group(0).replace('\n', ' ')

            text = re.sub(r'<m>.*?</m>', replace_newlines, text, flags=re.DOTALL)
            text = re.sub(r'<me>.*?</me>', replace_newlines, text, flags=re.DOTALL)
            return text

        full_text = normalize_latex_tags(full_text)

        # Split into lines
        lines = [line.strip() for line in full_text.split('\n') if line.strip()]

    except ET.ParseError as e:
        print(f"Warning: XML parsing error: {e}")
        # Fallback: preserve <m> and <me> tags but strip others
        # First, protect <m> and <me> tags
        protected = xml_content.replace('<m>', '___M_START___').replace('</m>', '___M_END___')
        protected = protected.replace('<me>', '___ME_START___').replace('</me>', '___ME_END___')

        # Strip all other XML tags
        cleaned = re.sub(r'<[^>]+>', '', protected)

        # Restore protected tags
        cleaned = cleaned.replace('___M_START___', '<m>').replace('___M_END___', '</m>')
        cleaned = cleaned.replace('___ME_START___', '<me>').replace('___ME_END___', '</me>')

        # Clean up entities
        cleaned = cleaned.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')\
                         .replace('&quot;', '"').replace('&apos;', "'")

        # Normalize excessive blank lines
        cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)
        lines = [line.strip() for line in cleaned.split('\n') if line.strip()]

    # Prefix each line with a 1-indexed line number to make agent references precise
    numbered_lines = [f"{i+1:04d}| {line}" for i, line in enumerate(lines)]
    return '\n'.join(numbered_lines)


def build_agent_prompt(agent_type: str, agent_focus: str, exemplar_anchors: str,
                       master_prompt: str, domain_prompt: str, rubric_content: str,
                       module_content: str) -> str:
    """Build the complete prompt for a single agent."""

    prompt = f"""# AGENT IDENTITY
You are Agent {agent_focus} in a {agent_type} review team.
Type: {"Rubric-Focused Specialist" if rubric_content else "Generalist Cross-Cutting Reviewer"}

# IMPORTANT: XML PROMPTS & HUMAN-READABLE OUTPUT
You will receive XML-structured prompts and module content. The XML structure helps you parse sections clearly.
HOWEVER: When presenting findings to humans (in JSON output and reports), use clear, readable prose.
Your findings will be displayed to authors - they need actionable feedback, not XML fragments.

# LAYERED INSTRUCTIONS

## Layer 0: Exemplar Anchors (Reference Only)
Use these exemplars and few-shot issues to calibrate judgments. Do not flag patterns that match these exemplars. Prefer fixes that align to their style and structure.
{exemplar_anchors}

## Layer 1: Universal Review Context
{master_prompt}

## Layer 2: Domain-Specific Guidelines
{domain_prompt}
"""

    if rubric_content:
        prompt += f"""
## Layer 3: Rubric Competency Focus
{rubric_content}

Your PRIMARY focus is evaluating against this rubric, but you may flag other issues you observe.
"""
    else:
        prompt += """
## Layer 3: Generalist Role
As a generalist, you review holistically across all competencies. Look for cross-cutting issues,
patterns that span categories, and problems that specialist reviewers might miss by being too focused.
"""

    prompt += f"""

# MODULE TO REVIEW (line-numbered)

{module_content}

# OUTPUT FORMAT

Provide your findings as a JSON array of issues:

[
  {{
    "issue_description": "Specific issue with exact line numbers and quoted text",
    "line_numbers": [10, 11, 12],
    "quoted_text": "The exact problematic text from the module",
    "category": "Pedagogical Flow|Structural Integrity|Conceptual Clarity|Assessment Quality|Mechanical Compliance|Mathematical Formatting|Punctuation & Grammar|Accessibility|Consistency|Other",
    "severity": 1-5,
    "student_impact": "How this affects student learning",
    "suggested_fix": "Concrete actionable remedy",
    "confidence": 0.0-1.0
  }}
]

CRITICAL REQUIREMENTS:
1. Every issue MUST include specific line numbers (refer to the prefixed numbers like "0042|")
2. Every issue MUST include quoted text from the module
3. Be specific, not vague (e.g., "Line 0042: 'some students' should specify which students")
4. Focus on learning impact, not nitpicking
5. If no issues found, return empty array: []
"""

    return prompt


class RuleBasedDetector:
    """Generic rule-based issue detector that works on any module."""

    def __init__(self, module_text: str, agent_type: str, agent_id: str):
        self.lines = module_text.split('\n')
        self.agent_type = agent_type
        self.agent_id = agent_id

        # Per-agent deterministic variability
        seed = int(hashlib.md5(agent_id.encode("utf-8")).hexdigest()[:8], 16)
        self.rng = random.Random(seed)

    def should_flag(self, severity: int) -> bool:
        """Determine if agent should flag issue based on severity."""
        probability_map = {
            5: 0.90,  # 90% of agents catch critical issues
            4: 0.80,  # 80% of agents catch major issues
            3: 0.60,  # 60% of agents catch moderate issues
            2: 0.40,  # 40% of agents catch minor issues
            1: 0.20   # 20% of agents catch trivial issues
        }
        return self.rng.random() < probability_map.get(severity, 0.5)

    def extract_line_content(self, line_index: int) -> str:
        """Extract content from a line by index (removes line number prefix)."""
        if 0 <= line_index < len(self.lines):
            line = self.lines[line_index]
            # Remove line number prefix (e.g., "0042| ")
            if '|' in line:
                return line.split('|', 1)[1].strip()
        return ""

    def get_line_number(self, line: str) -> int:
        """Extract line number from numbered line."""
        if '|' in line:
            try:
                return int(line.split('|')[0].strip())
            except:
                pass
        return 0

    def detect_todo_placeholders(self) -> List[Dict[str, Any]]:
        """Detect Todo placeholders (UNFINISHED content markers)."""
        findings = []

        for i, line in enumerate(self.lines):
            content = self.extract_line_content(i)
            line_num = self.get_line_number(line)

            # Check for Todo/TODO/todo in various contexts
            if re.search(r'\btodo\b', content, re.IGNORECASE):
                if self.should_flag(3):  # Severity 3 for unfinished content
                    # Determine what type of Todo it is
                    if '<Title>' in content:
                        suggested_fix = "Provide a descriptive title for the module"
                    elif '<Description>' in content:
                        suggested_fix = "Write a clear description of what students will learn"
                    elif '<KSAs>' in content:
                        suggested_fix = "List the Knowledge, Skills, and Abilities required"
                    elif '<LearningOutcomes>' in content:
                        suggested_fix = "Define specific, measurable learning outcomes"
                    else:
                        suggested_fix = "Replace placeholder with actual content"

                    findings.append({
                        "issue_description": f"UNFINISHED - Line {line_num}: Contains 'Todo' placeholder",
                        "line_numbers": [line_num],
                        "quoted_text": content,
                        "category": "UNFINISHED",
                        "severity": 3,
                        "student_impact": "Placeholder indicates unfinished content that students will see",
                        "suggested_fix": suggested_fix,
                        "confidence": 1.0
                    })

        return findings

    def detect_contractions(self) -> List[Dict[str, Any]]:
        """Detect contractions (what's, let's, don't, etc.)."""
        findings = []

        # Common contractions to detect
        contractions = {
            r"\bwhat's\b": "what is",
            r"\blet's\b": "let us",
            r"\bdon't\b": "do not",
            r"\bdoesn't\b": "does not",
            r"\bwon't\b": "will not",
            r"\bcan't\b": "cannot",
            r"\bisn't\b": "is not",
            r"\baren't\b": "are not",
            r"\bwasn't\b": "was not",
            r"\bweren't\b": "were not",
            r"\bhasn't\b": "has not",
            r"\bhaven't\b": "have not",
            r"\bhadn't\b": "had not",
            r"\bwouldn't\b": "would not",
            r"\bcouldn't\b": "could not",
            r"\bshouldn't\b": "should not",
            r"\bit's\b": "it is",  # But need to distinguish from possessive "its"
            r"\bthat's\b": "that is",
            r"\bthere's\b": "there is",
            r"\bhere's\b": "here is",
        }

        for i, line in enumerate(self.lines):
            content = self.extract_line_content(i)
            line_num = self.get_line_number(line)

            for pattern, replacement in contractions.items():
                matches = list(re.finditer(pattern, content, re.IGNORECASE))
                for match in matches:
                    # Special case: "it's" vs "its" - only flag if followed by not a possessive context
                    if pattern == r"\bit's\b":
                        # Check if it's likely possessive (followed by a noun)
                        after_text = content[match.end():].strip()
                        if after_text and after_text[0].islower():
                            continue  # Skip if likely possessive

                    if self.should_flag(2):  # Severity 2 for style violations
                        findings.append({
                            "issue_description": f"Line {line_num}: Contraction '{match.group()}' should be avoided",
                            "line_numbers": [line_num],
                            "quoted_text": content[max(0, match.start()-20):min(len(content), match.end()+20)],
                            "category": "Mechanical Compliance",
                            "severity": 2,
                            "student_impact": "Contractions reduce formality and may confuse ESL learners",
                            "suggested_fix": f"Replace '{match.group()}' with '{replacement}'",
                            "confidence": 0.85
                        })

        return findings

    def detect_passive_voice(self) -> List[Dict[str, Any]]:
        """Detect passive voice constructions (is/was/are/were + past participle)."""
        findings = []

        # Common passive voice patterns
        passive_patterns = [
            # "is/are/was/were + past participle"
            r'\b(is|are|was|were)\s+(\w+ed|found|given|known|shown|seen|made|done|written|taken)\b',
            # "has/have/had been + past participle"
            r'\b(has|have|had)\s+been\s+(\w+ed|found|given|known|shown|seen|made|done|written|taken)\b',
            # "being + past participle"
            r'\bbeing\s+(\w+ed|found|given|known|shown|seen|made|done|written|taken)\b',
            # Common passive constructions
            r'\bit\s+is\s+(\w+ed|found|essential|important|necessary|required)\b',
        ]

        for i, line in enumerate(self.lines):
            content = self.extract_line_content(i)
            line_num = self.get_line_number(line)

            for pattern in passive_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    passive_phrase = match.group()
                    # Skip if inside LaTeX tags
                    if self.is_in_math(content, match.start()):
                        continue

                    severity = 2  # Moderate issue for style
                    if self.should_flag(severity):
                        findings.append({
                            "issue_description": f"Passive voice construction: '{passive_phrase}'",
                            "line_numbers": [line_num],
                            "quoted_text": content[max(0, match.start()-20):min(len(content), match.end()+20)],
                            "category": "Mechanical Compliance",
                            "severity": severity,
                            "student_impact": "Active voice is clearer and more direct for struggling readers",
                            "suggested_fix": f"Rewrite in active voice. Instead of '{passive_phrase}', specify who/what performs the action",
                            "confidence": 0.75
                        })
                        break  # One finding per line

        return findings

    def detect_imperative_in_hints(self) -> List[Dict[str, Any]]:
        """Detect imperative voice in hints (commands like 'Use', 'Try', 'Remember')."""
        findings = []

        # Imperative verbs commonly found at start of sentences
        imperative_verbs = [
            'Use', 'Try', 'Remember', 'Consider', 'Apply', 'Calculate', 'Find',
            'Determine', 'Check', 'Verify', 'Look', 'Think', 'Recall', 'Note',
            'Make', 'Take', 'Choose', 'Select', 'Compare', 'Evaluate', 'Start',
            'Begin', 'Write', 'Draw', 'Sketch', 'Plot', 'Solve', 'Substitute'
        ]

        in_hint = False
        hint_content = []
        hint_start_line = None

        for i, line in enumerate(self.lines):
            content = self.extract_line_content(i)
            line_num = self.get_line_number(line)

            # Check if we're entering or exiting a hint
            if '<hint>' in line or '<Hint>' in line:
                in_hint = True
                hint_start_line = line_num
                hint_content = []
            elif '</hint>' in line or '</Hint>' in line:
                in_hint = False
                # Check the complete hint content
                full_hint = ' '.join(hint_content)
                for verb in imperative_verbs:
                    if re.search(rf'\b{verb}\b', full_hint):
                        severity = 3  # Higher severity for hint issues
                        if self.should_flag(severity):
                            findings.append({
                                "issue_description": f"Hint uses imperative voice (command): starts with '{verb}'",
                                "line_numbers": [hint_start_line],
                                "quoted_text": full_hint[:100] + "..." if len(full_hint) > 100 else full_hint,
                                "category": "Student Engagement",
                                "severity": severity,
                                "student_impact": "Hints should guide thinking, not give commands. Commands can feel patronizing",
                                "suggested_fix": f"Rephrase as a question or observation. Instead of '{verb}...', try 'What happens if...' or 'Notice that...'",
                                "confidence": 0.80
                            })
                            break
            elif in_hint:
                hint_content.append(content)

        return findings

    def detect_interval_notation_issues(self) -> List[Dict[str, Any]]:
        """Detect inconsistent interval notation (using < > instead of interval notation)."""
        findings = []

        # Pattern for inequality chains that should be interval notation
        inequality_patterns = [
            # "a < x < b" or "a ≤ x ≤ b" patterns
            r'(-?\d+\.?\d*)\s*(<|≤|<=)\s*\w+\s*(<|≤|<=)\s*(-?\d+\.?\d*)',
            # "x > a and x < b" patterns
            r'\w+\s*[<>]=?\s*(-?\d+\.?\d*)\s+and\s+\w+\s*[<>]=?\s*(-?\d+\.?\d*)',
        ]

        for i, line in enumerate(self.lines):
            content = self.extract_line_content(i)
            line_num = self.get_line_number(line)

            for pattern in inequality_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    inequality = match.group()

                    # Skip if already in LaTeX tags
                    if '<m>' in line and '</m>' in line:
                        # Check if this inequality is inside math tags
                        math_start = content.find('<m>')
                        math_end = content.find('</m>')
                        if math_start < match.start() < math_end:
                            continue

                    severity = 2
                    if self.should_flag(severity):
                        # Determine appropriate interval notation
                        if '<' in inequality and '≤' not in inequality and '<=' not in inequality:
                            suggestion = "open interval notation like (a, b)"
                        elif '≤' in inequality or '<=' in inequality:
                            suggestion = "closed interval notation like [a, b]"
                        else:
                            suggestion = "appropriate interval notation"

                        findings.append({
                            "issue_description": f"Inequality chain should use interval notation: '{inequality}'",
                            "line_numbers": [line_num],
                            "quoted_text": content[max(0, match.start()-20):min(len(content), match.end()+20)],
                            "category": "Mathematical Formatting",
                            "severity": severity,
                            "student_impact": "Interval notation is standard in calculus and clearer for expressing ranges",
                            "suggested_fix": f"Replace '{inequality}' with {suggestion}",
                            "confidence": 0.70
                        })
                        break

        return findings

    def is_in_math(self, content: str, position: int) -> bool:
        """Check if a position in content is inside LaTeX math tags."""
        # Find all math tag positions
        for match in re.finditer(r'<m[e]?>.*?</m[e]?>', content, re.DOTALL):
            if match.start() <= position <= match.end():
                return True
        return False

    def detect_vague_pronouns(self) -> List[Dict[str, Any]]:
        """Detect vague pronoun usage (it, this, they without clear antecedent)."""
        findings = []

        vague_patterns = [
            (r'^(It|This)\s+', "Sentence starts with vague pronoun"),
            (r'\.\s+(It|This)\s+', "Sentence starts with vague pronoun after period"),
            (r'\bthey\b', "Use of 'they' pronoun"),
            (r'\bit\s+(is|was|has|can|will|should|could|would|may|might)\b', "Vague 'it' reference"),
        ]

        for i, line in enumerate(self.lines):
            content = self.extract_line_content(i)
            line_num = self.get_line_number(line)

            for pattern, description in vague_patterns:
                matches = list(re.finditer(pattern, content, re.IGNORECASE))
                for match in matches:
                    if self.should_flag(2):  # Severity 2
                        findings.append({
                            "issue_description": f"Line {line_num}: {description} - '{match.group()}'",
                            "line_numbers": [line_num],
                            "quoted_text": content[max(0, match.start()-20):min(len(content), match.end()+40)],
                            "category": "Conceptual Clarity",
                            "severity": 2,
                            "student_impact": "Vague pronouns increase cognitive load for struggling readers",
                            "suggested_fix": "Replace with explicit noun reference",
                            "confidence": 0.70
                        })

        return findings

    def detect_missing_latex(self) -> List[Dict[str, Any]]:
        """
        Detect mathematical notation not wrapped in LaTeX tags.

        REFINED APPROACH (reduces false positives):
        - HIGH PRIORITY (Severity 3): Display-context math (equations, formulas, complex expressions)
        - LOW PRIORITY (Severity 1): Inline symbols in prose (often acceptable without LaTeX)
        - SKIP: Arrows and simple symbols commonly used in narrative text
        """
        findings = []

        # HIGH PRIORITY: Display-context math patterns (Severity 3)
        # These should definitely use LaTeX for proper formatting
        display_math_patterns = [
            (r'\b[a-zA-Z]\s*=\s*[-+]?\d+', "Variable assignment without LaTeX"),
            (r'\b(lim|sin|cos|tan|log|ln|exp)\s*\(', "Mathematical function without LaTeX"),
            (r'[a-zA-Z]_\d+', "Subscript notation without LaTeX"),
            (r'\^\{?[0-9n+\-]+\}?', "Superscript notation without LaTeX"),
            (r'\d+\s*/\s*\d+', "Fraction without LaTeX"),
            (r'∑|∏|∫', "Summation/product/integral symbol without LaTeX"),
        ]

        # LOW PRIORITY: Inline symbols (Severity 1)
        # These are often acceptable in prose but could be improved
        inline_symbol_patterns = [
            (r'[≈≤≥≠±∓√∞]', "Mathematical symbol in prose"),
        ]

        for i, line in enumerate(self.lines):
            content = self.extract_line_content(i)
            line_num = self.get_line_number(line)

            # Skip if line already has LaTeX tags (<m> or <me>)
            if '<m>' in content or '<me>' in content or '</m>' in content or '</me>' in content:
                continue

            # Check display-context patterns (HIGH PRIORITY)
            for pattern, description in display_math_patterns:
                matches = list(re.finditer(pattern, content))
                for match in matches:
                    if self.should_flag(3):  # Severity 3 (was 2)
                        findings.append({
                            "issue_description": f"Line {line_num}: {description}",
                            "line_numbers": [line_num],
                            "quoted_text": content[max(0, match.start()-10):min(len(content), match.end()+10)],
                            "category": "Mathematical Formatting",
                            "severity": 3,
                            "student_impact": "Mathematical expressions without LaTeX may not render consistently across devices",
                            "suggested_fix": f"Wrap in <m>...</m> tags for consistent rendering",
                            "confidence": 0.80
                        })

            # Check inline symbols (LOW PRIORITY) - only flag occasionally
            # These are acceptable in prose, so we flag at low severity and low confidence
            for pattern, description in inline_symbol_patterns:
                matches = list(re.finditer(pattern, content))
                for match in matches:
                    # Only flag 30% of the time (reduce noise)
                    if self.should_flag(1) and random.random() < 0.3:
                        findings.append({
                            "issue_description": f"Line {line_num}: {description}",
                            "line_numbers": [line_num],
                            "quoted_text": content[max(0, match.start()-10):min(len(content), match.end()+10)],
                            "category": "Mathematical Formatting",
                            "severity": 1,
                            "student_impact": "Inline symbols are generally acceptable but LaTeX improves consistency",
                            "suggested_fix": f"Consider wrapping in <m>...</m> tags if symbol is central to the concept",
                            "confidence": 0.50
                        })

        return findings

    def detect_lazy_starts(self) -> List[Dict[str, Any]]:
        """Detect 'There is/are' lazy sentence starts."""
        findings = []

        lazy_patterns = [
            r'^There\s+(is|are|was|were)\s+',
            r'\.\s+There\s+(is|are|was|were)\s+',
        ]

        for i, line in enumerate(self.lines):
            content = self.extract_line_content(i)
            line_num = self.get_line_number(line)

            for pattern in lazy_patterns:
                matches = list(re.finditer(pattern, content, re.IGNORECASE))
                for match in matches:
                    if self.should_flag(1):  # Severity 1 (low)
                        findings.append({
                            "issue_description": f"Line {line_num}: Lazy start with '{match.group().strip()}'",
                            "line_numbers": [line_num],
                            "quoted_text": content[match.start():min(len(content), match.end()+30)],
                            "category": "Conceptual Clarity",
                            "severity": 1,
                            "student_impact": "Less direct phrasing adds cognitive load",
                            "suggested_fix": "Start with the actual subject of the sentence",
                            "confidence": 0.60
                        })

        return findings

    def detect_complex_sentences(self) -> List[Dict[str, Any]]:
        """Detect overly complex sentence structures - ANALYZES SENTENCES, NOT LINES."""
        findings = []

        for i, line in enumerate(self.lines):
            content = self.extract_line_content(i)
            line_num = self.get_line_number(line)

            # CRITICAL: Split line into sentences first
            # Be careful with periods in math notation (e.g., "2.5" or "<m>...</m>")
            # Split on ". " followed by capital letter or end of string
            sentences = re.split(r'\.\s+(?=[A-Z]|$)', content)

            for sentence_idx, sentence in enumerate(sentences):
                sentence = sentence.strip()
                if not sentence or len(sentence) < 20:  # Skip very short fragments
                    continue

                # Check for multiple clauses (indicated by multiple commas)
                # IMPORTANT: Exclude commas inside mathematical expressions and mathematical objects
                # 1. Remove LaTeX tags and their contents
                text_without_math = re.sub(r'<m>.*?</m>', ' ', sentence, flags=re.DOTALL)
                text_without_math = re.sub(r'<me>.*?</me>', ' ', text_without_math, flags=re.DOTALL)

                # 2. Remove commas inside parentheses, brackets, and angle brackets (mathematical notation)
                # These are intervals like (-2, 3), coordinates like (x, y), function args, etc.
                text_without_math = re.sub(r'\([^)]*\)', ' ', text_without_math)  # Remove (...)
                text_without_math = re.sub(r'\[[^\]]*\]', ' ', text_without_math)  # Remove [...]
                text_without_math = re.sub(r'<[^>]*>', ' ', text_without_math)    # Remove <...>
                text_without_math = re.sub(r'\{[^}]*\}', ' ', text_without_math)  # Remove {...}

                # 3. Exclude serial comma patterns (lists like "A, B, and C" or "one, both, or neither")
                # These are normal lists, not complex sentences
                # Pattern: word, word, (and|or) word
                text_without_math = re.sub(r'\w+\s*,\s*\w+\s*,\s*(and|or)\s+\w+', ' ', text_without_math)
                # Also handle longer lists: word, word, word, (and|or) word
                text_without_math = re.sub(r'(\w+\s*,\s*){2,}\s*(and|or)\s+\w+', ' ', text_without_math)

                comma_count = text_without_math.count(',')
                # Flag INDIVIDUAL SENTENCES with 4+ commas (indicating multiple subordinate clauses)
                if comma_count >= 4:
                    if self.should_flag(1):
                        findings.append({
                            "issue_description": f"Line {line_num}: Complex sentence with {comma_count} commas",
                            "line_numbers": [line_num],
                            "quoted_text": sentence[:100] + "..." if len(sentence) > 100 else sentence,
                            "category": "Conceptual Clarity",
                            "severity": 1,
                            "student_impact": "Complex sentences with multiple clauses are harder for struggling readers",
                            "suggested_fix": "Break into simpler sentences with fewer subordinate clauses",
                            "confidence": 0.65
                        })
                        break  # Only flag the line once, even if multiple sentences are complex

            # Check for semicolons (discouraged)
            if ';' in content:
                if self.should_flag(1):
                    findings.append({
                        "issue_description": f"Line {line_num}: Semicolon usage discouraged",
                        "line_numbers": [line_num],
                        "quoted_text": content,
                        "category": "Punctuation & Grammar",
                        "severity": 1,
                        "student_impact": "Semicolons increase complexity for mobile readers",
                        "suggested_fix": "Split into two sentences or use comma with conjunction",
                        "confidence": 0.65
                    })

        return findings

    def detect_missing_definitions(self) -> List[Dict[str, Any]]:
        """
        Detect technical terms used without definition tags.
        Uses frequency-based heuristic: frequent terms are likely module-specific (Severity 4),
        infrequent terms are likely prerequisites (Severity 2).
        """
        findings = []

        # Infer module topic to avoid flagging the main subject
        module_topic_terms = set()
        early_content = ' '.join(self.lines[:10]).lower()

        # Extract key terms from early content (likely the module's main topic)
        if 'power series' in early_content:
            module_topic_terms.update(['power series', 'series'])
        if 'taylor series' in early_content or 'maclaurin' in early_content:
            module_topic_terms.update(['taylor series', 'series'])
        if 'convergence' in early_content:
            module_topic_terms.add('convergence')
        if 'integral' in early_content and 'improper' in early_content:
            module_topic_terms.update(['improper integral', 'integral'])

        # CALC 2 BASIC VOCABULARY: Fundamental concepts taught at start of Calc 2
        # These are universal vocabulary terms, not tests or specific techniques
        calc2_vocabulary = [
            r'\bconvergence\b', r'\bconverges\b', r'\bconvergent\b',
            r'\bdivergence\b', r'\bdiverges\b', r'\bdivergent\b',
            r'\bsequence\b', r'\bsequences\b',
            r'\bseries\b',  # General term (not specific types like "power series")
            r'\bterm\b', r'\bterms\b',  # As in "terms of a series"
            r'\bpartial sum\b', r'\bpartial sums\b',
            r'\binfinite series\b',
            r'\bfinite sum\b',
        ]

        # EARLY CALC 2: Basic series concepts and first convergence tests (Chapters 1-3)
        # These are typically covered BEFORE most modules - don't flag them
        early_calc2_fundamentals = [
            r'\balternating series test\b',
            r'\bp-series\b',
            r'\bgeometric series\b',
            r'\bharmonic series\b',
            r'\btelescoping series\b',
            r'\bnth term test\b',
            r'\bdivergence test\b',
        ]

        # MID CALC 2: Advanced convergence tests and techniques (Chapters 3-5)
        # Flag these ONLY if module is clearly about earlier topics
        mid_calc2_terms = [
            r'\b(ratio test|root test|integral test|comparison test|limit comparison test)\b',
            r'\b(integration by parts|partial fractions|trigonometric substitution)\b',
            r'\bimproper integral\b',
        ]

        # LATE CALC 2: Power/Taylor series (Chapters 5-7)
        # Flag these as module-specific if not defined
        calc2_compound_terms = [
            r'\b(radius of convergence|interval of convergence)\b',
            r'\b(power series|taylor series|maclaurin series)\b',
            r'\btaylor polynomial\b',
        ]

        # CALC 1 FUNDAMENTALS: Never flag these (universal prerequisites from Calculus 1)
        calc1_fundamentals = [
            r'\blimit\b', r'\bderivative\b', r'\bintegral\b', r'\bfunction\b',
            r'\bcontinuous\b', r'\bdifferentiable\b', r'\bantiderivative\b',
            r'\btangent line\b', r'\bsecant line\b', r'\brate of change\b',
            r'\bcritical point\b', r'\bmaximum\b', r'\bminimum\b',
            r'\bconcave up\b', r'\bconcave down\b', r'\binflection point\b',
            r'\bdefinite integral\b', r'\bindefinite integral\b', r'\briemann sum\b',
            r'\barea under.{0,10}curve\b', r'\bsubstitution\b',
            r'\bchain rule\b', r'\bproduct rule\b', r'\bquotient rule\b', r'\bpower rule\b',
        ]

        # PRE-CALCULUS FUNDAMENTALS: Basic terms taught before Calculus - don't flag these
        foundational_patterns = [
            r'\bvariable\b', r'\bequation\b', r'\bexpression\b', r'\bgraph\b',
            r'\breal number\b', r'\bcomplex number\b', r'\bpolynomial\b',
            r'\bcoefficient\b', r'\bterm\b', r'\bnumber\b', r'\binterval\b',
            r'\bdomain\b', r'\brange\b', r'\bslope\b', r'\bintercept\b',
            r'\bexponential\b', r'\blogarithm\b', r'\btrigonometric\b',
            r'\bsine\b', r'\bcosine\b', r'\btangent\b',
        ]

        # Track defined terms (both formal and informal definitions)
        defined_terms = set()
        for i, line in enumerate(self.lines):
            content = self.extract_line_content(i)

            # Formal definitions: <definition><b>Term</b> is...</definition>
            if '<definition>' in content:
                match = re.search(r'<b>([^<]+)</b>', content)
                if match:
                    defined_terms.add(match.group(1).lower())

            # Informal definitions: Recognize natural ways of introducing/defining technical terms
            # These patterns catch definitions that don't use formal <definition> tags
            content_lower = content.lower()

            # Patterns to run on lowercase content
            lowercase_patterns = [
                # Explicit definition statements
                r'([a-z\s]+)\s+is\s+defined\s+(?:as|to\s+be)',  # "X is defined as/to be"
                r'([a-z\s]+),\s+defined\s+as',  # "X, defined as"

                # "Call/called" statements
                r'call(?:ed)?\s+(?:this|it)\s+the\s+([a-z\s]+)',  # "we call this the X" or "called the X"
                r'(?:is|are)\s+called\s+the\s+([a-z\s]+)',  # "is called the X"

                # "This/It" referential definitions (after introducing a term)
                r'this\s+(?:is|defines|represents|denotes)\s+(?:the\s+)?([a-z\s]+)',  # "this is/represents the X"
                r'it\s+(?:is|defines|represents|denotes)\s+(?:the\s+)?([a-z\s]+)',  # "it represents the X"

                # Direct "X is" statements (simple explanatory statements)
                r'the\s+([a-z\s]+)\s+is\s+(?:then|simply|just|always|never)',  # "the X is then..."
            ]

            # Patterns to run on original content (case-sensitive)
            original_patterns = [
                # Appositive constructions: "the radius of convergence, R. This represents..."
                r'the\s+([a-z\s]+),\s+[A-Z]',  # Capital letter after comma suggests explanation/definition
            ]

            # Process lowercase patterns
            for pattern in lowercase_patterns:
                matches = re.finditer(pattern, content_lower)
                for match in matches:
                    term = match.group(1).strip()
                    # Only capture multi-word technical phrases (2+ words)
                    # Exclude generic phrases
                    if len(term.split()) >= 2 and not term.startswith(('the distance', 'the center', 'the value')):
                        defined_terms.add(term)

            # Process original content patterns (case-sensitive)
            for pattern in original_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    term = match.group(1).strip().lower()  # Normalize to lowercase for storage
                    if len(term.split()) >= 2 and not term.startswith(('the distance', 'the center', 'the value')):
                        defined_terms.add(term)

        # Collect occurrences of Calc 2 compound terms (mid and late only)
        term_occurrences = {}

        for i, line in enumerate(self.lines):
            content = self.extract_line_content(i)
            line_num = self.get_line_number(line)

            # Check mid and late Calc 2 terms
            all_patterns = mid_calc2_terms + calc2_compound_terms
            for pattern in all_patterns:
                matches = list(re.finditer(pattern, content, re.IGNORECASE))
                for match in matches:
                    term = match.group().lower()

                    # Skip if already defined
                    if term in defined_terms:
                        continue

                    # Skip if it's the module's main topic
                    if term in module_topic_terms:
                        continue

                    # Skip if it's a Calc 1 fundamental
                    is_calc1 = False
                    for calc1_pattern in calc1_fundamentals:
                        if re.fullmatch(calc1_pattern, term, re.IGNORECASE):
                            is_calc1 = True
                            break
                    if is_calc1:
                        continue

                    # Skip if it's a basic foundational term
                    is_foundational = False
                    for found_pattern in foundational_patterns:
                        if re.fullmatch(found_pattern, term, re.IGNORECASE):
                            is_foundational = True
                            break
                    if is_foundational:
                        continue

                    # Skip if it's basic Calc 2 vocabulary (convergence, divergence, sequence, series, etc.)
                    # These are foundational concepts taught at the very beginning of Calc 2
                    is_calc2_vocab = False
                    for vocab_pattern in calc2_vocabulary:
                        if re.fullmatch(vocab_pattern, term, re.IGNORECASE):
                            is_calc2_vocab = True
                            break
                    if is_calc2_vocab:
                        continue

                    # Skip if it's an early Calc 2 fundamental (alternating series test, p-series, etc.)
                    # These are typically covered before most modules
                    is_early_calc2 = False
                    for early_pattern in early_calc2_fundamentals:
                        if re.fullmatch(early_pattern, term, re.IGNORECASE):
                            is_early_calc2 = True
                            break
                    if is_early_calc2:
                        continue

                    # Collect occurrence
                    if term not in term_occurrences:
                        term_occurrences[term] = []

                    quote = content[max(0, match.start()-20):min(len(content), match.end()+20)]
                    term_occurrences[term].append({
                        'line_num': line_num,
                        'quote': quote,
                        'original_case': match.group(),
                        'line_index': i
                    })

        # Classify terms by structure, frequency, and position
        for term, occurrences in term_occurrences.items():
            frequency = len(occurrences)
            first_appearance = min(occ['line_index'] for occ in occurrences)
            line_numbers = [occ['line_num'] for occ in occurrences]
            original_case = occurrences[0]['original_case']
            first_quote = occurrences[0]['quote']

            # Count words in term (multi-word phrases are likely module-specific)
            word_count = len(term.split())

            # REFINED HEURISTIC:
            # 1. Multi-word technical phrases (e.g., "radius of convergence") → likely NEW (Severity 4)
            # 2. Single-word terms (e.g., "convergence", "limit") → likely PREREQUISITE (Severity 2)
            #    UNLESS they appear very frequently (10+ times) AND early → may need verification

            if word_count >= 2:
                # Multi-word phrase → likely module-specific concept
                severity = 4
                if self.should_flag(severity):
                    findings.append({
                        "issue_description": f"Technical term '{original_case}' appears {frequency} times but may lack clear definition. Lines: {', '.join(map(str, line_numbers[:5]))}{'...' if len(line_numbers) > 5 else ''}",
                        "line_numbers": line_numbers,
                        "quoted_text": first_quote,
                        "category": "Structural Integrity",
                        "severity": 4,
                        "student_impact": "Compound technical term is likely specific to this module. Students studying alone need explicit definitions to understand new concepts.",
                        "suggested_fix": f"Has the term '{original_case}' been defined previously in this module or a prerequisite? If not, is the explanation provided here clear and straightforward? Consider adding formal definition: <definition><b>{original_case}</b> is ...</definition>",
                        "confidence": 0.80
                    })
            else:
                # Single-word term → likely prerequisite (even if frequent)
                severity = 2
                if self.should_flag(severity):
                    findings.append({
                        "issue_description": f"Verify definition status: '{original_case}' appears {frequency} times. Used on lines: {', '.join(map(str, line_numbers[:5]))}{'...' if len(line_numbers) > 5 else ''}",
                        "line_numbers": line_numbers,
                        "quoted_text": first_quote,
                        "category": "Structural Integrity",
                        "severity": 2,
                        "student_impact": "Single-word foundational term is likely prerequisite knowledge from standard Calc 2 progression, but should be verified to ensure accessibility for all students.",
                        "suggested_fix": f"Verify: Has '{original_case}' been defined in this module or a prerequisite? If not, consider adding a brief definition or reminder of the concept.",
                        "confidence": 0.60
                    })

        return findings

    def detect_authoring_issues(self) -> List[Dict[str, Any]]:
        """Detect authoring-specific issues."""
        findings = []

        # Check for abstract before concrete
        for i in range(len(self.lines) - 1):
            content = self.extract_line_content(i)
            line_num = self.get_line_number(self.lines[i])

            # Look for abstract mathematical definitions without prior example
            if re.search(r'∑|∏|∫|lim', content) and i < 20:  # Early in module
                # Check if there's a concrete example before this
                has_example = False
                for j in range(max(0, i - 5), i):
                    prev_content = self.extract_line_content(j)
                    if 'example' in prev_content.lower() or 'consider' in prev_content.lower():
                        has_example = True
                        break

                if not has_example and self.should_flag(2):
                    findings.append({
                        "issue_description": f"Line {line_num}: Abstract definition appears before concrete example",
                        "line_numbers": [line_num],
                        "quoted_text": content[:80],
                        "category": "Pedagogical Flow",
                        "severity": 2,
                        "student_impact": "Abstract-first approach increases cognitive load",
                        "suggested_fix": "Introduce a concrete example before the abstract definition",
                        "confidence": 0.65
                    })

        # Check for missing scaffolding
        for i, line in enumerate(self.lines):
            content = self.extract_line_content(i)
            line_num = self.get_line_number(line)

            # Look for sudden jumps to complex topics
            if 'apply the ratio test' in content.lower():
                # Check if ratio test was introduced/explained
                explained = False
                for j in range(max(0, i - 10), i):
                    prev_content = self.extract_line_content(j)
                    if 'ratio test' in prev_content.lower() and ('is' in prev_content or 'helps' in prev_content):
                        explained = True
                        break

                if not explained and self.should_flag(3):
                    findings.append({
                        "issue_description": f"Line {line_num}: Jumps to applying test without explanation",
                        "line_numbers": [line_num],
                        "quoted_text": content[:80],
                        "category": "Pedagogical Flow",
                        "severity": 3,
                        "student_impact": "Students may not understand why this test is needed",
                        "suggested_fix": "Add explanation of what the test does and why we need it",
                        "confidence": 0.70
                    })

        return findings


def simulate_agent_review(agent_id: str, prompt: str) -> List[Dict[str, Any]]:
    """
    Simulate an agent review using rule-based detection.

    This replaces the hardcoded findings with generic pattern matching
    that works on any module.
    """

    # Extract module content from prompt
    # Look for the MODULE section specifically from our build_agent_prompt
    module_start = prompt.find("# MODULE TO REVIEW (line-numbered)")

    # Find the OUTPUT FORMAT section that comes AFTER the module content
    # We need to find the one that's part of our prompt, not in loaded prompts
    output_marker = "\n\n# OUTPUT FORMAT\n\nProvide your findings"
    module_end = prompt.find(output_marker, module_start)

    if module_end == -1:
        # Try alternate format
        module_end = prompt.find("\n# OUTPUT FORMAT\n", module_start)

    if module_start == -1 or module_end == -1 or module_end <= module_start:
        # Silently return empty findings if module boundaries not found
        return []

    # Extract content between markers
    module_content = prompt[module_start:module_end]
    # Skip the header lines
    lines = module_content.split('\n')
    # Find where actual content starts (after empty line)
    content_start = 0
    for i, line in enumerate(lines):
        if line.strip() == "" and i > 0:
            content_start = i + 1
            break
    module_content = '\n'.join(lines[content_start:]).strip()

    # Determine agent type from ID
    agent_type = "authoring" if "authoring" in agent_id.lower() else "style"

    # Create detector
    detector = RuleBasedDetector(module_content, agent_type, agent_id)

    findings = []

    # Apply different rules based on agent type and specialization

    # All agents can detect unfinished content
    findings.extend(detector.detect_todo_placeholders())

    if agent_type == "style":
        # Style agents focus on mechanical issues
        findings.extend(detector.detect_contractions())
        findings.extend(detector.detect_missing_latex())
        findings.extend(detector.detect_lazy_starts())
        findings.extend(detector.detect_complex_sentences())
        findings.extend(detector.detect_passive_voice())
        findings.extend(detector.detect_imperative_in_hints())
        findings.extend(detector.detect_interval_notation_issues())

        # Specialists focus on their area
        if "mechanical" in agent_id.lower():
            # Extra focus on mechanical compliance
            findings.extend(detector.detect_contractions())  # May catch more
            findings.extend(detector.detect_passive_voice())  # Mechanical issue
        elif "mathematical" in agent_id.lower():
            # Extra focus on math formatting
            findings.extend(detector.detect_missing_latex())  # May catch more
            findings.extend(detector.detect_interval_notation_issues())  # Math formatting
        elif "punctuation" in agent_id.lower():
            # Focus on punctuation issues
            findings.extend(detector.detect_complex_sentences())
            findings.extend(detector.detect_passive_voice())  # Grammar issue

    else:  # authoring agents
        # Authoring agents focus on pedagogical issues
        findings.extend(detector.detect_vague_pronouns())
        findings.extend(detector.detect_missing_definitions())
        findings.extend(detector.detect_authoring_issues())

        # Specialists focus on their area
        if "pedagogical" in agent_id.lower():
            # Extra focus on flow
            findings.extend(detector.detect_authoring_issues())  # May catch more
        elif "structural" in agent_id.lower():
            # Focus on structure
            findings.extend(detector.detect_missing_definitions())  # May catch more
        elif "conceptual" in agent_id.lower():
            # Focus on clarity
            findings.extend(detector.detect_vague_pronouns())  # May catch more

    # Generalist agents sample from all categories but with lower probability
    if "generalist" in agent_id.lower():
        # Generalists have broader but shallower coverage
        # They already got some findings above, but with their reduced probability
        pass

    # Remove duplicates (same line, same issue type)
    seen = set()
    unique_findings = []
    for finding in findings:
        key = (finding["line_numbers"][0] if finding["line_numbers"] else 0,
               finding["category"],
               finding["issue_description"][:30])
        if key not in seen:
            seen.add(key)
            unique_findings.append(finding)

    return unique_findings


def aggregate_consensus_issues(all_findings: List[Dict[str, Any]],
                                total_agents: int) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Aggregate individual agent findings into consensus issues and non-consensus flagged issues.

    Issues flagged by multiple agents get higher confidence.
    Similar issues are grouped together.

    Returns:
        (consensus_issues, non_consensus_issues)
    """

    # Group similar issues by description similarity
    issue_groups = defaultdict(list)

    for finding in all_findings:
        # Simple similarity: group by first 50 chars of description
        key = finding["issue_description"][:50]
        issue_groups[key].append(finding)

    consensus_issues = []
    non_consensus_issues = []

    for group_key, grouped_findings in issue_groups.items():
        # Take the highest confidence version as representative
        representative = max(grouped_findings, key=lambda x: x["confidence"])

        # Calculate consensus metrics
        agent_count = len(grouped_findings)
        avg_confidence = sum(f["confidence"] for f in grouped_findings) / agent_count
        max_severity = max(f["severity"] for f in grouped_findings)

        # Consensus percentage
        consensus_pct = (agent_count / total_agents)

        # Priority (1–5 scale): Consensus Tier System
        # High severity + high consensus = high priority
        if agent_count >= 20:      # Very High consensus (67%+)
            consensus_tier = 0
        elif agent_count >= 12:    # High consensus (40-66%)
            consensus_tier = -1
        elif agent_count >= 8:     # Medium consensus (27-39%)
            consensus_tier = -2
        elif agent_count >= 4:     # Low consensus (13-26%)
            consensus_tier = -3
        else:                      # Below threshold
            consensus_tier = -4

        priority = max_severity + consensus_tier
        priority = max(1, min(5, priority))  # Clamp to [1, 5]

        issue = {
            "priority": priority,
            "severity": max_severity,
            "confidence": avg_confidence,
            "consensus_percentage": consensus_pct * 100,
            "issue_description": representative["issue_description"],
            "category": representative["category"],
            "location": f"Lines {', '.join(map(str, representative['line_numbers']))}",
            "line_numbers": representative["line_numbers"],
            "quoted_text": representative["quoted_text"],
            "student_impact": representative["student_impact"],
            "suggested_fix": representative["suggested_fix"],
            "agent_count": agent_count
        }

        # Consensus threshold: at least 4 agents OR severity 5
        # Rationale: encourage more non-consensus (flagged) issues to surface
        if agent_count >= 4 or max_severity == 5:
            consensus_issues.append(issue)
        else:
            # Single/dual/tri-agent findings go to non-consensus flagged issues
            non_consensus_issues.append(issue)

    # Sort by priority (descending)
    consensus_issues.sort(key=lambda x: x["priority"], reverse=True)
    non_consensus_issues.sort(key=lambda x: x["priority"], reverse=True)

    return consensus_issues, non_consensus_issues


def generate_html_report(consensus_issues: List[Dict[str, Any]],
                         non_consensus_issues: List[Dict[str, Any]],
                         all_findings: List[Dict[str, Any]],
                         agent_config: Dict[str, Any],
                         module_content: str) -> str:
    """
    Generate comprehensive HTML report with 10-tab interface.

    Tabs:
    1. Overview - Summary statistics and priority distribution
    2. Consensus Issues - Issues with 4+ agent agreement
    3. Flagged Issues - Issues with 1-3 agents
    4. All Findings - Complete list by category
    5. Agent Breakdown - Findings by agent type
    6. Category Analysis - Grouping by authoring/style categories
    7. Original Input - Line-numbered module text
    8. Next Steps - Workflow recommendations
    9. System Architecture - Flowchart and explanation
    10. Complete Workflow - 4-pass production workflow (Reviewer & Content Editor phases)
    """

    total_agents = agent_config["authoring"]["total"] + agent_config["style"]["total"]
    num_consensus = len(consensus_issues)
    num_flagged = len(non_consensus_issues)

    # Category distribution
    authoring_categories = ["Pedagogical Flow", "Structural Integrity", "Student Engagement",
                           "Conceptual Clarity", "Assessment Quality", "UNFINISHED"]
    style_categories = ["Mechanical Compliance", "Mathematical Formatting", "Punctuation & Grammar",
                       "Accessibility", "Consistency"]

    # Count issues by category for all issues
    all_issues = consensus_issues + non_consensus_issues
    category_counts = defaultdict(int)
    for issue in all_issues:
        category_counts[issue["category"]] += 1

    # Priority distribution
    priority_counts = defaultdict(int)
    for issue in all_issues:
        priority_counts[issue["priority"]] += 1

    # Agent type breakdown
    authoring_findings = []
    style_findings = []
    for finding in all_findings:
        # Infer from category
        if finding.get("category") in authoring_categories:
            authoring_findings.append(finding)
        else:
            style_findings.append(finding)

    # Generate timestamp
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    # Convert module_content to line-numbered HTML preserving LaTeX
    def text_to_numbered_html_with_latex(text):
        """Convert line-numbered text to HTML, preserving <m> and <me> tags."""
        lines = text.split('\n')
        html_lines = []

        for line in lines:
            # Extract line number and content
            if '|' in line:
                parts = line.split('|', 1)
                line_num = parts[0].strip()
                content = parts[1] if len(parts) > 1 else ''
            else:
                line_num = ''
                content = line

            # Preserve LaTeX tags in content
            # Don't HTML-escape <m> and <me> tags
            protected = content.replace('<m>', '___LATEX_M_START___')
            protected = protected.replace('</m>', '___LATEX_M_END___')
            protected = protected.replace('<me>', '___LATEX_ME_START___')
            protected = protected.replace('</me>', '___LATEX_ME_END___')

            # HTML escape the rest
            escaped = html_module.escape(protected)

            # Restore LaTeX with dollar sign delimiters
            escaped = escaped.replace('___LATEX_M_START___', '$')
            escaped = escaped.replace('___LATEX_M_END___', '$')
            escaped = escaped.replace('___LATEX_ME_START___', '$$')
            escaped = escaped.replace('___LATEX_ME_END___', '$$')

            # Build line with number
            if line_num:
                html_lines.append(
                    f'<div style="font-family: monospace; margin: 2px 0;">'
                    f'<span style="color: #999; margin-right: 1em; user-select: none;">{line_num}</span>'
                    f'<span>{escaped}</span>'
                    f'</div>'
                )
            else:
                html_lines.append(f'<div style="font-family: monospace; margin: 2px 0;">{escaped}</div>')

        return '\n'.join(html_lines)

    # Display the EXTRACTED, LINE-NUMBERED TEXT that agents actually analyzed
    # This ensures line numbers in issues match what's shown in Original Input tab
    import html as html_escape_module

    # extract_text_from_module() ALREADY returns numbered text (0001| ..., 0002| ..., etc.)
    # So we just use it directly - don't number again!
    extracted_text_with_numbers = extract_text_from_module(module_content)

    # Split into lines and format for HTML display with LaTeX preservation
    text_lines = extracted_text_with_numbers.split('\n')
    formatted_lines = []
    for line in text_lines:
        # Each line is formatted as "0001| content"
        if '|' in line:
            parts = line.split('|', 1)
            line_num = parts[0].strip()
            content = parts[1] if len(parts) > 1 else ''
        else:
            line_num = ''
            content = line

        # Preserve LaTeX tags in content while escaping HTML
        protected = content.replace('<m>', '___LATEX_M_START___')
        protected = protected.replace('</m>', '___LATEX_M_END___')
        protected = protected.replace('<me>', '___LATEX_ME_START___')
        protected = protected.replace('</me>', '___LATEX_ME_END___')

        # HTML escape the rest
        escaped = html_escape_module.escape(protected)

        # Restore LaTeX with dollar sign delimiters
        escaped = escaped.replace('___LATEX_M_START___', '$')
        escaped = escaped.replace('___LATEX_M_END___', '$')
        escaped = escaped.replace('___LATEX_ME_START___', '$$')
        escaped = escaped.replace('___LATEX_ME_END___', '$$')

        # Format with line number
        if line_num:
            formatted_lines.append(
                f'<div style="font-family: monospace; margin: 0;">'
                f'<span style="color: #666; margin-right: 10px; user-select: none;">{line_num}</span>'
                f'<span>{escaped}</span>'
                f'</div>'
            )
        else:
            formatted_lines.append(f'<div style="font-family: monospace; margin: 0;">{escaped}</div>')

    escaped_module = '\n'.join(formatted_lines)

    # Build the HTML with 9 tabs
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LEARNVIA Content Review Report</title>

    <!-- MathJax for LaTeX rendering -->
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$']],
                displayMath: [['$$', '$$']],
                processEscapes: false
            }},
            startup: {{
                pageReady: () => {{
                    return MathJax.startup.defaultPageReady().then(() => {{
                        console.log('MathJax initial typeset starting...');
                        return MathJax.typesetPromise();
                    }}).then(() => {{
                        console.log('MathJax initial typeset complete');
                    }});
                }}
            }}
        }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.95;
        }}

        .tabs {{
            display: flex;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
            overflow-x: auto;
            white-space: nowrap;
        }}

        .tab {{
            padding: 15px 25px;
            cursor: pointer;
            background: #f8f9fa;
            border: none;
            color: #495057;
            font-weight: 600;
            transition: all 0.3s ease;
            position: relative;
            font-size: 14px;
            flex-shrink: 0;
        }}

        .tab:hover {{
            background: #e9ecef;
        }}

        .tab.active {{
            background: white;
            color: #667eea;
            border-bottom: 3px solid #667eea;
        }}

        .tab-content {{
            display: none;
            padding: 30px;
            animation: fadeIn 0.5s;
        }}

        .tab-content.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}

        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}

        .stat-card h3 {{
            color: #495057;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}

        .stat-card .value {{
            font-size: 2.5em;
            font-weight: 700;
            color: #667eea;
        }}

        .stat-card .description {{
            color: #6c757d;
            font-size: 0.9em;
            margin-top: 5px;
        }}

        .issue-card {{
            background: white;
            border: 1px solid #e9ecef;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            transition: all 0.3s ease;
        }}

        .issue-card:hover {{
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            transform: translateY(-2px);
        }}

        .issue-header {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 15px;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .priority-5 {{ background: #dc3545; color: white; }}
        .priority-4 {{ background: #fd7e14; color: white; }}
        .priority-3 {{ background: #ffc107; color: #212529; }}
        .priority-2 {{ background: #17a2b8; color: white; }}
        .priority-1 {{ background: #6c757d; color: white; }}

        .severity-5 {{ background: #c62828; color: white; }}
        .severity-4 {{ background: #e65100; color: white; }}
        .severity-3 {{ background: #f57f17; color: white; }}
        .severity-2 {{ background: #1565c0; color: white; }}
        .severity-1 {{ background: #616161; color: white; }}

        .category-badge {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        .consensus-meter {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 4px 12px;
            background: #e9ecef;
            border-radius: 20px;
            font-size: 0.85em;
        }}

        .issue-description {{
            font-size: 1.1em;
            font-weight: 600;
            color: #2c3e50;
            margin: 15px 0;
        }}

        .issue-location {{
            color: #6c757d;
            font-size: 0.95em;
            margin: 10px 0;
        }}

        .quoted-text {{
            background: #f8f9fa;
            padding: 15px;
            border-left: 3px solid #667eea;
            border-radius: 5px;
            margin: 15px 0;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            overflow-x: auto;
        }}

        .issue-impact {{
            background: #fff3cd;
            padding: 12px;
            border-radius: 5px;
            margin: 10px 0;
        }}

        .suggested-fix {{
            background: #d4edda;
            padding: 12px;
            border-radius: 5px;
            margin: 10px 0;
        }}

        .chart-container {{
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}

        .bar-chart {{
            display: flex;
            align-items: flex-end;
            justify-content: space-around;
            height: 200px;
            margin: 20px 0;
        }}

        .bar {{
            width: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 5px 5px 0 0;
            position: relative;
            transition: all 0.3s ease;
        }}

        .bar:hover {{
            transform: translateY(-5px);
        }}

        .bar-label {{
            position: absolute;
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 0.8em;
            white-space: nowrap;
        }}

        .bar-value {{
            position: absolute;
            top: -25px;
            left: 50%;
            transform: translateX(-50%);
            font-weight: bold;
            color: #667eea;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}

        th {{
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #495057;
            border-bottom: 2px solid #e9ecef;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #e9ecef;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        .original-input {{
            background: #263238;
            color: #aed581;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            overflow-x: auto;
            white-space: pre;
            line-height: 1.5;
        }}

        .line-number {{
            color: #546e7a;
            margin-right: 15px;
            user-select: none;
        }}

        .line-content {{
            color: #cfd8dc;
        }}

        .workflow-section {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}

        .workflow-step {{
            display: flex;
            align-items: center;
            margin: 15px 0;
        }}

        .step-number {{
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
        }}

        .step-content h4 {{
            color: #2c3e50;
            margin-bottom: 5px;
        }}

        .step-content p {{
            color: #6c757d;
            font-size: 0.95em;
        }}

        .flowchart {{
            text-align: center;
            padding: 30px;
            background: white;
        }}

        .flowchart-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 10px;
            display: inline-block;
            margin: 10px;
            font-weight: 600;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}

        .flowchart-arrow {{
            font-size: 2em;
            color: #667eea;
            margin: 10px 0;
        }}

        .info-box {{
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}

        .warning-box {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}

        .success-box {{
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>LEARNVIA Content Review System</h1>
            <div class="subtitle">30-Agent Multi-Perspective Analysis Report</div>
            <div class="subtitle" style="margin-top: 10px; font-size: 0.9em; opacity: 0.8;">
                Generated: {timestamp}
            </div>
        </div>

        <div class="tabs">
            <button class="tab active" onclick="showTab(event, 'overview')">Overview</button>
            <button class="tab" onclick="showTab(event, 'workflow')">Complete Workflow</button>
            <button class="tab" onclick="showTab(event, 'architecture')">System Architecture</button>
            <button class="tab" onclick="showTab(event, 'agent-breakdown')">Agent Breakdown</button>
            <button class="tab" onclick="showTab(event, 'original-input')">Original Input</button>
            <button class="tab" onclick="showTab(event, 'consensus')">Consensus Issues</button>
            <button class="tab" onclick="showTab(event, 'flagged')">Flagged Issues</button>
            <button class="tab" onclick="showTab(event, 'all-findings')">All Findings</button>
            <button class="tab" onclick="showTab(event, 'category-analysis')">Category Analysis</button>
        </div>

        <!-- Tab 1: Overview -->
        <div id="overview" class="tab-content active">
            <h2>Review Overview</h2>

            <div class="stat-grid">
                <div class="stat-card">
                    <h3>Total Agents</h3>
                    <div class="value">{total_agents}</div>
                    <div class="description">15 Authoring + 15 Style Agents</div>
                </div>

                <div class="stat-card">
                    <h3>Consensus Issues</h3>
                    <div class="value">{num_consensus}</div>
                    <div class="description">Issues flagged by 4+ agents</div>
                </div>

                <div class="stat-card">
                    <h3>Flagged Issues</h3>
                    <div class="value">{num_flagged}</div>
                    <div class="description">Issues flagged by 1-3 agents</div>
                </div>

                <div class="stat-card">
                    <h3>Total Findings</h3>
                    <div class="value">{len(all_findings)}</div>
                    <div class="description">All individual agent findings</div>
                </div>
            </div>

            <div class="chart-container">
                <h3>Priority Distribution</h3>
                <div class="bar-chart">
                    {"".join([f'''
                    <div class="bar" style="height: {(priority_counts.get(i, 0) / max(max(priority_counts.values()) if priority_counts else 0, 1)) * 100}%;">
                        <div class="bar-value">{priority_counts.get(i, 0)}</div>
                        <div class="bar-label">Priority {i}</div>
                    </div>''' for i in range(1, 6)])}
                </div>
            </div>

            <div class="info-box">
                <strong>Review Summary:</strong> This module has been analyzed by 30 specialized AI agents,
                each focusing on different aspects of content quality, pedagogy, and style compliance.
                The consensus mechanism ensures that only issues identified by multiple agents are
                marked as high-confidence findings.
            </div>
        </div>

        <!-- Tab 4: Agent Breakdown -->
        <div id="agent-breakdown" class="tab-content">
            <h2>Agent Type Analysis</h2>

            <div class="stat-grid">
                <div class="stat-card">
                    <h3>Authoring Agents</h3>
                    <div class="value">{len(authoring_findings)}</div>
                    <div class="description">Findings from pedagogy-focused agents</div>
                </div>

                <div class="stat-card">
                    <h3>Style Agents</h3>
                    <div class="value">{len(style_findings)}</div>
                    <div class="description">Findings from style-focused agents</div>
                </div>
            </div>

            <h3>Agent Specializations</h3>

            <div class="workflow-section">
                <h4>Authoring Specialists (9 agents)</h4>
                <ul>
                    <li>Pedagogical Flow</li>
                    <li>Structural Integrity</li>
                    <li>Student Engagement</li>
                    <li>Conceptual Clarity</li>
                    <li>Assessment Quality</li>
                </ul>

                <h4 style="margin-top: 20px;">Style Specialists (9 agents)</h4>
                <ul>
                    <li>Mechanical Compliance</li>
                    <li>Mathematical Formatting</li>
                    <li>Punctuation & Grammar</li>
                    <li>Accessibility</li>
                    <li>Consistency</li>
                </ul>

                <h4 style="margin-top: 20px;">Generalists (12 agents)</h4>
                <p>6 authoring generalists and 6 style generalists provide cross-cutting perspectives</p>
            </div>
        </div>

        <!-- Tab 5: Original Input -->
        <div id="original-input" class="tab-content mathjax-process">
            <h2>Original Input (What Agents Analyzed)</h2>
            <p><strong>This is the extracted, human-readable text that all 30 agents analyzed.</strong> Line numbers here match the line numbers in all issue reports. LaTeX math is rendered for readability. XML tags have been removed to show the actual content.</p>

            <button onclick="if(window.MathJax) {{ window.MathJax.typesetPromise().then(() => console.log('Manual typeset done')).catch(e => console.error('Typeset error:', e)); }} else {{ console.error('MathJax not loaded'); }}" style="background: #007bff; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; margin-bottom: 10px;">Force Render Math</button>

            <div class="original-input mathjax-process">{escaped_module}</div>
        </div>

        <!-- Tab 6: Consensus Issues -->
        <div id="consensus" class="tab-content">
            <h2>Consensus Issues</h2>
            <p>Issues identified by 4 or more agents, indicating high confidence in the finding.</p>

            {_format_issues_html(consensus_issues, total_agents, show_all=False, max_issues=50)}

            {f'<p style="text-align: center; color: #6c757d; margin-top: 30px;"><em>Showing {min(50, len(consensus_issues))} of {len(consensus_issues)} consensus issues</em></p>' if len(consensus_issues) > 50 else ''}
        </div>

        <!-- Tab 7: Flagged Issues -->
        <div id="flagged" class="tab-content">
            <h2>Flagged Issues</h2>
            <p>Issues identified by 1-3 agents. These may require manual review to determine validity.</p>

            {_format_issues_html(non_consensus_issues, total_agents, show_all=False, max_issues=30)}

            {f'<p style="text-align: center; color: #6c757d; margin-top: 30px;"><em>Showing {min(30, len(non_consensus_issues))} of {len(non_consensus_issues)} flagged issues</em></p>' if len(non_consensus_issues) > 30 else ''}
        </div>

        <!-- Tab 8: All Findings -->
        <div id="all-findings" class="tab-content">
            <h2>All Findings by Category</h2>

            <table>
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Total Issues</th>
                        <th>Consensus</th>
                        <th>Flagged</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
                    {_format_category_table_html(category_counts, consensus_issues, non_consensus_issues)}
                </tbody>
            </table>

            <h3 style="margin-top: 40px;">Sample Issues by Category</h3>
            {_format_issues_by_category_html(all_issues, authoring_categories, style_categories)}
        </div>

        <!-- Tab 9: Category Analysis -->
        <div id="category-analysis" class="tab-content">
            <h2>Category Analysis</h2>

            <h3>Authoring Categories</h3>
            {_format_category_details_html(consensus_issues + non_consensus_issues, authoring_categories, "authoring")}

            <h3 style="margin-top: 40px;">Style Categories</h3>
            {_format_category_details_html(consensus_issues + non_consensus_issues, style_categories, "style")}
        </div>

        <!-- Tab 2: Complete Workflow -->
        <div id="workflow" class="tab-content">
            <h2>Complete 4-Pass Workflow</h2>

            <div class="info-box">
                <strong>Note:</strong> This report represents <strong>Pass 1</strong> of the complete workflow.
                The full production workflow includes 4 passes across two review phases.
            </div>

            <div class="workflow-section">
                <h3 style="color: #667eea; margin-top: 30px;">Reviewer Phase (Passes 1 & 2)</h3>
                <p><em>Uses both Authoring Guide and Style Guide</em></p>

                <div class="flowchart" style="margin-top: 20px;">
                    <div class="flowchart-box" style="background: #667eea; color: white; font-weight: bold;">Pass 1: Initial Review</div>
                    <div class="flowchart-arrow">↓</div>
                    <div class="flowchart-box">30 Agents (15 Authoring + 15 Style)</div>
                    <div class="flowchart-arrow">↓</div>
                    <div class="flowchart-box">Consensus Building</div>
                    <div class="flowchart-arrow">↓</div>
                    <div class="flowchart-box" style="background: #4caf50; color: white; font-weight: bold;">Output to Author</div>
                </div>

                <div class="flowchart" style="margin-top: 30px;">
                    <div class="flowchart-box" style="background: #667eea; color: white; font-weight: bold;">Pass 2: Reviewer Validation</div>
                    <div class="flowchart-arrow">↓</div>
                    <div class="flowchart-box">Author's Revisions + Original Content</div>
                    <div class="flowchart-arrow">↓</div>
                    <div class="flowchart-box">30 Agents Re-review</div>
                    <div class="flowchart-arrow">↓</div>
                    <div class="flowchart-box">Verify Fixes + New Issues</div>
                    <div class="flowchart-arrow">↓</div>
                    <div class="flowchart-box" style="background: #4caf50; color: white; font-weight: bold;">Output to Author & Reviewer</div>
                </div>
            </div>

            <div class="workflow-section" style="margin-top: 50px;">
                <h3 style="color: #764ba2; margin-top: 30px;">Content Editor Phase (Passes 3 & 4)</h3>
                <p><em>Uses Style Guide only (no authoring guide)</em></p>

                <div class="flowchart" style="margin-top: 20px;">
                    <div class="flowchart-box" style="background: #764ba2; color: white; font-weight: bold;">Pass 3: Style Focus</div>
                    <div class="flowchart-arrow">↓</div>
                    <div class="flowchart-box">15 Style Agents Only</div>
                    <div class="flowchart-arrow">↓</div>
                    <div class="flowchart-box">Style & Formatting Issues</div>
                    <div class="flowchart-arrow">↓</div>
                    <div class="flowchart-box" style="background: #4caf50; color: white; font-weight: bold;">Output to Author</div>
                </div>

                <div class="flowchart" style="margin-top: 30px;">
                    <div class="flowchart-box" style="background: #764ba2; color: white; font-weight: bold;">Pass 4: Final Polish</div>
                    <div class="flowchart-arrow">↓</div>
                    <div class="flowchart-box">Author's Style Revisions</div>
                    <div class="flowchart-arrow">↓</div>
                    <div class="flowchart-box">15 Style Agents Re-review</div>
                    <div class="flowchart-arrow">↓</div>
                    <div class="flowchart-box">Verify Style Compliance</div>
                    <div class="flowchart-arrow">↓</div>
                    <div class="flowchart-box" style="background: #ff9800; color: white; font-weight: bold;">Output to Author & Content Editor</div>
                </div>
            </div>

            <div class="info-box" style="margin-top: 40px;">
                <h3>Phase Distinction</h3>
                <ul>
                    <li><strong>Reviewer Phase:</strong> Comprehensive review covering both pedagogical quality (authoring) and style compliance. Ensures content is educationally sound and well-written.</li>
                    <li><strong>Content Editor Phase:</strong> Focused exclusively on style, formatting, and mechanical compliance. Ensures consistency and polish without re-evaluating pedagogical decisions.</li>
                </ul>
            </div>

            <div class="success-box" style="margin-top: 30px;">
                <h3>Why 4 Passes?</h3>
                <ul>
                    <li><strong>Pass 1 & 3:</strong> Initial identification of issues allows authors to make revisions</li>
                    <li><strong>Pass 2 & 4:</strong> Validation passes ensure fixes are correct and don't introduce new issues</li>
                    <li><strong>Separation of concerns:</strong> Content editor phase focuses purely on style without reopening pedagogical decisions</li>
                    <li><strong>Progressive refinement:</strong> Each pass builds on the previous work, moving from rough draft to polished content</li>
                </ul>
            </div>

            <div class="warning-box" style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 20px; margin-top: 30px; border-radius: 4px;">
                <h3 style="color: #856404;">Current Implementation Status</h3>
                <p><strong>Currently implemented:</strong> Pass 1 only (Reviewer Phase, Initial Review)</p>
                <p><strong>In development:</strong> Passes 2, 3, and 4 represent the planned production workflow</p>
                <p>This report demonstrates the architecture and capabilities of the multi-agent system using rule-based detection.</p>
            </div>
        </div>

        <!-- Tab 3: System Architecture -->
        <div id="architecture" class="tab-content">
            <h2>System Architecture</h2>

            <div class="flowchart">
                <div class="flowchart-box">Module Input</div>
                <div class="flowchart-arrow">↓</div>
                <div class="flowchart-box">30 AI Agents</div>
                <div class="flowchart-arrow">↓</div>
                <div class="flowchart-box">Individual Findings</div>
                <div class="flowchart-arrow">↓</div>
                <div class="flowchart-box">Consensus Algorithm</div>
                <div class="flowchart-arrow">↓</div>
                <div class="flowchart-box">Prioritized Issues</div>
                <div class="flowchart-arrow">↓</div>
                <div class="flowchart-box">Review Report</div>
            </div>

            <div class="info-box" style="margin-top: 40px;">
                <h3>How the System Works</h3>
                <ol>
                    <li><strong>Multi-Agent Analysis:</strong> 30 specialized agents review the content from different perspectives</li>
                    <li><strong>Layered Prompting:</strong> Each agent receives layered instructions including exemplars, domain rules, and specific rubrics</li>
                    <li><strong>Independent Review:</strong> Agents work independently to avoid groupthink</li>
                    <li><strong>Consensus Building:</strong> Issues are aggregated and ranked by agreement level</li>
                    <li><strong>Priority Scoring:</strong> Combined severity and consensus determine priority (1-5 scale)</li>
                    <li><strong>Report Generation:</strong> Findings are organized into actionable categories</li>
                </ol>
            </div>

            <div class="success-box">
                <h3>Key Benefits</h3>
                <ul>
                    <li>Reduces individual agent bias through multiple perspectives</li>
                    <li>Identifies both obvious and subtle content issues</li>
                    <li>Provides confidence scoring based on consensus</li>
                    <li>Scales to any module size or complexity</li>
                    <li>Produces consistent, objective reviews</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        function showTab(evt, tabName) {{
            // Hide all tab contents
            var tabContents = document.getElementsByClassName('tab-content');
            for (var i = 0; i < tabContents.length; i++) {{
                tabContents[i].classList.remove('active');
            }}

            // Remove active class from all tabs
            var tabs = document.getElementsByClassName('tab');
            for (var i = 0; i < tabs.length; i++) {{
                tabs[i].classList.remove('active');
            }}

            // Show the selected tab content
            document.getElementById(tabName).classList.add('active');

            // Re-render MathJax for the newly visible tab (especially Original Input)
            if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {{
                console.log('Tab switched to:', tabName, '- retypesetting MathJax...');
                MathJax.typesetPromise([document.getElementById(tabName)])
                    .then(() => console.log('MathJax retypeset complete for tab:', tabName))
                    .catch((err) => console.log('MathJax error:', err));
            }}

            // Mark the clicked tab as active
            evt.currentTarget.classList.add('active');
        }}

        // Debug MathJax
        window.addEventListener('DOMContentLoaded', function() {{
            console.log('=== MathJax Debug ===');
            console.log('MathJax loaded:', typeof MathJax !== 'undefined');

            if (typeof MathJax !== 'undefined') {{
                console.log('MathJax version:', MathJax.version);
                console.log('MathJax config:', MathJax.config);

                // Check for math elements
                const inlineMath = document.body.innerHTML.match(/\\\\\(/g);
                const displayMath = document.body.innerHTML.match(/\\\\\[/g);
                console.log('Inline math delimiters found:', inlineMath ? inlineMath.length : 0);
                console.log('Display math delimiters found:', displayMath ? displayMath.length : 0);

                // Try manual typeset
                console.log('Attempting manual typeset...');
                MathJax.startup.promise.then(() => {{
                    console.log('MathJax ready, typesetting...');
                    return MathJax.typesetPromise();
                }}).then(() => {{
                    console.log('Typeset complete!');

                    // Check if any math was actually rendered
                    const renderedMath = document.querySelectorAll('.MathJax, .MathJax_Display, mjx-container');
                    console.log('Rendered math elements:', renderedMath.length);

                    if (renderedMath.length === 0) {{
                        console.error('No math was rendered! Checking for issues...');

                        // Try to find the Original Input tab content
                        const originalInput = document.getElementById('original-input');
                        if (originalInput) {{
                            console.log('Original Input tab found');
                            const mathContent = originalInput.innerHTML.substring(0, 500);
                            console.log('First 500 chars of Original Input:', mathContent);

                            // Force typeset on Original Input specifically
                            console.log('Force typesetting Original Input tab...');
                            MathJax.typesetPromise([originalInput]).then(() => {{
                                console.log('Forced typeset complete');
                                const rendered2 = originalInput.querySelectorAll('.MathJax, .MathJax_Display, mjx-container');
                                console.log('Rendered in Original Input after force:', rendered2.length);
                            }}).catch(err => {{
                                console.error('Force typeset error:', err);
                            }});
                        }}
                    }}
                }}).catch((err) => {{
                    console.error('MathJax typeset error:', err);
                }});
            }} else {{
                console.error('MathJax is not loaded!');
            }}
        }});
    </script>
</body>
</html>
    """

    return html


def _format_issues_html(issues: List[Dict[str, Any]], total_agents: int,
                        show_all: bool = False, max_issues: int = 50) -> str:
    """Helper method to format issues as HTML cards."""

    def escape_preserve_latex(text):
        """Escape HTML but preserve <m> and <me> LaTeX tags."""
        # Protect LaTeX tags
        text = text.replace('<m>', '___LATEX_M_START___')
        text = text.replace('</m>', '___LATEX_M_END___')
        text = text.replace('<me>', '___LATEX_ME_START___')
        text = text.replace('</me>', '___LATEX_ME_END___')

        # Escape HTML
        text = html_module.escape(text)

        # Restore LaTeX with dollar sign delimiters
        text = text.replace('___LATEX_M_START___', '$')
        text = text.replace('___LATEX_M_END___', '$')
        text = text.replace('___LATEX_ME_START___', '$$')
        text = text.replace('___LATEX_ME_END___', '$$')

        return text

    html = ""
    issues_to_show = issues if show_all else issues[:max_issues]

    for issue in issues_to_show:
        quoted_text = issue.get('quoted_text', '')
        quoted_preview = escape_preserve_latex(quoted_text[:300]) + ('...' if len(quoted_text) > 300 else '')

        html += f"""
        <div class="issue-card">
            <div class="issue-header">
                <span class="badge priority-{issue['priority']}">Priority {issue['priority']}</span>
                <span class="badge severity-{issue['severity']}">Severity {issue['severity']}</span>
                <span class="badge category-badge">{issue['category']}</span>
                <span class="consensus-meter">
                    <strong>{issue['agent_count']}/{total_agents}</strong> agents
                    ({issue['consensus_percentage']:.1f}% consensus)
                </span>
            </div>

            <div class="issue-description">
                {html_module.escape(issue['issue_description'])}
            </div>

            <div class="issue-location">
                📍 {issue['location']}
            </div>

            <div class="quoted-text">
                {quoted_preview}
            </div>

            <div class="issue-impact">
                <strong>Student Impact:</strong> {html_module.escape(issue['student_impact'])}
            </div>

            <div class="suggested-fix">
                <strong>Suggested Fix:</strong> {escape_preserve_latex(issue['suggested_fix'])}
            </div>
        </div>
        """

    return html


def _format_category_table_html(category_counts: Dict[str, int],
                                consensus_issues: List[Dict[str, Any]],
                                non_consensus_issues: List[Dict[str, Any]]) -> str:
    """Helper method to format category statistics table."""
    html = ""
    total_issues = sum(category_counts.values())

    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        consensus_count = sum(1 for i in consensus_issues if i['category'] == category)
        flagged_count = sum(1 for i in non_consensus_issues if i['category'] == category)
        percentage = (count / total_issues * 100) if total_issues > 0 else 0

        html += f"""
        <tr>
            <td><span class="badge category-badge">{category}</span></td>
            <td>{count}</td>
            <td>{consensus_count}</td>
            <td>{flagged_count}</td>
            <td>{percentage:.1f}%</td>
        </tr>
        """

    return html


def _format_issues_by_category_html(all_issues: List[Dict[str, Any]],
                                    authoring_categories: List[str],
                                    style_categories: List[str]) -> str:
    """Helper method to show sample issues grouped by category."""
    html = ""

    # Group issues by category
    issues_by_category = defaultdict(list)
    for issue in all_issues:
        issues_by_category[issue['category']].append(issue)

    # Show samples from each category
    for category in authoring_categories + style_categories + ["Other"]:
        if category in issues_by_category:
            category_issues = issues_by_category[category][:2]  # Show max 2 per category
            if category_issues:
                html += f"""
                <h4 style="margin-top: 30px;">{category}</h4>
                """
                for issue in category_issues:
                    html += f"""
                    <div class="issue-card" style="margin-left: 20px;">
                        <div class="issue-header">
                            <span class="badge priority-{issue['priority']}">Priority {issue['priority']}</span>
                            <span class="consensus-meter">{issue['agent_count']} agents</span>
                        </div>
                        <div style="margin-top: 10px;">
                            {html_module.escape(issue['issue_description'][:150])}...
                        </div>
                    </div>
                    """

    return html


def _format_category_details_html(all_issues: List[Dict[str, Any]],
                                  categories: List[str], category_type: str) -> str:
    """Helper method to format detailed category analysis."""
    html = ""

    for category in categories:
        category_issues = [i for i in all_issues if i['category'] == category]
        if category_issues:
            # Calculate statistics
            avg_priority = sum(i['priority'] for i in category_issues) / len(category_issues)
            avg_severity = sum(i['severity'] for i in category_issues) / len(category_issues)
            consensus_count = sum(1 for i in category_issues if i.get('agent_count', 0) >= 4)

            html += f"""
            <div class="workflow-section">
                <h4>{category}</h4>
                <div class="stat-grid" style="margin-top: 15px;">
                    <div style="padding: 10px;">
                        <strong>Total Issues:</strong> {len(category_issues)}
                    </div>
                    <div style="padding: 10px;">
                        <strong>Consensus Issues:</strong> {consensus_count}
                    </div>
                    <div style="padding: 10px;">
                        <strong>Avg Priority:</strong> {avg_priority:.1f}
                    </div>
                    <div style="padding: 10px;">
                        <strong>Avg Severity:</strong> {avg_severity:.1f}
                    </div>
                </div>

                <div style="margin-top: 15px;">
                    <strong>Top Issues:</strong>
                    <ul style="margin-top: 10px;">
                        {_format_top_issues_list(category_issues[:3])}
                    </ul>
                </div>
            </div>
            """

    return html


def _format_top_issues_list(issues: List[Dict[str, Any]]) -> str:
    """Helper method to format a list of top issues."""
    html = ""
    for issue in issues:
        html += f"""
        <li style="margin: 5px 0;">
            <span class="badge priority-{issue['priority']}" style="font-size: 0.75em;">P{issue['priority']}</span>
            {html_module.escape(issue['issue_description'][:100])}...
        </li>
        """
    return html




def main():
    """Main execution function."""
    global TEST_MODULE_PATH, OUTPUT_PATH

    # Parse command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python run_review.py <module_folder> <xml_file>")
        print("\nExample:")
        print("  python run_review.py Power_Series power_series_original.xml")
        print("  python run_review.py Fund_Thm_of_Calculus module_5_6.xml")
        sys.exit(1)

    module_folder = sys.argv[1]
    xml_file = sys.argv[2]

    # Set paths based on arguments
    MODULE_PATH = TESTING_PATH / module_folder
    TEST_MODULE_PATH = MODULE_PATH / xml_file
    OUTPUT_PATH = MODULE_PATH / "output"

    # Validate paths
    if not TEST_MODULE_PATH.exists():
        print(f"Error: Module XML not found: {TEST_MODULE_PATH}")
        sys.exit(1)

    print("=" * 80)
    print("LEARNVIA 30-Agent Content Review System - GENERIC VERSION")
    print("=" * 80)
    print(f"Module: {module_folder}")
    print(f"XML: {xml_file}")
    print(f"Output: {OUTPUT_PATH}")
    print("=" * 80)
    print()

    # Load layered prompts (V3 XML SYSTEM)
    print("Loading V3 XML layered prompt system...")
    master_prompt = load_prompt_file("master_review_context_v3.xml")
    authoring_prompt = load_prompt_file("authoring_prompt_rules_v3.xml")
    style_prompt = load_prompt_file("style_prompt_rules_v3.xml")
    try:
        exemplar_anchors = load_prompt_file("exemplar_anchors_v3.xml")
    except FileNotFoundError:
        exemplar_anchors = ""
        print("Warning: exemplar_anchors_v3.xml not found")
    print(f"✓ Master context: {len(master_prompt)} chars")
    print(f"✓ Authoring rules: {len(authoring_prompt)} chars")
    print(f"✓ Style rules: {len(style_prompt)} chars")
    print(f"✓ Exemplar anchors: {len(exemplar_anchors)} chars")
    print()

    # Load module content (XML ONLY)
    print("Loading test module XML...")
    module_xml = load_module_content(TEST_MODULE_PATH)

    # Extract text IN-MEMORY ONLY for pattern detection
    # This is TRANSIENT - never saved to disk
    module_text = extract_text_from_module(module_xml)
    print(f"✓ Module XML loaded: {len(module_xml)} chars")
    print(f"✓ Extracted text for analysis: {len(module_text)} chars (transient, in-memory only)")
    print()

    # Create output directory
    try:
        OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

    # Simulate 30 agent reviews
    print("Simulating 30 agent reviews with GENERIC RULES...")
    print()

    all_findings = []

    # Authoring agents
    print("AUTHORING AGENTS (15 total):")
    for i in range(AGENT_CONFIG["authoring"]["total"]):
        if i < AGENT_CONFIG["authoring"]["rubric_focused"]:
            # Rubric-focused agent
            competency = AGENT_CONFIG["authoring"]["competencies"][i % len(AGENT_CONFIG["authoring"]["competencies"])]
            rubric_file = f"authoring_{competency.lower().replace(' ', '_')}.xml"
            try:
                rubric_content = load_rubric_file(rubric_file)
            except FileNotFoundError:
                rubric_content = ""

            agent_id = f"Authoring-Specialist-{competency.replace(' ', '')}-{i+1}"
            agent_type = "authoring"
            focus = f"Specialist: {competency}"
        else:
            # Generalist agent
            rubric_content = ""
            agent_id = f"Authoring-Generalist-{i+1}"
            agent_type = "authoring"
            focus = "Generalist (Cross-Cutting)"

        prompt = build_agent_prompt(agent_type, focus, exemplar_anchors, master_prompt, authoring_prompt,
                                     rubric_content, module_text)

        findings = simulate_agent_review(agent_id, prompt)
        all_findings.extend(findings)

        print(f"  ✓ {agent_id}: {len(findings)} findings")

    print()
    print("STYLE AGENTS (15 total):")
    for i in range(AGENT_CONFIG["style"]["total"]):
        if i < AGENT_CONFIG["style"]["rubric_focused"]:
            # Rubric-focused agent
            competency = AGENT_CONFIG["style"]["competencies"][i % len(AGENT_CONFIG["style"]["competencies"])]
            rubric_file = f"style_{competency.lower().replace(' ', '_')}.xml"
            try:
                rubric_content = load_rubric_file(rubric_file)
            except FileNotFoundError:
                rubric_content = ""

            agent_id = f"Style-Specialist-{competency.replace(' ', '')}-{i+1}"
            agent_type = "style"
            focus = f"Specialist: {competency}"
        else:
            # Generalist agent
            rubric_content = ""
            agent_id = f"Style-Generalist-{i+1}"
            agent_type = "style"
            focus = f"Generalist (Cross-Cutting)"

        prompt = build_agent_prompt(agent_type, focus, exemplar_anchors, master_prompt, style_prompt,
                                     rubric_content, module_text)

        findings = simulate_agent_review(agent_id, prompt)
        all_findings.extend(findings)

        print(f"  ✓ {agent_id}: {len(findings)} findings")

    print()
    print("=" * 80)
    print(f"TOTAL FINDINGS: {len(all_findings)}")
    print()

    # Aggregate consensus issues
    print("Aggregating consensus issues...")
    consensus_issues, non_consensus = aggregate_consensus_issues(all_findings, 30)
    print(f"✓ Consensus issues identified: {len(consensus_issues)}")
    print(f"✓ Non-consensus flagged issues: {len(non_consensus)}")
    print()

    # Generate HTML report
    print("Generating HTML report...")
    # Pass the ORIGINAL XML to the HTML report (will be displayed in "Original Input" tab)
    html_report = generate_html_report(consensus_issues, non_consensus, all_findings, AGENT_CONFIG, module_xml)

    output_file = OUTPUT_PATH / "test_module_review_report_generic.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_report)

    print(f"✓ Report saved: {output_file}")
    print()

    # Save JSON data for further analysis
    json_output = OUTPUT_PATH / "test_module_review_data_generic.json"
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_agents": 30,
            "consensus_issues_count": len(consensus_issues),
            "non_consensus_issues_count": len(non_consensus),
            "consensus_issues": consensus_issues,
            "non_consensus_issues": non_consensus,
            "all_findings": all_findings
        }, f, indent=2)

    print(f"✓ JSON data saved: {json_output}")
    print()

    print("=" * 80)
    print("GENERIC SIMULATION COMPLETE")
    print("=" * 80)
    print()
    print(f"Open the report: {output_file}")
    print()


if __name__ == "__main__":
    main()