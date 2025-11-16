#!/usr/bin/env python3
"""
test-rules.py - Test TavoAI rules against sample code

This script executes rules against test samples to validate:
- Rules detect vulnerable code (true positives)
- Rules don't flag safe code (false positives)
- Rule execution works correctly
- Performance metrics

Usage:
    python test-rules.py [--rules-dir DIR] [--bundle BUNDLE] [--language LANG]
    python test-rules.py --help
"""

import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass

import yaml


@dataclass
class TestResult:
    """Result of testing a single rule"""

    rule_path: Path
    rule_id: str
    vulnerable_detected: int
    vulnerable_total: int
    safe_flagged: int
    safe_total: int
    execution_time_ms: float
    errors: List[str]

    @property
    def true_positive_rate(self) -> float:
        """Percentage of vulnerable samples correctly detected"""
        return (
            self.vulnerable_detected / self.vulnerable_total
            if self.vulnerable_total > 0
            else 0
        )

    @property
    def false_positive_rate(self) -> float:
        """Percentage of safe samples incorrectly flagged"""
        return self.safe_flagged / self.safe_total if self.safe_total > 0 else 0

    @property
    def accuracy(self) -> float:
        """Overall accuracy across all test samples"""
        total_correct = self.vulnerable_detected + (self.safe_total - self.safe_flagged)
        total_samples = self.vulnerable_total + self.safe_total
        return total_correct / total_samples if total_samples > 0 else 0


