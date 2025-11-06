"""
Mock API responses that provide realistic, content-aware feedback
Based on actual rubric analysis rather than random generation
"""

import asyncio
import random
import re
from typing import List, Dict, Any
from dataclasses import dataclass
import sys
from pathlib import Path

# Import models from real system
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))
from CODE.models import ReviewFeedback, ReviewerRole, SeverityLevel, ReviewPass


class ContentAnalyzer:
    """Analyzes content for real issues based on rubrics"""

    def analyze_pedagogical_flow(self, content: str) -> List[Dict]:
        """Check for pedagogical flow issues"""
        issues = []

        # Check for missing learning objectives
        if "learning objective" not in content.lower() and "you will learn" not in content.lower():
            issues.append({
                "issue": "Missing clear learning objectives at module start",
                "severity": 5,
                "location": "Module introduction",
                "issue_type": "missing_objectives",
                "solution": "Add explicit learning objectives section stating what students will know and be able to do after completing this module"
            })

        # Check for prerequisite violations
        if "binary search tree" in content.lower():
            bst_pos = content.lower().index("binary search tree")
            if "binary tree" not in content[:bst_pos].lower():
                issues.append({
                    "issue": "Binary Search Trees introduced before basic Binary Trees",
                    "severity": 4,
                    "location": "BST section",
                    "issue_type": "prerequisite_violation",
                    "solution": "Reorder sections to introduce Binary Trees before Binary Search Trees"
                })

        # Check for complexity jumps
        sections = content.split("##")
        if len(sections) > 3:
            # Check if advanced topics come too early
            for i, section in enumerate(sections[:3]):
                if any(term in section.lower() for term in ["O(log n)", "time complexity", "space complexity"]):
                    if i < 2 and "introduction" not in sections[0].lower():
                        issues.append({
                            "issue": "Complexity analysis introduced before basic concepts",
                            "severity": 3,
                            "location": f"Section {i}",
                            "issue_type": "poor_scaffolding"
                        })

        return issues

    def analyze_structural_integrity(self, content: str) -> List[Dict]:
        """Check for structural issues"""
        issues = []

        # Check for section organization
        headers = re.findall(r'^##+ .+$', content, re.MULTILINE)

        # Check for missing introduction
        if not content.strip().startswith("#"):
            issues.append({
                "issue": "Module lacks proper title header",
                "severity": 3,
                "location": "Beginning of module",
                "issue_type": "structure"
            })

        # Check for missing conclusion
        if "conclusion" not in content.lower() and "summary" not in content.lower():
            issues.append({
                "issue": "Module lacks conclusion or summary section",
                "severity": 3,
                "location": "End of module",
                "issue_type": "structure",
                "solution": "Add a conclusion that reinforces key concepts and provides next steps"
            })

        # Check for unbalanced sections
        sections = content.split("##")
        section_lengths = [len(s) for s in sections if s.strip()]
        if section_lengths:
            avg_length = sum(section_lengths) / len(section_lengths)
            for i, length in enumerate(section_lengths):
                if length > avg_length * 3:
                    issues.append({
                        "issue": f"Section {i} is disproportionately long",
                        "severity": 2,
                        "location": f"Section {i}",
                        "issue_type": "structure"
                    })

        return issues

    def analyze_conceptual_clarity(self, content: str) -> List[Dict]:
        """Check for clarity issues"""
        issues = []

        # Check for undefined terms
        technical_terms = ["O(1)", "O(n)", "O(log n)", "LIFO", "FIFO", "traversal", "heap property"]
        for term in technical_terms:
            if term in content:
                # Check if term is defined nearby
                term_pos = content.index(term)
                context = content[max(0, term_pos-200):term_pos+200]
                if "means" not in context and "is" not in context and "defined as" not in context:
                    issues.append({
                        "issue": f"Technical term '{term}' used without definition",
                        "severity": 3,
                        "location": f"Near '{term}'",
                        "issue_type": "clarity"
                    })

        # Check for vague language
        vague_phrases = ["various", "different", "several", "some"]
        for phrase in vague_phrases:
            if phrase in content.lower():
                issues.append({
                    "issue": f"Vague language: '{phrase}' - be more specific",
                    "severity": 2,
                    "location": f"Search for '{phrase}'",
                    "issue_type": "clarity"
                })
                break  # Only report once per type

        return issues

    def analyze_style_compliance(self, content: str) -> List[Dict]:
        """Check for style violations"""
        issues = []

        # Check for contractions
        contractions = ["we'll", "you'll", "don't", "won't", "can't", "we've", "they're", "it's"]
        for contraction in contractions:
            if contraction in content.lower():
                issues.append({
                    "issue": f"Contraction '{contraction}' violates style guide",
                    "severity": 2,
                    "location": f"Search for '{contraction}'",
                    "issue_type": "style_contraction",
                    "solution": f"Replace '{contraction}' with full form"
                })

        # Check for imperative voice at beginning of sentences
        sentences = re.split(r'[.!?]\s+', content)
        imperative_starts = ["Try", "Remember", "Consider", "Think", "Look at"]
        for sentence in sentences[:10]:  # Check first 10 sentences
            for imp in imperative_starts:
                if sentence.strip().startswith(imp):
                    issues.append({
                        "issue": f"Imperative voice: '{imp}...' - use declarative",
                        "severity": 2,
                        "location": f"Sentence starting with '{imp}'",
                        "issue_type": "style_voice"
                    })
                    break

        # Check for inconsistent formatting
        if "```python" in content and "```Python" in content:
            issues.append({
                "issue": "Inconsistent code block language formatting",
                "severity": 2,
                "location": "Code blocks",
                "issue_type": "style_consistency"
            })

        return issues

    def analyze_assessment_quality(self, content: str) -> List[Dict]:
        """Check assessment and practice problems"""
        issues = []

        # Check if practice problems exist
        if "practice" in content.lower() or "problem" in content.lower():
            # Check if solutions are provided
            if "solution" not in content.lower() and "answer" not in content.lower():
                issues.append({
                    "issue": "Practice problems lack solutions or hints",
                    "severity": 3,
                    "location": "Practice Problems section",
                    "issue_type": "assessment",
                    "solution": "Add solutions or detailed hints for practice problems"
                })

            # Check if problems align with content
            if "practice problem" in content.lower():
                problems_section = content[content.lower().index("practice problem"):]
                if "LRU cache" in problems_section and "LRU" not in content[:content.lower().index("practice problem")]:
                    issues.append({
                        "issue": "Practice problem references concept (LRU) not covered in content",
                        "severity": 4,
                        "location": "Practice Problems",
                        "issue_type": "assessment"
                    })

        return issues


