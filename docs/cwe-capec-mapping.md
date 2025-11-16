# CWE/CAPEC Mapping Guide for TavoAI Rules

## Overview

This guide provides comprehensive mapping between TavoAI security rules and industry-standard security frameworks including CWE (Common Weakness Enumeration), CAPEC (Common Attack Pattern Enumeration and Classification), OWASP LLM Top 10, and ISO 42001.

## CWE (Common Weakness Enumeration)

### CWE Structure

CWE uses a hierarchical classification:

```
CWE-1000+  Research Concepts
CWE-700-1000  Pillar/Category
CWE-100-699   Class/Base
CWE-1-99      Variant
```

### Key CWE Categories for AI/ML Security

#### Input Validation and Sanitization
```
CWE-20: Improper Input Validation
├── CWE-79: Cross-site Scripting
├── CWE-89: SQL Injection
├── CWE-78: OS Command Injection
└── CWE-502: Deserialization of Untrusted Data
```

#### Authentication and Access Control
```
CWE-287: Improper Authentication
├── CWE-798: Use of Hard-coded Credentials
├── CWE-862: Missing Authorization
└── CWE-863: Incorrect Authorization
```

#### Cryptographic Issues
```
CWE-310: Cryptographic Issues
├── CWE-327: Use of a Broken or Risky Cryptographic Algorithm
├── CWE-328: Use of Weak Hash
└── CWE-329: Not Using a Random IV with CBC Mode
```

#### AI/ML Specific Issues
```
CWE-1395: Dependency on Vulnerable Third-Party Component
CWE-20: Improper Input Validation (for AI inputs)
CWE-200: Exposure of Sensitive Information (model leakage)
CWE-284: Improper Access Control (model access)
```

## CAPEC (Common Attack Pattern Enumeration)

### CAPEC Structure

CAPEC organizes attacks by:
- **Meta Attack Patterns**: High-level attack strategies
- **Attack Patterns**: Specific attack techniques
- **Mechanisms of Attack**: Implementation details

### AI/ML Attack Patterns

#### Prompt Injection Attacks
```
CAPEC-550: Install New Service (prompt manipulation)
CAPEC-151: Identity Spoofing (persona manipulation)
CAPEC-137: Parameter Manipulation (prompt parameter tampering)
```

#### Model Exploitation
```
CAPEC-165: File Manipulation (model file tampering)
CAPEC-176: Configuration Data Manipulation (model configuration)
CAPEC-77: Manipulating User-Controlled Variables (input manipulation)
```

#### Data Poisoning
```
CAPEC-183: Create Malicious Client (poison training data)
CAPEC-184: Software Integrity Attack (corrupt training pipeline)
CAPEC-552: Local Execution of Code (inject malicious training code)
```

## OWASP LLM Top 10 Mapping

### LLM01: Prompt Injection
```yaml
standards:
  cwe: ["CWE-1395", "CWE-20", "CWE-502"]
  capec: ["CAPEC-550", "CAPEC-137", "CAPEC-77"]
  owasp_llm: ["LLM01"]
  iso_42001: ["7.5.1"]  # Information security
```

**Description**: Injection of malicious prompts to manipulate AI behavior
**Examples**: Direct prompt manipulation, jailbreak attacks, context poisoning
**Remediation**: Input validation, prompt sanitization, output filtering

### LLM02: Insecure Output Handling
```yaml
standards:
  cwe: ["CWE-79", "CWE-89", "CWE-78"]
  capec: ["CAPEC-7", "CAPEC-66", "CAPEC-77"]
  owasp_llm: ["LLM02"]
  iso_42001: ["8.2.1"]  # Validation of AI outputs
```

**Description**: Unvalidated AI outputs used in security-critical operations
**Examples**: XSS via AI responses, SQL injection from AI-generated queries
**Remediation**: Output validation, content filtering, safe execution patterns

### LLM03: Training Data Poisoning
```yaml
standards:
  cwe: ["CWE-502", "CWE-20"]
  capec: ["CAPEC-183", "CAPEC-184", "CAPEC-552"]
  owasp_llm: ["LLM03"]
  iso_42001: ["7.3.1"]  # Data quality management
```

