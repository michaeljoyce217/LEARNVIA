#!/usr/bin/env python3
"""
Main demo orchestrator for Learnvia review system.
Demonstrates consensus-based aggregation of feedback from 60 AI agents.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Add paths for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mock_agents import MockAgentSystem
from synthetic_author import SyntheticAuthor
from synthetic_reviewer import SyntheticReviewer, SyntheticCopyEditor
from generate_demo_report import DemoReportGenerator

# Import the consensus aggregator
from src.aggregator import ConsensusAggregator
from src.models import (
    ReviewFeedback, ConsensusResult, ReviewReport,
    ReviewPass, SeverityLevel, ModuleContent
)


class LearnviaDemoOrchestrator:
    """Orchestrates the complete Learnvia review demo workflow with consensus aggregation."""

    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.content_path = self.base_path / "sample_content"
        self.outputs_path = self.base_path / "outputs"
        self.actors_path = self.base_path / "synthetic_actors"

        # Create outputs directory if it doesn't exist
        self.outputs_path.mkdir(exist_ok=True)

        # Initialize systems
        self.agent_system = MockAgentSystem()
        self.aggregator = ConsensusAggregator(similarity_threshold=0.75)
        self.author = SyntheticAuthor(str(self.actors_path / "author_persona.json"))
        self.reviewer = SyntheticReviewer(str(self.actors_path / "reviewer_persona.json"))
        self.copy_editor = SyntheticCopyEditor(str(self.actors_path / "copy_editor_persona.json"))
        self.report_generator = DemoReportGenerator()

        # Track workflow data
        self.workflow_data = {
            "start_time": datetime.now().isoformat(),
            "passes": [],
            "consensus_tracking": {
                "high_confidence_issues": 0,
                "low_confidence_issues": 0,
                "total_individual_findings": 0,
                "aggregated_issues": 0
            },
            "statistics": {
                "total_issues_found": 0,
                "total_issues_fixed": 0,
                "issues_by_pass": {}
            }
        }

    def run_complete_demo(self):
        """Run the complete demo workflow with consensus aggregation."""
        print("\n" + "="*80)
        print("LEARNVIA CONSENSUS-BASED REVIEW SYSTEM DEMO")
        print("="*80)
        print(f"\nStarting demo at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n🤖 System: 60 AI agents with consensus aggregation")
        print("📊 Approach: Multiple agents review → Consensus synthesis → Unified feedback\n")

        # Load original draft
        print("📄 Loading original draft (Power Rule topic with intentional issues)...")
        original_content = self._load_original_draft()
        current_content = original_content
        module = ModuleContent(content=current_content, module_id="power_rule_demo", title="The Power Rule")

        # PASS 1: Initial Review with Consensus
        print("\n" + "-"*60)
        print("🔍 PASS 1: Initial Review (20 independent agents)")
        print("-"*60)
        consensus_results_1, pass1_data = self._run_pass_with_consensus(
            current_content, module, 1, ReviewPass.CONTENT_PASS_1
        )

        # Author Revision after Pass 1
        print("\n📝 Author revising based on consensus feedback...")
        current_content = self._author_revision_consensus(current_content, consensus_results_1, 1)
        self._save_content(current_content, "draft_v2_after_pass1.md")

        # PASS 2: Second Review with Consensus
        print("\n" + "-"*60)
        print("🔍 PASS 2: Second Review (Different 20 independent agents)")
        print("-"*60)
        consensus_results_2, pass2_data = self._run_pass_with_consensus(
            current_content, module, 2, ReviewPass.CONTENT_PASS_2
        )

        # Author Revision after Pass 2
        print("\n📝 Author revising based on consensus feedback...")
        current_content = self._author_revision_consensus(current_content, consensus_results_2, 2)
        self._save_content(current_content, "draft_v3_after_pass2.md")

        # Human Reviewer Decision
        print("\n" + "-"*60)
        print("👤 HUMAN REVIEW: Content Review")
        print("-"*60)
        reviewer_decision = self._human_review_consensus(current_content, consensus_results_2, 2)

        if reviewer_decision["ready_for_copy_edit"]:
            print("✅ Approved for copy editing")

            # PASS 3: Copy Edit with Consensus
            print("\n" + "-"*60)
            print("✏️ PASS 3: Copy Editing (10 strict style agents)")
            print("-"*60)
            consensus_results_3, pass3_data = self._run_pass_with_consensus(
                current_content, module, 3, ReviewPass.COPY_PASS_1
            )

            # Copy Editor Review
            print("\n👤 COPY EDITOR REVIEW (EXTREMELY STRICT)")
            copy_edit_decision = self._copy_editor_review_consensus(current_content, consensus_results_3, 3)

            if not copy_edit_decision["final_approval"]:
                # Fix remaining issues
                print("\n📝 Making final corrections based on consensus...")
                current_content = self._apply_copy_edits_consensus(current_content, consensus_results_3)
                self._save_content(current_content, "draft_v4_after_copy_edit.md")

                # PASS 4: Final Copy Edit with Consensus
                print("\n" + "-"*60)
                print("✏️ PASS 4: Final Copy Edit (Different 10 strict style agents)")
                print("-"*60)
                consensus_results_4, pass4_data = self._run_pass_with_consensus(
                    current_content, module, 4, ReviewPass.COPY_PASS_2
                )

                # Final Copy Editor Approval
                print("\n👤 FINAL COPY EDITOR REVIEW (ZERO TOLERANCE)")
                final_decision = self._copy_editor_review_consensus(current_content, consensus_results_4, 4)

                if final_decision["final_approval"]:
                    print("✅ APPROVED FOR PUBLICATION")
                else:
                    print("❌ STILL HAS ISSUES - Would require another iteration")

                self._save_content(current_content, "draft_v5_final.md")

        # Generate comprehensive report
        print("\n" + "-"*60)
        print("📊 Generating comprehensive consensus report...")
        print("-"*60)
        self._generate_final_report()

        print("\n" + "="*80)
        print("✨ DEMO COMPLETE!")
        print("="*80)
        print(f"\nOutputs saved to: {self.outputs_path}")
        print("\n🔑 Key Consensus Metrics:")
        print(f"  - Total individual findings: {self.workflow_data['consensus_tracking']['total_individual_findings']}")
        print(f"  - Aggregated consensus issues: {self.workflow_data['consensus_tracking']['aggregated_issues']}")
        print(f"  - High confidence issues: {self.workflow_data['consensus_tracking']['high_confidence_issues']}")
        print(f"  - Low confidence issues: {self.workflow_data['consensus_tracking']['low_confidence_issues']}")
        print("\n📁 Files generated:")
        print("  - consensus_report.html (comprehensive HTML report)")
        print("  - consensus_report.md (markdown summary)")
        print("  - pass_*_consensus.json (consensus data per pass)")
        print("  - pass_*_individual.json (individual agent feedback)")
        print("  - draft versions in sample_content/")

    def _load_original_draft(self) -> str:
        """Load the original draft content."""
        draft_path = self.content_path / "draft_v1_original.md"
        with open(draft_path, 'r') as f:
            return f.read()

    def _save_content(self, content: str, filename: str):
        """Save content to file."""
        filepath = self.content_path / filename
        with open(filepath, 'w') as f:
            f.write(content)

    def _run_pass_with_consensus(self, content: str, module: ModuleContent,
                                pass_number: int, review_pass: ReviewPass) -> Tuple[List[ConsensusResult], Dict]:
        """Run a review pass with consensus aggregation."""

        # Step 1: Get individual feedback from all agents
        print(f"  📥 Collecting feedback from agents...")
        individual_feedback = self.agent_system.analyze_content(content, pass_number)

        # Track individual findings
        self.workflow_data["consensus_tracking"]["total_individual_findings"] += len(individual_feedback)

        # Save individual feedback for transparency
        individual_file = self.outputs_path / f"pass_{pass_number}_individual.json"
        with open(individual_file, 'w') as f:
            json.dump([f.to_dict() for f in individual_feedback], f, indent=2, default=str)

        print(f"  🔢 Received {len(individual_feedback)} individual findings from agents")

        # Step 2: Aggregate feedback into consensus
        print(f"  🤝 Aggregating feedback to find consensus...")
        consensus_results = self.aggregator.aggregate(individual_feedback)

        # Track aggregated results
        self.workflow_data["consensus_tracking"]["aggregated_issues"] += len(consensus_results)

        # Step 3: Filter by confidence threshold
        high_confidence = self.aggregator.filter_by_confidence(consensus_results, threshold=0.7)
        medium_confidence = self.aggregator.filter_by_confidence(consensus_results, threshold=0.4)
        low_confidence = [r for r in consensus_results if r.confidence < 0.4]

        self.workflow_data["consensus_tracking"]["high_confidence_issues"] += len(high_confidence)
        self.workflow_data["consensus_tracking"]["low_confidence_issues"] += len(low_confidence)

        print(f"  ✅ Consensus achieved on {len(consensus_results)} unique issues:")
        print(f"     - High confidence (≥70% agreement): {len(high_confidence)} issues")
        print(f"     - Medium confidence (40-70%): {len([r for r in medium_confidence if r.confidence < 0.7])} issues")
        print(f"     - Low confidence (<40%): {len(low_confidence)} issues")

        # Step 4: Generate report from consensus
        report = self.aggregator.generate_report(
            consensus_results,
            module.module_id,
            review_pass
        )

        # Save consensus data
        consensus_file = self.outputs_path / f"pass_{pass_number}_consensus.json"
        with open(consensus_file, 'w') as f:
            f.write(report.to_json())

        # Display top issues
        print(f"\n  📋 Top Consensus Issues (by priority):")
        top_issues = sorted(consensus_results, key=lambda r: r.get_priority_score(), reverse=True)[:5]
        for i, issue in enumerate(top_issues, 1):
            confidence_pct = issue.confidence * 100
            print(f"     {i}. [{issue.severity}/5 severity, {confidence_pct:.0f}% agreement] {issue.issue[:60]}...")

        # Update workflow data
        self.workflow_data["statistics"]["total_issues_found"] += len(consensus_results)
        self.workflow_data["statistics"]["issues_by_pass"][pass_number] = len(consensus_results)

        # Prepare data for report generator
        pass_data = {
            "individual_feedback_count": len(individual_feedback),
            "consensus_issues": len(consensus_results),
            "confidence_breakdown": {
                "high": len(high_confidence),
                "medium": len([r for r in medium_confidence if r.confidence < 0.7]),
                "low": len(low_confidence)
            },
            "top_issues": [
                {
                    "issue": issue.issue,
                    "severity": issue.severity,
                    "confidence": f"{issue.confidence:.1%}",
                    "agreeing_agents": f"{issue.agreeing_reviewers}/{issue.total_reviewers}",
                    "location": issue.location,
                    "suggestions": issue.suggestions[:2] if issue.suggestions else []
                }
                for issue in top_issues
            ],
            "decision": self._determine_decision(consensus_results, pass_number)
        }

        self.report_generator.add_pass_data(pass_number, pass_data)

        return consensus_results, pass_data

    def _determine_decision(self, consensus_results: List[ConsensusResult], pass_number: int) -> str:
        """Determine the decision based on consensus results."""
        critical_count = len([r for r in consensus_results if r.severity >= 5 and r.confidence >= 0.7])
        high_count = len([r for r in consensus_results if r.severity >= 4 and r.confidence >= 0.7])

        if critical_count > 0:
            return "CRITICAL ISSUES - Must fix before proceeding"
        elif high_count > 3:
            return "MULTIPLE HIGH-PRIORITY ISSUES - Significant revision needed"
        elif high_count > 0:
            return "SOME IMPORTANT ISSUES - Revision recommended"
        elif len(consensus_results) > 10:
            return "MANY MINOR ISSUES - Clean up needed"
        elif pass_number > 2:
            return "STYLE ISSUES FOUND - Copy editing required"
        else:
            return "READY FOR NEXT PHASE"

    def _author_revision_consensus(self, content: str, consensus_results: List[ConsensusResult],
                                  pass_number: int) -> str:
        """Simulate author revision based on consensus feedback."""
        # Convert consensus results to feedback format for author
        high_priority = [r for r in consensus_results if r.confidence >= 0.7 and r.severity >= 3]

        print(f"  📝 Author addressing {len(high_priority)} high-priority consensus issues...")

        # Simulate fixes (in real system, author would manually revise)
        fixed_count = 0
        revised_content = content

        # Fix critical mathematical errors
        for result in consensus_results:
            if result.severity >= 5 and result.confidence >= 0.9:
                if "x^n-1 should be x^(n-1)" in result.issue:
                    revised_content = revised_content.replace("d/dx(x^n) = n * x^n-1",
                                                              "d/dx(x^n) = nx^(n-1)")
                    fixed_count += 1
                elif "n*x^(n+1) instead of nx^(n-1)" in result.issue:
                    revised_content = revised_content.replace("d/dx(x^n) = n * x^(n+1)",
                                                              "d/dx(x^n) = nx^(n-1)")
                    fixed_count += 1
                elif "3x^3" in result.issue:
                    revised_content = revised_content.replace("Multiply by 3: 3x^3",
                                                              "Multiply by 3 and reduce exponent by 1")
                    fixed_count += 1

        # Fix some high-confidence style issues if in later passes
        if pass_number >= 2:
            for result in consensus_results:
                if result.confidence >= 0.8 and "contraction" in result.issue_type.lower():
                    # Fix a few contractions
                    replacements = [
                        ("don't", "do not"),
                        ("it's", "it is"),
                        ("let's", "let us"),
                        ("won't", "will not")
                    ]
                    for old, new in replacements[:3]:  # Fix first 3
                        if old in revised_content:
                            revised_content = revised_content.replace(old, new, 1)
                            fixed_count += 1
                            break

        # Save revision summary
        with open(self.outputs_path / f"author_revision_{pass_number}_consensus.txt", 'w') as f:
            f.write(f"CONSENSUS-BASED REVISION SUMMARY - PASS {pass_number}\n")
            f.write(f"{'='*60}\n\n")
            f.write(f"Total consensus issues: {len(consensus_results)}\n")
            f.write(f"High-priority issues: {len(high_priority)}\n")
            f.write(f"Issues addressed: {fixed_count}\n\n")
            f.write("Top issues by consensus:\n")
            for i, result in enumerate(high_priority[:10], 1):
                f.write(f"\n{i}. [{result.severity}/5, {result.confidence:.1%} agreement]\n")
                f.write(f"   Issue: {result.issue}\n")
                f.write(f"   Location: {result.location}\n")
                if result.suggestions:
                    f.write(f"   Suggestion: {result.suggestions[0]}\n")

        self.workflow_data["statistics"]["total_issues_fixed"] += fixed_count

        print(f"  ✅ Author fixed {fixed_count}/{len(high_priority)} high-priority issues")

        return revised_content

    def _human_review_consensus(self, content: str, consensus_results: List[ConsensusResult],
                               pass_number: int) -> Dict:
        """Simulate human reviewer decision based on consensus."""
        # Human focuses on high-confidence issues
        high_confidence = [r for r in consensus_results if r.confidence >= 0.7]
        critical_issues = [r for r in high_confidence if r.severity >= 5]

        review = {
            "reviewer": "Dr. Emily Chen",
            "timestamp": datetime.now().isoformat(),
            "consensus_issues_reviewed": len(high_confidence),
            "critical_issues": len(critical_issues),
            "decision": "APPROVE_FOR_COPY_EDIT" if len(critical_issues) == 0 else "REQUEST_REVISION",
            "ready_for_copy_edit": len(critical_issues) == 0,
            "comments": []
        }

        if critical_issues:
            review["comments"].append(f"Found {len(critical_issues)} critical issues with high consensus")
        else:
            review["comments"].append("No critical issues found. Content is pedagogically sound.")

        review["comments"].append(f"Reviewed {len(high_confidence)} high-confidence consensus issues")

        # Save review report
        with open(self.outputs_path / f"human_review_consensus_{pass_number}.txt", 'w') as f:
            f.write("HUMAN REVIEWER CONSENSUS-BASED DECISION\n")
            f.write("="*60 + "\n\n")
            f.write(f"Reviewer: {review['reviewer']}\n")
            f.write(f"Date: {review['timestamp']}\n")
            f.write(f"Consensus issues reviewed: {review['consensus_issues_reviewed']}\n")
            f.write(f"Critical issues: {review['critical_issues']}\n")
            f.write(f"Decision: {review['decision']}\n\n")
            f.write("Comments:\n")
            for comment in review['comments']:
                f.write(f"  - {comment}\n")

        print(f"  Reviewer: {review['reviewer']}")
        print(f"  Consensus issues reviewed: {review['consensus_issues_reviewed']}")
        print(f"  Decision: {review['decision']}")

        return review

    def _copy_editor_review_consensus(self, content: str, consensus_results: List[ConsensusResult],
                                     pass_number: int) -> Dict:
        """Simulate extremely strict copy editor review based on consensus."""
        # Copy editor is EXTREMELY strict - looks at ALL issues
        style_issues = [r for r in consensus_results
                       if "contraction" in r.issue_type or "voice" in r.issue_type
                       or "formatting" in r.issue_type]

        high_conf_style = [r for r in style_issues if r.confidence >= 0.7]

        review = {
            "editor": "Dr. Margaret Thompson (ZERO TOLERANCE)",
            "timestamp": datetime.now().isoformat(),
            "style_violations_found": len(style_issues),
            "high_confidence_violations": len(high_conf_style),
            "decision": "REJECT - VIOLATIONS FOUND" if high_conf_style else "APPROVED",
            "final_approval": len(high_conf_style) == 0,
            "requirements": [
                "ZERO contractions allowed",
                "NO imperative voice permitted",
                "PERFECT LaTeX formatting required",
                "ABSOLUTE consistency mandatory"
            ],
            "verdict": "NOT ACCEPTABLE" if high_conf_style else "ACCEPTABLE"
        }

        # Save report
        with open(self.outputs_path / f"copy_editor_consensus_{pass_number}.txt", 'w') as f:
            f.write("COPY EDITOR CONSENSUS REVIEW - EXTREMELY STRICT\n")
            f.write("="*60 + "\n\n")
            f.write(f"Editor: {review['editor']}\n")
            f.write(f"Standards: ZERO TOLERANCE FOR ANY VIOLATION\n\n")
            f.write(f"Consensus style violations found: {review['style_violations_found']}\n")
            f.write(f"High-confidence violations: {review['high_confidence_violations']}\n")
            f.write(f"Decision: {review['decision']}\n")
            f.write(f"Verdict: {review['verdict']}\n\n")
            f.write("Requirements:\n")
            for req in review['requirements']:
                f.write(f"  ✓ {req}\n")

            if high_conf_style:
                f.write("\nVIOLATIONS REQUIRING CORRECTION:\n")
                for i, issue in enumerate(high_conf_style[:10], 1):
                    f.write(f"\n{i}. [{issue.confidence:.0%} consensus] {issue.issue}\n")
                    f.write(f"   Location: {issue.location}\n")

        print(f"  Editor: {review['editor']}")
        print(f"  Violations found (consensus): {review['style_violations_found']}")
        print(f"  Decision: {review['decision']}")

        return review

    def _apply_copy_edits_consensus(self, content: str, consensus_results: List[ConsensusResult]) -> str:
        """Apply copy edits based on consensus feedback."""
        # Focus on high-consensus style issues
        style_issues = [r for r in consensus_results
                       if r.confidence >= 0.8 and
                       ("contraction" in r.issue_type or "voice" in r.issue_type)]

        revised = content
        fixes_applied = 0

        # Fix all contractions with high consensus
        contraction_fixes = {
            "don't": "do not", "doesn't": "does not", "won't": "will not",
            "can't": "cannot", "let's": "let us", "it's": "it is",
            "isn't": "is not", "aren't": "are not", "we'll": "we will",
            "you'll": "you will", "they'll": "they will", "we're": "we are"
        }

        for old, new in contraction_fixes.items():
            if old in revised:
                revised = revised.replace(old, new)
                fixes_applied += 1
            if old.capitalize() in revised:
                revised = revised.replace(old.capitalize(), new.capitalize())
                fixes_applied += 1

        print(f"  Applied {fixes_applied} consensus-based copy edits")

        return revised

    def _generate_final_report(self):
        """Generate the final comprehensive report."""
        # Calculate final statistics
        total_found = self.workflow_data["statistics"]["total_issues_found"]
        total_fixed = self.workflow_data["statistics"]["total_issues_fixed"]

        self.report_generator.report_data["statistics"] = {
            "total_issues_found": total_found,
            "total_issues_fixed": total_fixed,
            "fix_rate": (total_fixed / total_found * 100) if total_found > 0 else 0,
            "issues_by_pass": self.workflow_data["statistics"]["issues_by_pass"],
            "consensus_metrics": self.workflow_data["consensus_tracking"]
        }

        # Generate reports with consensus focus
        self.report_generator.generate_html_report(str(self.outputs_path / "consensus_report.html"))
        self.report_generator.generate_markdown_report(str(self.outputs_path / "consensus_report.md"))

        # Save raw workflow data
        with open(self.outputs_path / "workflow_consensus_data.json", 'w') as f:
            json.dump(self.workflow_data, f, indent=2, default=str)

        print("  ✅ Consensus reports generated successfully")


def main():
    """Main entry point."""
    orchestrator = LearnviaDemoOrchestrator()
    orchestrator.run_complete_demo()


if __name__ == "__main__":
    main()