#!/usr/bin/env python3
"""
Test script to verify the realistic workflow components are working
"""

import sys
from pathlib import Path

# Add parent directory to path for CODE imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

print("Testing imports...")

# Test CODE imports
try:
    from CODE.orchestrator import RevisionOrchestrator, ModuleLoader
    from CODE.models import ModuleContent, ReviewPass, ReviewReport
    from CODE.aggregator import ConsensusAggregator
    from CODE.report_generator import ReportGenerator
    print("✅ CODE imports successful")
except ImportError as e:
    print(f"❌ CODE import failed: {e}")
    sys.exit(1)

# Test local script imports
try:
    sys.path.insert(0, str(Path(__file__).parent / "scripts"))
    from mock_api_responses import MockAPIClient, MockReviewerPool
    from synthetic_actors import SyntheticAuthor, SyntheticHumanReviewer
    print("✅ Local script imports successful")
except ImportError as e:
    print(f"❌ Local script import failed: {e}")
    sys.exit(1)

# Test basic instantiation
try:
    mock_api = MockAPIClient()
    aggregator = ConsensusAggregator()
    author = SyntheticAuthor()
    print("✅ Component instantiation successful")
except Exception as e:
    print(f"❌ Component instantiation failed: {e}")
    sys.exit(1)

# Test loading sample module
try:
    input_path = Path(__file__).parent / "input" / "sample_module.md"
    with open(input_path, 'r') as f:
        content = f.read()
    module = ModuleContent(
        content=content,
        module_id="test_module",
        title="Test Module"
    )
    print(f"✅ Sample module loaded ({len(content)} characters)")
except Exception as e:
    print(f"❌ Module loading failed: {e}")
    sys.exit(1)

print("\n🎉 All tests passed! The realistic workflow is ready to run.")
print("\nTo run the full demonstration:")
print("  python scripts/run_realistic_workflow.py")