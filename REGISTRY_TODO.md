# TavoAI Rules - Official Rule Bundle Development

**Project**: TavoAI Rules (New Repository)  
**Initiative**: Universal Security Tool Registry  
**Status**: 📋 Planning Phase  
**Owner**: Security Research Team  

---

## Overview

This repository will contain all official TavoAI rule bundles for the Universal Security Tool Registry. This document outlines the development of production-ready rule bundles across multiple security frameworks and compliance standards.

**Repository Purpose**:
1. Official TavoAI rule bundles (OWASP, ISO, MIT AI Risk)
2. Community free bundle (for adoption)
3. Rule testing and validation
4. Documentation and examples
5. Version control and changelog management

**Reference**: See `../architecting/REGISTRY_PLAN.md` for complete architecture.

---

## Repository Structure

```
tavo-rules/
├── README.md
├── bundles/
│   ├── owasp-llm-top-10/
│   │   ├── manifest.json
│   │   ├── rules/
│   │   │   ├── llm01-prompt-injection.yaml
│   │   │   ├── llm02-insecure-output-handling.yaml
│   │   │   ├── llm03-training-data-poisoning.yaml
│   │   │   ├── llm04-model-denial-of-service.yaml
│   │   │   ├── llm05-supply-chain-vulnerabilities.yaml
│   │   │   ├── llm06-sensitive-information-disclosure.yaml
│   │   │   ├── llm07-insecure-plugin-design.yaml
│   │   │   ├── llm08-excessive-agency.yaml
│   │   │   ├── llm09-overreliance.yaml
│   │   │   └── llm10-model-theft.yaml
│   │   ├── README.md
│   │   ├── CHANGELOG.md
│   │   └── tests/
│   │       └── test_samples/
│   ├── iso-42001-compliance/
│   ├── mit-ai-risk-repository/
│   ├── prompt-injection-detection/
│   ├── bias-detection/
│   └── community-free/
├── templates/
│   ├── rule-template.yaml
│   └── bundle-manifest-template.json
├── docs/
│   ├── rule-development-guide.md
│   ├── testing-guide.md
│   └── bundle-packaging-guide.md
├── scripts/
│   ├── validate-rules.py
│   ├── test-rules.py
│   ├── package-bundle.py
│   └── publish-bundle.py
└── tests/
    ├── test_validation.py
    └── test_samples/
```

---

## Phase 1: OWASP LLM Top 10 Bundle (Week 11 - 1 week)

### Task 1.1: LLM01 - Prompt Injection
**File**: `bundles/owasp-llm-top-10/rules/llm01-prompt-injection.yaml`

Create comprehensive prompt injection detection rule:

```yaml
version: "1.0"
id: "tavoai-owasp-llm01-prompt-injection"
name: "OWASP LLM01: Prompt Injection Detection"
category: "security"
subcategory: "prompt-injection"
severity: "critical"
rule_type: "hybrid"
compatible_models:
  - "openai/gpt-4"
  - "google/gemini-pro"
  - "anthropic/claude-3-opus"
pricing_tier: "paid"
tags:
  - "owasp-llm-01"
  - "prompt-injection"
  - "llm-security"
  - "critical"

heuristics:
  - type: "semgrep"
    pattern: |
      # Detect unescaped user input in LLM prompts
      $USER_INPUT = ...
      ...
      $LLM.prompt($...,$USER_INPUT,$...)
    message: "Potential prompt injection: user input used directly in LLM prompt without sanitization"
  
  - type: "semgrep"
    pattern: |
      # Detect string concatenation with user input
      $PROMPT = $PREFIX + $USER_INPUT + $SUFFIX
      ...
      $LLM.prompt($PROMPT)
    message: "User input concatenated into prompt - potential prompt injection"
  
  - type: "opa"
    policy: |
      package prompt_injection
      
      # Check for missing input validation before LLM call
      deny[msg] {
        input.code contains "request."
        input.code contains ".prompt("
        not input.code contains "sanitize"
        not input.code contains "validate"
        msg := "Missing input validation before LLM prompt"
      }

ai_analysis:
  trigger:
    - "heuristics_matched"
    - "high_risk_files"
  
  prompt_template: |
    You are a security expert analyzing code for prompt injection vulnerabilities.
    
    Code to analyze:
    ```{language}
    {code_snippet}
    ```
    
    File: {file_path}
    Line: {line_number}
    
    Heuristic findings: {heuristic_findings}
    
    Analyze this code for prompt injection vulnerabilities. Check for:
    
    1. **Direct User Input**: Is user input passed directly to LLM prompts without validation?
    2. **Insufficient Sanitization**: Are sanitization methods robust against injection attacks?
    3. **Jailbreak Patterns**: Could input contain jailbreak or role manipulation attempts?
    4. **Output Validation**: Is LLM output validated before use in sensitive operations?
    5. **Privilege Escalation**: Could injected prompts escalate privileges or access?
    
    Provide your analysis in the following format:
    - Severity: low/medium/high/critical
    - Vulnerable lines: array of line numbers
    - Description: detailed explanation of the vulnerability
    - Remediation: specific code fixes and best practices
    - OWASP mapping: ["LLM01"]
    - Confidence: 0.0-1.0 (how confident you are in this finding)
  
  expected_response_schema:
    type: "object"
    required: ["severity", "vulnerable_lines", "description", "remediation", "owasp_mapping", "confidence"]
    properties:
      severity:
        type: "string"
        enum: ["low", "medium", "high", "critical"]
      vulnerable_lines:
        type: "array"
        items:
          type: "number"
      description:
        type: "string"
        minLength: 50
      remediation:
        type: "string"
        minLength: 50
      owasp_mapping:
        type: "array"
        items:
          type: "string"
      confidence:
        type: "number"
        minimum: 0
        maximum: 1

execution:
  max_tokens: 2000
  temperature: 0.1
  cache_results: true
  cache_duration: "7d"
  fallback_model: "openai/gpt-3.5-turbo"
```

