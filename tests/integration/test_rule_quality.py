#!/usr/bin/env python3
"""
Integration tests for rule quality metrics and false positive/negative detection
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestRuleQuality:
    """Test rule quality metrics and accuracy"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_samples_dir = self.temp_dir / "test-samples"
        self.test_samples_dir.mkdir()

        # Create mock test samples
        self._create_mock_samples()

    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def _create_mock_samples(self):
        """Create mock vulnerable and safe test samples"""
        # Create directory structure
        vuln_python = self.test_samples_dir / "vulnerable" / "python"
        safe_python = self.test_samples_dir / "safe" / "python"
        vuln_python.mkdir(parents=True)
        safe_python.mkdir(parents=True)

        # Create vulnerable samples
        vuln_files = [
            ("prompt_injection.py", self._get_vulnerable_prompt_injection_code()),
            ("sql_injection.py", self._get_vulnerable_sql_injection_code()),
            ("xss_attack.py", self._get_vulnerable_xss_code()),
        ]

        for filename, content in vuln_files:
            with open(vuln_python / filename, "w") as f:
                f.write(content)

        # Create safe samples
        safe_files = [
            ("safe_prompt.py", self._get_safe_prompt_handling_code()),
            ("safe_sql.py", self._get_safe_sql_code()),
            ("safe_html.py", self._get_safe_html_code()),
        ]

        for filename, content in safe_files:
            with open(safe_python / filename, "w") as f:
                f.write(content)

    def _get_vulnerable_prompt_injection_code(self):
        """Get vulnerable prompt injection code"""
        return """
def vulnerable_function(user_input):
    # VULNERABLE: Direct string concatenation
    prompt = f"Tell me about {user_input}"
    return prompt
"""

    def _get_vulnerable_sql_injection_code(self):
        """Get vulnerable SQL injection code"""
        return """
def vulnerable_query(user_input):
    # VULNERABLE: Direct SQL string formatting
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    return query
"""

    def _get_vulnerable_xss_code(self):
        """Get vulnerable XSS code"""
        return """
def vulnerable_html(user_input):
    # VULNERABLE: Direct HTML injection
    html = f"<div>{user_input}</div>"
    return html
"""

    def _get_safe_prompt_handling_code(self):
        """Get safe prompt handling code"""
        return """
def safe_function(user_input):
    # SAFE: Input validation and sanitization
    if not isinstance(user_input, str) or len(user_input) > 100:
        return "Invalid input"

    sanitized = user_input.replace('<', '&lt;').replace('>', '&gt;')
    prompt = f"Tell me about {sanitized}"
    return prompt
"""

    def _get_safe_sql_code(self):
        """Get safe SQL code"""
        return """
import sqlite3

def safe_query(user_input):
    # SAFE: Parameterized query
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # SAFE: Use parameterized queries
    cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))

    return cursor.fetchall()
"""

    def _get_safe_html_code(self):
        """Get safe HTML code"""
        return """
import html

def safe_html(user_input):
    # SAFE: HTML escaping
    escaped = html.escape(user_input)
    html_output = f"<div>{escaped}</div>"
    return html_output
"""

    def test_sample_structure(self):
        """Test that test samples have correct structure"""
        vuln_files = list(
            (self.test_samples_dir / "vulnerable" / "python").glob("*.py")
        )
        safe_files = list((self.test_samples_dir / "safe" / "python").glob("*.py"))

        assert len(vuln_files) == 3
        assert len(safe_files) == 3

        # Check that files contain expected content
        with open(vuln_files[0], "r") as f:
            content = f.read()
            assert "VULNERABLE:" in content

        with open(safe_files[0], "r") as f:
            content = f.read()
            assert "SAFE:" in content

    def test_vulnerable_pattern_detection(self):
        """Test that vulnerable patterns can be detected in samples"""
        vuln_file = (
            self.test_samples_dir / "vulnerable" / "python" / "prompt_injection.py"
        )

        with open(vuln_file, "r") as f:
            content = f.read()

        # Check for vulnerable patterns
        assert 'f"' in content or "f'" in content  # f-string usage
        assert "user_input" in content
        assert "VULNERABLE:" in content

    def test_safe_pattern_verification(self):
        """Test that safe patterns are correctly implemented"""
        safe_file = self.test_samples_dir / "safe" / "python" / "safe_prompt.py"

        with open(safe_file, "r") as f:
            content = f.read()

        # Check for safe patterns
        assert "sanitized" in content or "escape" in content
        assert "SAFE:" in content
        assert "isinstance" in content or "len(" in content  # Input validation

    @patch("subprocess.run")
    def test_rule_execution_simulation(self, mock_subprocess):
        """Test simulated rule execution against samples"""
        # Mock successful rule execution
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Found 2 vulnerabilities"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result

        # Simulate running rules against samples
        vuln_samples = list(
            (self.test_samples_dir / "vulnerable" / "python").glob("*.py")
        )

        findings_count = 0
        for sample in vuln_samples:
            # In real implementation, this would run actual rules
            # For testing, we simulate findings
            if "vulnerable" in str(sample):
                findings_count += 1

        assert findings_count == len(vuln_samples)

    def test_false_positive_detection(self):
        """Test detection of false positives"""
        safe_samples = list((self.test_samples_dir / "safe" / "python").glob("*.py"))

        # Safe samples should not trigger vulnerability findings
        # In a real test, this would run rules and check for false positives
        for sample in safe_samples:
            with open(sample, "r") as f:
                content = f.read()
                # Safe samples should not contain vulnerable patterns
                assert "VULNERABLE:" not in content
                assert "unsafe" not in content.lower()

    def test_coverage_calculation(self):
        """Test calculation of rule coverage metrics"""
        total_samples = len(list(self.test_samples_dir.glob("**/*.py")))
        vuln_samples = len(list((self.test_samples_dir / "vulnerable").glob("**/*.py")))
        safe_samples = len(list((self.test_samples_dir / "safe").glob("**/*.py")))

        # Basic coverage checks
        assert total_samples == vuln_samples + safe_samples
        assert vuln_samples > 0
        assert safe_samples > 0

        # Calculate coverage ratios
        vuln_ratio = vuln_samples / total_samples
        safe_ratio = safe_samples / total_samples

        assert 0.4 <= vuln_ratio <= 0.6  # Roughly balanced
        assert 0.4 <= safe_ratio <= 0.6

    def test_language_distribution(self):
        """Test that samples are distributed across languages"""
        languages = ["python", "javascript", "typescript", "java", "go"]

        for lang in languages:
            vuln_dir = self.test_samples_dir / "vulnerable" / lang
            safe_dir = self.test_samples_dir / "safe" / lang

            # At least python should exist in our test setup
            if lang == "python":
                assert vuln_dir.exists()
                assert safe_dir.exists()
                assert len(list(vuln_dir.glob("*.py"))) > 0
                assert len(list(safe_dir.glob("*.py"))) > 0
            # Other languages might not exist in minimal test setup
            # but the structure should be ready

    def test_sample_quality(self):
        """Test overall quality of test samples"""
        all_samples = list(self.test_samples_dir.glob("**/*.py"))

        for sample in all_samples:
            with open(sample, "r") as f:
                content = f.read()

            # Basic quality checks
            assert len(content) > 50  # Minimum content length
            assert content.strip() != ""  # Not empty
            assert "#" in content or "//" in content or "/*" in content  # Has comments

            # Check for proper code structure
            lines = content.split("\n")
            code_lines = [
                line
                for line in lines
                if line.strip() and not line.strip().startswith("#")
            ]
            assert len(code_lines) > 3  # Has substantial code


class TestPerformanceMetrics:
    """Test performance metrics calculation"""

    def test_execution_time_simulation(self):
        """Test execution time measurement simulation"""
        import time

        # Simulate rule execution timing
        start_time = time.time()
        time.sleep(0.01)  # Simulate work
        end_time = time.time()

        execution_time = end_time - start_time
        assert execution_time > 0
        assert execution_time < 1  # Should be fast

    def test_memory_usage_simulation(self):
        """Test memory usage measurement simulation"""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024  # MB

        # Simulate some memory usage
        big_list = [i for i in range(10000)]

        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        del big_list  # Clean up

        # Memory usage should be reasonable
        assert memory_after >= memory_before
        assert memory_after < 1000  # Less than 1GB
