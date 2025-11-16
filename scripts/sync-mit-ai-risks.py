#!/usr/bin/env python3
"""
MIT AI Risk Repository Sync Script

This script pulls the latest version of the MIT AI Risk Repository database
and converts risks into TavoAI rule format.

Usage:
    python sync-mit-ai-risks.py [--api-key KEY] [--sheet-id ID] [--output-dir DIR]

Requirements:
    pip install pandas pyyaml requests

MIT AI Risk Repository: https://airisk.mit.edu
"""

import argparse
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml

# Third-party imports (install via pip)
try:
    import csv
    import io
    import requests
except ImportError as e:
    print(f"Missing required packages. Install with: pip install pyyaml requests")
    print(f"Error: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MITRiskSync:
    """Sync MIT AI Risk Repository to TavoAI rules"""

    # Default Google Sheets ID for MIT AI Risk Repository
    DEFAULT_SHEET_ID = "1zbIPiSIAu6v9MI98HtB4gyM_sI4JsOSuAlVLWAIqw_U"

    # Domain mappings from MIT to TavoAI categories
    DOMAIN_MAPPING = {
        "Discrimination & Toxicity": {
            "subdomain": "discrimination",
            "category": "ethics",
            "severity": "high"
        },
        "Privacy & Security": {
            "subdomain": "security-privacy",
            "category": "security",
            "severity": "high"
        },
        "Misinformation": {
            "subdomain": "misinformation",
            "category": "ethics",
            "severity": "medium"
        },
        "Malicious Actors": {
            "subdomain": "malicious-use",
            "category": "security",
            "severity": "critical"
        },
        "Human-Computer Interaction": {
            "subdomain": "human-computer-interaction",
            "category": "ethics",
            "severity": "medium"
        },
        "Sociotechnical Harms": {
            "subdomain": "sociotechnical-risks",
            "category": "ethics",
            "severity": "high"
        },
        "AI Harms to the Environment": {
            "subdomain": "environmental",
            "category": "ethics",
            "severity": "medium"
        }
    }

    def __init__(self, sheet_id: Optional[str] = None, output_dir: Optional[str] = None):
        self.sheet_id = sheet_id or self.DEFAULT_SHEET_ID
        self.output_dir = Path(output_dir or "bundles/ai-enhanced/mit-ai-risk-repo/rules")

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download_sheet_csv(self) -> Optional[str]:
        """Download the Google Sheet as CSV using public access"""
        try:
            # Try to access the sheet publicly with redirect handling
            url = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/export?format=csv"
            response = requests.get(url, allow_redirects=True)

            if response.status_code == 200:
                logger.info("Successfully downloaded MIT AI Risk Database as CSV")
                return response.text
            else:
                logger.error(f"Failed to download sheet: HTTP {response.status_code}")
                logger.error(f"Response: {response.text[:500]}")
                return None

        except Exception as e:
            logger.error(f"Error downloading sheet: {e}")
            return None

    def parse_csv_data(self, csv_content: str) -> List[Dict[str, Any]]:
        """Parse CSV content into risk records"""
        try:
            # Parse CSV content using standard library
            csv_reader = csv.DictReader(io.StringIO(csv_content))

            risks = []
            for row in csv_reader:
                risk = {
                    'id': str(row.get('ID', '')),
                    'risk': str(row.get('Risk', '')),
                    'domain': str(row.get('Domain', '')),
                    'subdomain': str(row.get('Subdomain', '')),
                    'entity': str(row.get('Entity', '')),
                    'intent': str(row.get('Intent', '')),
                    'timing': str(row.get('Timing', '')),
                    'source_title': str(row.get('Source Title', '')),
                    'authors': str(row.get('Authors', '')),
                    'year': str(row.get('Year', '')),
                    'quote': str(row.get('Quote', '')),
                    'page_number': str(row.get('Page Number', ''))
                }
                risks.append(risk)

            logger.info(f"Parsed {len(risks)} risks from MIT database")
            return risks

        except Exception as e:
            logger.error(f"Error parsing CSV data: {e}")
            return []

    def generate_rule_from_risk(self, risk: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a MIT risk record into a TavoAI rule"""

        # Generate rule ID
        risk_id = risk.get('id', 'unknown')
        rule_id = f"tavoai-mit-risk-{risk_id}"

        # Map domain to TavoAI categories
        domain = risk.get('domain', '')
        domain_config = self.DOMAIN_MAPPING.get(domain, {
            'subdomain': 'general',
            'category': 'security',
            'severity': 'medium'
        })

        # Extract risk description
        risk_description = risk.get('risk', '')
        quote = risk.get('quote', '')

        # Determine rule type based on content
        rule_type = 'hybrid'  # Default to hybrid for AI-augmented analysis

        # Generate heuristics based on risk content
        heuristics = self._generate_heuristics(risk_description, domain)

        # Generate AI analysis prompt
        ai_analysis = self._generate_ai_analysis(risk, domain_config)

        # Build the rule
        rule = {
            'version': '1.0',
            'id': rule_id,
            'name': f"MIT AI Risk: {risk_description[:80]}{'...' if len(risk_description) > 80 else ''}",
            'category': domain_config['category'],
            'subcategory': domain_config['subdomain'],
            'severity': domain_config['severity'],
            'rule_type': rule_type,
            'standards': {
                'mit_ai_risk': [domain.lower().replace(' ', '-').replace('&', 'and')],
                'iso_42001': self._map_to_iso42001(domain),
                'nist_ai_rmf': self._map_to_nist(domain),
                'cwe': self._map_to_cwe(domain),
                'capec': self._map_to_capec(domain)
            },
            'compatible_models': [
                'openai/gpt-4',
                'anthropic/claude-3-opus'
            ],
            'tags': [
                'mit-ai-risk',
                domain_config['subdomain'],
                'ai-risk-repository'
            ]
        }

        # Add heuristics if any were generated
        if heuristics:
            rule['heuristics'] = heuristics

        # Add AI analysis
        rule['ai_analysis'] = ai_analysis

        # Add execution config
        rule['execution'] = {
            'max_tokens': 2000,
            'temperature': 0.1
        }

        # Add SARIF output config
        rule['sarif_output'] = {
            'rule_id': rule_id,
            'rule_name': rule['name'],
            'short_description': risk_description[:200],
            'full_description': f"{risk_description}\n\nSource: {risk.get('source_title', '')}\nAuthors: {risk.get('authors', '')}\nYear: {risk.get('year', '')}",
            'help_uri': f"https://airisk.mit.edu/risk/{risk_id}",
            'tags': rule['tags']
        }

        return rule

    def _generate_heuristics(self, risk_description: str, domain: str) -> List[Dict[str, Any]]:
        """Generate heuristics based on risk description and domain"""
        heuristics = []

        # Common patterns based on domain
        if 'discrimination' in domain.lower():
            heuristics.append({
                'type': 'semgrep',
                'languages': ['python'],
                'pattern': 'model\\.fit\\(.*\\).*gender|race|age',
                'message': 'Potential discriminatory model training',
                'severity': 'high'
            })

        elif 'privacy' in domain.lower():
            heuristics.append({
                'type': 'semgrep',
                'languages': ['python'],
                'pattern': 'collect.*data.*personal|private',
                'message': 'Potential privacy violation in data collection',
                'severity': 'high'
            })

        elif 'misinformation' in domain.lower():
            heuristics.append({
                'type': 'semgrep',
                'languages': ['python'],
                'pattern': 'generate.*text|response.*without.*validation',
                'message': 'Potential misinformation generation',
                'severity': 'medium'
            })

        # Add keyword-based heuristics
        keywords = re.findall(r'\b\w+\b', risk_description.lower())
        for keyword in keywords[:3]:  # Use first 3 keywords
            if len(keyword) > 3:  # Skip short words
                heuristics.append({
                    'type': 'semgrep',
                    'languages': ['python', 'javascript', 'typescript'],
                    'pattern': f'.*{re.escape(keyword)}.*',
                    'message': f'Potential {keyword} risk detected',
                    'severity': 'low'
                })

        return heuristics[:5]  # Limit to 5 heuristics

    def _generate_ai_analysis(self, risk: Dict[str, Any], domain_config: Dict[str, str]) -> Dict[str, Any]:
        """Generate AI analysis configuration"""
        risk_description = risk.get('risk', '')
        entity = risk.get('entity', '')
        intent = risk.get('intent', '')
        timing = risk.get('timing', '')

        prompt = f"""
        Analyze this AI system for the following MIT AI Risk Repository risk:

        Risk: {risk_description}
        Domain: {risk.get('domain', '')}
        Entity: {entity}
        Intent: {intent}
        Timing: {timing}

        Code to analyze:
        {{{{code_snippet}}}}

        File: {{{{file_path}}}}
        Context: {{{{heuristic_findings}}}}

        Evaluate whether this code exhibits the risk described above. Consider:
        1. Does the code enable or contribute to this specific risk?
        2. Are there mitigating factors present?
        3. What is the severity and likelihood of this risk occurring?
        4. What remediation steps would address this risk?

        Focus on the specific characteristics of this risk from the MIT AI Risk Repository.
        """

        return {
            'trigger': ['always'],
            'high_risk_patterns': [
                f"*/{domain_config['subdomain'].replace('-', '/*').replace('_', '/*')}/*",
                "*/ai/*",
                "*/model/*"
            ],
            'prompt_template': prompt.strip(),
            'expected_response_schema': {
                'type': 'object',
                'required': ['severity', 'vulnerable_lines', 'description', 'remediation', 'standards_mapping', 'confidence'],
                'properties': {
                    'severity': {'enum': ['low', 'medium', 'high', 'critical']},
                    'vulnerable_lines': {'type': 'array', 'items': {'type': 'number'}},
                    'description': {'type': 'string', 'minLength': 100},
                    'remediation': {'type': 'string', 'minLength': 100},
                    'standards_mapping': {'type': 'object'},
                    'confidence': {'type': 'number', 'minimum': 0, 'maximum': 1}
                }
            }
        }

    def _map_to_iso42001(self, domain: str) -> List[str]:
        """Map MIT domain to ISO 42001 sections"""
        mapping = {
            "Discrimination & Toxicity": ["6.2.2", "7.7.1"],
            "Privacy & Security": ["7.5.1", "7.5.2"],
            "Misinformation": ["7.3.1", "8.2.3"],
            "Malicious Actors": ["7.5.1", "8.2.1"],
            "Human-Computer Interaction": ["8.2.3"],
            "Sociotechnical Harms": ["7.7.1"],
            "AI Harms to the Environment": ["6.2.2"]
        }
        return mapping.get(domain, ["6.2.2"])

    def _map_to_nist(self, domain: str) -> List[str]:
        """Map MIT domain to NIST AI RMF functions"""
        mapping = {
            "Discrimination & Toxicity": ["MEASURE-2.2", "VALIDATE-2.3"],
            "Privacy & Security": ["PROTECT-3.1", "PROTECT-3.2"],
            "Misinformation": ["VALIDATE-2.1", "VALIDATE-2.3"],
            "Malicious Actors": ["PROTECT-3.1", "VALIDATE-2.1"],
            "Human-Computer Interaction": ["VALIDATE-2.3"],
            "Sociotechnical Harms": ["GOVERN-1.4"],
            "AI Harms to the Environment": ["MEASURE-2.2"]
        }
        return mapping.get(domain, ["MEASURE-2.2"])

    def _map_to_cwe(self, domain: str) -> List[str]:
        """Map MIT domain to CWE identifiers"""
        mapping = {
            "Discrimination & Toxicity": ["CWE-710", "CWE-20"],
            "Privacy & Security": ["CWE-200", "CWE-359"],
            "Misinformation": ["CWE-502", "CWE-20"],
            "Malicious Actors": ["CWE-284", "CWE-502"],
            "Human-Computer Interaction": ["CWE-710"],
            "Sociotechnical Harms": ["CWE-710"],
            "AI Harms to the Environment": ["CWE-710"]
        }
        return mapping.get(domain, ["CWE-710"])

    def _map_to_capec(self, domain: str) -> List[str]:
        """Map MIT domain to CAPEC identifiers"""
        mapping = {
            "Discrimination & Toxicity": ["CAPEC-183", "CAPEC-165"],
            "Privacy & Security": ["CAPEC-167", "CAPEC-118"],
            "Misinformation": ["CAPEC-183", "CAPEC-184"],
            "Malicious Actors": ["CAPEC-550", "CAPEC-137"],
            "Human-Computer Interaction": ["CAPEC-114", "CAPEC-183"],
            "Sociotechnical Harms": ["CAPEC-165"],
            "AI Harms to the Environment": ["CAPEC-165"]
        }
        return mapping.get(domain, ["CAPEC-165"])

    def save_rule(self, rule: Dict[str, Any]):
        """Save a rule to a YAML file"""
        rule_id = rule['id']
        filename = f"{rule_id}.yaml"
        filepath = self.output_dir / filename

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(rule, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            logger.info(f"Saved rule: {filepath}")
        except Exception as e:
            logger.error(f"Failed to save rule {rule_id}: {e}")

    def get_mock_data(self) -> List[Dict[str, Any]]:
        """Generate mock risk data for testing"""
        return [
            {
                'id': 'R001',
                'risk': 'AI systems that create unfair discrimination',
                'domain': 'Discrimination & Toxicity',
                'subdomain': 'Unfair discrimination and misrepresentation',
                'entity': 'AI',
                'intent': 'Unintentional',
                'timing': 'Post-deployment',
                'source_title': 'AI Risk Repository Test',
                'authors': 'MIT Team',
                'year': '2024',
                'quote': 'AI systems can create unfair discrimination',
                'page_number': '1'
            },
            {
                'id': 'R002',
                'risk': 'Unauthorized access to sensitive personal data',
                'domain': 'Privacy & Security',
                'subdomain': 'Compromise of privacy by obtaining sensitive information',
                'entity': 'AI',
                'intent': 'Unintentional',
                'timing': 'Post-deployment',
                'source_title': 'AI Risk Repository Test',
                'authors': 'MIT Team',
                'year': '2024',
                'quote': 'AI can compromise user privacy',
                'page_number': '2'
            },
            {
                'id': 'R003',
                'risk': 'AI systems generating misleading information',
                'domain': 'Misinformation',
                'subdomain': 'False or misleading information',
                'entity': 'AI',
                'intent': 'Unintentional',
                'timing': 'Post-deployment',
                'source_title': 'AI Risk Repository Test',
                'authors': 'MIT Team',
                'year': '2024',
                'quote': 'AI can generate misleading information',
                'page_number': '3'
            }
        ]

    def sync(self, limit: Optional[int] = None, use_mock: bool = False):
        """Sync all risks from MIT AI Risk Repository"""
        logger.info("Starting MIT AI Risk Repository sync")

        if use_mock:
            # Use mock data for testing
            risks = self.get_mock_data()
            logger.info("Using mock data for testing")
        else:
            # Download the latest data
            csv_content = self.download_sheet_csv()
            if not csv_content:
                logger.error("Failed to download MIT AI Risk Database")
                return

            # Parse the risks
            risks = self.parse_csv_data(csv_content)
            if not risks:
                logger.error("Failed to parse risk data")
                return

        # Limit for testing
        if limit:
            risks = risks[:limit]
            logger.info(f"Limited to {limit} risks for testing")

        # Convert and save each risk as a rule
        for i, risk in enumerate(risks):
            try:
                rule = self.generate_rule_from_risk(risk)
                self.save_rule(rule)

                if (i + 1) % 100 == 0:
                    logger.info(f"Processed {i + 1}/{len(risks)} risks")

            except Exception as e:
                logger.error(f"Failed to process risk {risk.get('id', 'unknown')}: {e}")
                continue

        logger.info(f"Successfully synced {len(risks)} MIT AI risks to TavoAI rules")

    def validate_rules(self):
        """Validate generated rules using existing validation script"""
        try:
            import subprocess
            script_dir = Path(__file__).parent
            validate_script = script_dir / 'validate-rules.py'

            if not validate_script.exists():
                logger.warning("validate-rules.py not found, skipping validation")
                return

            # The validate script expects the repo root (containing schemas/), not the rules dir
            repo_root = script_dir.parent

            result = subprocess.run([
                sys.executable, str(validate_script),
                '--rules-dir', str(repo_root),
                '--rules'
            ], capture_output=True, text=True, cwd=str(repo_root))

            if result.returncode == 0:
                logger.info("All generated rules passed validation")
            else:
                logger.warning("Some rules failed validation")
                if result.stdout:
                    logger.info(result.stdout)
                if result.stderr:
                    logger.warning(result.stderr)

        except Exception as e:
            logger.error(f"Failed to run validation: {e}")


def main():
    parser = argparse.ArgumentParser(description="Sync MIT AI Risk Repository to TavoAI rules")
    parser.add_argument('--sheet-id', default=MITRiskSync.DEFAULT_SHEET_ID,
                       help='Google Sheets ID for MIT AI Risk Database')
    parser.add_argument('--output-dir', default='bundles/ai-enhanced/mit-ai-risk-repo/rules',
                       help='Output directory for generated rules')
    parser.add_argument('--limit', type=int, help='Limit number of risks to process (for testing)')
    parser.add_argument('--validate', action='store_true', help='Validate generated rules')
    parser.add_argument('--mock-data', action='store_true', help='Use mock data for testing')

    args = parser.parse_args()

    # Initialize sync tool
    sync_tool = MITRiskSync(
        sheet_id=args.sheet_id,
        output_dir=args.output_dir
    )

    # Run sync
    sync_tool.sync(limit=args.limit, use_mock=args.mock_data)

    # Validate if requested
    if args.validate:
        sync_tool.validate_rules()


if __name__ == '__main__':
    main()
