#!/usr/bin/env python3
"""
Unit tests for memory_integration.py
"""

import sys
import json
import tempfile
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'skills' / 'project-analyzer' / 'scripts'))

# Import with the correct module name (using hyphen-to-underscore conversion)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "memory_integration",
    Path(__file__).parent.parent.parent / 'skills' / 'project-analyzer' / 'scripts' / 'memory_integration.py'
)
memory_integration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory_integration)
MemoryIntegration = memory_integration.MemoryIntegration


def test_memory_integration_with_session_id():
    """Test MemoryIntegration initialization with explicit session ID."""
    integration = MemoryIntegration(session_id='test-session-123')
    assert integration.session_id == 'test-session-123'


def test_memory_integration_without_session_id():
    """Test MemoryIntegration initialization without session ID."""
    try:
        integration = MemoryIntegration()
        # Should raise ValueError if no session ID found
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert 'No session ID' in str(e)


def test_create_isolated_params():
    """Test creation of isolated parameters."""
    integration = MemoryIntegration(session_id='test-session-123')

    content = {
        'timestamp': '2025-11-27',
        'project_name': 'test-project',
        'issues_found': 5
    }

    params = integration.create_isolated_params(
        content=content,
        tags=['test-tag'],
        importance=8
    )

    assert params['session_filter_mode'] == 'session_only'
    assert params['session_id'] == 'test-session-123'
    assert params['importance'] == 8
    assert 'test-tag' in params['tags']
    assert params['source'] == 'project-catalyst-analyzer'
    assert params['domain'] == 'project-catalyst'

    # Content should be JSON-serialized
    assert isinstance(params['content'], str)
    parsed_content = json.loads(params['content'])
    assert parsed_content['project_name'] == 'test-project'


def test_ensure_isolation_valid():
    """Test isolation enforcement with valid parameters."""
    integration = MemoryIntegration(session_id='test-session-123')

    params = {
        'session_filter_mode': 'session_only',
        'session_id': 'test-session-123'
    }

    # Should not raise any exception
    integration.ensure_isolation(params)


def test_ensure_isolation_invalid_mode():
    """Test isolation enforcement with invalid session_filter_mode."""
    integration = MemoryIntegration(session_id='test-session-123')

    params = {
        'session_filter_mode': 'all',  # Invalid!
        'session_id': 'test-session-123'
    }

    try:
        integration.ensure_isolation(params)
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert 'session_filter_mode must be' in str(e)


def test_ensure_isolation_missing_session_id():
    """Test isolation enforcement with missing session_id."""
    integration = MemoryIntegration(session_id='test-session-123')

    params = {
        'session_filter_mode': 'session_only',
        # Missing session_id!
    }

    try:
        integration.ensure_isolation(params)
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert 'session_id is required' in str(e)


def test_store_analysis():
    """Test storing analysis results."""
    integration = MemoryIntegration(session_id='test-session-123')

    analysis_results = {
        'detections': [
            {'id': 'missing-readme', 'confidence': 'high'},
            {'id': 'missing-gitignore', 'confidence': 'high'}
        ],
        'recommendations': [
            {
                'id': 'missing-readme',
                'template': 'documentation/README',
                'severity': 'high'
            }
        ],
        'summary': {
            'issues_found': 2,
            'high_severity': 1,
            'medium_severity': 1,
            'low_severity': 0,
            'total_patterns': 10
        },
        'project_types': ['python'],
        'frameworks': ['django']
    }

    params = integration.store_analysis(analysis_results, 'test-project')

    # Verify isolation
    assert params['session_filter_mode'] == 'session_only'
    assert params['session_id'] == 'test-session-123'

    # Verify content structure
    content = json.loads(params['content'])
    assert content['project_name'] == 'test-project'
    assert content['patterns_detected'] == 2
    assert content['issues_found'] == 2
    assert len(content['recommendations']) == 1
    assert content['project_type'] == ['python']
    assert content['frameworks'] == ['django']
    assert 'timestamp' in content
    assert 'health_score' in content

    # Verify tags
    assert 'project-analysis' in params['tags']
    assert 'test-project' in params['tags']


def test_retrieve_analysis_history():
    """Test retrieving analysis history."""
    integration = MemoryIntegration(session_id='test-session-123')

    params = integration.retrieve_analysis_history('test-project')

    # Verify isolation
    assert params['session_filter_mode'] == 'session_only'
    assert params['session_id'] == 'test-session-123'

    # Verify search parameters
    assert 'test-project' in params['query']
    assert 'project-analysis' in params['tags']
    assert params['limit'] == 10
    assert params['response_format'] == 'concise'


def test_calculate_health_score():
    """Test health score calculation."""
    integration = MemoryIntegration(session_id='test-session-123')

    # Perfect project (no issues)
    analysis = {
        'summary': {
            'total_patterns': 10,
            'issues_found': 0,
            'high_severity': 0,
            'medium_severity': 0,
            'low_severity': 0
        }
    }
    health_score = integration._calculate_health_score(analysis)
    assert health_score == 100

    # Project with 1 high severity issue
    analysis = {
        'summary': {
            'total_patterns': 10,
            'issues_found': 1,
            'high_severity': 1,
            'medium_severity': 0,
            'low_severity': 0
        }
    }
    health_score = integration._calculate_health_score(analysis)
    assert health_score == 70  # 100 - 10 (1/10*100) - 20 (1*20)

    # Project with multiple issues
    analysis = {
        'summary': {
            'total_patterns': 10,
            'issues_found': 4,
            'high_severity': 1,
            'medium_severity': 2,
            'low_severity': 1
        }
    }
    health_score = integration._calculate_health_score(analysis)
    # Calculation: 100 - 40 (4/10*100) - 20 (1*20) - 20 (2*10) = 20
    assert health_score == 20

    # Health score should never go below 0
    analysis = {
        'summary': {
            'total_patterns': 10,
            'issues_found': 10,
            'high_severity': 10,
            'medium_severity': 0,
            'low_severity': 0
        }
    }
    health_score = integration._calculate_health_score(analysis)
    assert health_score == 0  # Capped at 0


def test_get_project_session_id_from_file():
    """Test reading session ID from .claude/project-session-id file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create .claude directory and session ID file
        claude_dir = Path(tmpdir) / '.claude'
        claude_dir.mkdir()
        session_file = claude_dir / 'project-session-id'
        session_file.write_text('file-session-456')

        # Change to temp directory
        import os
        old_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            integration = MemoryIntegration()
            assert integration.session_id == 'file-session-456'
        finally:
            os.chdir(old_cwd)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
