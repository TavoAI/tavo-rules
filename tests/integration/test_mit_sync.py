#!/usr/bin/env python3
"""
Integration tests for MIT AI Risk sync functionality
"""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the sync functionality
import sys

sys.path.append(str(Path(__file__).parent.parent.parent / "scripts"))

from sync_mit_ai_risks import MITRiskSync


class TestMITRiskSync:
    """Test the MIT AI Risk sync functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.sync_tool = MITRiskSync(sheet_id="test_sheet", output_dir=self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_sync_initialization(self):
        """Test that sync tool initializes correctly"""
        assert self.sync_tool.sheet_id == "test_sheet"
        assert self.sync_tool.output_dir == self.temp_dir
        assert self.sync_tool.output_dir.exists()

    def test_get_mock_data(self):
        """Test mock data generation"""
        mock_data = self.sync_tool.get_mock_data()

        assert isinstance(mock_data, list)
        assert len(mock_data) == 3  # We defined 3 mock risks

        # Check structure of first risk
        risk = mock_data[0]
        required_fields = ["id", "risk", "domain", "entity", "intent", "timing"]

        for field in required_fields:
            assert field in risk
            assert risk[field] is not None

    def test_csv_parsing(self):
        """Test CSV data parsing"""
        csv_content = """ID,Risk,Domain,Entity,Intent,Timing
R001,Test risk 1,Security & Privacy,AI,Unintentional,Post-deployment
R002,Test risk 2,Misinformation,Human,Intentional,Pre-deployment
"""

        risks = self.sync_tool.parse_csv_data(csv_content)

        assert len(risks) == 2
        assert risks[0]["id"] == "R001"
        assert risks[0]["domain"] == "Security & Privacy"
        assert risks[1]["id"] == "R002"
        assert risks[1]["entity"] == "Human"

    def test_rule_generation(self):
        """Test rule generation from risk data"""
        test_risk = {
            "id": "R001",
            "risk": "AI systems that create unfair discrimination",
            "domain": "Discrimination & Toxicity",
            "entity": "AI",
            "intent": "Unintentional",
            "timing": "Post-deployment",
            "source_title": "Test Source",
            "authors": "Test Author",
            "year": "2024",
            "quote": "Test quote",
            "page_number": "1",
        }

        rule = self.sync_tool.generate_rule_from_risk(test_risk)

        # Check required fields
        assert rule["id"] == "tavoai-mit-risk-R001"
        assert "MIT AI Risk" in rule["name"]
        assert rule["category"] == "ethics"
        assert rule["subcategory"] == "discrimination"
        assert rule["severity"] == "high"
        assert rule["rule_type"] == "hybrid"

        # Check standards mapping
        assert "mit_ai_risk" in rule["standards"]
        assert "iso_42001" in rule["standards"]
        assert "nist_ai_rmf" in rule["standards"]

        # Check heuristics exist
        assert "heuristics" in rule
        assert len(rule["heuristics"]) > 0

        # Check AI analysis exists
        assert "ai_analysis" in rule
        assert "prompt_template" in rule["ai_analysis"]

        # Check SARIF output
        assert "sarif_output" in rule
        assert rule["sarif_output"]["rule_id"] == rule["id"]

    @patch("sync_mit_ai_risks.MITRiskSync.download_sheet_csv")
    def test_sync_with_mock_download(self, mock_download):
        """Test sync with mocked download"""
        # Mock CSV download
        mock_download.return_value = """ID,Risk,Domain,Entity,Intent,Timing
R001,Test risk 1,Security & Privacy,AI,Unintentional,Post-deployment
R002,Test risk 2,Misinformation,Human,Intentional,Pre-deployment
"""

        self.sync_tool.sync(limit=2)

        # Check that rules were created
        rule_files = list(self.temp_dir.glob("*.yaml"))
        assert len(rule_files) == 2

        # Check content of first rule
        with open(rule_files[0], "r") as f:
            import yaml

            rule_data = yaml.safe_load(f)

            assert "tavoai-mit-risk-R001" in rule_data["id"]
            assert rule_data["category"] == "security"
            assert rule_data["subcategory"] == "security-privacy"

    def test_sync_with_mock_data(self):
        """Test sync using mock data"""
        self.sync_tool.sync(limit=2, use_mock=True)

        # Check that rules were created
        rule_files = list(self.temp_dir.glob("*.yaml"))
        assert len(rule_files) == 2

        # Verify rule content
        with open(rule_files[0], "r") as f:
            import yaml

            rule_data = yaml.safe_load(f)

            assert rule_data["version"] == "1.0"
            assert "tavoai-mit-risk-R" in rule_data["id"]
            assert rule_data["rule_type"] == "hybrid"

    def test_domain_mappings(self):
        """Test domain to category mappings"""
        mappings = self.sync_tool.DOMAIN_MAPPING

        # Check that all expected domains are mapped
        expected_domains = [
            "Discrimination & Toxicity",
            "Privacy & Security",
            "Misinformation",
            "Malicious Actors",
            "Human-Computer Interaction",
            "Sociotechnical Harms",
            "AI Harms to the Environment",
        ]

        for domain in expected_domains:
            assert domain in mappings
            mapping = mappings[domain]
            assert "category" in mapping
            assert "subdomain" in mapping
            assert "severity" in mapping

    def test_standards_mapping(self):
        """Test standards mapping functions"""
        # Test ISO mapping
        iso_mapping = self.sync_tool._map_to_iso42001("Discrimination & Toxicity")
        assert isinstance(iso_mapping, list)
        assert len(iso_mapping) > 0

        # Test NIST mapping
        nist_mapping = self.sync_tool._map_to_nist("Privacy & Security")
        assert isinstance(nist_mapping, list)
        assert len(nist_mapping) > 0

        # Test CWE mapping
        cwe_mapping = self.sync_tool._map_to_cwe("Misinformation")
        assert isinstance(cwe_mapping, list)

        # Test CAPEC mapping
        capec_mapping = self.sync_tool._map_to_capec("Malicious Actors")
        assert isinstance(capec_mapping, list)

    @patch("sync_mit_ai_risks.requests.get")
    def test_csv_download_error_handling(self, mock_get):
        """Test error handling in CSV download"""
        # Mock a failed request
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        mock_get.return_value = mock_response

        result = self.sync_tool.download_sheet_csv()
        assert result is None

    def test_empty_csv_handling(self):
        """Test handling of empty CSV data"""
        risks = self.sync_tool.parse_csv_data("")
        assert risks == []

    def test_invalid_csv_handling(self):
        """Test handling of invalid CSV data"""
        risks = self.sync_tool.parse_csv_data(
            "invalid,csv,data\nwithout,proper,headers"
        )
        # Should still parse but might not have expected fields
        assert isinstance(risks, list)