**Description**: Malicious data introduced during model training
**Examples**: Backdoor insertion, bias amplification, performance degradation
**Remediation**: Data validation, integrity checks, provenance tracking

### LLM04: Model Denial of Service
```yaml
standards:
  cwe: ["CWE-400", "CWE-770"]
  capec: ["CAPEC-125", "CAPEC-488"]
  owasp_llm: ["LLM04"]
  iso_42001: ["8.3.1"]  # Resource management
```

**Description**: Resource exhaustion attacks against AI models
**Examples**: Infinite loops, excessive token consumption, computational attacks
**Remediation**: Rate limiting, resource monitoring, timeout mechanisms

### LLM05: Supply Chain Vulnerabilities
```yaml
standards:
  cwe: ["CWE-1395", "CWE-494"]
  capec: ["CAPEC-439", "CAPEC-440"]
  owasp_llm: ["LLM05"]
  iso_42001: ["7.6.1"]  # Third-party management
```

**Description**: Compromised components in AI supply chain
**Examples**: Malicious models, poisoned datasets, vulnerable dependencies
**Remediation**: Supply chain security, integrity verification, dependency scanning

### LLM06: Sensitive Information Disclosure
```yaml
standards:
  cwe: ["CWE-200", "CWE-359"]
  capec: ["CAPEC-118", "CAPEC-167"]
  owasp_llm: ["LLM06"]
  iso_42001: ["7.5.1"]  # Information security
```

**Description**: AI systems leaking sensitive information
**Examples**: Training data exposure, prompt leakage, inference attacks
**Remediation**: Data sanitization, access controls, output filtering

### LLM07: Insecure Plugin Design
```yaml
standards:
  cwe: ["CWE-284", "CWE-862"]
  capec: ["CAPEC-17", "CAPEC-36"]
  owasp_llm: ["LLM07"]
  iso_42001: ["8.2.2"]  # Plugin security validation
```

**Description**: Vulnerable plugin architectures in AI systems
**Examples**: Privilege escalation, unauthorized access, insecure integrations
**Remediation**: Secure plugin architecture, permission models, validation

### LLM08: Excessive Agency
```yaml
standards:
  cwe: ["CWE-284", "CWE-862"]
  capec: ["CAPEC-233", "CAPEC-114"]
  owasp_llm: ["LLM08"]
  iso_42001: ["7.2.2"]  # AI system boundaries
```

**Description**: AI systems with excessive permissions or autonomy
**Examples**: Unauthorized actions, privilege misuse, scope creep
**Remediation**: Permission boundaries, human oversight, action limits

### LLM09: Overreliance
```yaml
standards:
  cwe: ["CWE-710", "CWE-20"]
  capec: ["CAPEC-114", "CAPEC-183"]
  owasp_llm: ["LLM09"]
  iso_42001: ["8.2.3"]  # Human oversight requirements
```

**Description**: Blind trust in AI outputs without validation
**Examples**: Critical decisions without verification, false confidence
**Remediation**: Human-in-the-loop, confidence thresholds, validation requirements

### LLM10: Model Theft
```yaml
standards:
  cwe: ["CWE-200", "CWE-284"]
  capec: ["CAPEC-167", "CAPEC-165"]
  owasp_llm: ["LLM10"]
  iso_42001: ["7.5.2"]  # Model protection
```

**Description**: Unauthorized access to or theft of AI models
**Examples**: Model exfiltration, API abuse, intellectual property theft
**Remediation**: Access controls, model protection, usage monitoring

## ISO 42001 AI Management System Mapping

### ISO 42001 Structure

ISO 42001 organizes AI governance into sections:

```
Section 6: Planning (AI system design and development)
Section 7: Support (resource and infrastructure management)
Section 8: Operation (AI system deployment and monitoring)
Section 9: Performance evaluation (continuous improvement)
Section 10: Improvement (corrective and preventive actions)
```

### Key ISO 42001 Mappings

#### Risk Management (7.2)
```yaml
iso_42001: ["7.2.1"]  # AI system risk assessment
standards:
  cwe: ["CWE-710"]
  capec: ["CAPEC-100"]
  description: "Formal risk assessment for AI systems"
```