class MockAPIClient:
    """Mock API client that returns realistic responses"""

    def __init__(self):
        self.analyzer = ContentAnalyzer()
        self.response_delay = 0.1  # Simulate API latency

    async def get_review(self, content: str, reviewer_config: Dict) -> Dict:
        """Generate realistic review based on content and reviewer type"""
        await asyncio.sleep(self.response_delay)

        # Determine what this reviewer focuses on
        focus = reviewer_config.get("focus", "general")
        competency = reviewer_config.get("competency", None)

        issues = []

        if competency == "Pedagogical Flow" or focus == "general":
            issues.extend(self.analyzer.analyze_pedagogical_flow(content))

        if competency == "Structural Integrity" or focus == "general":
            issues.extend(self.analyzer.analyze_structural_integrity(content))

        if competency == "Conceptual Clarity" or focus == "general":
            issues.extend(self.analyzer.analyze_conceptual_clarity(content))

        if competency in ["Mechanical Compliance", "Consistency"] or focus == "style":
            issues.extend(self.analyzer.analyze_style_compliance(content))

        if competency == "Assessment Quality" or focus == "general":
            issues.extend(self.analyzer.analyze_assessment_quality(content))

        # Add some variation between agents
        if len(issues) > 2 and random.random() > 0.3:  # 70% chance to find each issue (if we have enough)
            sample_size = random.randint(max(1, len(issues) - 2), len(issues))
            issues = random.sample(issues, sample_size)

        # Vary severity slightly between agents
        for issue in issues:
            if random.random() < 0.2:  # 20% chance to adjust severity
                issue["severity"] = max(1, min(5, issue["severity"] + random.choice([-1, 1])))

        return {"issues": issues}


