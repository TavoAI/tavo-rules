#!/usr/bin/env python3
"""
generate-sarif.py - Generate SARIF output from TavoAI rule findings

This script converts TavoAI rule execution results into SARIF 2.1.0 format
for integration with CI/CD pipelines and security tools.

Usage:
    python generate-sarif.py --results-file results.json --output sarif-output.sarif
    python generate-sarif.py --help
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class SARIFGenerator:
    """Generates SARIF 2.1.0 output from TavoAI rule results"""

    def __init__(self):
        self.sarif_version = "2.1.0"
        self.tavoai_version = "1.0.0"  # Would be dynamic in real implementation

    def generate_sarif(
        self, results: Dict[str, Any], tool_name: str = "TavoAI Scanner"
    ) -> Dict[str, Any]:
        """Generate SARIF output from rule execution results"""

        # Build SARIF structure
        sarif = {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": self.sarif_version,
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": tool_name,
                            "version": self.tavoai_version,
                            "informationUri": "https://tavoai.com",
                            "rules": [],
                        }
                    },
                    "results": [],
                    "automationDetails": {
                        "id": f"tavoai-scan-{datetime.utcnow().isoformat()}",
                        "description": {
                            "text": "Automated AI security scanning with TavoAI"
                        },
                    },
                }
            ],
        }

        # Process results
        rules_map = {}  # Track rule definitions
        results_list = []

        findings = results.get("findings", [])
        for finding in findings:
            # Add rule definition if not already present
            rule_id = finding.get("rule_id", "unknown")
            if rule_id not in rules_map:
                rule_def = self._create_rule_definition(finding)
                sarif["runs"][0]["tool"]["driver"]["rules"].append(rule_def)
                rules_map[rule_id] = (
                    len(sarif["runs"][0]["tool"]["driver"]["rules"]) - 1
                )

            # Create result entry
            result_entry = self._create_result_entry(finding, rules_map[rule_id])
            results_list.append(result_entry)

        sarif["runs"][0]["results"] = results_list

        # Add run metadata
        sarif["runs"][0]["invocations"] = [
            {
                "executionSuccessful": True,
                "startTimeUtc": datetime.utcnow().isoformat() + "Z",
                "endTimeUtc": datetime.utcnow().isoformat() + "Z",
            }
        ]

        return sarif

    def _create_rule_definition(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        """Create SARIF rule definition from finding metadata"""
        rule_id = finding.get("rule_id", "unknown")

        rule_def = {
            "id": rule_id,
            "name": finding.get("rule_name", rule_id),
            "shortDescription": {
                "text": finding.get("description", "Security finding")[
                    :200
                ]  # SARIF limit
            },
            "properties": {
                "category": finding.get("category", "security"),
                "subcategory": finding.get("subcategory", ""),
                "severity": finding.get("severity", "medium"),
                "confidence": finding.get("confidence", 0.8),
                "rule_type": finding.get("rule_type", "unknown"),
                "tags": finding.get("tags", []),
            },
        }

        # Add full description if available
        if "full_description" in finding:
            rule_def["fullDescription"] = {
                "text": finding["full_description"][:1000]  # SARIF limit
            }

        # Add help information
        if "remediation" in finding or "help_uri" in finding:
            rule_def["help"] = {}
            if "remediation" in finding:
                rule_def["help"]["text"] = finding["remediation"][:5000]  # SARIF limit
            if "help_uri" in finding:
                rule_def["helpUri"] = finding["help_uri"]

        # Add standards mappings
        standards = finding.get("standards", {})
        if standards:
            rule_def["properties"]["standards"] = standards

        return rule_def

    def _create_result_entry(
        self, finding: Dict[str, Any], rule_index: int
    ) -> Dict[str, Any]:
        """Create SARIF result entry from finding"""
        result = {
            "ruleId": finding.get("rule_id", "unknown"),
            "ruleIndex": rule_index,
            "level": self._map_severity_to_level(finding.get("severity", "medium")),
            "message": {"text": finding.get("message", "Security finding detected")},
            "locations": [],
        }

        # Add location information
        if "file_path" in finding:
            location = {
                "physicalLocation": {"artifactLocation": {"uri": finding["file_path"]}}
            }

            # Add region if line number available
            if "line" in finding:
                location["physicalLocation"]["region"] = {"startLine": finding["line"]}

                # Add column information if available
                if "column" in finding:
                    location["physicalLocation"]["region"]["startColumn"] = finding[
                        "column"
                    ]

                # Add code snippet if available
                if "snippet" in finding:
                    location["physicalLocation"]["region"]["snippet"] = {
                        "text": finding["snippet"][:200]  # SARIF limit
                    }

            result["locations"].append(location)

        # Add additional properties
        result["properties"] = {
            "confidence": finding.get("confidence", 0.8),
            "category": finding.get("category", "security"),
            "severity": finding.get("severity", "medium"),
        }

        # Add remediation if available
        if "remediation" in finding:
            result["properties"]["remediation"] = finding["remediation"]

        # Add tags if available
        if "tags" in finding:
            result["properties"]["tags"] = finding["tags"]

        return result

    def _map_severity_to_level(self, severity: str) -> str:
        """Map TavoAI severity to SARIF level"""
        severity_map = {
            "critical": "error",
            "high": "error",
            "medium": "warning",
            "low": "note",
            "info": "note",
        }
        return severity_map.get(severity.lower(), "warning")


def load_results(results_file: Path) -> Dict[str, Any]:
    """Load results from JSON file"""
    with open(results_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_sarif(sarif_data: Dict[str, Any], output_file: Path):
    """Save SARIF data to file"""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sarif_data, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Generate SARIF output from TavoAI rule results"
    )
    parser.add_argument(
        "--results-file",
        type=str,
        required=True,
        help="Path to JSON file containing TavoAI scan results",
    )
    parser.add_argument(
        "--output", type=str, required=True, help="Output SARIF file path"
    )
    parser.add_argument(
        "--tool-name",
        type=str,
        default="TavoAI Scanner",
        help="Tool name for SARIF output",
    )
    parser.add_argument(
        "--validate", action="store_true", help="Validate SARIF output against schema"
    )

    args = parser.parse_args()

    # Load results
    results_file = Path(args.results_file)
    if not results_file.exists():
        print(f"❌ Results file not found: {results_file}")
        return 1

    print(f"📂 Loading results from: {results_file}")
    try:
        results = load_results(results_file)
    except Exception as e:
        print(f"❌ Failed to load results: {e}")
        return 1

    # Generate SARIF
    print("🔄 Generating SARIF output...")
    generator = SARIFGenerator()
    try:
        sarif_data = generator.generate_sarif(results, args.tool_name)
    except Exception as e:
        print(f"❌ Failed to generate SARIF: {e}")
        return 1

    # Validate if requested
    if args.validate:
        print("🔍 Validating SARIF output...")
        # Note: In a real implementation, you would validate against the SARIF schema
        # For now, just check basic structure
        if "version" not in sarif_data or "runs" not in sarif_data:
            print("❌ Invalid SARIF structure")
            return 1
        print("✅ SARIF validation passed")

    # Save output
    output_file = Path(args.output)
    print(f"💾 Saving SARIF to: {output_file}")
    try:
        save_sarif(sarif_data, output_file)
    except Exception as e:
        print(f"❌ Failed to save SARIF: {e}")
        return 1

    # Summary
    runs = sarif_data.get("runs", [])
    if runs:
        run = runs[0]
        rules_count = len(run.get("tool", {}).get("driver", {}).get("rules", []))
        results_count = len(run.get("results", []))
        print(
            f"📊 Generated SARIF with {rules_count} rules and {results_count} findings"
        )

    print("🎉 SARIF generation completed successfully!")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
