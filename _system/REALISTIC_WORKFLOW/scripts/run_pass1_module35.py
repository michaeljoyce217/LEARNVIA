#!/usr/bin/env python3
"""
Run Pass 1 review on Module 3.5 (Product and Quotient Rules) - XML version
"""
import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

from CODE.models import ModuleContent, ReviewPass
from REALISTIC_WORKFLOW.scripts.mock_api_responses import MockAPIClient, MockReviewerPool
from CODE.aggregator import ConsensusAggregator


async def run_pass1_review():
    """Run Pass 1 review on Module 3.5 XML"""

    # Load the XML module
    module_path = Path(__file__).parent.parent.parent / "modules" / "module_3.5.xml"
    print(f"Loading module from: {module_path}")

    with open(module_path, 'r', encoding='utf-8') as f:
        xml_content = f.read()

    # Create module object
    module = ModuleContent(
        title="Product and Quotient Rules (Module 3.5)",
        content=xml_content,
        module_id="3.5"
    )

    print(f"\nModule loaded:")
    print(f"  Title: {module.title}")
    print(f"  Size: {len(xml_content)} characters")
    print(f"  Lines: {len(xml_content.splitlines())}")

    # Create API client and reviewer pool
    api_client = MockAPIClient()

    # Pass 1: 30 agents (15 authoring + 15 style)
    print(f"\n{'='*60}")
    print(f"PASS 1: Content Review (30 agents)")
    print(f"{'='*60}")

    # Run authoring agents (15)
    print(f"\nRunning 15 authoring agents...")
    auth_pool = MockReviewerPool(
        review_pass=ReviewPass.CONTENT_PASS_1,
        num_reviewers=15,
        api_client=api_client,
        style_only=False
    )
    auth_feedback = await auth_pool.review_parallel(module)
    print(f"  ✓ Collected {len(auth_feedback)} authoring findings")

    # Run style agents (15)
    print(f"\nRunning 15 style agents...")
    style_pool = MockReviewerPool(
        review_pass=ReviewPass.CONTENT_PASS_1,
        num_reviewers=15,
        api_client=api_client,
        style_only=True
    )
    style_feedback = await style_pool.review_parallel(module)
    print(f"  ✓ Collected {len(style_feedback)} style findings")

    # Combine all feedback
    all_feedback = auth_feedback + style_feedback
    print(f"\nTotal findings before consensus: {len(all_feedback)}")

    # Run consensus aggregation with lower threshold to catch more issues
    print(f"\nRunning consensus aggregation...")
    aggregator = ConsensusAggregator(
        similarity_threshold=0.60  # Lower threshold: 60% similarity to group issues together
    )

    consensus_issues = aggregator.aggregate(all_feedback)

    print(f"  ✓ {len(consensus_issues)} consensus issues identified")
    print(f"  ✓ Noise reduction: {100 * (len(all_feedback) - len(consensus_issues)) / len(all_feedback):.1f}%")

    # Sort by severity
    consensus_issues.sort(key=lambda x: x.severity, reverse=True)

    # Create output structure
    # Include FULL content for preview (user wants to see everything)
    results = {
        "timestamp": datetime.now().isoformat(),
        "module": {
            "title": module.title,
            "module_id": module.module_id,
            "char_count": len(xml_content),
            "line_count": len(xml_content.splitlines()),
            "format": "XML",
            "preview": xml_content  # Full content, not truncated
        },
        "pass1": {
            "authoring_agents": 15,
            "style_agents": 15,
            "total_agents": 30,
            "total_findings": len(all_feedback),
            "authoring_findings": len(auth_feedback),
            "style_findings": len(style_feedback)
        },
        "consensus": {
            "total_issues": len(consensus_issues),
            "noise_reduction_pct": round(100 * (len(all_feedback) - len(consensus_issues)) / len(all_feedback), 2),
            "issues": []
        }
    }

    # Add consensus issues
    for issue in consensus_issues:
        results["consensus"]["issues"].append({
            "issue": issue.issue,
            "severity": issue.severity,
            "confidence": round(issue.confidence, 2),
            "location": issue.location,
            "suggestions": issue.suggestions,
            "issue_type": issue.issue_type,
            "agreeing_reviewers": issue.agreeing_reviewers,
            "should_provide_solution": issue.should_provide_solution
        })

    # Save results
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "pass1_module35_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*60}")
    print(f"RESULTS SAVED")
    print(f"{'='*60}")
    print(f"Output: {output_file}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total findings: {len(all_feedback)}")
    print(f"Consensus issues: {len(consensus_issues)}")
    print(f"Noise reduction: {results['consensus']['noise_reduction_pct']}%")

    print(f"\nTop 5 Issues by Severity:")
    for i, issue in enumerate(consensus_issues[:5], 1):
        print(f"  {i}. [{issue.severity}] {issue.issue}")
        print(f"     Confidence: {issue.confidence:.0%}, Location: {issue.location}")

    return results


if __name__ == "__main__":
    print("="*60)
    print("Pass 1 Review: Module 3.5 (Product and Quotient Rules)")
    print("="*60)

    results = asyncio.run(run_pass1_review())

    print(f"\n✓ Review complete!")
