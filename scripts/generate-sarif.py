#!/usr/bin/env python3
"""
generate-sarif.py - Generate SARIF output from TavoAI rule findings

This script converts TavoAI rule execution results into SARIF 2.1.0 format
for integration with CI/CD pipelines and security tools.

Usage:
    python generate-sarif.py --sample --output sarif-output.sarif  # Generate from sample data
    python generate-sarif.py --results-file results.json --output sarif-output.sarif  # From TavoAI results
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

        # Initialize taxonomy definitions
        self.taxonomies = self._initialize_taxonomies()

    def _initialize_taxonomies(self) -> Dict[str, Any]:
        """Initialize security taxonomies for SARIF output"""
        return {
            "CWE": {
                "name": "CWE",
                "version": "4.13",
                "releaseDateUtc": "2023-10-01T00:00:00Z",
                "informationUri": "https://cwe.mitre.org/",
                "organization": "MITRE",
                "shortDescription": {"text": "Common Weakness Enumeration"},
            },
            "CAPEC": {
                "name": "CAPEC",
                "version": "3.9",
                "releaseDateUtc": "2023-10-01T00:00:00Z",
                "informationUri": "https://capec.mitre.org/",
                "organization": "MITRE",
                "shortDescription": {
                    "text": "Common Attack Pattern Enumeration and Classification"
                },
            },
            "OWASP": {
                "name": "OWASP LLM Top 10",
                "version": "2024",
                "releaseDateUtc": "2024-01-01T00:00:00Z",
                "informationUri": "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
                "organization": "OWASP",
                "shortDescription": {
                    "text": "OWASP Top 10 for Large Language Model Applications"
                },
            },
            "ISO42001": {
                "name": "ISO 42001",
                "version": "2023",
                "releaseDateUtc": "2023-01-01T00:00:00Z",
                "informationUri": "https://www.iso.org/standard/81232.html",
                "organization": "ISO",
                "shortDescription": {"text": "AI Management System Standard"},
            },
        }

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
                    "taxonomies": list(self.taxonomies.values()),
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

        # Add comprehensive standards mappings with taxonomy references
        standards = finding.get("standards", {})
        if standards:
            rule_def["properties"]["standards"] = standards

            # Create taxonomy references for SARIF 2.1.0
            relationships = []

            # CWE mappings
            cwe_ids = self._extract_standard_ids(standards.get("cwe", []))
            for cwe_id in cwe_ids:
                relationships.append(
                    {
                        "target": {
                            "id": f"CWE-{cwe_id}",
                            "toolComponent": {"name": "CWE"},
                        },
                        "kinds": ["relevant"],
                    }
                )

            # CAPEC mappings
            capec_ids = self._extract_standard_ids(standards.get("capec", []))
            for capec_id in capec_ids:
                relationships.append(
                    {
                        "target": {
                            "id": f"CAPEC-{capec_id}",
                            "toolComponent": {"name": "CAPEC"},
                        },
                        "kinds": ["relevant"],
                    }
                )

            # OWASP LLM mappings
            owasp_ids = standards.get("owasp_llm", [])
            for owasp_id in owasp_ids:
                relationships.append(
                    {
                        "target": {
                            "id": owasp_id.upper(),
                            "toolComponent": {"name": "OWASP LLM Top 10"},
                        },
                        "kinds": ["relevant"],
                    }
                )

            # ISO 42001 mappings
            iso_ids = standards.get("iso_42001", [])
            for iso_id in iso_ids:
                relationships.append(
                    {
                        "target": {
                            "id": f"ISO42001-{iso_id}",
                            "toolComponent": {"name": "ISO 42001"},
                        },
                        "kinds": ["relevant"],
                    }
                )

            if relationships:
                rule_def["relationships"] = relationships

        return rule_def

    def _extract_standard_ids(self, standards_list: List[str]) -> List[str]:
        """Extract numeric IDs from standards references"""
        ids = []
        for std in standards_list:
            # Handle formats like "CWE-123", "123", etc.
            if isinstance(std, str):
                # Extract numeric part
                import re

                match = re.search(r"(\d+)", str(std))
                if match:
                    ids.append(match.group(1))
        return ids

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
            region = {}
            if "line" in finding:
                region["startLine"] = finding["line"]

            # Add line range if available
            if "start_line" in finding and "end_line" in finding:
                region["startLine"] = finding["start_line"]
                region["endLine"] = finding["end_line"]
            elif "line" in finding:
                region["startLine"] = finding["line"]

            # Add column information if available
            if "column" in finding:
                region["startColumn"] = finding["column"]
            if "end_column" in finding:
                region["endColumn"] = finding["end_column"]

            # Add code snippet if available
            if "snippet" in finding:
                region["snippet"] = {"text": finding["snippet"][:200]}  # SARIF limit

            if region:
                location["physicalLocation"]["region"] = region

            result["locations"].append(location)

        # Add additional properties
        result["properties"] = {
            "confidence": finding.get("confidence", 0.8),
            "category": finding.get("category", "security"),
            "severity": finding.get("severity", "medium"),
            "rule_type": finding.get("rule_type", "unknown"),
        }

        # Add AI-specific properties if available
        if "ai_analysis" in finding:
            ai_analysis = finding["ai_analysis"]
            result["properties"]["ai_analysis"] = {
                "severity": ai_analysis.get("severity"),
                "confidence": ai_analysis.get("confidence"),
                "tokens_used": ai_analysis.get("tokens_used"),
                "cost_usd": ai_analysis.get("cost_usd"),
            }

        # Add remediation if available
        if "remediation" in finding:
            result["properties"]["remediation"] = finding["remediation"]

        # Add tags if available
        if "tags" in finding:
            result["properties"]["tags"] = finding["tags"]

        # Add standards mappings for this specific finding
        standards = finding.get("standards", {})
        if standards:
            result["properties"]["standards"] = standards

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

    def create_sample_results(self) -> Dict[str, Any]:
        """Create sample TavoAI results for testing SARIF generation"""
        return {
            "scan_id": "sample-scan-001",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tool_version": "1.0.0",
            "findings": [
                {
                    "rule_id": "owasp-llm-01",
                    "rule_name": "Prompt Injection",
                    "description": "Potential prompt injection vulnerability",
                    "message": "Direct user input passed to LLM without validation",
                    "severity": "high",
                    "confidence": 0.85,
                    "category": "security",
                    "subcategory": "llm-security",
                    "rule_type": "hybrid",
                    "file_path": "src/chat.py",
                    "line": 42,
                    "snippet": "response = openai.ChatCompletion.create(messages=[user_input])",
                    "tags": ["owasp-llm", "injection"],
                    "remediation": "Validate and sanitize user input before passing to LLM",
                    "help_uri": "https://owasp.org/www-project-top-10-for-large-language-model-applications/LLM01_2023-Prompt_Injection.html",
                    "standards": {
                        "cwe": ["CWE-77", "CWE-89"],
                        "capec": ["CAPEC-137"],
                        "owasp_llm": ["LLM01"],
                        "iso_42001": ["6.2.2", "8.1.3"],
                    },
                    "ai_analysis": {
                        "severity": "high",
                        "confidence": 0.92,
                        "description": "AI analysis confirms prompt injection vulnerability with high confidence",
                        "tokens_used": 245,
                        "cost_usd": 0.0049,
                    },
                },
                {
                    "rule_id": "iso42001-risk-mgmt",
                    "rule_name": "ISO 42001 Risk Management",
                    "description": "Missing risk assessment procedures",
                    "message": "AI system deployed without documented risk assessment",
                    "severity": "medium",
                    "confidence": 0.78,
                    "category": "compliance",
                    "subcategory": "iso-42001",
                    "rule_type": "hybrid",
                    "file_path": "deploy.py",
                    "start_line": 15,
                    "end_line": 25,
                    "snippet": "model = load_model()\nstart_serving(model)",
                    "tags": ["iso-42001", "risk-management"],
                    "remediation": "Implement comprehensive risk assessment before deployment",
                    "standards": {
                        "iso_42001": ["6.1.1", "6.1.2", "6.1.3"],
                        "nist_ai_rmf": ["ID"],
                    },
                },
                {
                    "rule_id": "bias-detection-001",
                    "rule_name": "Bias Detection - Protected Attributes",
                    "description": "Potential bias in decision making",
                    "message": "Decision logic uses protected attributes",
                    "severity": "medium",
                    "confidence": 0.65,
                    "category": "ethics",
                    "subcategory": "bias-detection",
                    "rule_type": "hybrid",
                    "file_path": "ml_model.py",
                    "line": 78,
                    "snippet": "if user.age > 65: return DENIED",
                    "tags": ["bias", "fairness", "ethics"],
                    "remediation": "Remove protected attributes from decision logic",
                    "standards": {"iso_42001": ["6.2.2"], "cwe": ["CWE-20"]},
                },
            ],
        }


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
        help="Path to JSON file containing TavoAI scan results (not needed with --sample)",
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
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Generate SARIF from sample TavoAI results instead of loading from file",
    )

    args = parser.parse_args()

    # Load results
    if args.sample:
        print("📂 Generating sample TavoAI results...")
        generator = SARIFGenerator()
        results = generator.create_sample_results()
        print("✅ Sample results generated")
    else:
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
