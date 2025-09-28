# Tavo Rules Repository

Open source security rule bundles for Tavo AI security scanning.

## Repository Structure

```text
tavo-rules/
├── bundles/                    # Rule bundles directory
│   ├── llm-security/          # OWASP LLM Top 10 rules
│   ├── ai-ethics/             # AI ethics and fairness rules
│   ├── compliance/            # Regulatory compliance rules
│   ├── infrastructure/        # Cloud/container security rules
│   └── application/           # Web/API security rules
├── README.md                  # This file
└── LICENSE                    # Open source license
```

Each bundle directory contains:

- `index.json`: Bundle metadata and rule catalog
- `*.yaml`: OpenGrep pattern matching rules
- `*.rego`: OPA policy evaluation rules (future)

## Bundle Categories

- **llm-security**: OWASP LLM Top 10 and AI security rules
- **ai-ethics**: AI ethics, bias detection, and fairness rules
- **compliance**: Regulatory compliance rules (ISO 42001, SOC 2, GDPR)
- **infrastructure**: Cloud, container, and infrastructure security
- **application**: Web applications, APIs, and authentication security

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