**Testing**:
- Create test samples with vulnerable code
- Create test samples with safe code
- Validate against known prompt injection patterns

**Acceptance Criteria**:
- [ ] Rule detects common prompt injection patterns
- [ ] AI analysis provides accurate severity
- [ ] Remediation suggestions actionable
- [ ] False positive rate <10%

---

### Task 1.2-1.10: Complete OWASP LLM Top 10

Create rules for remaining OWASP categories:

**LLM02 - Insecure Output Handling**
- Detect unvalidated LLM outputs used in SQL, shell commands, HTML
- Check for output sanitization and escaping

**LLM03 - Training Data Poisoning**
- Detect untrusted data sources for training
- Check for data validation and verification

**LLM04 - Model Denial of Service**
- Detect unbounded loops or recursive calls to LLM
- Check for rate limiting and resource constraints

**LLM05 - Supply Chain Vulnerabilities**
- Detect usage of unverified model sources
- Check for model integrity verification

**LLM06 - Sensitive Information Disclosure**
- Detect logging of prompts/responses with PII
- Check for data masking and redaction

**LLM07 - Insecure Plugin Design**
- Detect plugin permissions without validation
- Check for plugin input/output validation

**LLM08 - Excessive Agency**
- Detect LLM with unrestricted function calling
- Check for human-in-the-loop controls

**LLM09 - Overreliance**
- Detect critical decisions without human verification
- Check for confidence thresholds

**LLM10 - Model Theft**
- Detect exposed model endpoints without auth
- Check for API key protection

**Dependencies**: Same as Task 1.1

**Acceptance Criteria**: Same as Task 1.1 for each rule

---

### Task 1.11: Bundle Packaging
**File**: `bundles/owasp-llm-top-10/manifest.json`

Create bundle manifest:

```json
{
  "id": "tavoai-owasp-llm-top-10",
  "name": "TavoAI OWASP LLM Top 10",
  "description": "Comprehensive security rules for the OWASP LLM Top 10 vulnerabilities. Includes hybrid heuristic + AI analysis for accurate detection with actionable remediation.",
  "version": "1.0.0",
  "artifact_type": "code_rule",
  "pricing_tier": "paid",
  "author": "TavoAI",
  "license": "Proprietary",
  "artifacts": [
    "rules/llm01-prompt-injection.yaml",
    "rules/llm02-insecure-output-handling.yaml",
    "rules/llm03-training-data-poisoning.yaml",
    "rules/llm04-model-denial-of-service.yaml",
    "rules/llm05-supply-chain-vulnerabilities.yaml",
    "rules/llm06-sensitive-information-disclosure.yaml",
    "rules/llm07-insecure-plugin-design.yaml",
    "rules/llm08-excessive-agency.yaml",
    "rules/llm09-overreliance.yaml",
    "rules/llm10-model-theft.yaml"
  ],
  "dependencies": [],
  "tags": [
    "owasp",
    "llm-top-10",
    "security",
    "comprehensive"
  ],
  "homepage": "https://tavoai.com/bundles/owasp-llm-top-10",
  "documentation": "https://docs.tavoai.com/bundles/owasp-llm-top-10"
}
```

