#!/usr/bin/env python3
"""
create-bundle-manifests.py - Create bundle manifests for all TavoAI rule bundles

This script generates manifest.json files for all rule bundles based on the
bundle-manifest-schema.json specification.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class BundleManifestGenerator:
    """Generates bundle manifests for TavoAI rule bundles"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.bundles_dir = repo_root / "bundles"
        self.schemas_dir = repo_root / "schemas"

        # Load the manifest schema for validation
        self.manifest_schema = self._load_schema("bundle-manifest-schema.json")

    def _load_schema(self, schema_file: str) -> Dict[str, Any]:
        """Load JSON schema file"""
        schema_path = self.schemas_dir / schema_file
        with open(schema_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_rule_metadata(self, rule_file: Path) -> Dict[str, Any]:
        """Load rule metadata from YAML file"""
        try:
            with open(rule_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Skip files that look like they contain multiple documents or malformed content
            if "EOF" in content or "cat >" in content or "<<" in content:
                print(f"Warning: Skipping malformed rule file: {rule_file}")
                return self._get_default_metadata(rule_file)

            rule_data = yaml.safe_load(content)

            if rule_data is None:
                print(f"Warning: Empty or invalid YAML in {rule_file}")
                return self._get_default_metadata(rule_file)

            # Extract key metadata
            metadata = {
                "id": rule_data.get("id", ""),
                "name": rule_data.get("name", ""),
                "version": rule_data.get("version", "1.0"),
                "category": rule_data.get("category", ""),
                "subcategory": rule_data.get("subcategory", ""),
                "severity": rule_data.get("severity", "medium"),
                "standards": rule_data.get("standards", {}),
                "tags": rule_data.get("tags", []),
            }

            return metadata

        except Exception as e:
            print(f"Warning: Failed to load rule {rule_file}: {e}")
            return self._get_default_metadata(rule_file)

    def _get_default_metadata(self, rule_file: Path) -> Dict[str, Any]:
        """Get default metadata for a rule file when parsing fails"""
        filename = rule_file.stem
        return {
            "id": filename,
            "name": filename.replace("-", " ").replace("_", " ").title(),
            "version": "1.0",
            "category": "security",
            "subcategory": "unknown",
            "severity": "medium",
            "standards": {},
            "tags": [],
        }

    def _determine_pricing_tier(self, bundle_name: str) -> str:
        """Determine pricing tier based on bundle name"""
        if "free" in bundle_name or "owasp-llm-basic" in bundle_name:
            return "free"
        elif (
            "ai-enhanced" in bundle_name
            or "pro" in bundle_name
            or "compliance" in bundle_name
        ):
            return "paid"
        else:
            return "enterprise"

    def _get_bundle_description(self, bundle_name: str) -> str:
        """Get description for bundle based on name"""
        descriptions = {
            "free/owasp-llm-basic": "Heuristic-only OWASP LLM Top 10 rules for basic security scanning",
            "ai-enhanced/owasp-llm-pro": "AI-enhanced OWASP LLM Top 10 analysis with deep contextual understanding",
            "ai-enhanced/iso-42001-compliance": "Comprehensive ISO 42001 AI governance compliance rules",
            "ai-enhanced/mit-ai-risk-repo": "MIT AI Risk Repository rules covering emerging AI safety concerns",
            "ai-enhanced/ai-ethics": "AI Ethics rules for fairness, transparency, and responsible AI development",
            "ai-enhanced/bias-detection": "Bias detection rules for identifying and mitigating AI bias issues",
        }

        # Try exact match first
        if bundle_name in descriptions:
            return descriptions[bundle_name]

        # Try partial matches
        for key, desc in descriptions.items():
            if key in bundle_name or bundle_name in key:
                return desc

        return f"TavoAI security rules bundle: {bundle_name}"

    def _get_bundle_author(self, bundle_name: str) -> str:
        """Get author information for bundle"""
        return "TavoAI Security Team"

    def _get_bundle_homepage(self, bundle_name: str) -> str:
        """Get homepage URL for bundle"""
        return "https://github.com/TavoAI/tavo-rules"

    def _get_bundle_documentation(self, bundle_name: str) -> Optional[str]:
        """Get documentation URL for bundle"""
        return "https://docs.tavoai.com/rules"

    def _analyze_bundle_rules(self, bundle_path: Path) -> Dict[str, Any]:
        """Analyze rules in bundle to extract metadata"""
        rules_dir = bundle_path / "rules"
        if not rules_dir.exists():
            return {"rules": [], "categories": [], "severities": []}

        rules = []
        categories = set()
        severities = set()
        standards = {}

        # Find all rule files
        rule_files = []
        if rules_dir.is_dir():
            rule_files = list(rules_dir.glob("*.yaml")) + list(rules_dir.glob("*.yml"))

        for rule_file in rule_files:
            try:
                rule_metadata = self._load_rule_metadata(rule_file)
                rules.append(
                    {
                        "id": rule_metadata["id"],
                        "name": rule_metadata["name"],
                        "version": rule_metadata["version"],
                        "severity": rule_metadata["severity"],
                        "category": rule_metadata["category"],
                        "tags": rule_metadata["tags"],
                    }
                )

                categories.add(rule_metadata["category"])
                severities.add(rule_metadata["severity"])

                # Aggregate standards
                for std_type, std_values in rule_metadata.get("standards", {}).items():
                    if std_type not in standards:
                        standards[std_type] = set()
                    if isinstance(std_values, list):
                        standards[std_type].update(std_values)
                    else:
                        standards[std_type].add(str(std_values))

            except Exception as e:
                print(f"Warning: Failed to load rule {rule_file}: {e}")
                continue

        # Convert sets to lists for JSON serialization
        for std_type in standards:
            standards[std_type] = sorted(list(standards[std_type]))

        return {
            "rules": rules,
            "categories": sorted(list(categories)),
            "severities": sorted(list(severities)),
            "standards": standards,
            "rule_count": len(rules),
            "rule_files": rule_files,
        }

    def create_bundle_manifest(self, bundle_path: Path) -> Dict[str, Any]:
        """Create manifest for a single bundle"""
        bundle_name = bundle_path.name
        parent_dir = bundle_path.parent.name

        # Handle nested bundle structure (free/, ai-enhanced/, enterprise/)
        if parent_dir in ["free", "ai-enhanced", "enterprise"]:
            full_bundle_name = f"{parent_dir}/{bundle_name}"
        else:
            full_bundle_name = bundle_name

        print(f"Creating manifest for bundle: {full_bundle_name}")

        # Analyze rules in bundle
        analysis = self._analyze_bundle_rules(bundle_path)
        rule_files = analysis.get("rule_files", [])

        # Create manifest
        manifest = {
            "id": bundle_name.replace("/", "-").replace("_", "-"),
            "name": bundle_name.replace("-", " ").replace("_", " ").title(),
            "description": self._get_bundle_description(full_bundle_name),
            "version": "1.0.0",
            "artifact_type": "rule_bundle",
            "pricing_tier": self._determine_pricing_tier(full_bundle_name),
            "author": self._get_bundle_author(full_bundle_name),
            "license": "MIT",
            "homepage": self._get_bundle_homepage(full_bundle_name),
            "documentation": self._get_bundle_documentation(full_bundle_name),
            "created_at": datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "artifacts": [f"rules/{rule_file.name}" for rule_file in rule_files],
            "dependencies": [],
            "tags": analysis["categories"]
            + [f"severity-{s}" for s in analysis["severities"]],
            "metadata": {
                "rule_count": analysis["rule_count"],
                "categories": analysis["categories"],
                "severities": analysis["severities"],
                "standards": analysis["standards"],
                "compatible_scanners": ["tavoai", "semgrep", "opengrep"],
                "min_scanner_version": "1.0.0",
            },
        }

        return manifest

    def save_manifest(self, bundle_path: Path, manifest: Dict[str, Any]):
        """Save manifest to bundle directory"""
        manifest_file = bundle_path / "manifest.json"

        with open(manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved manifest: {manifest_file}")

    def create_all_manifests(self):
        """Create manifests for all bundles"""
        if not self.bundles_dir.exists():
            print(f"❌ Bundles directory not found: {self.bundles_dir}")
            return

        bundle_count = 0

        # Find all bundle directories (those containing rules/)
        for bundle_path in self.bundles_dir.rglob("*"):
            if bundle_path.is_dir() and (bundle_path / "rules").exists():
                try:
                    manifest = self.create_bundle_manifest(bundle_path)
                    self.save_manifest(bundle_path, manifest)
                    bundle_count += 1
                except Exception as e:
                    print(f"❌ Failed to create manifest for {bundle_path}: {e}")

        print(f"\n🎉 Created manifests for {bundle_count} bundles")

    def validate_manifest(self, manifest: Dict[str, Any]) -> bool:
        """Basic validation of manifest structure"""
        required_fields = ["id", "name", "version", "artifact_type", "pricing_tier"]
        for field in required_fields:
            if field not in manifest:
                print(f"❌ Missing required field: {field}")
                return False

        if manifest.get("artifact_type") != "rule_bundle":
            print("❌ Invalid artifact_type")
            return False

        pricing_tiers = ["free", "paid", "enterprise"]
        if manifest.get("pricing_tier") not in pricing_tiers:
            print(f"❌ Invalid pricing_tier: {manifest.get('pricing_tier')}")
            return False

        return True


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Create bundle manifests for TavoAI rule bundles"
    )
    parser.add_argument(
        "--repo-root",
        type=str,
        default=".",
        help="Root directory of the tavo-rules repository",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate existing manifests, don't create new ones",
    )

    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    generator = BundleManifestGenerator(repo_root)

    if args.validate_only:
        print("🔍 Validating existing manifests...")
        # TODO: Implement validation of existing manifests
        print("Validation not yet implemented")
    else:
        print("📦 Creating bundle manifests...")
        generator.create_all_manifests()
        print("✅ Bundle manifest creation complete!")


if __name__ == "__main__":
    main()
