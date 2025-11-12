#!/usr/bin/env python3
"""
Realistic 9-Step Workflow Demonstration
Uses actual CODE components with mock API responses
"""

import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
import logging

# Add parent directory to path for CODE imports
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

# Import REAL system components from CODE package
from CODE.orchestrator import RevisionOrchestrator, ModuleLoader
from CODE.models import ModuleContent, ReviewPass, ReviewReport
from CODE.aggregator import ConsensusAggregator
from CODE.report_generator import ReportGenerator

# Import our mock components
from mock_api_responses import MockAPIClient, MockReviewerPool
from synthetic_actors import SyntheticAuthor, SyntheticHumanReviewer

# Setup logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "workflow_execution.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RealisticWorkflowOrchestrator:
    """Orchestrates the realistic 9-step workflow demonstration"""

    def __init__(self):
        self.input_dir = Path(__file__).parent.parent / "input"
        self.output_dir = Path(__file__).parent.parent / "outputs"
        self.output_dir.mkdir(exist_ok=True)

        # Initialize real components with mock API
        self.mock_api = MockAPIClient()
        self.aggregator = ConsensusAggregator()
        self.report_generator = ReportGenerator()

        # Initialize synthetic actors for human steps
        self.author = SyntheticAuthor()
        self.human_reviewer = SyntheticHumanReviewer()

        # Track workflow state
        self.current_module = None
        self.workflow_history = []

    def log_step(self, step_num, description):
        """Log and display workflow step"""
        separator = "=" * 70
        logger.info(f"\n{separator}")
        logger.info(f"STEP {step_num}: {description}")
        logger.info(separator)
        self.workflow_history.append({
            "step": step_num,
            "description": description,
            "timestamp": datetime.now().isoformat()
        })

    async def run_complete_workflow(self):
        """Execute the complete 9-step workflow"""
        logger.info("Starting Realistic Workflow Demonstration")
        logger.info("This uses REAL system components with mock API responses")

        # Step 1: Author delivers module
        self.log_step(1, "Author Delivers Initial Module")
        self.current_module = self.load_initial_module()
        logger.info(f"Loaded module: {self.current_module.module_id}")
        logger.info(f"Content length: {len(self.current_module.content)} characters")

        # Step 2: Pass 1 Content Review (Real system)
        self.log_step(2, "Pass 1 Content Review - 30 Agents")
        pass1_report = await self.run_content_review(
            self.current_module,
            ReviewPass.CONTENT_PASS_1,
            "pass1_content"
        )
        logger.info(f"Pass 1 identified {len(pass1_report.consensus_results)} consensus issues")
        self.display_priority_summary(pass1_report)

        # Step 3: Author makes revisions
        self.log_step(3, "Author Reviews Feedback and Makes Revisions")
        revised_module = self.author.revise_module(
            self.current_module,
            pass1_report,
            revision_round=1
        )
        self.save_revision(revised_module, "revision1_module.md")
        logger.info(f"Author addressed {self.author.get_revision_count()} issues")
        self.current_module = revised_module

        # Step 4: Pass 2 Content Review (Real system, different agents)
        self.log_step(4, "Pass 2 Content Review - 30 Different Agents")
        pass2_report = await self.run_content_review(
            self.current_module,
            ReviewPass.CONTENT_PASS_2,
            "pass2_content"
        )
        logger.info(f"Pass 2 identified {len(pass2_report.consensus_results)} consensus issues")
        improvement = self.calculate_improvement(pass1_report, pass2_report)
        logger.info(f"Improvement from Pass 1: {improvement:.1f}%")

        # Step 5: Human reviewer reconciliation
        self.log_step(5, "Human Reviewer Checkpoint - Content Approval")
        human_decision = self.human_reviewer.review_content_passes(
            pass1_report,
            pass2_report,
            self.current_module
        )
        logger.info(f"Human reviewer decision: {human_decision['decision']}")
        logger.info(f"Approved issues: {len(human_decision['approved_issues'])}")
        logger.info(f"Disputed issues resolved: {len(human_decision['disputes_resolved'])}")

        # Step 6: Pass 3 Copy Edit (Real system)
        self.log_step(6, "Pass 3 Copy Edit - 8 Style Agents")
        pass3_report = await self.run_copy_edit(
            self.current_module,
            ReviewPass.COPY_PASS_1,
            "pass3_copy"
        )
        logger.info(f"Pass 3 identified {len(pass3_report.consensus_results)} style issues")

        # Step 7: Author makes copy edits
        self.log_step(7, "Author Makes Style Corrections")
        copy_edited_module = self.author.apply_copy_edits(
            self.current_module,
            pass3_report
        )
        self.save_revision(copy_edited_module, "revision2_module.md")
        logger.info(f"Author fixed {self.author.get_copy_edit_count()} style issues")
        self.current_module = copy_edited_module

        # Step 8: Pass 4 Final Copy Edit (Real system, different agents)
        self.log_step(8, "Pass 4 Final Copy Edit - 8 Different Agents")
        pass4_report = await self.run_copy_edit(
            self.current_module,
            ReviewPass.COPY_PASS_2,
            "pass4_copy"
        )
        logger.info(f"Pass 4 identified {len(pass4_report.consensus_results)} remaining issues")

        # Step 9: Human copy editor final check
        self.log_step(9, "Human Copy Editor Final Approval")
        final_decision = self.human_reviewer.final_copy_approval(
            pass3_report,
            pass4_report,
            self.current_module
        )
        logger.info(f"Copy editor decision: {final_decision['decision']}")

        if final_decision['decision'] == "APPROVED":
            self.save_revision(self.current_module, "final_module.md")
            logger.info("Module approved for publication!")
        else:
            logger.info(f"Module requires additional work: {final_decision['reason']}")

        # Generate final summary
        self.generate_final_summary(
            pass1_report, pass2_report, pass3_report, pass4_report
        )

    def load_initial_module(self):
        """Load the sample module"""
        module_path = self.input_dir / "sample_module.md"
        with open(module_path, 'r') as f:
            content = f.read()

        return ModuleContent(
            content=content,
            module_id="data_structures_intro",
            title="Introduction to Data Structures",
            author="Demo Author"
        )

    async def run_content_review(self, module, review_pass, output_prefix):
        """Run a content review pass using real components with mock API"""
        logger.info(f"Initializing {review_pass.value} with 30 agents...")

        # Create mock reviewer pool that mimics real ReviewerPool
        pool = MockReviewerPool(review_pass, 30, self.mock_api)

        # Run reviews in parallel (real async execution)
        logger.info("Executing parallel agent reviews...")
        feedback_list = await pool.review_parallel(module)
        logger.info(f"Collected {len(feedback_list)} individual feedback items")

        # Use REAL aggregator to process feedback
        logger.info("Running consensus aggregation...")
        consensus_results = self.aggregator.aggregate(feedback_list)
        logger.info(f"Aggregated to {len(consensus_results)} consensus issues")

        # Generate report using real report generator
        report = self.aggregator.generate_report(
            consensus_results=consensus_results,
            module_id=module.module_id,
            review_pass=review_pass,
            strengths=self.identify_strengths(consensus_results)
        )

        # Save report in multiple formats
        self.save_report(report, output_prefix)

        return report

    async def run_copy_edit(self, module, review_pass, output_prefix):
        """Run a copy edit pass focusing on style only"""
        logger.info(f"Initializing {review_pass.value} with 8 style agents...")

        # Create mock reviewer pool for copy editing
        pool = MockReviewerPool(review_pass, 8, self.mock_api, style_only=True)

        # Run reviews
        logger.info("Executing parallel style reviews...")
        feedback_list = await pool.review_parallel(module)
        logger.info(f"Collected {len(feedback_list)} style feedback items")

        # Aggregate
        consensus_results = self.aggregator.aggregate(feedback_list)
        logger.info(f"Aggregated to {len(consensus_results)} consensus style issues")

        # Generate report
        report = self.aggregator.generate_report(
            consensus_results=consensus_results,
            module_id=module.module_id,
            review_pass=review_pass,
            strengths=self.identify_style_strengths(consensus_results)
        )

        # Save report
        self.save_report(report, output_prefix)

        return report

    def identify_strengths(self, consensus_results):
        """Identify module strengths based on what's NOT in issues"""
        strengths = []
        issue_types = set(r.issue_type for r in consensus_results if hasattr(r, 'issue_type'))

        if "missing_objectives" not in issue_types:
            strengths.append("Learning objectives are clearly stated")
        if "poor_scaffolding" not in issue_types:
            strengths.append("Content builds complexity gradually")
        if "unclear_examples" not in issue_types:
            strengths.append("Examples effectively illustrate concepts")

        return strengths[:5]  # Return top 5

    def identify_style_strengths(self, consensus_results):
        """Identify style strengths"""
        strengths = []
        issues_text = " ".join([r.issue for r in consensus_results])

        if "contraction" not in issues_text.lower():
            strengths.append("Professional tone maintained throughout")
        if "punctuation" not in issues_text.lower():
            strengths.append("Punctuation follows style guidelines")
        if "consistency" not in issues_text.lower():
            strengths.append("Formatting is consistent")

        return strengths[:3]

    def save_report(self, report, prefix):
        """Save report in multiple formats"""
        # JSON format
        json_path = self.output_dir / f"{prefix}_report.json"
        with open(json_path, 'w') as f:
            f.write(report.to_json())

        # Markdown format
        md_path = self.output_dir / f"{prefix}_report.md"
        with open(md_path, 'w') as f:
            f.write(self.report_generator.generate_markdown_report(report))

        logger.info(f"Reports saved: {prefix}_report.json and .md")

    def save_revision(self, module, filename):
        """Save revised module content"""
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            f.write(module.content)
        logger.info(f"Saved revision: {filename}")

    def calculate_improvement(self, before_report, after_report):
        """Calculate improvement percentage between passes"""
        before_count = len(before_report.consensus_results)
        after_count = len(after_report.consensus_results)

        if before_count == 0:
            return 100.0

        reduction = before_count - after_count
        return (reduction / before_count) * 100

    def display_priority_summary(self, report):
        """Display priority matrix summary"""
        matrix = report.get_priority_matrix()
        logger.info("Priority Matrix:")
        logger.info(f"  - Critical (Immediate): {len(matrix['immediate'])} issues")
        logger.info(f"  - High (Important): {len(matrix['important'])} issues")
        logger.info(f"  - Medium (Consider): {len(matrix['consider'])} issues")
        logger.info(f"  - Low (Optional): {len(matrix['optional'])} issues")

    def generate_final_summary(self, pass1, pass2, pass3, pass4):
        """Generate workflow summary"""
        summary = {
            "workflow": "9-Step Realistic Review",
            "timestamp": datetime.now().isoformat(),
            "results": {
                "pass1_issues": len(pass1.consensus_results),
                "pass2_issues": len(pass2.consensus_results),
                "pass3_issues": len(pass3.consensus_results),
                "pass4_issues": len(pass4.consensus_results),
                "total_improvement": self.calculate_improvement(pass1, pass4)
            },
            "history": self.workflow_history
        }

        summary_path = self.output_dir / "workflow_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)

        logger.info("\n" + "=" * 70)
        logger.info("WORKFLOW COMPLETE")
        logger.info("=" * 70)

        # Generate visual report
        logger.info("\nGenerating comprehensive visual report...")
        try:
            from generate_visual_report import main as generate_report
            report_path = generate_report()
            logger.info(f"Visual report generated: {report_path}")
        except Exception as e:
            logger.error(f"Could not generate visual report: {e}")
        logger.info(f"Total improvement: {summary['results']['total_improvement']:.1f}%")
        logger.info(f"Final issues remaining: {summary['results']['pass4_issues']}")
        logger.info(f"Summary saved to: workflow_summary.json")


async def main():
    """Main entry point"""
    orchestrator = RealisticWorkflowOrchestrator()
    await orchestrator.run_complete_workflow()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("REALISTIC WORKFLOW DEMONSTRATION")
    print("Using REAL Learnvia Review System Components")
    print("=" * 70 + "\n")

    asyncio.run(main())

    print("\n✅ Workflow complete! Check outputs/ for generated reports.")
    print("📊 Review logs/workflow_execution.log for detailed execution trace.\n")