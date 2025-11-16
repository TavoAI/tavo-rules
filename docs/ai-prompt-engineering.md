# AI Prompt Engineering for TavoAI Rules

## Overview

This guide covers best practices for crafting effective AI prompts in TavoAI hybrid rules. Well-designed prompts are crucial for accurate security analysis, cost optimization, and consistent results.

## Core Principles

### 1. Security Context

Always establish the AI's role as a security expert:

```yaml
prompt_template: |
  You are a senior cybersecurity engineer with 15+ years of experience
  specializing in AI and LLM security. You have deep expertise in:

  - OWASP LLM Top 10 vulnerabilities
  - CWE/CAPEC attack patterns
  - ISO 42001 AI governance requirements
  - Modern secure coding practices
  - AI system security architecture

  Your analysis must be thorough, accurate, and focused on practical security implications.
```

### 2. Structured Analysis Framework

Use structured prompts that guide the AI through systematic analysis:

```yaml
prompt_template: |
  Analyze this code for [SPECIFIC_VULNERABILITY] vulnerabilities:

  ## Code to Analyze
  ```{language}
  {code_snippet}
  ```

  ## Context
  - File: {file_path}
  - Line: {line_number}
  - Heuristic findings: {heuristic_findings}

  ## Required Analysis Steps

  1. **Threat Modeling**: Identify potential attack vectors
  2. **Vulnerability Assessment**: Evaluate exploitability and impact
  3. **Code Review**: Examine implementation details
  4. **Remediation Planning**: Suggest specific fixes
  5. **Standards Mapping**: Link to relevant security frameworks

  ## Analysis Requirements

  For each potential vulnerability, provide:
  - Specific code locations (line numbers)
  - Technical description of the issue
  - Exploitability assessment (high/medium/low)
  - Potential impact (confidentiality/integrity/availability)
  - Remediation steps with code examples
  - Relevant CWE/CAPEC/OWASP mappings
  - Confidence score (0.0-1.0)
```

### 3. Cost Optimization

Design prompts to minimize token usage while maximizing accuracy:

```yaml
# ❌ Inefficient (too verbose)
prompt_template: "Please analyze this code very carefully and thoroughly..."

# ✅ Efficient (focused and specific)
prompt_template: |
  Analyze for prompt injection vulnerabilities:

  Code: {code_snippet}

  Check:
  1. Direct user input in prompts
  2. Missing sanitization
  3. Jailbreak patterns

  Format: severity|lines|description|fix|cwe|confidence
```

## Prompt Patterns by Rule Type

### 1. Vulnerability Detection

For detecting specific security issues:

```yaml
prompt_template: |
  SECURITY AUDIT: {VULNERABILITY_TYPE}

  Code Analysis Request:
  ```{language}
  {code_snippet}
  ```

  Security Check:
  - Does this code contain {VULNERABILITY_TYPE}?
  - What is the exploitability level?
  - What remediation is required?

  Response Format:
  - Detection: YES/NO
  - Severity: LOW/MEDIUM/HIGH/CRITICAL
  - Evidence: specific code patterns
  - Remediation: actionable steps
  - Confidence: 0.0-1.0
```

### 2. Code Quality Assessment

For evaluating implementation quality:

```yaml
prompt_template: |
  CODE SECURITY REVIEW

  Implementation:
  ```{language}
  {code_snippet}
  ```

  Evaluate against {FRAMEWORK} requirements:

  1. **Compliance**: Does this meet {FRAMEWORK} standards?
  2. **Security**: Are security best practices followed?
  3. **Risk**: What are the residual security risks?

  Provide specific findings with:
  - Non-compliant elements
  - Security gaps
  - Improvement recommendations
  - Standards references
```

### 3. Risk Assessment

For evaluating overall security posture:

```yaml
prompt_template: |
  SECURITY RISK ASSESSMENT

  System Component:
  ```{language}
  {code_snippet}
  ```

  Risk Analysis Framework:

  **Threat Identification:**
  - What could go wrong?
  - Who could exploit this?
  - How could it be exploited?

  **Impact Assessment:**
  - Confidentiality impact
  - Integrity impact
  - Availability impact

  **Likelihood Evaluation:**
  - Attack vector complexity
  - Required attacker skill level
  - Current mitigation effectiveness

  **Risk Scoring:**
  - Overall risk level
  - Recommended priority
  - Mitigation strategies
```

