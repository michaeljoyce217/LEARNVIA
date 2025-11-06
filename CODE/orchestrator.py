"""
Main orchestration module for the Learnvia AI revision system.
Coordinates the 4-pass review process with 60 AI reviewers.
"""

import asyncio
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import os
import json

from .models import (
    ModuleContent, ReviewSession, ReviewPass,
    ReviewReport, ReviewFeedback
)
from .reviewers import ReviewerPool, APIClient, get_project_root
from .aggregator import ConsensusAggregator
from .report_generator import ReportGenerator


class RevisionOrchestrator:
    """Orchestrates the complete AI revision process."""

    def __init__(self, api_key: Optional[str] = None,
                 output_dir: str = None):
        """Initialize the orchestrator."""
        if output_dir is None:
            output_dir = str(get_project_root() / "reports")
        self.api_client = APIClient(api_key)
        self.aggregator = ConsensusAggregator()
        self.report_generator = ReportGenerator()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Define reviewer counts for 4-pass system
        self.reviewer_counts = {
            ReviewPass.CONTENT_PASS_1: 20,  # Mixed content + style
            ReviewPass.CONTENT_PASS_2: 20,  # Different 20 agents, independent
            ReviewPass.COPY_PASS_1: 10,     # Pure style/mechanical
            ReviewPass.COPY_PASS_2: 10      # Different 10 agents, independent
        }

    async def run_complete_review_async(self, module: ModuleContent,
                                       author_experience: str = "new") -> ReviewSession:
        """Run the complete 4-pass review process with author resubmit between passes.

        PASS 1: 20 agents review content + style (independent)
        → Author revises and resubmits
        PASS 2: Different 20 agents review content + style (independent)
        → Human reviewer checkpoint (author can dispute, human has final say)
        → Feedback loop collects model failures

        PASS 3: 10 agents review copy edit only (independent)
        → Author revises and resubmits
        PASS 4: Different 10 agents review copy edit only (independent)
        → Human copy editor checkpoint (author can dispute, human has final say)
        → Feedback loop collects model failures
        """
        session = ReviewSession(module=module)

        print(f"\n{'='*70}")
        print(f"✨ Starting AI Review Session for Module: {module.module_id}")
        print(f"{'='*70}\n")

        # ==================== ROUND 1: CONTENT REVIEW ====================
        print("📚 ROUND 1: CONTENT & STYLE REVIEW")
        print("="*70)

        # PASS 1: Initial content review (20 agents)
        print("\n🔍 PASS 1: Initial Content & Style Review (20 independent agents)...")
        print("   10 agents: Pedagogical quality ONLY (authoring guidelines)")
        print("   10 agents: Writing mechanics ONLY (style guidelines)")
        pass1_report = await self._run_pass(
            module, ReviewPass.CONTENT_PASS_1, session, author_experience
        )
        self._save_report(pass1_report, "pass1_content")
        self._display_summary(pass1_report)

        # Author revision period
        print("\n⏸️  AUTHOR RESUBMIT: Address feedback from Pass 1")
        print("   Author revises content based on feedback and resubmits\n")

        # PASS 2: Second content review (different 20 agents, independent)
        print("🔍 PASS 2: Re-review Content & Style (20 DIFFERENT independent agents)...")
        print("   10 agents: Pedagogical quality ONLY (authoring guidelines)")
        print("   10 agents: Writing mechanics ONLY (style guidelines)")
        print("   Fresh review with NO knowledge of Pass 1 results")
        pass2_report = await self._run_pass(
            module, ReviewPass.CONTENT_PASS_2, session, author_experience
        )
        self._save_report(pass2_report, "pass2_content")
        self._display_summary(pass2_report)

        # Human reviewer checkpoint
        print("\n" + "="*70)
        print("👤 HUMAN REVIEWER CHECKPOINT")
        print("="*70)
        print("   • Author can dispute AI feedback via 'Dispute' button")
        print("   • Human reviewer validates disputes and makes final call")
        print("   • Author + Reviewer must agree before proceeding")
        print("   • Model failures fed back for system improvement")
        print("\n   ⏸️  Waiting for human review resolution...\n")

        # ==================== ROUND 2: COPY EDITING ====================
        print("📝 ROUND 2: COPY EDITING (Style/Mechanical Only)")
        print("="*70)

        # PASS 3: Initial copy edit (10 agents)
        print("\n🔍 PASS 3: Initial Copy Edit (10 independent agents)...")
        print("   Focus ONLY on style/mechanical issues (NO pedagogy)")
        pass3_report = await self._run_pass(
            module, ReviewPass.COPY_PASS_1, session, author_experience
        )
        self._save_report(pass3_report, "pass3_copy")
        self._display_summary(pass3_report)

        # Author revision period
        print("\n⏸️  AUTHOR RESUBMIT: Address feedback from Pass 3")
        print("   Author makes final style/mechanical corrections and resubmits\n")

        # PASS 4: Second copy edit (different 10 agents, independent)
        print("🔍 PASS 4: Re-review Copy Edit (10 DIFFERENT independent agents)...")
        print("   Fresh review with NO knowledge of Pass 3 results")
        pass4_report = await self._run_pass(
            module, ReviewPass.COPY_PASS_2, session, author_experience
        )
        self._save_report(pass4_report, "pass4_copy")
        self._display_summary(pass4_report)

        # Human copy editor checkpoint
        print("\n" + "="*70)
        print("👤 HUMAN COPY EDITOR CHECKPOINT")
        print("="*70)
        print("   • Author can dispute AI feedback via 'Dispute' button")
        print("   • Human copy editor validates disputes and makes final call")
        print("   • Author + Copy Editor must agree before finalizing")
        print("   • Model failures fed back for system improvement")

        # Final assessment
        print("\n" + "="*70)
        print("📋 FINAL ASSESSMENT")
        print("="*70)
        self._generate_final_assessment(pass4_report)

        session.complete_session()
        print(f"\n✅ All 4 passes completed in {session.get_duration_minutes():.1f} minutes")
        print(f"📊 Total API calls made: {session.api_calls_made}")
        print(f"   (Pass 1: 20 + Pass 2: 20 + Pass 3: 10 + Pass 4: 10 = 60 total)\n")

        return session

    def run_complete_review(self, module: ModuleContent,
                           author_experience: str = "new") -> ReviewSession:
        """Synchronous wrapper for complete review."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                self.run_complete_review_async(module, author_experience)
            )
        finally:
            loop.close()

    async def run_single_pass_async(self, module: ModuleContent,
                                   review_pass: ReviewPass,
                                   author_experience: str = "new") -> ReviewReport:
        """Run a single review pass."""
        session = ReviewSession(module=module)
        report = await self._run_pass(module, review_pass, session, author_experience)
        self._save_report(report, f"{review_pass.value}")
        return report

    def run_single_pass(self, module: ModuleContent,
                       review_pass: ReviewPass,
                       author_experience: str = "new") -> ReviewReport:
        """Synchronous wrapper for single pass."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                self.run_single_pass_async(module, review_pass, author_experience)
            )
        finally:
            loop.close()

    async def _run_pass(self, module: ModuleContent,
                       review_pass: ReviewPass,
                       session: ReviewSession,
                       author_experience: str,
                       previous_report: Optional[ReviewReport] = None) -> ReviewReport:
        """Run a single review pass."""
        session.current_pass = review_pass

        # Create reviewer pool
        num_reviewers = self.reviewer_counts[review_pass]
        pool = ReviewerPool(review_pass, num_reviewers, self.api_client)

        # Run reviews in parallel
        start_time = datetime.now()
        feedback_list = await pool.review_parallel(module)
        end_time = datetime.now()

        # Update session
        for feedback in feedback_list:
            session.add_feedback(feedback)
        session.api_calls_made += num_reviewers

        # Aggregate feedback
        consensus_results = self.aggregator.aggregate(feedback_list)

        # If this is a progress review, check improvement
        if previous_report and "progress" in review_pass.value:
            consensus_results = self._apply_adaptive_focus(
                consensus_results, previous_report
            )

        # Generate report
        report = self.aggregator.generate_report(
            consensus_results=consensus_results,
            module_id=module.module_id,
            review_pass=review_pass,
            strengths=self._identify_strengths(consensus_results, review_pass)
        )
        report.author_experience_level = author_experience

        session.add_report(report)

        print(f"   ✓ Completed in {(end_time - start_time).total_seconds():.1f} seconds")
        print(f"   ✓ {len(feedback_list)} pieces of feedback collected")
        print(f"   ✓ {len(consensus_results)} consensus issues identified")

        return report

    def _apply_adaptive_focus(self, current_results: List,
                             previous_report: ReviewReport) -> List:
        """Apply adaptive focusing based on previous pass results."""
        # Calculate improvement rate
        improvement_rate = self.aggregator.get_improvement_rate(
            previous_report.consensus_results,
            current_results
        )

        # Adjust focus based on improvement
        if improvement_rate >= 0.8:
            # High improvement - focus on polish
            print("   📈 High improvement detected - focusing on polish and refinement")
            return [r for r in current_results if r.severity <= 3]

        elif improvement_rate >= 0.5:
            # Moderate improvement - reinforce critical issues
            print("   📊 Moderate improvement - reinforcing important issues")
            return [r for r in current_results if r.severity >= 3]

        else:
            # Low improvement - focus on highest severity only
            print("   ⚠️  Low improvement - focusing on critical issues only")
            return [r for r in current_results if r.severity >= 4]

    def _identify_strengths(self, consensus_results: List,
                          review_pass: ReviewPass) -> List[str]:
        """Identify CONTENT strengths based on what's NOT in the issues.
        Focus on what the MODULE does well, not author evaluation.
        Returns top 3-5 'best hits' as per feedback guidelines."""
        strengths = []
        issue_types = set(r.issue_type for r in consensus_results if hasattr(r, 'issue_type'))

        if review_pass in [ReviewPass.CONTENT_PASS_1, ReviewPass.CONTENT_PASS_2]:
            # Content review checks BOTH pedagogy and style

            # Pedagogical strengths (focus on content quality)
            if "pedagogical_flow" not in issue_types:
                strengths.append("The content demonstrates excellent pedagogical flow for the target learner")
            if "missing_examples" not in issue_types:
                strengths.append("Examples effectively illustrate concepts in student-relevant ways")
            if "quiz_questions" not in issue_types:
                strengths.append("Assessment questions align well with learning objectives")
            if not any("chunk" in r.issue.lower() for r in consensus_results):
                strengths.append("Complex concepts are appropriately chunked for independent study")
            if "scaffolding" not in issue_types:
                strengths.append("The content builds complexity gradually and systematically")

            # Style strengths (also checked in content passes)
            if not any("contraction" in r.issue.lower() for r in consensus_results):
                strengths.append("The text maintains proper style conventions throughout")
            if not any("imperative" in r.issue.lower() for r in consensus_results):
                strengths.append("Instructions use appropriate declarative voice")

        else:  # ReviewPass.COPY_PASS_1 or ReviewPass.COPY_PASS_2
            # Copy edit is ONLY style/mechanical (focus on presentation quality)
            if not any("contraction" in r.issue.lower() for r in consensus_results):
                strengths.append("The text avoids contractions as required by style guide")
            if not any("imperative" in r.issue.lower() for r in consensus_results):
                strengths.append("The content uses proper declarative voice consistently")
            if not any("punctuation" in r.issue.lower() for r in consensus_results):
                strengths.append("Punctuation follows style guide conventions")
            if not any("latex" in r.issue.lower() for r in consensus_results):
                strengths.append("Mathematical notation is properly formatted in LaTeX")
            if not any("formatting" in r.issue.lower() for r in consensus_results):
                strengths.append("Formatting is consistent and professional throughout")

        if not any(r.severity >= 4 for r in consensus_results):
            strengths.append("The module contains no critical issues requiring immediate attention")

        if not strengths:
            strengths.append("The content provides a solid foundation for student learning")

        # Return top 3-5 strengths (feedback guideline)
        return strengths[:5]

    def _calculate_improvement(self, before: ReviewReport,
                              after: ReviewReport) -> float:
        """Calculate improvement between two reports."""
        return self.aggregator.get_improvement_rate(
            before.consensus_results,
            after.consensus_results
        )

    def _save_report(self, report: ReviewReport, filename_prefix: str):
        """Save report in multiple formats."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{filename_prefix}_{report.module_id}_{timestamp}"

        # Save text report
        text_path = os.path.join(self.output_dir, f"{base_name}.txt")
        with open(text_path, 'w') as f:
            f.write(self.report_generator.generate_text_report(report))

        # Save markdown report
        md_path = os.path.join(self.output_dir, f"{base_name}.md")
        with open(md_path, 'w') as f:
            f.write(self.report_generator.generate_markdown_report(report))

        # Save JSON report
        json_path = os.path.join(self.output_dir, f"{base_name}.json")
        with open(json_path, 'w') as f:
            f.write(report.to_json())

        # Save HTML report
        html_path = os.path.join(self.output_dir, f"{base_name}.html")
        with open(html_path, 'w') as f:
            f.write(self.report_generator.generate_html_report(report))

        print(f"   📁 Reports saved to {self.output_dir}")

    def _display_summary(self, report: ReviewReport):
        """Display a summary of the report."""
        matrix = report.get_priority_matrix()

        print("\n   Priority Summary:")
        print(f"   • 🔴 Critical: {len(matrix['immediate'])} issues")
        print(f"   • 🟠 Important: {len(matrix['important'])} issues")
        print(f"   • 🟡 Consider: {len(matrix['consider'])} issues")
        print(f"   • 🟢 Optional: {len(matrix['optional'])} issues")

        if report.strengths:
            print("\n   Strengths identified:")
            for strength in report.strengths[:3]:
                print(f"   ✓ {strength}")

    def _generate_final_assessment(self, final_report: ReviewReport):
        """Generate final assessment based on last report."""
        matrix = final_report.get_priority_matrix()

        total_critical = len(matrix['immediate'])
        total_important = len(matrix['important'])

        if total_critical == 0 and total_important == 0:
            print("✅ MODULE READY FOR HUMAN REVIEW")
            print("   Recommendation: Standard review recommended")
            print("   All major issues have been identified and documented")

        elif total_critical == 0 and total_important <= 3:
            print("⚠️ MODULE MOSTLY READY")
            print("   Recommendation: Review with mentoring focus")
            print(f"   {total_important} important issues remain for discussion")

        else:
            print("🔴 MODULE NEEDS ATTENTION")
            print("   Recommendation: Substantial support needed")
            print(f"   {total_critical} critical and {total_important} important issues remain")

        print(f"\n   Estimated remaining work: {final_report.estimated_revision_time} minutes")


class ModuleLoader:
    """Helper class to load modules from files."""

    @staticmethod
    def load_from_file(filepath: str, module_id: Optional[str] = None) -> ModuleContent:
        """Load a module from a text file."""
        with open(filepath, 'r') as f:
            content = f.read()

        if not module_id:
            module_id = os.path.basename(filepath).replace('.txt', '')

        # Extract title from content if possible
        title = ""
        lines = content.split('\n')
        if lines:
            title = lines[0].strip('#').strip()

        return ModuleContent(
            content=content,
            module_id=module_id,
            title=title
        )

    @staticmethod
    def load_from_json(json_path: str) -> ModuleContent:
        """Load a module from a JSON file."""
        with open(json_path, 'r') as f:
            data = json.load(f)

        return ModuleContent(
            content=data.get('content', ''),
            module_id=data.get('module_id', ''),
            title=data.get('title', ''),
            author=data.get('author', ''),
            components=data.get('components', {})
        )