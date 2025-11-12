"""
Synthetic actors that simulate human behavior in the workflow
These handle author revisions and human reviewer decisions
"""

import re
import random
from typing import List, Dict, Any
import sys
from pathlib import Path

# Import models from real system
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))
from CODE.models import ModuleContent, ReviewReport


class SyntheticAuthor:
    """Simulates an author responding to feedback"""

    def __init__(self):
        self.revision_count = 0
        self.copy_edit_count = 0

    def revise_module(self, module: ModuleContent, report: ReviewReport,
                      revision_round: int) -> ModuleContent:
        """Simulate author revising module based on feedback"""
        content = module.content
        self.revision_count = 0

        # Get high-priority issues
        matrix = report.get_priority_matrix()
        critical_issues = matrix.get('immediate', [])
        important_issues = matrix.get('important', [])

        # Address critical issues (90% compliance)
        for issue in critical_issues:
            if random.random() < 0.9:  # 90% chance to fix critical issues
                content = self._apply_fix(content, issue)
                self.revision_count += 1

        # Address important issues (70% compliance)
        for issue in important_issues[:5]:  # Fix up to 5 important issues
            if random.random() < 0.7:  # 70% chance to fix important issues
                content = self._apply_fix(content, issue)
                self.revision_count += 1

        # Add learning objectives if missing
        if any("objective" in str(issue.issue).lower() for issue in critical_issues):
            if "learning objective" not in content.lower():
                intro_end = content.find("\n##")
                if intro_end > 0:
                    learning_obj = "\n## Learning Objectives\n\nBy the end of this module, you will:\n"
                    learning_obj += "- Understand fundamental data structures and their properties\n"
                    learning_obj += "- Know when to use arrays vs linked lists vs trees\n"
                    learning_obj += "- Be able to analyze time and space complexity\n"
                    learning_obj += "- Implement basic operations for each data structure\n"
                    content = content[:intro_end] + learning_obj + content[intro_end:]
                    self.revision_count += 1

        # Add conclusion if missing
        if any("conclusion" in str(issue.issue).lower() for issue in important_issues):
            if "conclusion" not in content.lower():
                conclusion = "\n\n## Conclusion\n\n"
                conclusion += "In this module, we explored fundamental data structures including arrays, "
                conclusion += "linked lists, trees, and hash tables. Each structure has unique properties "
                conclusion += "that make it suitable for different use cases.\n\n"
                conclusion += "Key takeaways:\n"
                conclusion += "- Arrays provide O(1) access but expensive insertion/deletion\n"
                conclusion += "- Linked lists excel at insertion/deletion but have O(n) access\n"
                conclusion += "- Trees offer logarithmic operations when balanced\n"
                conclusion += "- Hash tables provide near-constant time operations on average\n\n"
                conclusion += "Continue practicing with the provided problems to master these concepts."
                content += conclusion
                self.revision_count += 1

        # Fix some contractions
        contractions_map = {
            "we'll": "we will",
            "you'll": "you will",
            "don't": "do not",
            "won't": "will not",
            "can't": "cannot",
            "we've": "we have",
            "they're": "they are",
            "it's": "it is"
        }

        for contraction, replacement in contractions_map.items():
            if contraction in content.lower():
                # Case-insensitive replacement
                pattern = re.compile(re.escape(contraction), re.IGNORECASE)
                content = pattern.sub(replacement, content)
                self.revision_count += 1

        return ModuleContent(
            content=content,
            module_id=module.module_id,
            title=module.title,
            author=module.author
        )

    def _apply_fix(self, content: str, issue) -> str:
        """Apply a fix for a specific issue"""
        issue_text = str(issue.issue).lower() if hasattr(issue, 'issue') else str(issue).lower()

        # Simulate various fixes based on issue type
        if "binary search tree" in issue_text and "before" in issue_text:
            # Reorder BST section
            if "## Binary Search Trees" in content and "## Binary Trees" in content:
                # Simple reordering simulation
                parts = content.split("## Binary Search Trees")
                if len(parts) == 2:
                    bst_section = "## Binary Search Trees" + parts[1].split("\n##")[0]
                    remaining = "\n##".join(parts[1].split("\n##")[1:]) if "\n##" in parts[1] else ""
                    content = parts[0] + remaining + "\n" + bst_section

        elif "complexity analysis" in issue_text:
            # Move complexity discussion later
            complexity_mentions = re.finditer(r'O\([^)]+\)', content)
            # This would be complex to fix properly, so simulate partial fix
            pass

        return content

    def apply_copy_edits(self, module: ModuleContent, report: ReviewReport) -> ModuleContent:
        """Apply style and mechanical corrections"""
        content = module.content
        self.copy_edit_count = 0

        # Get style issues
        all_issues = report.consensus_results

        for issue in all_issues:
            if hasattr(issue, 'issue_type'):
                if "style" in issue.issue_type or "mechanical" in issue.issue_type:
                    if random.random() < 0.85:  # 85% fix rate for style issues
                        content = self._apply_style_fix(content, issue)
                        self.copy_edit_count += 1

        # Fix remaining contractions more thoroughly
        content = self._fix_all_contractions(content)

        # Fix imperative voice
        content = self._fix_imperative_voice(content)

        return ModuleContent(
            content=content,
            module_id=module.module_id,
            title=module.title,
            author=module.author
        )

    def _apply_style_fix(self, content: str, issue) -> str:
        """Apply style-specific fixes"""
        issue_text = str(issue.issue).lower()

        if "contraction" in issue_text:
            # Already handled in _fix_all_contractions
            pass
        elif "imperative" in issue_text:
            # Already handled in _fix_imperative_voice
            pass
        elif "consistency" in issue_text:
            # Fix code block formatting
            content = content.replace("```Python", "```python")

        return content

    def _fix_all_contractions(self, content: str) -> str:
        """Thoroughly fix all contractions"""
        replacements = {
            "We'll": "We will",
            "we'll": "we will",
            "You'll": "You will",
            "you'll": "you will",
            "don't": "do not",
            "Don't": "Do not",
            "won't": "will not",
            "Won't": "Will not",
            "can't": "cannot",
            "Can't": "Cannot",
            "we've": "we have",
            "We've": "We have",
            "they're": "they are",
            "They're": "They are",
            "it's": "it is",
            "It's": "It is",
            "you're": "you are",
            "You're": "You are"
        }

        for contraction, replacement in replacements.items():
            content = content.replace(contraction, replacement)

        return content

    def _fix_imperative_voice(self, content: str) -> str:
        """Convert imperative voice to declarative"""
        replacements = {
            "Try these problems:": "The following problems provide practice:",
            "Remember -": "It is important to note that",
            "Think of": "Consider",
            "Look at": "Examining",
            "Let's look at": "The following section examines",
            "Let's": "This section will"
        }

        for imperative, declarative in replacements.items():
            content = content.replace(imperative, declarative)

        return content

    def get_revision_count(self) -> int:
        """Get count of revisions made"""
        return self.revision_count

    def get_copy_edit_count(self) -> int:
        """Get count of copy edits made"""
        return self.copy_edit_count