**Testing**:
- Validate manifest against schema
- Ensure all artifact files exist
- Check pricing tier alignment

**Acceptance Criteria**:
- [ ] Manifest valid
- [ ] All rules included
- [ ] Metadata complete

---

## Phase 2: Additional Bundles (Week 11-12)

### Task 2.1: ISO 42001 Compliance Bundle (15 rules)

Create compliance-focused rules:

1. **AI Risk Management** - Detect missing risk assessments
2. **Data Governance** - Check for data lineage tracking
3. **Model Documentation** - Ensure model cards exist
4. **Testing & Validation** - Check for adequate testing
5. **Monitoring & Logging** - Ensure audit trails
6. **Bias Detection** - Check for fairness testing
7. **Explainability** - Ensure interpretability measures
8. **Privacy Protection** - Check for PII handling
9. **Security Controls** - Validate access controls
10. **Incident Response** - Check for error handling
11. **Third-Party Management** - Validate vendor checks
12. **Change Management** - Ensure version control
13. **Performance Monitoring** - Check for drift detection
14. **Stakeholder Communication** - Validate transparency
15. **Continuous Improvement** - Check for feedback loops

**File Structure**: Similar to OWASP bundle

**Acceptance Criteria**: Same quality standards as OWASP bundle

---

### Task 2.2: MIT AI Risk Repository Bundle (20 rules)

Map rules to MIT AI Risk taxonomy:

1. **Distributional Risks** - Societal distribution of harms
2. **Malicious Use** - Intentional misuse detection
3. **Human-Computer Interaction** - Interface safety
4. **Sociotechnical Risks** - Social impact assessment
5-20. Additional risk categories from MIT taxonomy

**Reference**: https://airisk.mit.edu/

**Acceptance Criteria**: Rules cover major risk categories

---

### Task 2.3: Prompt Injection Detection Bundle (8 rules)

Specialized prompt injection rules:

1. **Direct Injection** - Basic user input injection
2. **Indirect Injection** - Third-party content injection
3. **Jailbreak Attempts** - Role manipulation detection
4. **System Prompt Leakage** - Prompt extraction attempts
5. **Delimiter Attacks** - Delimiter bypass detection
6. **Context Manipulation** - Context window attacks
7. **Output Manipulation** - Response manipulation
8. **Privilege Escalation** - Permission bypass

---

### Task 2.4: Bias Detection Bundle (6 rules)

Fairness and bias detection rules:

1. **Protected Attributes** - Direct use of sensitive attributes
2. **Proxy Discrimination** - Indirect bias via correlated features
3. **Training Data Bias** - Biased dataset detection
4. **Model Outputs** - Biased prediction patterns
5. **Disparate Impact** - Statistical bias measurement
6. **Fairness Metrics** - Missing fairness checks

---

### Task 2.5: Community Free Bundle (5 rules)

Basic rules for adoption:

1. **Basic Prompt Injection** - Simple heuristic-only
2. **API Key Exposure** - Hardcoded API keys
3. **Basic Bias Check** - Direct protected attribute use
4. **Output Validation** - Missing output checks
5. **Rate Limiting** - Missing rate limits

**Pricing**: Free (community)

---

## Testing Infrastructure

### Task 3.1: Rule Validation Script
**File**: `scripts/validate-rules.py`

Create automated validation:

```python
#!/usr/bin/env python3
import yaml
import jsonschema
import sys
from pathlib import Path

def validate_rule(rule_path: Path) -> bool:
    """Validate rule YAML against schema"""
    with open('schemas/rule-schema.json') as f:
        schema = json.load(f)
    
    with open(rule_path) as f:
        rule = yaml.safe_load(f)
    
    try:
        jsonschema.validate(rule, schema)
        print(f"✓ {rule_path.name} is valid")
        return True
    except jsonschema.ValidationError as e:
        print(f"✗ {rule_path.name} is invalid: {e.message}")
        return False

def main():
    bundles_dir = Path('bundles')
    all_valid = True
    
    for rule_file in bundles_dir.rglob('*.yaml'):
        if not validate_rule(rule_file):
            all_valid = False
    
    sys.exit(0 if all_valid else 1)

if __name__ == '__main__':
    main()
```

**Testing**:
- Test with valid rules
- Test with invalid rules
- Test error reporting

**Acceptance Criteria**:
- [ ] Validates all rules
- [ ] Clear error messages
- [ ] Returns proper exit codes

---

### Task 3.2: Rule Testing Script
**File**: `scripts/test-rules.py`