## Response Schema Design

### Structured Output

Always specify exact response format to ensure consistency:

```yaml
expected_response_schema:
  type: "object"
  required: ["severity", "vulnerable_lines", "description", "remediation", "standards_mapping", "confidence"]
  properties:
    severity:
      type: "string"
      enum: ["low", "medium", "high", "critical"]
      description: "Risk severity level"
    vulnerable_lines:
      type: "array"
      items:
        type: "number"
        minimum: 1
      description: "Line numbers containing vulnerabilities"
    description:
      type: "string"
      minLength: 50
      maxLength: 1000
      description: "Detailed vulnerability description"
    remediation:
      type: "string"
      minLength: 50
      maxLength: 1000
      description: "Specific remediation steps"
    standards_mapping:
      type: "object"
      properties:
        cwe:
          type: "array"
          items: { type: "string" }
        capec:
          type: "array"
          items: { type: "string" }
        owasp_llm:
          type: "array"
          items: { type: "string" }
    confidence:
      type: "number"
      minimum: 0
      maximum: 1
      description: "Analysis confidence score"
```

### Error Handling

Include error handling in prompts:

```yaml
prompt_template: |
  Analyze the following code. If you cannot provide a confident analysis,
  respond with confidence score below 0.3 and explain your uncertainty.

  If the code is safe, explicitly state this with high confidence.
  If you're unsure about any aspect, clearly indicate this in your response.
```

## Model-Specific Optimization

### GPT-4 Optimization

```yaml
execution:
  max_tokens: 2000
  temperature: 0.1    # Low for consistency
  model: "openai/gpt-4"

prompt_template: |
  You are an expert security analyst. Be precise and thorough.

  Analyze this code systematically:

  1. Identify security issues
  2. Assess severity and impact
  3. Provide specific remediation
  4. Map to security standards

  Use evidence from the code to support your conclusions.
```

### Claude Optimization

```yaml
execution:
  max_tokens: 2000
  temperature: 0.1
  model: "anthropic/claude-3-opus"

prompt_template: |
  As a senior security engineer, conduct a methodical security analysis:

  First, understand the code's purpose and context.
  Then, systematically evaluate security implications.
  Finally, provide actionable recommendations.

  Be comprehensive but concise. Use specific examples from the code.
```

### Gemini Optimization

```yaml
execution:
  max_tokens: 2000
  temperature: 0.1
  model: "google/gemini-pro"

prompt_template: |
  Perform a security code review of this implementation:

  SECURITY ANALYSIS FRAMEWORK:

  🔍 **Code Understanding**: What does this code do?
  🛡️ **Security Assessment**: What security issues exist?
  📊 **Risk Evaluation**: How severe are these issues?
  🔧 **Remediation Planning**: How should they be fixed?

  Provide specific, actionable findings with code examples.
```

## Context Integration

### Heuristic Context

Use heuristic findings to guide AI analysis:

```yaml
prompt_template: |
  Heuristic analysis found: {heuristic_findings}

  Based on these initial findings, perform deeper analysis:

  1. Confirm the heuristic detections are true positives
  2. Identify additional issues the heuristics might have missed
  3. Assess the overall security posture
  4. Provide comprehensive remediation guidance
```

### File Context

Include file and project context:

```yaml
prompt_template: |
  File: {file_path}
  Language: {language}
  Project context: This appears to be {project_type}

  Analyze this {language} code for security vulnerabilities:

  Consider {language}-specific security patterns and best practices.
  Evaluate the code's role within the broader application architecture.
```

## Cost Management Strategies

### 1. Token Optimization

```yaml
# Minimize prompt length
prompt_template: |
  SECURITY CHECK: {vulnerability_type}

  Code: {code_snippet}

  Issues? Severity? Remediation? Confidence?
```

### 2. Caching Strategy

```yaml
execution:
  cache_results: true
  cache_duration: "7d"  # Cache for 7 days
  cache_key: "rule_{rule_id}_file_{file_hash}_lines_{line_range}"
```

### 3. Fallback Models

```yaml
execution:
  fallback_model: "openai/gpt-3.5-turbo"  # Cheaper fallback
  fallback_trigger: "cost_exceeded"       # Use when expensive model too costly
```

