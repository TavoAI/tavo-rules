# OWASP LLM Top 10 Pro

AI-enhanced security rules with deep contextual analysis for OWASP LLM Top 10 vulnerabilities.

## Overview

This premium bundle provides advanced LLM security scanning with AI-powered deep analysis, contextual understanding, and comprehensive vulnerability detection. Requires TavoAI API key for LLM analysis capabilities.

## Key Features

- ✅ **AI-Powered Analysis**: Deep contextual understanding of code patterns
- ✅ **Multi-Layer Detection**: Combines heuristics with AI reasoning
- ✅ **Contextual Accuracy**: Understands code intent and security implications
- ✅ **Comprehensive Coverage**: All OWASP LLM Top 10 vulnerabilities
- ✅ **SARIF Output**: Industry-standard security findings format
- ✅ **Standards Mapping**: CWE, CAPEC, OWASP LLM mappings

## Included Rules

| Rule ID | Name | Severity | AI Enhancement |
|---------|------|----------|----------------|
| `llm01` | Prompt Injection | High | Context-aware injection detection |
| `llm02` | Insecure Output Handling | High | Output validation analysis |
| `llm03` | Training Data Poisoning | Medium | Data pipeline security review |
| `llm04` | Model Denial of Service | Medium | Resource usage pattern analysis |
| `llm05` | Supply Chain Vulnerabilities | High | Dependency chain analysis |
| `llm06` | Sensitive Information Disclosure | High | Data flow and leakage analysis |
| `llm07` | Insecure Plugin Design | Medium | Plugin architecture review |
| `llm08` | Excessive Agency | Medium | Permission and access analysis |
| `llm09` | Overreliance | Low | Usage pattern analysis |
| `llm10` | Model Theft | High | Model protection analysis |

## Usage

### TavoAI CLI

```bash
# Requires API key
export TAVOAI_API_KEY=your_api_key_here

# Scan with AI-enhanced analysis
tavoai scan --bundle owasp-llm-pro --path ./code

# Generate SARIF report
tavoai scan --bundle owasp-llm-pro --path ./code --format sarif --output results.sarif
```

### Programmatic Usage

```python
from tavoai import Scanner

scanner = Scanner(api_key="your_api_key")

results = scanner.scan_codebase(
    path="./my-project",
    bundle_name="owasp-llm-pro",
    mode="hybrid"  # Enables AI analysis
)

# Export to SARIF
sarif_output = scanner.generate_sarif(results)
with open("security-results.sarif", "w") as f:
    f.write(sarif_output)
```

### GitHub Actions

```yaml
- name: AI-Enhanced Security Scan
  uses: tavoai/scan-action@v1
  with:
    bundle: owasp-llm-pro
    path: ./src
    api-key: ${{ secrets.TAVOAI_API_KEY }}
    format: sarif
  # Upload SARIF for GitHub Security tab
  - name: Upload SARIF
    uses: github/codeql-action/upload-sarif@v2
    with:
      sarif_file: results.sarif
```

## AI Analysis Features

### Deep Contextual Understanding
- Analyzes code intent beyond surface patterns
- Understands data flow and control structures
- Identifies indirect vulnerabilities

### Intelligent False Positive Reduction
- Contextual analysis reduces false alarms
- Understands sanitization and validation
- Recognizes safe usage patterns

### Standards-Aware Analysis
- Maps findings to CWE, CAPEC, OWASP standards
- Provides remediation guidance
- Includes severity scoring

## Performance

- **Analysis Depth**: Deep contextual analysis
- **Processing Time**: 2-10 seconds per file (AI analysis)
- **Accuracy**: >90% detection rate with <5% false positives
- **Token Usage**: Efficient AI prompting minimizes costs

## Requirements

- **API Key**: Required for AI analysis features
- **Billing**: Metered usage for AI analysis
- **Dependencies**: TavoAI SDK
- **Languages**: All major programming languages

## Standards Compliance

### OWASP LLM Top 10 Mapping
- **LLM01**: Prompt Injection → CWE-77, CWE-89, CAPEC-137
- **LLM02**: Insecure Output Handling → CWE-79, CWE-200
- **LLM03**: Training Data Poisoning → CWE-20, CWE-502
- **LLM04**: Model Denial of Service → CWE-400, CWE-770
- **LLM05**: Supply Chain Vulnerabilities → CWE-494, CWE-829
- **LLM06**: Sensitive Information Disclosure → CWE-200, CWE-359
- **LLM07**: Insecure Plugin Design → CWE-284, CWE-285
- **LLM08**: Excessive Agency → CWE-284, CWE-862
- **LLM09**: Overreliance → CWE-20, CWE-710
- **LLM10**: Model Theft → CWE-284, CWE-287

## Support

- **Documentation**: [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- **API Docs**: [TavoAI API](https://docs.tavoai.com/api)
- **Issues**: [GitHub Issues](https://github.com/TavoAI/tavo-rules/issues)
- **Support**: [TavoAI Support](https://support.tavoai.com)

## Changelog

### v1.0.0
- Initial release with AI-enhanced OWASP LLM Top 10 analysis
- Deep contextual analysis for all vulnerability types
- SARIF 2.1.0 output with comprehensive standards mapping
- Multi-language support with language-specific analysis