Test rules against sample code:

```python
#!/usr/bin/env python3
from tavoai import RegistryClient
from pathlib import Path

def test_rule(rule_path: Path, test_samples_dir: Path) -> bool:
    """Test rule against sample code"""
    client = RegistryClient(api_key=os.getenv('TAVOAI_API_KEY'))
    
    # Load rule
    with open(rule_path) as f:
        rule_yaml = f.read()
    
    # Test against vulnerable samples
    vulnerable_dir = test_samples_dir / 'vulnerable'
    for sample in vulnerable_dir.glob('*.py'):
        result = client.execute_code_rule(
            rule_yaml=rule_yaml,
            code=sample.read_text(),
            language='python'
        )
        
        if not result.heuristics.findings:
            print(f"✗ {rule_path.name} missed vulnerability in {sample.name}")
            return False
    
    # Test against safe samples
    safe_dir = test_samples_dir / 'safe'
    for sample in safe_dir.glob('*.py'):
        result = client.execute_code_rule(
            rule_yaml=rule_yaml,
            code=sample.read_text(),
            language='python'
        )
        
        if result.heuristics.findings:
            print(f"✗ {rule_path.name} false positive on {sample.name}")
            return False
    
    print(f"✓ {rule_path.name} passed all tests")
    return True
```

**Testing**:
- Test with known vulnerable code
- Test with known safe code
- Measure false positive/negative rates

**Acceptance Criteria**:
- [ ] Tests all rules
- [ ] Detects regressions
- [ ] Reports metrics

---

### Task 3.3: Bundle Packaging Script
**File**: `scripts/package-bundle.py`

Package bundles as .tavoai-bundle files:

```python
#!/usr/bin/env python3
import zipfile
import json
from pathlib import Path

def package_bundle(bundle_dir: Path, output_dir: Path):
    """Package bundle as .tavoai-bundle ZIP file"""
    manifest_path = bundle_dir / 'manifest.json'
    
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    bundle_id = manifest['id']
    version = manifest['version']
    output_file = output_dir / f"{bundle_id}-{version}.tavoai-bundle"
    
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add manifest
        zf.write(manifest_path, 'manifest.json')
        
        # Add all artifacts
        for artifact in manifest['artifacts']:
            artifact_path = bundle_dir / artifact
            zf.write(artifact_path, f"artifacts/{artifact}")
        
        # Add README and LICENSE
        if (bundle_dir / 'README.md').exists():
            zf.write(bundle_dir / 'README.md', 'README.md')
        if (bundle_dir / 'LICENSE').exists():
            zf.write(bundle_dir / 'LICENSE', 'LICENSE')
        if (bundle_dir / 'CHANGELOG.md').exists():
            zf.write(bundle_dir / 'CHANGELOG.md', 'CHANGELOG.md')
    
    print(f"✓ Packaged {bundle_id} v{version} to {output_file}")
```

**Acceptance Criteria**:
- [ ] Creates valid ZIP files
- [ ] Includes all artifacts
- [ ] Follows bundle format spec

---

## Documentation

### Task 4.1: Rule Development Guide
**File**: `docs/rule-development-guide.md`

Comprehensive guide for creating rules:

- Rule structure and YAML syntax
- Heuristic pattern writing (Semgrep, OPA)
- AI prompt engineering best practices
- Testing and validation procedures
- Packaging and publishing workflow

---

### Task 4.2: Each Bundle README
**File**: `bundles/{bundle-name}/README.md`

Per-bundle documentation:

- Bundle overview and purpose
- List of included rules
- Usage examples
- Installation instructions
- Version history

---

## Success Criteria

### Quality
- [ ] All 59 rules created and validated
- [ ] False positive rate <10%
- [ ] False negative rate <5%
- [ ] AI analysis accuracy >90%

### Testing
- [ ] All rules tested against samples
- [ ] Vulnerable code detected
- [ ] Safe code passes
- [ ] No regressions in updates

### Documentation
- [ ] Each bundle has README
- [ ] CHANGELOG maintained
- [ ] Development guide complete
- [ ] Examples provided

### Packaging
- [ ] All bundles packaged correctly
- [ ] Manifests valid
- [ ] Published to registry
- [ ] Versioning consistent

---

## Notes

- Security research required for accurate rules
- Regular updates as new vulnerabilities discovered
- Community feedback integration
- Coordinate with API server for rule execution testing
- Maintain high quality standards (TavoAI brand)

---

**Last Updated**: October 25, 2025  
**Next Review**: After Phase 1 completion (Week 11)

