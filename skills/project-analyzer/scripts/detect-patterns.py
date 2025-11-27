#!/usr/bin/env python3
"""
detect-patterns.py - Apply detection patterns from YAML configuration

Purpose: Apply rule-based detection patterns to project structure,
         identify missing files, and generate recommendations.

Usage: python detect-patterns.py [project-structure-json] [patterns-yaml]
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional

class PatternDetector:
    """Applies detection patterns to project structure."""

    def __init__(self, patterns_file: str):
        """Initialize detector with patterns YAML file."""
        self.patterns_file = Path(patterns_file)

        if not self.patterns_file.exists():
            raise FileNotFoundError(f"Patterns file not found: {self.patterns_file}")

        with open(self.patterns_file, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        self.patterns = self.config.get('patterns', [])
        self.scoring = self.config.get('scoring', {})
        self.severity = self.config.get('severity', {})

    def detect(self, project_structure: Dict) -> Dict:
        """Apply detection patterns to project structure."""
        results = {
            'project_name': project_structure.get('project_name', 'unknown'),
            'project_types': project_structure.get('project_types', []),
            'frameworks': project_structure.get('frameworks', []),
            'detections': [],
            'recommendations': [],
            'summary': {
                'total_patterns': len(self.patterns),
                'issues_found': 0,
                'high_severity': 0,
                'medium_severity': 0,
                'low_severity': 0,
            }
        }

        files = set(project_structure.get('files', []))
        directories = set(project_structure.get('directories', []))

        for pattern in self.patterns:
            detection = self._apply_pattern(pattern, files, directories, project_structure)

            if detection:
                results['detections'].append(detection)

                if detection['issue_found']:
                    results['summary']['issues_found'] += 1

                    severity = detection['severity']
                    if severity == 'high':
                        results['summary']['high_severity'] += 1
                    elif severity == 'medium':
                        results['summary']['medium_severity'] += 1
                    elif severity == 'low':
                        results['summary']['low_severity'] += 1

                    # Add recommendation
                    if 'recommendation' in detection:
                        results['recommendations'].append({
                            'id': detection['id'],
                            'template': detection['recommendation']['template'],
                            'reason': detection['recommendation']['reason'],
                            'severity': severity,
                            'confidence': detection['confidence'],
                            'priority_score': self._calculate_priority(detection)
                        })

        # Sort recommendations by priority score (highest first)
        results['recommendations'].sort(key=lambda x: x['priority_score'], reverse=True)

        return results

    def _apply_pattern(self, pattern: Dict, files: set, directories: set, project_structure: Dict) -> Optional[Dict]:
        """Apply single detection pattern."""
        pattern_id = pattern.get('id')
        pattern_type = pattern.get('type')
        check = pattern.get('check')
        applies_when = pattern.get('applies_when')

        # Check if pattern applies to this project
        if applies_when:
            if not self._check_condition(applies_when, files, directories, project_structure):
                return None

        detection = {
            'id': pattern_id,
            'type': pattern_type,
            'confidence': pattern.get('confidence', 'medium'),
            'severity': pattern.get('severity', 'medium'),
            'issue_found': False,
        }

        # Apply pattern based on type
        if pattern_type == 'file_absence':
            detection['issue_found'] = self._check_file_absence(check, files)

        elif pattern_type == 'directory_absence':
            detection['issue_found'] = self._check_directory_absence(check, directories)

        elif pattern_type == 'file_quality':
            detection['issue_found'] = self._check_file_quality(check, pattern.get('criteria', {}), project_structure)

        if detection['issue_found'] and 'recommendation' in pattern:
            # Check for language-specific variants
            recommendation = pattern['recommendation'].copy()

            if 'variants' in recommendation:
                variant = self._select_variant(recommendation['variants'], files, directories, project_structure)
                if variant:
                    recommendation['template'] = variant['template']

            detection['recommendation'] = recommendation

        return detection

    def _check_file_absence(self, check: str, files: set) -> bool:
        """Check if file is absent."""
        return check not in files and not any(f.endswith(check) for f in files)

    def _check_directory_absence(self, check, directories: set) -> bool:
        """Check if directory is absent."""
        if isinstance(check, str):
            check = [check]

        # Return True if ALL checks are absent (none found)
        for path in check:
            if path.endswith('.yml') or path.endswith('.yaml'):
                # File check (e.g., .gitlab-ci.yml)
                return True  # Simplified - would need files set
            else:
                # Directory check
                if any(d.startswith(path) for d in directories):
                    return False  # Found one, not absent

        return True  # All absent

    def _check_file_quality(self, file_path: str, criteria: Dict, project_structure: Dict) -> bool:
        """Check if file meets quality criteria."""
        # This would require reading file contents
        # For now, simplified implementation
        files = project_structure.get('files', [])

        if file_path not in files:
            return False  # File doesn't exist

        # Would need to read file and check:
        # - min_lines
        # - required_sections
        # For MVP, assume quality issue if file is very small

        return False  # Placeholder - needs file reading

    def _check_condition(self, condition: str, files: set, directories: set, project_structure: Dict) -> bool:
        """Check if condition applies."""
        # Simple condition parsing
        if 'package.json exists' in condition:
            return 'package.json' in files

        if 'requirements.txt' in condition or 'setup.py exists' in condition:
            return 'requirements.txt' in files or 'setup.py' in files

        if 'pom.xml' in condition or 'build.gradle exists' in condition:
            return any('pom.xml' in f or 'build.gradle' in f for f in files)

        return True  # Default: apply pattern

    def _select_variant(self, variants: List[Dict], files: set, directories: set, project_structure: Dict) -> Optional[Dict]:
        """Select appropriate template variant based on project type."""
        for variant in variants:
            condition = variant.get('condition', '')

            if self._check_condition(condition, files, directories, project_structure):
                return variant

        return None

    def _calculate_priority(self, detection: Dict) -> float:
        """Calculate priority score for recommendation."""
        confidence_map = {'high': 1.0, 'medium': 0.7, 'low': 0.4}
        severity_map = {'high': 10, 'medium': 5, 'low': 2}
        multiplier_map = {'high': 1.0, 'medium': 0.6, 'low': 0.3}

        confidence = confidence_map.get(detection['confidence'], 0.7)
        severity = detection['severity']
        priority_score = severity_map.get(severity, 5)
        multiplier = multiplier_map.get(severity, 0.6)

        return confidence * multiplier * priority_score


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python detect-patterns.py [project-structure-json] [patterns-yaml]", file=sys.stderr)
        return 1

    structure_file = sys.argv[1]
    patterns_file = sys.argv[2] if len(sys.argv) > 2 else None

    # Default patterns file location
    if not patterns_file:
        script_dir = Path(__file__).parent.parent
        patterns_file = script_dir / 'assets' / 'detection-patterns.yaml'

    try:
        # Load project structure
        with open(structure_file, 'r', encoding='utf-8') as f:
            project_structure = json.load(f)

        # Initialize detector
        detector = PatternDetector(str(patterns_file))

        # Detect patterns
        results = detector.detect(project_structure)

        # Output as JSON
        print(json.dumps(results, indent=2))

        return 0

    except Exception as e:
        print(f"Error detecting patterns: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