class RuleTester:
    """Tests TavoAI rules against sample code"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.samples_dir = repo_root / "tests" / "samples"
        self.bundles_dir = repo_root / "bundles"

    def find_test_samples(
        self, language: Optional[str] = None
    ) -> Dict[str, List[Path]]:
        """Find all test sample files, organized by language"""
        samples = {"vulnerable": [], "safe": []}

        if not self.samples_dir.exists():
            return samples

        # Find vulnerable samples
        vuln_dir = self.samples_dir / "vulnerable"
        if vuln_dir.exists():
            for file_path in vuln_dir.glob(
                "*.py" if language == "python" else f"*.{language}" if language else "*"
            ):
                if language and not file_path.name.endswith(f".{language}"):
                    continue
                samples["vulnerable"].append(file_path)

        # Find safe samples
        safe_dir = self.samples_dir / "safe"
        if safe_dir.exists():
            for file_path in safe_dir.glob(
                "*.py" if language == "python" else f"*.{language}" if language else "*"
            ):
                if language and not file_path.name.endswith(f".{language}"):
                    continue
                samples["safe"].append(file_path)

        return samples

    def test_single_rule(
        self, rule_path: Path, language: Optional[str] = None
    ) -> TestResult:
        """Test a single rule against sample code"""
        start_time = time.time()

        # Load rule
        try:
            with open(rule_path, "r", encoding="utf-8") as f:
                rule_data = yaml.safe_load(f)
        except Exception as e:
            return TestResult(
                rule_path=rule_path,
                rule_id="unknown",
                vulnerable_detected=0,
                vulnerable_total=0,
                safe_flagged=0,
                safe_total=0,
                execution_time_ms=0,
                errors=[f"Failed to load rule: {e}"],
            )

        rule_id = rule_data.get("id", "unknown")
        rule_type = rule_data.get("rule_type", "unknown")

        # Get test samples
        samples = self.find_test_samples(language)
        vulnerable_files = samples["vulnerable"]
        safe_files = samples["safe"]

        errors = []
        vulnerable_detected = 0
        safe_flagged = 0

        # Test against vulnerable samples (should detect)
        for vuln_file in vulnerable_files:
            try:
                detected = self._test_rule_against_file(rule_data, vuln_file)
                if detected:
                    vulnerable_detected += 1
            except Exception as e:
                errors.append(f"Error testing {vuln_file.name}: {e}")

        # Test against safe samples (should NOT detect)
        for safe_file in safe_files:
            try:
                detected = self._test_rule_against_file(rule_data, safe_file)
                if detected:
                    safe_flagged += 1
            except Exception as e:
                errors.append(f"Error testing {safe_file.name}: {e}")

        execution_time = (time.time() - start_time) * 1000

        return TestResult(
            rule_path=rule_path,
            rule_id=rule_id,
            vulnerable_detected=vulnerable_detected,
            vulnerable_total=len(vulnerable_files),
            safe_flagged=safe_flagged,
            safe_total=len(safe_files),
            execution_time_ms=execution_time,
            errors=errors,
        )

    def _test_rule_against_file(
        self, rule_data: Dict[str, Any], file_path: Path
    ) -> bool:
        """Test a rule against a single file"""
        # Read file content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        rule_type = rule_data.get("rule_type", "unknown")

        # Test heuristics (available for all rule types except ai-only)
        if rule_type != "ai-only":
            heuristics = rule_data.get("heuristics", [])
            for heuristic in heuristics:
                if self._test_heuristic(heuristic, content, file_path):
                    return True

        # For hybrid/ai-only rules, we would test AI analysis here
        # For now, assume heuristics-only testing
        return False

    def _test_heuristic(
        self, heuristic: Dict[str, Any], content: str, file_path: Path
    ) -> bool:
        """Test a single heuristic against content"""
        heuristic_type = heuristic.get("type", "")
        pattern = heuristic.get("pattern", "")

        if heuristic_type == "semgrep":
            # Simple pattern matching for testing
            # In real implementation, this would use Semgrep
            return pattern in content
        elif heuristic_type == "opa":
            # Simple policy evaluation for testing
            # In real implementation, this would use OPA
            return False  # Placeholder

        return False

    def test_bundle(
        self, bundle_name: str, language: Optional[str] = None
    ) -> List[TestResult]:
        """Test all rules in a bundle"""
        results = []

        # Find bundle directory
        bundle_dir = self.bundles_dir / bundle_name
        if not bundle_dir.exists():
            print(f"Bundle not found: {bundle_dir}")
            return results

        # Find all rule files in bundle
        for rule_file in bundle_dir.rglob("*.yaml"):
            if rule_file.name == "index.json":
                continue  # Skip index files

            print(f"Testing rule: {rule_file.relative_to(self.repo_root)}")
            result = self.test_single_rule(rule_file, language)
            results.append(result)

        return results

    def test_all_bundles(
        self, language: Optional[str] = None
    ) -> Dict[str, List[TestResult]]:
        """Test all bundles"""
        results = {}

        # Test all bundle directories
        for bundle_dir in self.bundles_dir.iterdir():
            if bundle_dir.is_dir():
                bundle_name = bundle_dir.name
                print(f"\n🧪 Testing bundle: {bundle_name}")
                bundle_results = self.test_bundle(bundle_name, language)
                if bundle_results:
                    results[bundle_name] = bundle_results

        return results

    def print_summary(self, results: Dict[str, List[TestResult]]):
        """Print test results summary"""
        total_rules = 0
        total_vulnerable_detected = 0
        total_vulnerable_samples = 0
        total_safe_flagged = 0
        total_safe_samples = 0
        total_errors = 0

        for bundle_name, bundle_results in results.items():
            print(f"\n📦 Bundle: {bundle_name}")
            print("-" * 50)

            bundle_vuln_detected = 0
            bundle_vuln_total = 0
            bundle_safe_flagged = 0
            bundle_safe_total = 0

            for result in bundle_results:
                total_rules += 1
                total_errors += len(result.errors)

                bundle_vuln_detected += result.vulnerable_detected
                bundle_vuln_total += result.vulnerable_total
                bundle_safe_flagged += result.safe_flagged
                bundle_safe_total += result.safe_total

                print(f"  {result.rule_id}:")
                print(
                    f"    True Positives: {result.vulnerable_detected}/{result.vulnerable_total} ({result.true_positive_rate:.1%})"
                )
                print(
                    f"    False Positives: {result.safe_flagged}/{result.safe_total} ({result.false_positive_rate:.1%})"
                )
                print(f"    Accuracy: {result.accuracy:.1%}")
                print(f"    Execution Time: {result.execution_time_ms:.1f}ms")

                if result.errors:
                    print(f"    Errors: {len(result.errors)}")
                    for error in result.errors[:3]:  # Show first 3 errors
                        print(f"      - {error}")

            # Bundle summary
            if bundle_results:
                avg_accuracy = sum(r.accuracy for r in bundle_results) / len(
                    bundle_results
                )
                print(f"  Bundle Accuracy: {avg_accuracy:.1%}")

        # Overall summary
        print(f"\n📊 Overall Summary")
        print("=" * 50)
        print(f"Total Rules Tested: {total_rules}")
        print(
            f"True Positive Rate: {total_vulnerable_detected}/{total_vulnerable_samples} ({total_vulnerable_detected/total_vulnerable_samples:.1%})"
            if total_vulnerable_samples > 0
            else "No vulnerable samples tested"
        )
        print(
            f"False Positive Rate: {total_safe_flagged}/{total_safe_samples} ({total_safe_flagged/total_safe_samples:.1%})"
            if total_safe_samples > 0
            else "No safe samples tested"
        )
        print(f"Total Errors: {total_errors}")

        if total_errors == 0:
            print("🎉 All tests completed successfully!")
        else:
            print("⚠️  Some tests had errors. Review output above.")


def main():
    parser = argparse.ArgumentParser(
        description="Test TavoAI rules against sample code"
    )
    parser.add_argument(
        "--rules-dir",
        type=str,
        default=".",
        help="Root directory of the tavo-rules repository",
    )
    parser.add_argument(
        "--bundle", type=str, help="Specific bundle to test (e.g., 'owasp-llm-pro')"
    )
    parser.add_argument(
        "--language",
        type=str,
        choices=["python", "javascript", "typescript", "java", "go"],
        help="Language to test (filters sample files)",
    )
    parser.add_argument("--all", action="store_true", help="Test all bundles")

    args = parser.parse_args()

    if not any([args.bundle, args.all]):
        args.all = True

    repo_root = Path(args.rules_dir).resolve()
    tester = RuleTester(repo_root)

    if args.bundle:
        print(f"🧪 Testing bundle: {args.bundle}")
        results = {args.bundle: tester.test_bundle(args.bundle, args.language)}
    else:
        print("🧪 Testing all bundles...")
        results = tester.test_all_bundles(args.language)

    tester.print_summary(results)

    # Return non-zero exit code if there were errors
    total_errors = sum(
        len(result.errors)
        for bundle_results in results.values()
        for result in bundle_results
    )
    return 1 if total_errors > 0 else 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
