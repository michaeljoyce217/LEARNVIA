#!/usr/bin/env python3
"""
Analyze review logs to extract patterns for prompt improvement.

Extracts:
- Good catches (correctly identified issues)
- False positives (incorrectly flagged non-issues)
- Severity calibration examples (what's actually severity 5 vs 3 vs 1)
- Visual/animation issues to exclude from text review scope
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict


def analyze_review_log(csv_path):
    """Analyze a single review log CSV file."""
    good_catches = []
    false_positives = []
    severity_examples = defaultdict(list)
    visual_issues = []

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            # Skip first title row
            next(f)
            reader = csv.DictReader(f)
            headers = reader.fieldnames

            print(f"  Headers: {headers[:6]}...")  # Print first few for brevity

            for row in reader:
                # Extract key fields based on actual CSV structure
                # The headers have embedded newlines - access by full header text
                lesson = row.get('Lesson', '').strip()
                section = row.get('Section', '').strip()
                
                # Find Issue column (may have newline in header)
                issue = ''
                for key in row.keys():
                    if 'Issue' in key:
                        issue = row[key].strip()
                        break
                
                # Find Recommended Edit column
                recommended_edit = ''
                for key in row.keys():
                    if 'Recommended Edit' in key:
                        recommended_edit = row[key].strip()
                        break
                
                # Find Status column
                status = ''
                for key in row.keys():
                    if 'Status' in key and 'OS:' not in key:
                        status = row[key].strip()
                        break
                
                # Find Notes column
                notes = ''
                for key in row.keys():
                    if 'Notes' in key or 'Resolution' in key:
                        notes = row[key].strip()
                        break
                
                # Find Location column
                location = ''
                for key in row.keys():
                    if 'Location' in key:
                        location = row[key].strip()
                        break

                if not issue:
                    continue

                # Identify visual/animation issues - be more specific
                # Only exclude if it's clearly about visual elements, not text within animations
                is_visual = False
                visual_keywords = ['axes labels', 'x- and y-axes', 'graph style', 'color', 
                                  'pause break', 'scene transition', 'animation highlight',
                                  'edit animation', 'missing labels']
                
                if any(keyword in issue.lower() for keyword in visual_keywords):
                    is_visual = True
                elif 'graph' in issue.lower() and ('shown' in issue.lower() or 'y = ' in issue):
                    is_visual = True  # Graph content issues
                elif '<image source>' in issue or 'rendering' in issue.lower():
                    is_visual = True  # Rendering issues
                    
                if is_visual:
                    visual_issues.append({
                        'issue': issue,
                        'section': section,
                        'recommended_edit': recommended_edit,
                        'notes': notes
                    })
                    continue  # Skip visual issues for text review patterns

                # Classify based on status
                if status.lower() in ['resolved', 'done', 'completed', 'fixed', 'accepted']:
                    good_catches.append({
                        'issue': issue,
                        'section': section,
                        'recommended_edit': recommended_edit,
                        'notes': notes
                    })
                elif status.lower() in ['open', 'in progress', 'pending']:
                    # These are valid issues that haven't been addressed yet
                    good_catches.append({
                        'issue': issue,
                        'section': section,
                        'recommended_edit': recommended_edit,
                        'notes': notes
                    })
                elif status.lower() in ['invalid', 'rejected', 'wontfix', 'closed']:
                    false_positives.append({
                        'issue': issue,
                        'section': section,
                        'recommended_edit': recommended_edit,
                        'notes': notes
                    })

    except Exception as e:
        print(f"  Error reading {csv_path}: {e}")
        return None

    return {
        'good_catches': good_catches,
        'false_positives': false_positives,
        'severity_examples': severity_examples,
        'visual_issues': visual_issues
    }


def generate_report(all_results, output_path):
    """Generate markdown report from analysis results."""

    # Combine all results
    all_good = []
    all_false_pos = []
    all_severity = defaultdict(list)
    all_visual = []

    for result in all_results:
        if result is None:
            continue
        all_good.extend(result['good_catches'])
        all_false_pos.extend(result['false_positives'])
        for sev, examples in result['severity_examples'].items():
            all_severity[sev].extend(examples)
        all_visual.extend(result['visual_issues'])

    # Generate markdown
    report = f"""# Review Log Analysis

**Generated:** {Path(output_path).name}

## Summary

- Total good catches (text issues): {len(all_good)}
- Total false positives: {len(all_false_pos)}
- Total visual issues (excluded from text review): {len(all_visual)}

---

## Visual/Animation Issues (Out of Scope for Text Review)

These issues are handled by separate visual reviewer:

"""

    for i, visual in enumerate(all_visual[:20], 1):
        report += f"""
### Visual Issue {i}

**Section:** {visual['section']}
**Issue:** {visual['issue']}
**Recommended Edit:** {visual['recommended_edit']}
**Notes:** {visual['notes']}

---
"""

    report += """

## Good Catches (Keep These Patterns)

These TEXT issues were correctly identified and accepted/addressed by reviewers:

"""

    for i, catch in enumerate(all_good[:30], 1):
        report += f"""
### Good Catch {i}

**Section:** {catch['section']}
**Issue:** {catch['issue']}
**Recommended Edit:** {catch['recommended_edit']}
**Notes:** {catch['notes']}

---
"""

    if all_false_pos:
        report += """

## False Positives (Add to Anti-Pattern Guards)

These issues were flagged but rejected as invalid:

"""

        for i, fp in enumerate(all_false_pos[:20], 1):
            report += f"""
### False Positive {i}

**Section:** {fp['section']}
**Issue:** {fp['issue']}
**Recommended Edit:** {fp['recommended_edit']}
**Notes:** {fp['notes']}

**Action:** Add to anti-pattern guards in master_review_context.txt

---
"""
    else:
        report += """

## False Positives

No rejected issues found in these review logs. All flagged issues were either resolved or are still open.

"""

    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✓ Report written to: {output_path}")
    print(f"  Good catches: {len(all_good)}")
    print(f"  False positives: {len(all_false_pos)}")
    print(f"  Visual issues (excluded): {len(all_visual)}")


def main():
    """Main analysis workflow."""

    # Review log CSV files
    log_files = [
        'modules/Chapter 5 Review Log - 5.6 Beta.csv',
        'modules/Chapter 5 Review Log - 5.6 CE + Other.csv',
        'modules/Chapter 5 Review Log - 5.7 Beta.csv',
        'modules/Chapter 5 Review Log - 5.7 CE + Other.csv'
    ]

    all_results = []

    for log_file in log_files:
        path = Path(log_file)
        if not path.exists():
            print(f"⚠ Warning: {log_file} not found, skipping...")
            continue

        print(f"\nAnalyzing: {log_file}")
        result = analyze_review_log(path)
        if result:
            all_results.append(result)

    if not all_results:
        print("✗ No valid review logs found")
        sys.exit(1)

    # Generate combined report
    output_path = Path('docs/review_log_analysis.md')
    output_path.parent.mkdir(exist_ok=True)
    generate_report(all_results, output_path)


if __name__ == '__main__':
    main()
