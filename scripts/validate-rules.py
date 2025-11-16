#!/usr/bin/env python3
"""
validate-rules.py - Validate TavoAI rules against JSON schemas

This script validates YAML rule files and JSON manifests against their respective schemas.
It ensures all rules conform to the expected format and contain required fields.

Usage:
    python validate-rules.py [--rules-dir DIR] [--manifests] [--sarif-config]
    python validate-rules.py --help
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any

import jsonschema
import yaml


class RuleValidator:
    """Validates TavoAI rules against JSON schemas"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.schemas_dir = repo_root / "schemas"
        self.bundles_dir = repo_root / "bundles"

        # Load schemas
        self.rule_schema = self._load_schema("hybrid-rule-schema.json")
        self.manifest_schema = self._load_schema("bundle-manifest-schema.json")
        self.sarif_schema = self._load_schema("sarif-mapping-schema.json")

    def _load_schema(self, schema_file: str) -> Dict[str, Any]:
        """Load JSON schema from file"""
        schema_path = self.schemas_dir / schema_file
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def validate_rule_file(self, rule_path: Path) -> Tuple[bool, List[str]]:
        """Validate a single YAML rule file"""
        errors = []

        try:
            # Load YAML file
            with open(rule_path, 'r', encoding='utf-8') as f:
                rule_data = yaml.safe_load(f)

            # Validate against schema
            jsonschema.validate(rule_data, self.rule_schema)

            # Additional custom validations
            errors.extend(self._validate_rule_content(rule_data, rule_path))

        except yaml.YAMLError as e:
            errors.append(f"YAML parsing error: {e}")
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")
        except Exception as e:
            errors.append(f"Unexpected error: {e}")

        return len(errors) == 0, errors

    def _validate_rule_content(self, rule_data: Dict[str, Any], rule_path: Path) -> List[str]:
        """Custom validation logic for rule content"""
        errors = []

        # Validate rule ID format
        rule_id = rule_data.get('id', '')
        if not rule_id.startswith('tavoai-'):
            errors.append(f"Rule ID must start with 'tavoai-': {rule_id}")

        # Validate compatible models for AI rules
        rule_type = rule_data.get('rule_type', '')
        if rule_type in ['hybrid', 'ai-only']:
            compatible_models = rule_data.get('compatible_models', [])
            if not compatible_models:
                errors.append("AI rules must specify compatible_models")
            else:
                for model in compatible_models:
                    if '/' not in model:
                        errors.append(f"Invalid model format: {model} (expected 'provider/model')")

        # Validate heuristics exist for non-AI rules
        if rule_type in ['opengrep', 'opa', 'hybrid']:
            heuristics = rule_data.get('heuristics', [])
            if not heuristics:
                errors.append("Non-AI-only rules must have heuristics")

        # Validate AI analysis for AI rules
        if rule_type in ['hybrid', 'ai-only']:
            ai_analysis = rule_data.get('ai_analysis', {})
            if not ai_analysis:
                errors.append("AI rules must have ai_analysis section")

        # Validate standards mappings
        standards = rule_data.get('standards', {})
        if standards:
            errors.extend(self._validate_standards(standards))

        return errors

    def _validate_standards(self, standards: Dict[str, Any]) -> List[str]:
        """Validate standards mappings"""
        errors = []

        # CWE validation
        for cwe in standards.get('cwe', []):
            if not cwe.startswith('CWE-'):
                errors.append(f"Invalid CWE format: {cwe} (should be CWE-XXX)")

        # CAPEC validation
        for capec in standards.get('capec', []):
            if not capec.startswith('CAPEC-'):
                errors.append(f"Invalid CAPEC format: {capec} (should be CAPEC-XXX)")

        # OWASP LLM validation
        for owasp in standards.get('owasp_llm', []):
            if not owasp.startswith('LLM') or len(owasp) != 4:
                errors.append(f"Invalid OWASP LLM format: {owasp} (should be LLMXX)")

        return errors

    def validate_manifest_file(self, manifest_path: Path) -> Tuple[bool, List[str]]:
        """Validate a bundle manifest JSON file"""
        errors = []

        try:
            # Load JSON file
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_data = json.load(f)

            # Validate against schema
            jsonschema.validate(manifest_data, self.manifest_schema)

            # Additional custom validations
            errors.extend(self._validate_manifest_content(manifest_data, manifest_path))

        except json.JSONDecodeError as e:
            errors.append(f"JSON parsing error: {e}")
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")
        except Exception as e:
            errors.append(f"Unexpected error: {e}")

        return len(errors) == 0, errors

    def _validate_manifest_content(self, manifest_data: Dict[str, Any], manifest_path: Path) -> List[str]:
        """Custom validation logic for manifest content"""
        errors = []
        bundle_dir = manifest_path.parent

        # Validate bundle ID format
        bundle_id = manifest_data.get('id', '')
        if not bundle_id.startswith('tavoai-'):
            errors.append(f"Bundle ID must start with 'tavoai-': {bundle_id}")

        # Validate all artifacts exist
        artifacts = manifest_data.get('artifacts', [])
        for artifact in artifacts:
            artifact_path = bundle_dir / artifact
            if not artifact_path.exists():
                errors.append(f"Artifact file not found: {artifact_path}")

        return errors

    def validate_all_rules(self) -> Tuple[int, int]:
        """Validate all rule files in the repository"""
        total_files = 0
        valid_files = 0

        # Find all YAML rule files
        for rule_file in self.bundles_dir.rglob("*.yaml"):
            total_files += 1
            is_valid, errors = self.validate_rule_file(rule_file)

            if is_valid:
                valid_files += 1
                print(f"✅ {rule_file.relative_to(self.repo_root)}")
            else:
                print(f"❌ {rule_file.relative_to(self.repo_root)}")
                for error in errors:
                    print(f"   {error}")

        return valid_files, total_files

    def validate_all_manifests(self) -> Tuple[int, int]:
        """Validate all manifest files in the repository"""
        total_files = 0
        valid_files = 0

        # Find all manifest.json files
        for manifest_file in self.bundles_dir.rglob("manifest.json"):
            total_files += 1
            is_valid, errors = self.validate_manifest_file(manifest_file)

            if is_valid:
                valid_files += 1
                print(f"✅ {manifest_file.relative_to(self.repo_root)}")
            else:
                print(f"❌ {manifest_file.relative_to(self.repo_root)}")
                for error in errors:
                    print(f"   {error}")

        return valid_files, total_files


def main():
    parser = argparse.ArgumentParser(description="Validate TavoAI rules and manifests")
    parser.add_argument(
        "--rules-dir",
        type=str,
        default=".",
        help="Root directory of the tavo-rules repository"
    )
    parser.add_argument(
        "--rules",
        action="store_true",
        help="Validate rule YAML files"
    )
    parser.add_argument(
        "--manifests",
        action="store_true",
        help="Validate bundle manifest files"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate both rules and manifests"
    )

    args = parser.parse_args()

    if not any([args.rules, args.manifests, args.all]):
        args.all = True

    repo_root = Path(args.rules_dir).resolve()
    validator = RuleValidator(repo_root)

    total_valid = 0
    total_files = 0

    if args.rules or args.all:
        print("🔍 Validating rule files...")
        valid, total = validator.validate_all_rules()
        total_valid += valid
        total_files += total
        print()

    if args.manifests or args.all:
        print("🔍 Validating manifest files...")
        valid, total = validator.validate_all_manifests()
        total_valid += valid
        total_files += total
        print()

    # Summary
    print(f"📊 Summary: {total_valid}/{total_files} files valid")

    if total_valid == total_files:
        print("🎉 All validations passed!")
        return 0
    else:
        print("❌ Some validations failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
