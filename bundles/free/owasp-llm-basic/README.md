# OWASP LLM Top 10 Basic

Heuristic-only security rules for detecting OWASP LLM Top 10 vulnerabilities.

## Overview

This bundle provides fast, pattern-based detection for the most common LLM security vulnerabilities without requiring AI analysis or API keys. Perfect for basic security scanning and CI/CD integration.

## Included Rules

| Rule ID | Name | Severity | Description |
|---------|------|----------|-------------|
| `llm01` | Prompt Injection | High | Direct user input in LLM prompts |
| `llm02` | Insecure Output Handling | High | Unsafe handling of LLM responses |
| `llm03` | Training Data Poisoning | Medium | Potential training data contamination |
| `llm04` | Model Denial of Service | Medium | Resource exhaustion attacks |
| `llm05` | Supply Chain Vulnerabilities | High | Untrusted model sources |
| `llm06` | Sensitive Information Disclosure | High | Leaking sensitive data |
| `llm07` | Insecure Plugin Design | Medium | Plugin security issues |
| `llm08` | Excessive Agency | Medium | Overly permissive LLM actions |
| `llm09` | Overreliance | Low | Blind trust in LLM outputs |
| `llm10` | Model Theft | High | Unauthorized model access |

## Usage

### TavoAI CLI

```bash
# Scan with OWASP LLM Basic rules
tavoai scan --bundle owasp-llm-basic --path ./code

# Combine with other scanners
tavoai scan --bundle owasp-llm-basic --bundle semgrep-rules/python --path ./code
```

### Programmatic Usage

```python
from tavoai import Scanner

scanner = Scanner()
results = scanner.scan_codebase(
    path="./my-project",
    bundle_name="owasp-llm-basic"
)
```

### GitHub Actions

```yaml
- name: Security Scan
  uses: tavoai/scan-action@v1
  with:
    bundle: owasp-llm-basic
    path: ./src
```

## Standards Compliance

All rules map to OWASP LLM Top 10 standards:

- **LLM01**: Prompt Injection
- **LLM02**: Insecure Output Handling
- **LLM03**: Training Data Poisoning
- **LLM04**: Model Denial of Service
- **LLM05**: Supply Chain Vulnerabilities
- **LLM06**: Sensitive Information Disclosure
- **LLM07**: Insecure Plugin Design
- **LLM08**: Excessive Agency
- **LLM09**: Overreliance
- **LLM10**: Model Theft

## Performance

- **Speed**: Sub-second scanning for most codebases
- **Memory**: Minimal memory footprint
- **False Positives**: Low (pattern-based detection)
- **Languages**: Python, JavaScript, TypeScript, Java, Go

## Requirements

- **API Key**: Not required (free bundle)
- **Dependencies**: None
- **Compatible Tools**: Semgrep, OpenGrep, custom scanners

## Support

- **Documentation**: [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- **Issues**: [GitHub Issues](https://github.com/TavoAI/tavo-rules/issues)
- **Discussions**: [GitHub Discussions](https://github.com/TavoAI/tavo-rules/discussions)

## Changelog

### v1.0.0
- Initial release with 10 OWASP LLM Top 10 rules
- Pattern-based detection for all major LLM vulnerabilities
- Multi-language support (Python, JavaScript, TypeScript, Java, Go)
