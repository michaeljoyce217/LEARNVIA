"""
Synthetic author module that simulates realistic revision behavior.
"""

import re
import json
import random
from typing import List, Dict, Tuple
from mock_agents import Feedback, Severity, Competency


class SyntheticAuthor:
    """Simulates Dr. Sarah Chen's revision behavior."""

    def __init__(self, persona_file: str = "../synthetic_actors/author_persona.json"):
        with open(persona_file, 'r') as f:
            self.persona = json.load(f)

        self.revision_notes = []
        self.fix_probabilities = self.persona["revision_behavior"]["fix_probability_by_severity"]

    def revise_content(self, original_content: str, feedback: List[Feedback], pass_number: int) -> Tuple[str, List[str]]:
        """
        Revise content based on feedback.
        Returns revised content and revision notes.
        """
        self.revision_notes = []
        revised_content = original_content

        # Group feedback by severity
        feedback_by_severity = self._group_feedback_by_severity(feedback)

        # Process feedback from highest to lowest severity
        for severity_level in [5, 4, 3, 2, 1]:
            severity_key = str(severity_level)
            if severity_key not in feedback_by_severity:
                continue

            fix_probability = self.fix_probabilities.get(severity_key, 0.5)

            for f in feedback_by_severity[severity_key]:
                if random.random() < fix_probability:
                    revised_content, fixed = self._apply_fix(revised_content, f, pass_number)
                    if fixed:
                        self.revision_notes.append(f"Fixed: {f.issue} at {f.location}")
                else:
                    self.revision_notes.append(f"Missed: {f.issue} at {f.location} (will address later)")

        # Sometimes introduce new minor issues (realistic behavior)
        if pass_number == 1 and random.random() < 0.3:
            revised_content = self._introduce_minor_issues(revised_content)

        # Fix word count in framing if it was flagged
        if any("word count" in f.issue.lower() for f in feedback):
            revised_content = self._fix_framing_word_count(revised_content)

        return revised_content, self.revision_notes

    def _group_feedback_by_severity(self, feedback: List[Feedback]) -> Dict[str, List[Feedback]]:
        """Group feedback items by severity level."""
        grouped = {}
        for f in feedback:
            key = str(f.severity.value)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(f)
        return grouped

    def _apply_fix(self, content: str, feedback: Feedback, pass_number: int) -> Tuple[str, bool]:
        """Apply a specific fix based on feedback."""
        fixed = False

        # Handle contractions
        if "contraction" in feedback.issue.lower():
            contractions = {
                "don't": "do not",
                "doesn't": "does not",
                "won't": "will not",
                "can't": "cannot",
                "let's": "let us",
                "it's": "it is",
                "isn't": "is not",
                "aren't": "are not",
                "we'll": "we will",
                "you'll": "you will",
                "they'll": "they will",
                "we're": "we are",
                "you're": "you are",
                "they're": "they are"
            }

            for contraction, replacement in contractions.items():
                if contraction in content.lower():
                    # Be case-sensitive in replacement
                    content = re.sub(r'\b' + re.escape(contraction) + r'\b', replacement, content, flags=re.IGNORECASE)
                    fixed = True

        # Handle imperative voice
        elif "imperative" in feedback.issue.lower():
            imperative_fixes = {
                "Calculate the slope": "The slope is calculated",
                "Find the slope": "The slope can be found",
                "Look at": "Looking at",
                "Think about": "When considering",
                "Think of": "This can be thought of as",
                "Remember to": "It is important to",
                "Try these": "These problems provide practice",
                "Notice": "It can be observed that",
                "Use": "Using",
                "Identify": "Identifying"
            }

            for imperative, replacement in imperative_fixes.items():
                if imperative in content:
                    content = content.replace(imperative, replacement)
                    fixed = True

        # Handle LaTeX formatting
        elif "latex" in feedback.issue.lower() or "mathematical" in feedback.issue.lower():
            # Fix common patterns
            content = re.sub(r'(?<!\$)m = ([\(\)0-9\-\+\*/\s]+)(?!\$)', r'$m = \1$', content)
            content = re.sub(r'(?<!\$)(x\d|y\d)(?!\$)', r'$\1$', content)
            content = re.sub(r'(?<!\$)(\d+/\d+)(?!\$)', r'$\\frac{\1}$', content)

            # Fix the main slope formula
            if "m = (y2 - y1) / (x2 - x1)" in content:
                content = content.replace(
                    "m = (y2 - y1) / (x2 - x1)",
                    "$m = \\frac{y_2 - y_1}{x_2 - x_1}$"
                )
                fixed = True

        # Handle consistency issues
        elif "consistency" in feedback.issue.lower() or "inconsistent" in feedback.issue.lower():
            if "gradient" in content:
                content = content.replace("gradient", "slope")
                fixed = True

        return content, fixed

    def _introduce_minor_issues(self, content: str) -> str:
        """Realistically introduce new minor issues during revision."""
        lines = content.split('\n')

        # Sometimes miss a contraction when rewriting
        if random.random() < 0.2:
            replacements = [
                ("This is", "It's"),
                ("We are", "We're")
            ]
            for original, mistake in replacements:
                if original in content and random.random() < 0.3:
                    # Only introduce one new mistake
                    content = content.replace(original, mistake, 1)
                    self.revision_notes.append(f"(Accidentally introduced '{mistake}' while revising)")
                    break

        # Sometimes create slight word count issues when expanding
        if random.random() < 0.15:
            self.revision_notes.append("(May have slightly altered word count while revising framing)")

        return content

    def _fix_framing_word_count(self, content: str) -> str:
        """Fix the framing section word count."""
        framing_match = re.search(r'(## Framing\n\n)(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if framing_match:
            framing_text = framing_match.group(2)
            word_count = len(framing_text.split())

            if word_count < 100:
                # Add more content
                additional_text = (
                    " Understanding slope is crucial for advanced mathematics, "
                    "including calculus where derivatives represent instantaneous rates of change. "
                    "This concept also appears in physics when studying motion and forces, "
                    "in economics when analyzing trends and rates, and in engineering "
                    "when designing structures and systems. By mastering slope, students "
                    "build a foundation for understanding how quantities change in relation "
                    "to one another, a fundamental concept across all STEM fields."
                )

                # Trim to get closer to target
                words_needed = 125 - word_count
                additional_words = additional_text.split()[:words_needed]
                framing_text = framing_text.rstrip() + " " + " ".join(additional_words)

            elif word_count > 150:
                # Trim content
                words = framing_text.split()
                framing_text = " ".join(words[:140])  # Trim to 140 words

            # Replace in content
            content = content[:framing_match.start()] + \
                      framing_match.group(1) + framing_text + \
                      content[framing_match.end():]

            self.revision_notes.append(f"Adjusted framing word count from {word_count} to ~125 words")

        return content

    def generate_revision_summary(self, feedback: List[Feedback]) -> str:
        """Generate a summary of the revision process."""
        summary = "\n" + "="*60 + "\n"
        summary += f"AUTHOR REVISION SUMMARY - {self.persona['name']}\n"
        summary += "="*60 + "\n\n"

        # Count what was addressed
        total_issues = len(feedback)
        fixed_count = len([note for note in self.revision_notes if note.startswith("Fixed:")])
        missed_count = len([note for note in self.revision_notes if note.startswith("Missed:")])

        summary += f"Total issues identified: {total_issues}\n"
        summary += f"Issues addressed: {fixed_count}\n"
        summary += f"Issues deferred: {missed_count}\n"
        summary += f"Fix rate: {fixed_count/total_issues*100:.1f}%\n\n"

        summary += "Revision Notes:\n"
        summary += "-" * 40 + "\n"
        for note in self.revision_notes[:20]:  # Show first 20 notes
            summary += f"  • {note}\n"

        if len(self.revision_notes) > 20:
            summary += f"  ... and {len(self.revision_notes) - 20} more actions\n"

        summary += "\nAuthor's Internal Thoughts:\n"
        summary += "-" * 40 + "\n"

        thoughts = [
            "I tried to maintain clarity while fixing the style issues.",
            "Some of these style rules feel overly strict, but I understand the need for consistency.",
            "I focused on the high-severity issues first.",
            "I hope the examples still feel engaging after removing the conversational tone.",
            "The mathematical notation in LaTeX should be clearer now."
        ]

        for thought in random.sample(thoughts, min(3, len(thoughts))):
            summary += f"  • {thought}\n"

        return summary


if __name__ == "__main__":
    # Test the synthetic author
    import sys
    sys.path.append(".")
    from mock_agents import MockAgentSystem

    # Load original content
    with open("../sample_content/draft_v1_original.md", "r") as f:
        content = f.read()

    # Get mock feedback
    agent_system = MockAgentSystem()
    feedback = agent_system.analyze_content(content, pass_number=1)

    # Apply revisions
    author = SyntheticAuthor()
    revised_content, notes = author.revise_content(content, feedback, pass_number=1)

    # Print summary
    print(author.generate_revision_summary(feedback))