class MockReviewerPool:
    """Mock reviewer pool that mimics real ReviewerPool behavior"""

    def __init__(self, review_pass: ReviewPass, num_reviewers: int,
                 api_client: MockAPIClient, style_only: bool = False):
        self.review_pass = review_pass
        self.num_reviewers = num_reviewers
        self.api_client = api_client
        self.style_only = style_only

        # Create reviewer configurations
        self.reviewers = self._create_reviewers()

    def _create_reviewers(self) -> List[Dict]:
        """Create reviewer configurations based on pass type"""
        reviewers = []

        if self.style_only:
            # Copy edit passes - only style reviewers
            for i in range(self.num_reviewers):
                reviewers.append({
                    "id": f"style_reviewer_{i}",
                    "focus": "style",
                    "competency": random.choice(["Mechanical Compliance", "Consistency"])
                })
        else:
            # Content passes - mix of specialists and generalists
            # 60% specialists (rubric-focused)
            specialist_count = int(self.num_reviewers * 0.6)
            competencies = [
                "Pedagogical Flow", "Structural Integrity", "Conceptual Clarity",
                "Assessment Quality", "Mechanical Compliance"
            ]

            for i in range(specialist_count):
                reviewers.append({
                    "id": f"specialist_{i}",
                    "focus": "specialist",
                    "competency": competencies[i % len(competencies)]
                })

            # 40% generalists
            for i in range(self.num_reviewers - specialist_count):
                reviewers.append({
                    "id": f"generalist_{i}",
                    "focus": "general",
                    "competency": None
                })

        return reviewers

    async def review_parallel(self, module) -> List[ReviewFeedback]:
        """Run reviews in parallel and return feedback list"""
        tasks = []
        for reviewer in self.reviewers:
            tasks.append(self._review_single(module, reviewer))

        results = await asyncio.gather(*tasks)
        return results

    async def _review_single(self, module, reviewer_config) -> ReviewFeedback:
        """Perform single review"""
        response = await self.api_client.get_review(module.content, reviewer_config)

        feedback_items = []
        for issue in response["issues"]:
            # Determine role based on competency type
            competency = reviewer_config.get("competency", "")
            if competency in ["Structural Integrity", "Pedagogical Flow", "Conceptual Clarity",
                             "Assessment Quality", "Student Engagement"]:
                role = ReviewerRole.AUTHORING
            else:
                role = ReviewerRole.STYLE

            feedback = ReviewFeedback(
                reviewer_id=reviewer_config["id"],
                issue_type=issue.get("issue_type", "general"),
                severity=issue["severity"],
                location=issue.get("location", ""),
                issue=issue["issue"],
                suggestion=issue.get("solution", ""),
                confidence_contribution=random.uniform(0.7, 0.95)  # Realistic confidence range
            )
            feedback_items.append(feedback)

        # Return all feedback items (flattened)
        return feedback_items

    async def review_parallel(self, module) -> List[ReviewFeedback]:
        """Run reviews in parallel and return flattened feedback list"""
        tasks = []
        for reviewer in self.reviewers:
            tasks.append(self._review_single(module, reviewer))

        nested_results = await asyncio.gather(*tasks)

        # Flatten the list of lists
        flat_results = []
        for items in nested_results:
            if isinstance(items, list):
                flat_results.extend(items)
            else:
                flat_results.append(items)

        return flat_results