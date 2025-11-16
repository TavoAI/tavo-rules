# Tavo Rules Repository

Open source security rule bundles for Tavo AI security scanning.

## Repository Structure

```text
tavo-rules/
├── bundles/                    # Rule bundles directory
│   ├── free/                   # Free rule bundles (no API key required)
│   ├── ai-enhanced/            # AI-enhanced bundles (API key required)
│   └── enterprise/             # Enterprise rule bundles
├── formats/                    # External rule format references
│   ├── semgrep-rules/          # Semgrep rule format reference
│   ├── opa-policies/           # OPA policy format reference
│   ├── yara-rules/             # YARA rule format reference
│   └── sigma-rules/            # Sigma rule format reference
├── schemas/                    # JSON validation schemas
├── scripts/                    # Development and maintenance scripts
├── docs/                       # Documentation
├── templates/                  # Rule templates
├── README.md                   # This file
└── LICENSE                     # Open source license
```

## Bundle Categories

### Free Bundles (`bundles/free/`)
- **OWASP LLM Basic**: Heuristic-only OWASP LLM Top 10 rules
- Available without API key from GitHub
- Fast pattern-based detection

### AI-Enhanced Bundles (`bundles/ai-enhanced/`)
- **OWASP LLM Pro**: AI-enhanced OWASP LLM Top 10 analysis
- **ISO 42001**: AI governance compliance rules
- **MIT AI Risk**: Comprehensive AI risk detection
- **AI Ethics**: Ethical AI development rules
- **Bias Detection**: AI bias and fairness rules
- Require API key for LLM-powered deep analysis

### Enterprise Bundles (`bundles/enterprise/`)
- Custom enterprise rules
- Industry-specific compliance
- Advanced threat detection

## External Rule Integration

TavoAI supports running rules from external repositories while respecting licensing terms. We do not redistribute external rules but enable customers to use them directly.

### Supported External Sources

- **Semgrep Rules**: https://github.com/semgrep/semgrep-rules
- **OPA Policies**: https://github.com/open-policy-agent/library
- **YARA Rules**: https://github.com/Yara-Rules/rules
- **Sigma Rules**: https://github.com/SigmaHQ/sigma

### Usage

```bash
# Run external semgrep rules directly
tavoai scan --rules github:semgrep/semgrep-rules/python --target ./code

# Combine external and TavoAI rules
tavoai scan \
  --rules github:semgrep/semgrep-rules \
  --rules tavoai:ai-enhanced/owasp-llm-pro \
  --target ./code
```

See [External Rule Integration](./docs/external-rule-integration.md) for details.

## Licensing and Redistribution

### Our Rules (MIT License)
- All rules in `bundles/` are licensed under MIT
- Free to use, modify, and distribute
- AI-enhanced features require TavoAI API key

### External Rules
- We respect external repository licenses
- Do not redistribute or modify external rules
- Enable customers to access external rules directly
- Provide integration without violating licenses

## Rule Formats

### OpenGrep (YAML)

```yaml
rules:
  - id: rule_id
    message: "Security vulnerability description"
    languages: [python, javascript]
    patterns:
      - pattern: "vulnerable_pattern"
    severity: HIGH
    metadata:
      cwe: "CWE-123"
      owasp-llm: "LLM01"
```

### OPA (Rego)

```rego
package tavo.security

default allow = false

allow if {
    input.action == "read"
    input.resource.type == "secret"
    input.user.role == "admin"
}
```

## Contributing

1. Create rules in appropriate bundle directory
2. Test rules with `tavo-cli`
3. Submit pull request with rule documentation
4. Rules must include test cases and metadata