#### Data Governance (7.3)
```yaml
iso_42001: ["7.3.1"]  # Data quality management
standards:
  cwe: ["CWE-20", "CWE-502"]
  capec: ["CAPEC-183"]
  description: "Data quality, provenance, and governance"
```

#### AI System Development (6.2)
```yaml
iso_42001: ["6.2.1"]  # AI system design
standards:
  cwe: ["CWE-710"]
  capec: ["CAPEC-100"]
  description: "Secure AI system design principles"
```

#### Validation and Testing (8.2)
```yaml
iso_42001: ["8.2.1"]  # Validation of AI system performance
standards:
  cwe: ["CWE-20"]
  capec: ["CAPEC-124"]
  description: "AI system validation and testing"
```

#### Information Security (7.5)
```yaml
iso_42001: ["7.5.1"]  # Information security
standards:
  cwe: ["CWE-200", "CWE-284"]
  capec: ["CAPEC-118"]
  description: "Information security for AI systems"
```

## NIST AI Risk Management Framework Mapping

### NIST AI RMF Core Functions

```
IDENTIFY: Understand AI system context and risks
DEVELOP: Secure AI system development
VALIDATE: Testing and evaluation
DEPLOY: Secure deployment and operation
MONITOR: Ongoing monitoring and assessment
```

### NIST AI RMF Mappings

#### GOVERN Function
```yaml
nist_ai_rmf: ["GOVERN-1.3"]  # Risk management processes
standards:
  cwe: ["CWE-710"]
  capec: ["CAPEC-100"]
  description: "AI governance and risk management"
```

#### MEASURE Function
```yaml
nist_ai_rmf: ["MEASURE-2.1"]  # AI system measurement
standards:
  cwe: ["CWE-20"]
  capec: ["CAPEC-124"]
  description: "AI system performance measurement"
```

#### MANAGE Function
```yaml
nist_ai_rmf: ["MANAGE-3.2"]  # AI system management
standards:
  cwe: ["CWE-284"]
  capec: ["CAPEC-17"]
  description: "AI system operational management"
```

## Practical Mapping Examples

### Example 1: Prompt Injection Rule
```yaml
version: "1.0"
id: "tavoai-prompt-injection"
name: "Prompt Injection Detection"
standards:
  cwe: ["CWE-1395", "CWE-20", "CWE-502"]
  capec: ["CAPEC-550", "CAPEC-137", "CAPEC-77"]
  owasp_llm: ["LLM01"]
  iso_42001: ["7.5.1", "8.2.1"]
  nist_ai_rmf: ["VALIDATE-2.3"]
```

### Example 2: Data Poisoning Rule
```yaml
version: "1.0"
id: "tavoai-data-poisoning"
name: "Training Data Poisoning Detection"
standards:
  cwe: ["CWE-502", "CWE-20"]
  capec: ["CAPEC-183", "CAPEC-184", "CAPEC-552"]
  owasp_llm: ["LLM03"]
  iso_42001: ["7.3.1", "6.2.2"]
  nist_ai_rmf: ["DEVELOP-1.4"]
```

### Example 3: Model Access Control Rule
```yaml
version: "1.0"
id: "tavoai-model-access"
name: "AI Model Access Control"
standards:
  cwe: ["CWE-284", "CWE-862", "CWE-863"]
  capec: ["CAPEC-17", "CAPEC-36"]
  owasp_llm: ["LLM07", "LLM08", "LLM10"]
  iso_42001: ["7.5.2", "8.2.2"]
  nist_ai_rmf: ["DEPLOY-3.1"]
```

## Automated Mapping Tools

### CWE/CAPEC Lookup Functions

