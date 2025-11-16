# TavoAI Hybrid Rule Format Specification

## Overview

The TavoAI Hybrid Rule Format is a YAML-based specification for defining AI security rules that combine traditional heuristic pattern matching with AI-powered analysis. This format enables the creation of rules that are both fast (heuristic-only execution) and comprehensive (AI-augmented analysis).

## File Structure

All rules are defined in YAML files with the `.yaml` extension. The format supports three rule types:

- **opengrep/OPA**: Heuristic-only rules using Semgrep or OPA patterns
- **hybrid**: Rules combining heuristics with AI analysis
- **ai-only**: Pure AI analysis rules

## Schema Reference

### Core Properties

```yaml
# Required fields for all rules
version: "1.0"                                    # Rule format version
id: "tavoai-example-rule"                         # Unique rule identifier
name: "Example Security Rule"                     # Human-readable name
category: "security"                              # Primary category
subcategory: "injection"                           # Specific subcategory
severity: "high"                                  # Risk level: low/medium/high/critical
rule_type: "hybrid"                               # Execution type

# Optional fields
tags: ["example", "security", "ai"]              # Search tags
```

### Standards Mappings

```yaml
standards:
  # CWE identifiers
  cwe: ["CWE-79", "CWE-89"]

  # CAPEC identifiers
  capec: ["CAPEC-63", "CAPEC-66"]

  # OWASP LLM Top 10
  owasp_llm: ["LLM01"]

  # ISO 42001 sections
  iso_42001: ["7.2.1"]

  # NIST AI RMF functions
  nist_ai_rmf: ["GOVERN-1.3"]

  # MIT AI Risk categories
  mit_ai_risk: ["Malicious Use"]
```

### Compatible Models

```yaml
# For AI-enabled rules (hybrid, ai-only)
compatible_models:
  - "openai/gpt-4"
  - "google/gemini-pro"
  - "anthropic/claude-3-opus"
  - "tavoai/internal-llm"
```

## Rule Types

### 1. Opengrep Rules

Pure heuristic rules using Semgrep pattern matching.

```yaml
version: "1.0"
id: "tavoai-sql-injection-basic"
name: "SQL Injection Detection"
category: "security"
subcategory: "injection"
severity: "high"
rule_type: "opengrep"

standards:
  cwe: ["CWE-89"]
  capec: ["CAPEC-66"]

tags: ["sql", "injection", "database"]

heuristics:
  - type: "semgrep"
    languages: ["python", "javascript", "java"]
    pattern: |
      # Detect string concatenation in SQL queries
      $SQL = "SELECT * FROM users WHERE id = '" + $USER_INPUT + "'"
      ...
      $DB.execute($SQL)
    message: "Potential SQL injection: user input concatenated into SQL query"
    severity: "high"
```

### 2. OPA Rules

Pure heuristic rules using Open Policy Agent policies.

```yaml
version: "1.0"
id: "tavoai-access-control"
name: "Access Control Validation"
category: "security"
subcategory: "authorization"
severity: "medium"
rule_type: "opa"

standards:
  cwe: ["CWE-284"]

tags: ["access-control", "authorization"]

heuristics:
  - type: "opa"
    policy: |
      package access_control

      # Check for missing authorization checks
      deny[msg] {
        input.code contains "admin_function"
        not input.code contains "check_permissions"
        not input.code contains "is_authorized"
        msg := "Missing authorization check for admin function"
      }
```

### 3. Hybrid Rules

Rules combining heuristics with AI analysis for comprehensive coverage.

