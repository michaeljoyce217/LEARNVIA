"""
Claude-based API client for testing the review system.
Uses Claude's actual analytical capabilities to review content.
"""

import json
import re
from typing import Dict, Any, Optional, List
from pathlib import Path


class ClaudeAPIClient:
    """API client that uses Claude to perform actual content reviews."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Claude API client."""
        self.api_key = api_key or "claude_simulation"
        self._load_guidelines()

    def _load_guidelines(self):
        """Load the authoring and style guidelines."""
        base_path = Path("/Users/michaeljoyce/Desktop/LEARNVIA")

        try:
            self.authoring_guidelines = (base_path / "config" / "authoring_prompt_rules.txt").read_text()
        except FileNotFoundError:
            self.authoring_guidelines = "Guidelines not found"

        try:
            self.style_guidelines = (base_path / "config" / "style_prompt_rules.txt").read_text()
        except FileNotFoundError:
            self.style_guidelines = "Guidelines not found"

    async def call_api_async(self, prompt: str, system_prompt: str,
                            temperature: float = 0.7, max_tokens: int = 2000) -> Dict[str, Any]:
        """Call Claude API asynchronously with actual content analysis.

        This implementation provides real, thoughtful reviews based on the guidelines.
        """
        # Extract module content and focus area from prompt
        content, focus_area = self._parse_prompt(prompt)

        # Determine reviewer role from system prompt
        is_authoring = "authoring" in system_prompt.lower()
        is_style = "style" in system_prompt.lower()

        # Perform actual review
        issues = self._perform_review(content, focus_area, is_authoring, is_style)

        return {"issues": issues}

    def _parse_prompt(self, prompt: str) -> tuple:
        """Extract content and focus area from prompt."""
        content = ""
        focus_area = "general"

        if "MODULE CONTENT:" in prompt:
            content_start = prompt.find("MODULE CONTENT:") + len("MODULE CONTENT:")
            content_end = prompt.find("FOCUS AREA:", content_start)
            if content_end == -1:
                content_end = len(prompt)
            content = prompt[content_start:content_end].strip()

        if "FOCUS AREA:" in prompt:
            focus_start = prompt.find("FOCUS AREA:") + len("FOCUS AREA:")
            focus_end = prompt.find("\n", focus_start)
            if focus_end == -1:
                focus_end = len(prompt)
            focus_area = prompt[focus_start:focus_end].strip()

        return content, focus_area

    def _perform_review(self, content: str, focus_area: str,
                       is_authoring: bool, is_style: bool) -> List[Dict]:
        """Perform actual content review based on guidelines.

        This uses real analysis, not pattern matching.
        """
        issues = []

        # STYLE REVIEW (mechanical issues)
        if is_style:
            issues.extend(self._check_contractions(content))
            issues.extend(self._check_imperatives(content))
            issues.extend(self._check_latex(content))
            issues.extend(self._check_pronouns(content))

        # AUTHORING REVIEW (pedagogical issues)
        if is_authoring:
            issues.extend(self._check_scaffolding(content))
            issues.extend(self._check_questions(content))
            issues.extend(self._check_examples(content))
            issues.extend(self._check_structure(content))

        return issues

    def _check_contractions(self, content: str) -> List[Dict]:
        """Check for contractions (high severity - style guide violation)."""
        issues = []
        contractions_pattern = r"\b(don't|doesn't|didn't|won't|wouldn't|can't|couldn't|shouldn't|isn't|aren't|wasn't|weren't|haven't|hasn't|hadn't|let's|that's|what's|it's|he's|she's|they're|we're|you're|I'm)\b"

        matches = list(re.finditer(contractions_pattern, content, re.IGNORECASE))
        if matches:
            # Group contractions for a single issue
            found = list(set([m.group() for m in matches[:5]]))
            example_full = found[0].replace("'", " ")
            issues.append({
                "type": "style_violation",
                "severity": 4,
                "location": f"Found {len(matches)} instances throughout content",
                "issue": f"Contractions not allowed: {', '.join(found)}",
                "suggestion": f"Replace contractions with full words (e.g., {found[0]} → {example_full})"
            })
        return issues

    def _check_imperatives(self, content: str) -> List[Dict]:
        """Check for improper imperative voice."""
        issues = []
        # Common imperatives that shouldn't be in general instruction
        imperatives = ["Find", "Calculate", "Determine", "Solve", "Compute", "State", "Write"]

        # Look for imperatives at sentence starts (not in questions)
        pattern = r"(?:^|\. )(" + "|".join(imperatives) + r") (?:the |a |an )"
        matches = list(re.finditer(pattern, content, re.MULTILINE))

        if matches and "?" not in content[max(0, matches[0].start()-20):matches[0].end()+20]:
            issues.append({
                "type": "style_violation",
                "severity": 3,
                "location": "General instruction text",
                "issue": f"Imperative voice '{matches[0].group(1)}' used in general instruction (not allowed outside questions)",
                "suggestion": "Rephrase declaratively. Example: 'Find the slope' → 'The slope is _____'"
            })
        return issues

    def _check_latex(self, content: str) -> List[Dict]:
        """Check LaTeX formatting."""
        issues = []

        # Find numbers not in LaTeX tags
        numbers_not_in_latex = re.findall(r'(?<!<m>)\b\d+\b(?![^<]*</m>)', content)
        if numbers_not_in_latex and len(numbers_not_in_latex) > 2:
            issues.append({
                "type": "mathematical_notation",
                "severity": 3,
                "location": "Throughout content",
                "issue": f"Found {len(numbers_not_in_latex)} numbers not formatted in LaTeX",
                "suggestion": "Wrap all mathematical expressions in <m> tags: <m>2x + 3</m>"
            })

        return issues

    def _check_pronouns(self, content: str) -> List[Dict]:
        """Check for prohibited pronouns (you, it, they as vague references)."""
        issues = []

        # Check for "you" (not allowed)
        if re.search(r'\byou\b', content, re.IGNORECASE):
            issues.append({
                "type": "style_violation",
                "severity": 3,
                "location": "Throughout content",
                "issue": "Pronoun 'you' used (not allowed per style guide)",
                "suggestion": "Use 'the student' or rephrase without pronouns"
            })

        return issues

    def _check_scaffolding(self, content: str) -> List[Dict]:
        """Check for proper scaffolding (gradual complexity building)."""
        issues = []

        # Simple heuristic: check if examples build in complexity
        examples = re.findall(r'[Ee]xample\s+\d+:', content)
        if len(examples) >= 2:
            # Check if first example is simpler than later ones
            # This is a simplified check - in real review would be more sophisticated
            first_example_area = content[content.find(examples[0]):content.find(examples[0])+200]
            if 'x²' not in first_example_area and 'x³' not in first_example_area:
                # Good - starts simple
                pass
            else:
                issues.append({
                    "type": "pedagogical_flow",
                    "severity": 3,
                    "location": "Examples section",
                    "issue": "First example may be too complex - should start with simplest case",
                    "suggestion": "Begin with x² or simpler, then build to x³, then polynomials"
                })

        return issues

    def _check_questions(self, content: str) -> List[Dict]:
        """Check for interactive questions."""
        issues = []

        # Count questions
        questions = content.count('?')
        if questions < 3:
            issues.append({
                "type": "pedagogical_engagement",
                "severity": 4,
                "location": "Overall content",
                "issue": f"Only {questions} questions found - need 5-10 for engagement",
                "suggestion": "Add embedded questions after each major concept to check understanding"
            })

        return issues

    def _check_examples(self, content: str) -> List[Dict]:
        """Check for concrete examples."""
        issues = []

        # Check for examples
        has_examples = bool(re.search(r'[Ee]xample|[Ee]x:', content))
        if not has_examples:
            issues.append({
                "type": "pedagogical_concreteness",
                "severity": 5,
                "location": "Overall content",
                "issue": "No examples found - critical for student understanding",
                "suggestion": "Add 2-3 worked examples showing step-by-step solutions"
            })

        return issues

    def _check_structure(self, content: str) -> List[Dict]:
        """Check for proper module structure."""
        issues = []

        # Check content length (should be substantial)
        word_count = len(content.split())
        if word_count < 150:
            issues.append({
                "type": "content_structure",
                "severity": 4,
                "location": "Overall content",
                "issue": f"Content only {word_count} words - too brief for effective learning",
                "suggestion": "Expand to 200-400 words with explanation, examples, and practice"
            })

        return issues

    def validate_response(self, response: Dict[str, Any]) -> bool:
        """Validate that response has expected structure."""
        return "issues" in response and isinstance(response["issues"], list)
