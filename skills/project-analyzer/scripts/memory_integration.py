#!/usr/bin/env python3
"""
memory_integration.py - Integration with local-memory MCP server

Purpose: Store and retrieve project analysis results with mandatory isolation.
         Enforces session_filter_mode: "session_only" for all operations.

Usage: Import and use store_analysis() and retrieve_analysis() functions.
"""

import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class MemoryIntegration:
    """Handles local-memory integration with isolation enforcement."""

    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize memory integration.

        Args:
            session_id: Optional session ID. If not provided, attempts to read
                       from .claude/project-session-id file.
        """
        self.session_id = session_id or self._get_project_session_id()

        if not self.session_id:
            raise ValueError(
                "No session ID provided and could not read from "
                ".claude/project-session-id file"
            )

    def _get_project_session_id(self) -> Optional[str]:
        """Get project session ID from .claude/project-session-id file."""
        try:
            # Look for .claude/project-session-id in current directory or parents
            current = Path.cwd()

            for _ in range(5):  # Search up to 5 levels
                session_file = current / '.claude' / 'project-session-id'

                if session_file.exists():
                    with open(session_file, 'r', encoding='utf-8') as f:
                        return f.read().strip()

                if current.parent == current:
                    break

                current = current.parent

            return None

        except Exception:
            return None

    def create_isolated_params(self, content: Dict, tags: List[str], importance: int = 8) -> Dict:
        """
        Create parameters for local-memory with mandatory isolation.

        Args:
            content: Analysis content to store (will be JSON-serialized)
            tags: Tags for categorization
            importance: Importance level (1-10)

        Returns:
            Parameters dict with isolation enforced
        """
        # JSON-serialize content
        content_str = json.dumps(content, indent=2)

        # Create isolated parameters
        params = {
            'content': content_str,
            'tags': tags,
            'importance': importance,
            'source': 'project-catalyst-analyzer',
            'domain': 'project-catalyst',
            'session_filter_mode': 'session_only',  # MANDATORY
            'session_id': self.session_id,
        }

        return params

    def ensure_isolation(self, params: Dict) -> None:
        """
        Runtime verification of isolation parameters.

        Raises:
            ValueError: If isolation requirements not met
        """
        if params.get('session_filter_mode') != 'session_only':
            raise ValueError(
                f"Isolation violation: session_filter_mode must be 'session_only', "
                f"got '{params.get('session_filter_mode')}'"
            )

        if not params.get('session_id'):
            raise ValueError("Isolation violation: session_id is required")

    def store_analysis(self, analysis_results: Dict, project_name: str) -> Dict:
        """
        Store analysis results to local-memory with isolation.

        Args:
            analysis_results: Complete analysis results from detect-patterns.py
            project_name: Name of analyzed project

        Returns:
            Parameters dict ready for mcp__local_memory__store_memory()
        """
        # Prepare content
        content = {
            'timestamp': datetime.now().isoformat(),
            'project_name': project_name,
            'patterns_detected': len(analysis_results.get('detections', [])),
            'issues_found': analysis_results.get('summary', {}).get('issues_found', 0),
            'recommendations': analysis_results.get('recommendations', []),
            'confidence_scores': {
                d['id']: d['confidence']
                for d in analysis_results.get('detections', [])
            },
            'project_type': analysis_results.get('project_types', []),
            'frameworks': analysis_results.get('frameworks', []),
            'health_score': self._calculate_health_score(analysis_results),
        }

        # Create isolated parameters
        params = self.create_isolated_params(
            content=content,
            tags=['project-analysis', 'catalyst', 'pattern-detection', project_name],
            importance=8
        )

        # Verify isolation
        self.ensure_isolation(params)

        return params

    def retrieve_analysis_history(self, project_name: str) -> Dict:
        """
        Retrieve historical analysis for comparison.

        Args:
            project_name: Name of project to retrieve history for

        Returns:
            Search parameters dict ready for mcp__local_memory__search()
        """
        params = {
            'query': f'project-analysis {project_name}',
            'tags': ['project-analysis', project_name],
            'session_filter_mode': 'session_only',  # MANDATORY
            'session_id': self.session_id,
            'limit': 10,
            'response_format': 'concise',
        }

        # Verify isolation
        self.ensure_isolation(params)

        return params

    def _calculate_health_score(self, analysis_results: Dict) -> int:
        """Calculate project health score (0-100)."""
        summary = analysis_results.get('summary', {})
        total_patterns = summary.get('total_patterns', 1)
        issues_found = summary.get('issues_found', 0)
        high_severity = summary.get('high_severity', 0)
        medium_severity = summary.get('medium_severity', 0)

        # Weighted scoring
        issues_penalty = (issues_found / total_patterns) * 100
        high_penalty = high_severity * 20
        medium_penalty = medium_severity * 10

        health_score = max(0, 100 - issues_penalty - high_penalty - medium_penalty)

        return int(health_score)


def store_analysis_to_memory(analysis_results: Dict, project_name: str, session_id: Optional[str] = None) -> Dict:
    """
    Convenience function to store analysis with isolation.

    Args:
        analysis_results: Complete analysis results
        project_name: Name of analyzed project
        session_id: Optional session ID (auto-detected if not provided)

    Returns:
        Parameters dict ready for mcp__local_memory__store_memory()
    """
    integration = MemoryIntegration(session_id)
    return integration.store_analysis(analysis_results, project_name)


def retrieve_analysis_history(project_name: str, session_id: Optional[str] = None) -> Dict:
    """
    Convenience function to retrieve analysis history.

    Args:
        project_name: Name of project to retrieve history for
        session_id: Optional session ID (auto-detected if not provided)

    Returns:
        Search parameters dict ready for mcp__local_memory__search()
    """
    integration = MemoryIntegration(session_id)
    return integration.retrieve_analysis_history(project_name)


def main():
    """Main entry point for testing."""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python memory_integration.py store|retrieve [detection-results-json] [project-name]", file=sys.stderr)
        return 1

    command = sys.argv[1]
    results_file = sys.argv[2] if len(sys.argv) > 2 else None
    project_name = sys.argv[3] if len(sys.argv) > 3 else 'unknown'

    try:
        if command == 'store':
            # Load results
            with open(results_file, 'r', encoding='utf-8') as f:
                analysis_results = json.load(f)

            # Store to memory
            params = store_analysis_to_memory(analysis_results, project_name)

            print("# Parameters for mcp__local_memory__store_memory():")
            print(json.dumps(params, indent=2))

        elif command == 'retrieve':
            # Retrieve history
            params = retrieve_analysis_history(project_name)

            print("# Parameters for mcp__local_memory__search():")
            print(json.dumps(params, indent=2))

        else:
            print(f"Unknown command: {command}", file=sys.stderr)
            return 1

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