```yaml
version: "1.0"
id: "tavoai-prompt-injection-advanced"
name: "Advanced Prompt Injection Detection"
category: "security"
subcategory: "prompt-injection"
severity: "critical"
rule_type: "hybrid"

standards:
  cwe: ["CWE-1395"]
  owasp_llm: ["LLM01"]

compatible_models:
  - "openai/gpt-4"
  - "anthropic/claude-3-opus"

tags: ["prompt-injection", "llm", "ai-security"]

# Fast heuristic detection
heuristics:
  - type: "semgrep"
    languages: ["python", "javascript"]
    pattern: |
      # Basic pattern: user input in prompt
      $PROMPT = "... " + $USER_INPUT + " ..."
      $LLM.generate($PROMPT)
    message: "User input detected in LLM prompt - potential injection"
    severity: "high"

# AI-powered deep analysis
ai_analysis:
  trigger:
    - "heuristics_matched"      # Run AI when heuristics detect issues
    - "high_risk_files"          # Or for files matching patterns

  high_risk_patterns:           # File patterns triggering AI
    - "*/ai/*"
    - "*/llm/*"
    - "*/chatbot/*"

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

    1. **Direct User Input**: Is user input passed directly to LLM prompts?
    2. **Insufficient Sanitization**: Are sanitization methods robust?
    3. **Jailbreak Patterns**: Could input contain jailbreak attempts?
    4. **Output Validation**: Is LLM output validated before use?
    5. **Privilege Escalation**: Could injection escalate privileges?

    Provide analysis in the following format:
    - Severity: low/medium/high/critical
    - Vulnerable lines: [line numbers]
    - Description: detailed explanation
    - Remediation: specific code fixes
    - OWASP mapping: ["LLM01"]
    - Confidence: 0.0-1.0

  expected_response_schema:
    type: "object"
    required: ["severity", "vulnerable_lines", "description", "remediation", "owasp_mapping", "confidence"]
    properties:
      severity:
        type: "string"
        enum: ["low", "medium", "high", "critical"]
      vulnerable_lines:
        type: "array"
        items: { type: "number" }
      description:
        type: "string"
        minLength: 50
      remediation:
        type: "string"
        minLength: 50
      owasp_mapping:
        type: "array"
        items: { type: "string" }
      confidence:
        type: "number"
        minimum: 0
        maximum: 1

# Execution optimization
execution:
  max_tokens: 2000
  temperature: 0.1
  cache_results: true
  cache_duration: "7d"
  fallback_model: "openai/gpt-3.5-turbo"

# SARIF output configuration
sarif_output:
  rule_id: "tavoai-prompt-injection-advanced"
  rule_name: "Advanced Prompt Injection Detection"
  short_description: "Detects prompt injection vulnerabilities in LLM applications"
  full_description: "Comprehensive analysis of prompt injection risks including direct injection, jailbreak attempts, and privilege escalation"
  help_uri: "https://docs.tavoai.com/rules/prompt-injection"
  tags: ["security", "llm", "prompt-injection"]
```

### 4. AI-Only Rules

Pure AI analysis rules without heuristics (for complex contextual analysis).

```yaml
version: "1.0"
id: "tavoai-model-bias-detection"
name: "AI Model Bias Detection"
category: "ethics"
subcategory: "bias"
severity: "medium"
rule_type: "ai-only"

compatible_models:
  - "openai/gpt-4"
  - "anthropic/claude-3-opus"

ai_analysis:
  trigger:
    - "always"                  # Always run AI analysis for bias detection

  prompt_template: |
    You are an AI ethics expert analyzing machine learning models for bias.

    Model code and configuration:
    ```{language}
    {code_snippet}
    ```

    Analyze this machine learning model for potential biases. Consider:

    1. **Training Data**: Could the training data introduce bias?
    2. **Feature Selection**: Are features chosen in a biased way?
    3. **Model Architecture**: Could the architecture amplify biases?
    4. **Evaluation Metrics**: Are bias detection metrics included?
    5. **Fairness Constraints**: Are fairness constraints implemented?

    Provide detailed bias analysis.

  expected_response_schema:
    type: "object"
    required: ["bias_risks", "severity", "recommendations", "confidence"]
    properties:
      bias_risks: { type: "array", items: { type: "string" } }
      severity: { enum: ["low", "medium", "high", "critical"] }
      recommendations: { type: "array", items: { type: "string" } }
      confidence: { type: "number", minimum: 0, maximum: 1 }
```