```python
def get_cwe_mappings(vulnerability_type: str) -> List[str]:
    """Get relevant CWE IDs for a vulnerability type"""
    mappings = {
        "prompt_injection": ["CWE-1395", "CWE-20", "CWE-502"],
        "sql_injection": ["CWE-89", "CWE-20"],
        "xss": ["CWE-79", "CWE-20"],
        "access_control": ["CWE-284", "CWE-862"],
        "data_poisoning": ["CWE-502", "CWE-20"],
        "model_theft": ["CWE-200", "CWE-284"]
    }
    return mappings.get(vulnerability_type, [])

def get_capec_mappings(vulnerability_type: str) -> List[str]:
    """Get relevant CAPEC IDs for a vulnerability type"""
    mappings = {
        "prompt_injection": ["CAPEC-550", "CAPEC-137"],
        "sql_injection": ["CAPEC-66"],
        "xss": ["CAPEC-63"],
        "data_poisoning": ["CAPEC-183", "CAPEC-184"],
        "model_manipulation": ["CAPEC-165", "CAPEC-176"]
    }
    return mappings.get(vulnerability_type, [])
```

### Standards Validation

```python
def validate_standards_mapping(standards: Dict) -> List[str]:
    """Validate standards mappings for correctness"""
    errors = []

    # Validate CWE format
    for cwe in standards.get('cwe', []):
        if not cwe.startswith('CWE-'):
            errors.append(f"Invalid CWE format: {cwe}")

    # Validate CAPEC format
    for capec in standards.get('capec', []):
        if not capec.startswith('CAPEC-'):
            errors.append(f"Invalid CAPEC format: {capec}")

    # Validate OWASP LLM format
    for owasp in standards.get('owasp_llm', []):
        if not owasp.startswith('LLM') or len(owasp) != 4:
            errors.append(f"Invalid OWASP LLM format: {owasp}")

    return errors
```

## Rule Metadata Standards

### Complete Standards Block

```yaml
standards:
  # Core security frameworks
  cwe: ["CWE-79", "CWE-89", "CWE-20"]
  capec: ["CAPEC-63", "CAPEC-66"]

  # AI-specific frameworks
  owasp_llm: ["LLM01", "LLM02"]
  iso_42001: ["7.5.1", "8.2.1"]
  nist_ai_rmf: ["VALIDATE-2.3"]

  # Optional: Custom organization standards
  custom: ["ORG-SEC-001", "ORG-AI-005"]
```

### SARIF Output Integration

```yaml
sarif_output:
  rule_id: "tavoai-example-rule"
  rule_name: "Example Security Rule"
  properties:
    standards:
      cwe: ["CWE-79"]
      capec: ["CAPEC-63"]
      owasp_llm: ["LLM01"]
      iso_42001: ["7.5.1"]
```

## Maintenance and Updates

### Standards Evolution

1. **Monitor Updates**: Track new CWE/CAPEC releases
2. **Framework Alignment**: Update mappings for new AI security research
3. **Industry Adoption**: Include mappings to emerging AI security standards
4. **Tool Integration**: Ensure mappings work with security scanners and compliance tools

### Mapping Quality Assurance

```python
def audit_standards_coverage(rules_dir: Path) -> Dict:
    """Audit standards coverage across all rules"""
    coverage = {
        'cwe': set(),
        'capec': set(),
        'owasp_llm': set(),
        'iso_42001': set(),
        'nist_ai_rmf': set()
    }

    for rule_file in rules_dir.rglob("*.yaml"):
        try:
            with open(rule_file) as f:
                rule = yaml.safe_load(f)

            standards = rule.get('standards', {})
            for framework, ids in standards.items():
                if framework in coverage:
                    coverage[framework].update(ids)
        except Exception:
            continue

    return {k: sorted(list(v)) for k, v in coverage.items()}
```

## Resources

### Official Standards

- [CWE Official Site](https://cwe.mitre.org/)
- [CAPEC Official Site](https://capec.mitre.org/)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [ISO 42001](https://www.iso.org/standard/81230.html)
- [NIST AI RMF](https://www.nist.gov/itl/applied-cybersecurity/nice/resources/ai-risk-management-framework)

### Mapping Tools

- [CWE-CAPEC Mapping](https://capec.mitre.org/data/definitions/3000.html)
- [CWE Search](https://cwe.mitre.org/find.html)
- [CAPEC Browser](https://capec.mitre.org/browse/)

### Integration Examples

- [SARIF Standards Support](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html)
- [GitHub Security Tab](https://docs.github.com/en/code-security/security-advisories)
- [DefectDojo Integration](https://defectdojo.github.io/)
