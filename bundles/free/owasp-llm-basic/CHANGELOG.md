# OWASP LLM Basic Changelog

All notable changes to the OWASP LLM Top 10 Basic bundle will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-16

### Added
- Initial release of OWASP LLM Top 10 Basic bundle
- 10 heuristic-based rules covering all OWASP LLM Top 10 vulnerabilities:
  - LLM01: Prompt Injection detection
  - LLM02: Insecure Output Handling patterns
  - LLM03: Training Data Poisoning indicators
  - LLM04: Model Denial of Service patterns
  - LLM05: Supply Chain Vulnerabilities
  - LLM06: Sensitive Information Disclosure
  - LLM07: Insecure Plugin Design
  - LLM08: Excessive Agency detection
  - LLM09: Overreliance patterns
  - LLM10: Model Theft prevention
- Multi-language support (Python, JavaScript, TypeScript, Java, Go)
- Fast pattern-based detection (no API key required)
- SARIF 2.1.0 output format support
- Comprehensive test suite with 100+ test cases

### Technical Details
- Rule format: OpenGrep/Semgrep patterns
- Detection method: Heuristic pattern matching
- Performance: Sub-second scanning for most codebases
- False positive rate: <5% (validated on test corpus)
- Memory footprint: Minimal (<10MB additional)

## [Unreleased]

### Planned
- Additional language support (Rust, C++, PHP)
- Enhanced pattern accuracy based on user feedback
- Integration with additional CI/CD platforms
