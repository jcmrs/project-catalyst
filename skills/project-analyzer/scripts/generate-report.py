#!/usr/bin/env python3
"""
generate-report.py - Generate human-readable analysis report

Purpose: Format detection results into user-friendly report with
         recommendations, priority actions, and health score.

Usage: python generate-report.py [detection-results-json]
"""

import sys
import json
from typing import Dict, List

class ReportGenerator:
    """Generates formatted analysis reports."""

    # Emoji indicators
    STATUS_ICONS = {
        'ok': '✅',
        'warning': '⚠️',
        'error': '❌',
        'info': 'ℹ️',
        'search': '🔍',
        'chart': '📊',
        'rocket': '🚀',
    }

    def __init__(self, results: Dict):
        """Initialize generator with detection results."""
        self.results = results
        self.project_name = results.get('project_name', 'Unknown Project')
        self.project_types = results.get('project_types', [])
        self.frameworks = results.get('frameworks', [])
        self.detections = results.get('detections', [])
        self.recommendations = results.get('recommendations', [])
        self.summary = results.get('summary', {})

    def generate_report(self) -> str:
        """Generate complete analysis report."""
        sections = [
            self._generate_header(),
            self._generate_project_info(),
            self._generate_category_status(),
            self._generate_priority_actions(),
            self._generate_health_score(),
        ]

        return '\n\n'.join(sections)

    def _generate_header(self) -> str:
        """Generate report header."""
        return f"{self.STATUS_ICONS['search']} Project Analysis Results"

    def _generate_project_info(self) -> str:
        """Generate project information section."""
        lines = []

        # Project type
        if self.project_types:
            project_type = ', '.join(self.project_types).title()
        else:
            project_type = 'Unknown'

        lines.append(f"Project: {self.project_name}")
        lines.append(f"Type: {project_type}")

        # Frameworks
        if self.frameworks:
            frameworks_str = ', '.join(self.frameworks).title()
            lines.append(f"Frameworks: {frameworks_str}")

        # Statistics
        total_patterns = self.summary.get('total_patterns', 0)
        issues_found = self.summary.get('issues_found', 0)

        lines.append(f"Patterns Checked: {total_patterns}")
        lines.append(f"Issues Found: {issues_found}")

        return '\n'.join(lines)

    def _generate_category_status(self) -> str:
        """Generate status by category."""
        categories = {
            'Git Configuration': [],
            'Documentation': [],
            'CI/CD': [],
            'Code Quality': [],
            'Setup': [],
        }

        # Group detections by category
        for detection in self.detections:
            detection_id = detection['id']
            category = self._get_category(detection_id)

            if category in categories:
                categories[category].append(detection)

        # Generate status lines
        lines = []

        for category, detections in categories.items():
            if not detections:
                continue

            # Determine category status
            issues = [d for d in detections if d.get('issue_found')]
            has_high_severity = any(d.get('severity') == 'high' for d in issues)

            if not issues:
                status_icon = self.STATUS_ICONS['ok']
            elif has_high_severity:
                status_icon = self.STATUS_ICONS['error']
            else:
                status_icon = self.STATUS_ICONS['warning']

            lines.append(f"{category}: {status_icon}")

            # List issues
            for detection in detections:
                if detection.get('issue_found'):
                    issue_line = self._format_issue(detection)
                    lines.append(f"  {issue_line}")

        return '\n'.join(lines)

    def _format_issue(self, detection: Dict) -> str:
        """Format individual issue."""
        detection_id = detection['id']
        confidence = detection['confidence']
        severity = detection['severity']

        # Get icon
        if severity == 'high':
            icon = self.STATUS_ICONS['error']
        elif severity == 'medium':
            icon = self.STATUS_ICONS['warning']
        else:
            icon = self.STATUS_ICONS['info']

        # Get description
        description = self._get_description(detection_id)

        # Get recommendation command
        if 'recommendation' in detection:
            template = detection['recommendation']['template']
            reason = detection['recommendation']['reason']
            return (
                f"{icon} {description} (confidence: {confidence}, severity: {severity})\n"
                f"     → /apply-template {template}\n"
                f"     Reason: {reason}"
            )
        else:
            return f"{icon} {description} (confidence: {confidence}, severity: {severity})"

    def _generate_priority_actions(self) -> str:
        """Generate priority actions list."""
        if not self.recommendations:
            return f"{self.STATUS_ICONS['ok']} No priority actions needed!"

        lines = ["Priority Actions:"]

        # Take top 5 recommendations
        top_recommendations = self.recommendations[:5]

        for i, rec in enumerate(top_recommendations, 1):
            description = self._get_description(rec['id'])
            severity = rec['severity']
            template = rec['template']

            lines.append(f"  {i}. {description} ({severity} severity)")
            lines.append(f"     → /apply-template {template}")

        return '\n'.join(lines)

    def _generate_health_score(self) -> str:
        """Generate project health score."""
        # Calculate health score (0-100)
        total_patterns = self.summary.get('total_patterns', 1)
        issues_found = self.summary.get('issues_found', 0)
        high_severity = self.summary.get('high_severity', 0)
        medium_severity = self.summary.get('medium_severity', 0)

        # Weighted scoring
        issues_penalty = (issues_found / total_patterns) * 100
        high_penalty = high_severity * 20
        medium_penalty = medium_severity * 10

        health_score = max(0, 100 - issues_penalty - high_penalty - medium_penalty)

        # Determine rating
        if health_score >= 90:
            rating = "Excellent"
            icon = self.STATUS_ICONS['rocket']
        elif health_score >= 75:
            rating = "Good"
            icon = self.STATUS_ICONS['ok']
        elif health_score >= 50:
            rating = "Fair"
            icon = self.STATUS_ICONS['warning']
        else:
            rating = "Needs Improvement"
            icon = self.STATUS_ICONS['error']

        return f"{icon} Project Health: {health_score:.0f}/100 ({rating})"

    def _get_category(self, detection_id: str) -> str:
        """Get category from detection ID."""
        if 'gitignore' in detection_id or 'git-' in detection_id:
            return 'Git Configuration'
        elif 'readme' in detection_id or 'contributing' in detection_id or 'license' in detection_id:
            return 'Documentation'
        elif 'ci' in detection_id or 'workflow' in detection_id or 'docker' in detection_id:
            return 'CI/CD'
        elif 'eslint' in detection_id or 'prettier' in detection_id:
            return 'Code Quality'
        elif 'editorconfig' in detection_id:
            return 'Setup'
        else:
            return 'Other'

    def _get_description(self, detection_id: str) -> str:
        """Get human-readable description from detection ID."""
        descriptions = {
            'missing-gitignore': 'Missing .gitignore',
            'missing-ci-workflow': 'No CI/CD configuration',
            'missing-git-hooks': 'Missing Git hooks',
            'missing-readme': 'Missing README.md',
            'readme-minimal': 'README.md is minimal',
            'missing-contributing': 'Missing CONTRIBUTING.md',
            'missing-license': 'Missing LICENSE',
            'missing-build-workflow': 'Missing build workflow',
            'missing-release-workflow': 'Missing release workflow',
            'missing-dockerfile': 'Missing Dockerfile',
            'missing-eslint': 'Missing ESLint configuration',
            'missing-prettier': 'Missing Prettier configuration',
            'missing-editorconfig': 'Missing .editorconfig',
        }

        return descriptions.get(detection_id, detection_id.replace('-', ' ').title())


def main():
    """Main entry point."""
    import io

    # Fix encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    if len(sys.argv) < 2:
        print("Usage: python generate-report.py [detection-results-json]", file=sys.stderr)
        return 1

    results_file = sys.argv[1]

    try:
        # Load detection results
        if results_file == '-':
            results = json.load(sys.stdin)
        else:
            with open(results_file, 'r', encoding='utf-8') as f:
                results = json.load(f)

        # Generate report
        generator = ReportGenerator(results)
        report = generator.generate_report()

        print(report)

        return 0

    except Exception as e:
        print(f"Error generating report: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