## Execution Flow

### Heuristic-Only Execution (Fast, Free)

1. Load rule YAML
2. Execute heuristics (Semgrep/OPA)
3. Return findings immediately
4. No API key required

### Hybrid Execution (Balanced)

1. Load rule YAML
2. Execute heuristics first (fast pre-filter)
3. Check AI trigger conditions
4. If triggered, execute AI analysis
5. Merge heuristic + AI findings
6. API key required for AI portion

### AI-Only Execution (Comprehensive)

1. Load rule YAML
2. Execute AI analysis directly
3. API key always required
4. Maximum analysis depth

## Cost Optimization

The hybrid format enables intelligent cost optimization:

```yaml
execution:
  max_tokens: 2000          # Limit AI response length
  temperature: 0.1          # Low creativity for consistent results
  cache_results: true       # Cache AI responses
  cache_duration: "7d"      # Cache validity period
  fallback_model: "openai/gpt-3.5-turbo"  # Cheaper fallback
```

## Standards Compliance

### CWE/CAPEC Mapping

Rules must include relevant CWE and CAPEC identifiers:

```yaml
standards:
  cwe: ["CWE-79"]           # Cross-site Scripting
  capec: ["CAPEC-63"]       # Cross-Site Scripting
```

### OWASP LLM Top 10

AI-specific security mappings:

```yaml
standards:
  owasp_llm: ["LLM01"]      # Prompt Injection
```

### ISO 42001

AI management system compliance:

```yaml
standards:
  iso_42001: ["7.2.1"]      # AI system risk assessment
```

## Validation

Rules are validated against the JSON schema at `schemas/hybrid-rule-schema.json`:

```bash
# Validate all rules
python scripts/validate-rules.py --all

# Validate specific rule
python scripts/validate-rules.py path/to/rule.yaml
```

## Testing

Rules should be tested against sample code:

```bash
# Test all rules
python scripts/test-rules.py --all

# Test specific bundle
python scripts/test-rules.py --bundle owasp-llm-pro
```

## Best Practices

### Rule Design

1. **Start with Heuristics**: Design fast pattern-based detection first
2. **Add AI for Context**: Use AI to analyze complex scenarios heuristics can't catch
3. **Clear Triggers**: Define specific conditions for AI execution
4. **Cost-Effective**: Optimize token usage and caching
5. **Standards Mapping**: Include relevant CWE/CAPEC/OWASP mappings

### Performance

1. **Efficient Patterns**: Use specific, targeted Semgrep/OPA patterns
2. **Smart Triggers**: Only run AI when necessary
3. **Caching**: Leverage result caching for repeated scans
4. **Fallbacks**: Provide cheaper model fallbacks

### Maintenance

1. **Version Control**: Use semantic versioning for rules
2. **Regular Updates**: Update patterns based on new attack vectors
3. **Testing**: Maintain comprehensive test suites
4. **Documentation**: Keep detailed descriptions and remediation guidance

## Examples

See the `templates/` directory for complete rule examples:

- `heuristic-only-template.yaml` - Basic pattern matching rule
- `hybrid-rule-template.yaml` - Full hybrid rule with AI analysis
- `ai-only-template.yaml` - Pure AI analysis rule

## Migration from Legacy Formats

Existing rules can be migrated to the hybrid format:

```bash
# Convert legacy rule to hybrid format
python scripts/migrate-rule.py legacy-rule.json --output hybrid-rule.yaml
```

## Future Extensions

The format is designed to be extensible:

- **New Heuristic Types**: Additional pattern matching engines
- **Enhanced AI Features**: Multi-model analysis, confidence scoring
- **Custom Standards**: Organization-specific compliance frameworks
- **Plugin Architecture**: Third-party analysis integrations