class SyntheticHumanReviewer:
    """Simulates human reviewer decisions"""

    def review_content_passes(self, pass1_report: ReviewReport,
                              pass2_report: ReviewReport,
                              module: ModuleContent) -> Dict[str, Any]:
        """Simulate human review of content passes"""

        # Analyze improvement
        pass1_count = len(pass1_report.consensus_results)
        pass2_count = len(pass2_report.consensus_results)
        improvement_rate = (pass1_count - pass2_count) / pass1_count if pass1_count > 0 else 1.0

        # Get remaining critical issues
        matrix = pass2_report.get_priority_matrix()
        critical_remaining = len(matrix.get('immediate', []))

        decision = {
            "decision": "PROCEED" if critical_remaining <= 1 else "NEEDS_WORK",
            "approved_issues": [],
            "disputes_resolved": [],
            "additional_feedback": []
        }

        # Simulate reviewing and approving/disputing issues
        for issue in pass2_report.consensus_results[:10]:  # Review top 10 issues
            if hasattr(issue, 'severity'):
                if issue.severity >= 4:
                    # Critical issues - usually approved
                    if random.random() < 0.9:
                        decision["approved_issues"].append(str(issue.issue))
                    else:
                        # Occasionally dispute
                        decision["disputes_resolved"].append({
                            "issue": str(issue.issue),
                            "resolution": "Not applicable to this module type"
                        })
                else:
                    # Lower severity - more likely to dismiss
                    if random.random() < 0.6:
                        decision["approved_issues"].append(str(issue.issue))

        # Add human insight
        if improvement_rate > 0.7:
            decision["additional_feedback"].append(
                "Excellent response to initial feedback. Module shows significant improvement."
            )
        elif improvement_rate > 0.4:
            decision["additional_feedback"].append(
                "Good progress, but some core issues remain. Consider additional revision."
            )
        else:
            decision["additional_feedback"].append(
                "Limited improvement observed. Recommend closer review of feedback."
            )

        return decision

    def final_copy_approval(self, pass3_report: ReviewReport,
                            pass4_report: ReviewReport,
                            module: ModuleContent) -> Dict[str, Any]:
        """Simulate final copy editor approval"""

        # Check remaining issues
        remaining_issues = len(pass4_report.consensus_results)

        decision = {
            "decision": "APPROVED" if remaining_issues <= 3 else "NEEDS_REVISION",
            "remaining_concerns": [],
            "final_notes": []
        }

        # Review remaining issues
        for issue in pass4_report.consensus_results:
            if hasattr(issue, 'severity') and issue.severity >= 3:
                decision["remaining_concerns"].append(str(issue.issue))

        # Add final assessment
        if remaining_issues == 0:
            decision["final_notes"].append(
                "Perfect! All style issues have been resolved."
            )
        elif remaining_issues <= 3:
            decision["final_notes"].append(
                "Minor style issues remain but are acceptable for publication."
            )
        else:
            decision["final_notes"].append(
                f"{remaining_issues} style issues remain. Additional copy editing required."
            )
            decision["reason"] = "Too many mechanical errors for publication"

        return decision