## Testing and Validation

### Prompt Testing

```python
# Test prompts with known good/bad examples
test_cases = [
    {
        "code": "safe_code_example",
        "expected": {"severity": "low", "confidence": 0.9}
    },
    {
        "code": "vulnerable_code_example",
        "expected": {"severity": "high", "confidence": 0.95}
    }
]

for test_case in test_cases:
    result = test_prompt(prompt_template, test_case["code"])
    assert result["confidence"] > test_case["expected"]["confidence"]
```

### Accuracy Metrics

Track AI prompt performance:

```yaml
quality_metrics:
  accuracy: 0.95        # Correct analysis percentage
  precision: 0.92       # True positive rate
  recall: 0.89          # Vulnerability detection rate
  consistency: 0.96     # Same input produces same output
```

## Common Pitfalls

### 1. Overly Vague Prompts

```yaml
# ❌ Bad
"Check this code for security issues"

# ✅ Good
"Analyze for SQL injection, XSS, and authentication bypass vulnerabilities"
```

### 2. Missing Context

```yaml
# ❌ Bad
"Analyze this code"

# ✅ Good
"Analyze this Python Flask application code for OWASP Top 10 vulnerabilities"
```

### 3. No Output Structure

```yaml
# ❌ Bad
"Tell me about security issues"

# ✅ Good
"List security issues with: severity, location, description, remediation"
```

### 4. Temperature Too High

```yaml
# ❌ Bad
temperature: 0.8  # Creative but inconsistent

# ✅ Good
temperature: 0.1  # Focused and consistent
```

## Advanced Techniques

### 1. Chain-of-Thought Prompting

```yaml
prompt_template: |
  Think step-by-step about this security analysis:

  1. What is this code trying to accomplish?
  2. What security mechanisms are in place?
  3. What could potentially go wrong?
  4. How could an attacker exploit this?
  5. What specific changes would improve security?

  Now provide your final analysis with specific findings.
```

### 2. Few-Shot Learning

```yaml
prompt_template: |
  Examples of secure vs vulnerable patterns:

  SECURE: input.replace("'", "''")  # SQL escaping
  VULNERABLE: f"SELECT * FROM users WHERE id = {user_input}"

  SECURE: jwt.decode(token, verify=True)
  VULNERABLE: jwt.decode(token, options={"verify_signature": False})

  Now analyze this code:
  {code_snippet}

  Is this secure or vulnerable? Why?
```

### 3. Uncertainty Quantification

```yaml
prompt_template: |
  Provide your analysis with confidence intervals:

  For each finding:
  - Confidence score (0.0-1.0)
  - Uncertainty factors
  - Alternative interpretations
  - Additional evidence needed

  If confidence < 0.7, recommend manual review.
```

## Maintenance and Evolution

### Regular Prompt Updates

1. **Monitor Performance**: Track accuracy metrics over time
2. **User Feedback**: Incorporate user-reported issues
3. **New Threats**: Update for emerging vulnerability patterns
4. **Model Changes**: Adapt prompts for new model capabilities

### A/B Testing

```yaml
# Test different prompt versions
prompt_versions:
  v1: "Basic analysis prompt"
  v2: "Enhanced with examples"
  v3: "Structured output format"

# Compare accuracy and user satisfaction
```

### Continuous Improvement

```yaml
improvement_cycle:
  1. Collect performance metrics
  2. Identify problem patterns
  3. Develop improved prompts
  4. A/B test improvements
  5. Roll out successful changes
  6. Monitor ongoing performance
```

## Resources

### Prompt Engineering Tools
- OpenAI Playground: Test prompts interactively
- Anthropic Console: Claude prompt development
- Google AI Studio: Gemini prompt testing

### Best Practice Guides
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Google AI Prompting Strategies](https://ai.google.dev/docs/prompt_best_practices)

### Testing Frameworks
- [Promptfoo](https://github.com/promptfoo/promptfoo): Automated prompt testing
- [OpenPrompt](https://github.com/thunlp/OpenPrompt): Prompt learning toolkit

### Example Prompts
- `templates/prompt-examples/` - Curated prompt examples
- `docs/prompt-patterns.md` - Common prompt patterns
- Rule-specific prompts in `bundles/*/rules/`
