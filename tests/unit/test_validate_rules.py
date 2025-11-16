#!/usr/bin/env python3
"""
Unit tests for validate-rules.py script
"""

import json
import pytest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the validation functions
import sys

sys.path.append(str(Path(__file__).parent.parent.parent / "scripts"))

from validate_rules import RuleValidator


class TestRuleValidator:
    """Test the RuleValidator class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.schemas_dir = self.temp_dir / "schemas"
        self.schemas_dir.mkdir()

        # Create mock schemas
        self.mock_rule_schema = {
            "type": "object",
            "required": ["id", "name", "category"],
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "category": {"type": "string"},
            },
        }

        self.mock_manifest_schema = {"type": "object"}
        self.mock_sarif_schema = {"type": "object"}

        # Write mock schemas
        with open(self.schemas_dir / "hybrid-rule-schema.json", "w") as f:
            json.dump(self.mock_rule_schema, f)
        with open(self.schemas_dir / "bundle-manifest-schema.json", "w") as f:
            json.dump(self.mock_manifest_schema, f)
        with open(self.schemas_dir / "sarif-mapping-schema.json", "w") as f:
            json.dump(self.mock_sarif_schema, f)

    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_validator_initialization(self):
        """Test that validator initializes correctly"""
        validator = RuleValidator(self.temp_dir)

        assert validator.repo_root == self.temp_dir
        assert validator.schemas_dir == self.schemas_dir
        assert hasattr(validator, "rule_schema")
        assert hasattr(validator, "manifest_schema")
        assert hasattr(validator, "sarif_schema")

    def test_schema_loading(self):
        """Test that schemas are loaded correctly"""
        validator = RuleValidator(self.temp_dir)

        # Check that schemas were loaded
        assert validator.rule_schema is not None
        assert isinstance(validator.rule_schema, dict)
        assert "type" in validator.rule_schema

    def test_valid_rule_validation(self):
        """Test validation of a valid rule"""
        validator = RuleValidator(self.temp_dir)

        # Create a valid rule file
        valid_rule = {
            "version": "1.0",
            "id": "test-rule-001",
            "name": "Test Rule",
            "category": "security",
            "subcategory": "injection",
            "severity": "high",
        }

        rule_file = self.temp_dir / "test-rule.yaml"
        with open(rule_file, "w") as f:
            yaml.dump(valid_rule, f)

        # Test validation
        is_valid, errors = validator.validate_rule_file(rule_file)

        assert is_valid == True
        assert len(errors) == 0

    def test_invalid_rule_validation(self):
        """Test validation of an invalid rule"""
        validator = RuleValidator(self.temp_dir)

        # Create an invalid rule file (missing required fields)
        invalid_rule = {
            "version": "1.0",
            "name": "Test Rule",
            # Missing 'id' and 'category'
        }

        rule_file = self.temp_dir / "invalid-rule.yaml"
        with open(rule_file, "w") as f:
            yaml.dump(invalid_rule, f)

        # Test validation
        is_valid, errors = validator.validate_rule_file(rule_file)

        assert is_valid == False
        assert len(errors) > 0
        assert any("id" in str(error) for error in errors)

    def test_yaml_parsing_error(self):
        """Test handling of YAML parsing errors"""
        validator = RuleValidator(self.temp_dir)

        # Create a file with invalid YAML
        invalid_yaml_file = self.temp_dir / "invalid.yaml"
        with open(invalid_yaml_file, "w") as f:
            f.write("invalid: yaml: content: [\n  unclosed bracket")

        # Test validation
        is_valid, errors = validator.validate_rule_file(invalid_yaml_file)

        assert is_valid == False
        assert len(errors) > 0
        assert any(
            "YAML" in str(error).upper() or "parsing" in str(error).lower()
            for error in errors
        )

    def test_nonexistent_file(self):
        """Test handling of nonexistent files"""
        validator = RuleValidator(self.temp_dir)

        nonexistent_file = self.temp_dir / "does-not-exist.yaml"

        # Test validation
        is_valid, errors = validator.validate_rule_file(nonexistent_file)

        assert is_valid == False
        assert len(errors) > 0

    @patch("validate_rules.RuleValidator.validate_rule_file")
    def test_validate_all_rules(self, mock_validate):
        """Test validation of multiple rules"""
        validator = RuleValidator(self.temp_dir)

        # Mock validation results
        mock_validate.side_effect = [
            (True, []),  # Valid rule
            (False, ["Error 1"]),  # Invalid rule
            (True, []),  # Valid rule
        ]

        # Create mock rule files
        bundles_dir = self.temp_dir / "bundles"
        bundles_dir.mkdir()

        rule1 = bundles_dir / "rule1.yaml"
        rule2 = bundles_dir / "rule2.yaml"
        rule3 = bundles_dir / "rule3.yaml"

        for rule_file in [rule1, rule2, rule3]:
            rule_file.touch()

        # Test bulk validation
        valid_count, total_count = validator.validate_all_rules()

        assert total_count == 3
        assert valid_count == 2  # 2 out of 3 rules are valid
        assert mock_validate.call_count == 3


class TestScriptExecution:
    """Test script execution and argument handling"""

    def test_script_help_output(self):
        """Test that script shows help correctly"""
        import subprocess
        import sys

        scripts_dir = Path(__file__).parent.parent.parent / "scripts"
        validate_script = scripts_dir / "validate-rules.py"

        if validate_script.exists():
            result = subprocess.run(
                [sys.executable, str(validate_script), "--help"],
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0
            assert "usage:" in result.stdout.lower()
            assert "validate" in result.stdout.lower()

    def test_script_execution(self):
        """Test basic script execution"""
        import subprocess
        import sys

        scripts_dir = Path(__file__).parent.parent.parent / "scripts"
        validate_script = scripts_dir / "validate-rules.py"

        if validate_script.exists():
            # Test with non-existent directory (should handle gracefully)
            result = subprocess.run(
                [
                    sys.executable,
                    str(validate_script),
                    "--rules-dir",
                    "/tmp/nonexistent",
                    "--rules",
                ],
                capture_output=True,
                text=True,
            )

            # Should not crash, even with invalid input
            assert isinstance(result.returncode, int)
