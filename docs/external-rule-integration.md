# External Rule Integration

This document explains how TavoAI integrates with external rule repositories while respecting licensing constraints.

## Overview

TavoAI supports running rules from external sources to provide comprehensive security coverage. However, we respect licensing terms and do not redistribute or modify rules from external repositories.

## Supported External Rule Sources

### Semgrep Rules
- **Repository**: https://github.com/semgrep/semgrep-rules
- **License**: MIT (but redistribution restrictions apply)
- **Integration**: Direct reference from GitHub
- **Usage**: Customers can run semgrep rules directly from the source repository

### Open Policy Agent (OPA) Policies
- **Repository**: https://github.com/open-policy-agent/library
- **License**: Apache 2.0
- **Integration**: Direct reference from GitHub
- **Usage**: Rego policies can be executed via OPA integration

### YARA Rules
- **Repository**: https://github.com/Yara-Rules/rules
- **License**: Various (GPL, BSD, etc.)
- **Integration**: Direct reference from GitHub
- **Usage**: YARA patterns for malware detection

### Sigma Rules
- **Repository**: https://github.com/SigmaHQ/sigma
- **License**: MIT
- **Integration**: Direct reference from GitHub
- **Usage**: SIEM rule patterns for log analysis

## Integration Architecture

### Direct GitHub Access

TavoAI SDK supports running rules directly from external GitHub repositories:

```typescript
// Example: Running semgrep rules directly from GitHub
const scanner = new TavoAIScanner();

await scanner.scan({
  target: './my-code',
  rules: [
    {
      source: 'github',
      repo: 'semgrep/semgrep-rules',
      path: 'python/lang/security',
      type: 'semgrep'
    }
  ]
});
```

### Hybrid Approach

For enhanced analysis, combine external rules with TavoAI's AI-powered analysis:

```typescript
await scanner.scan({
  target: './my-code',
  rules: [
    // External semgrep rule
    {
      source: 'github',
      repo: 'semgrep/semgrep-rules',
      path: 'python/lang/security/injection.yaml',
      type: 'semgrep'
    },
    // TavoAI enhanced analysis
    {
      source: 'tavoai',
      bundle: 'ai-enhanced/owasp-llm-pro',
      rules: ['llm01-prompt-injection']
    }
  ],
  ai: {
    enabled: true,
    model: 'openai/gpt-4',
    enhanceExternalRules: true  // Apply AI analysis to external rule findings
  }
});
```

## Licensing Compliance

### Redistribution Restrictions

We **cannot**:
- Bundle external rules in our registry
- Modify external rules
- Distribute external rules under our license
- Create derivative works of external rules
- Include external rules in our git repositories

### Allowed Activities

We **can**:
- Reference external rules by URL/path
- Help customers access external rules
- Run external rules on customer code
- Provide our own complementary rules
- Enhance external rule findings with our AI analysis
- Support external rule formats in our tooling

### Specific Cases

#### Semgrep Rules
- **License**: Semgrep Rules License v1.0
- **Approach**: Direct GitHub access only
- **Implementation**: Customers specify `github:semgrep/semgrep-rules` in scan commands

#### OPA Policies
- **License**: Apache 2.0 (more permissive)
- **Approach**: Direct GitHub access
- **Implementation**: Rego policy evaluation via OPA integration

#### YARA Rules
- **License**: Various (GPL, BSD, etc.)
- **Approach**: Direct GitHub access
- **Implementation**: YARA pattern compilation and execution

#### Sigma Rules
- **License**: MIT (permissive)
- **Approach**: Direct GitHub access
- **Implementation**: SIEM rule processing and alerting

## Implementation Details

### SDK Integration

The TavoAI SDK includes methods for external rule execution:

```typescript
class ExternalRuleRunner {
  async loadFromGitHub(repo: string, path: string, type: RuleType): Promise<Rule[]>
  async executeExternalRules(rules: Rule[], target: string): Promise<Finding[]>
  async enhanceWithAI(findings: Finding[]): Promise<EnhancedFinding[]>
}
```

### CLI Support

Command-line interface supports external rule sources:

```bash
# Run semgrep rules directly
tavoai scan --rules github:semgrep/semgrep-rules/python/lang/security --target ./code

# Mix external and TavoAI rules
tavoai scan \
  --rules github:semgrep/semgrep-rules/python \
  --rules tavoai:ai-enhanced/owasp-llm-pro \
  --target ./code \
  --ai-enhance
```

### API Endpoints

REST API supports external rule sources:

```http
POST /api/v1/scan
Content-Type: application/json

{
  "target": "./code",
  "rules": [
    {
      "source": "github",
      "repo": "semgrep/semgrep-rules",
      "path": "python/lang/security",
      "type": "semgrep"
    }
  ],
  "ai": {
    "enhance": true
  }
}
```

## Customer Benefits

### Comprehensive Coverage

Customers get access to:
- **Semgrep's extensive rule library** (1000+ rules)
- **Industry-standard security patterns**
- **Specialized domain rules** (cloud, containers, etc.)
- **TavoAI's AI-enhanced analysis** of all findings

### Easy Integration

No need to maintain separate toolchains:

```bash
# Single command for comprehensive scanning
tavoai scan --rules github:semgrep/semgrep-rules --rules tavoai:all --target ./code
```

### Enhanced Analysis

External rules + AI enhancement = deeper insights:

```json
{
  "finding": {
    "rule": "semgrep:python.lang.security.injection.sql-injection",
    "severity": "high",
    "location": "app.py:42"
  },
  "ai_enhancement": {
    "confidence": 0.95,
    "context": "This appears to be a prepared statement vulnerability...",
    "remediation": "Use parameterized queries with proper escaping...",
    "standards": ["OWASP A01:2021", "CWE-89"]
  }
}
```

## Setup and Configuration

### Environment Variables

```bash
# GitHub API token (optional, for higher rate limits)
export GITHUB_TOKEN=your_token_here

# TavoAI API key (for AI enhancement)
export TAVOAI_API_KEY=your_key_here
```

### Configuration File

```yaml
# tavoai-config.yaml
external_rules:
  semgrep:
    enabled: true
    cache_dir: ~/.cache/tavoai/semgrep
  opa:
    enabled: true
    cache_dir: ~/.cache/tavoai/opa

ai_enhancement:
  enabled: true
  model: openai/gpt-4
  enhance_external: true
```

## Performance Considerations

### Caching

External rules are cached locally to improve performance:

```bash
# Clear cache
tavoai cache clear

# Show cache stats
tavoai cache stats
```

### Rate Limiting

Respect external API limits:
- GitHub: 5000 requests/hour (authenticated), 60/hour (unauthenticated)
- Automatic retry with exponential backoff

### Parallel Execution

Rules run in parallel for better performance:

```yaml
execution:
  parallel: true
  workers: 4
  timeout: 300
```

## Troubleshooting

### Common Issues

1. **Rate Limiting**:
   ```bash
   # Use GitHub token for higher limits
   export GITHUB_TOKEN=your_token
   ```

2. **Network Issues**:
   ```bash
   # Use proxy if needed
   export HTTPS_PROXY=http://proxy.company.com:8080
   ```

3. **Cache Issues**:
   ```bash
   # Clear and rebuild cache
   tavoai cache clear && tavoai cache build
   ```

### Debug Mode

Enable detailed logging:

```bash
tavoai scan --debug --rules github:semgrep/semgrep-rules/python --target ./code
```

## Future Enhancements

### Planned Features

1. **Rule Marketplace**: Browse and discover external rules
2. **Rule Compatibility**: Automatic format conversion
3. **Rule Analytics**: Usage statistics and effectiveness metrics
4. **Custom Rule Hosting**: Allow customers to share their rules
5. **Offline Mode**: Download and cache rules for air-gapped environments

## References

- [Semgrep Rules Documentation](https://semgrep.dev/docs/writing-rules/overview/)
- [Open Policy Agent](https://www.openpolicyagent.org/)
- [YARA Documentation](https://yara.readthedocs.io/)
- [Sigma Rules](https://github.com/SigmaHQ/sigma/wiki)
- [TavoAI Rule Format](./hybrid-format-spec.md)
