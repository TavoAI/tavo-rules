# TavoAI Rules API Integration Guide

This guide provides comprehensive instructions for integrating TavoAI security rules into your applications, CI/CD pipelines, and development workflows.

## Table of Contents

- [Quick Start](#quick-start)
- [SDK Installation](#sdk-installation)
- [Bundle Management](#bundle-management)
- [Scanning APIs](#scanning-apis)
- [CI/CD Integration](#ci-cd-integration)
- [Programmatic Usage](#programmatic-usage)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)

## Quick Start

### 1. Install TavoAI SDK

```bash
npm install @tavoai/sdk
# OR
pip install tavoai-sdk
# OR
go get github.com/tavoai/sdk-go
```

### 2. Basic Scanning

```bash
# Free bundle (no API key needed)
tavoai scan --bundle owasp-llm-basic --path ./src

# Paid bundle (API key required)
export TAVOAI_API_KEY=your_key_here
tavoai scan --bundle owasp-llm-pro --path ./src
```

### 3. Get Results

```bash
# JSON output (default)
tavoai scan --bundle owasp-llm-basic --path ./src --output results.json

# SARIF for GitHub Security tab
tavoai scan --bundle owasp-llm-basic --path ./src --format sarif --output results.sarif
```

## SDK Installation

### Node.js/TypeScript

```bash
npm install @tavoai/sdk
```

```typescript
import { TavoAIScanner } from '@tavoai/sdk';

const scanner = new TavoAIScanner({
  apiKey: process.env.TAVOAI_API_KEY // Optional for free bundles
});
```

### Python

```bash
pip install tavoai-sdk
```

```python
from tavoai import TavoAIScanner

scanner = TavoAIScanner(api_key=os.getenv('TAVOAI_API_KEY'))
```

### Go

```bash
go get github.com/tavoai/sdk-go
```

```go
import "github.com/tavoai/sdk-go"

scanner := tavoai.NewScanner(tavoai.Config{
    APIKey: os.Getenv("TAVOAI_API_KEY"),
})
```

### Docker

```bash
docker run -v $(pwd):/src tavoai/scanner:latest \
  --bundle owasp-llm-basic \
  --path /src
```

## Bundle Management

### Available Bundles

| Bundle | Pricing | Description | API Key Required |
|--------|---------|-------------|------------------|
| `owasp-llm-basic` | Free | OWASP LLM Top 10 heuristics | No |
| `owasp-llm-pro` | Paid | AI-enhanced OWASP LLM analysis | Yes |
| `iso-42001-compliance` | Paid | ISO 42001 governance compliance | Yes |
| `mit-ai-risk-repo` | Paid | MIT AI Risk Repository rules | Yes |
| `ai-ethics` | Paid | AI Ethics and fairness rules | Yes |
| `bias-detection` | Paid | Bias detection and mitigation | Yes |

### Bundle Discovery

```bash
# List all available bundles
tavoai bundles list

# Search bundles
tavoai bundles search "owasp"

# Get bundle details
tavoai bundles info owasp-llm-pro
```

### Bundle Installation

```bash
# Download bundle locally
tavoai bundles install owasp-llm-basic

# Update bundles
tavoai bundles update

# List installed bundles
tavoai bundles installed
```

## Scanning APIs

### Basic Scanning

```typescript
const results = await scanner.scan({
  path: './src',
  bundle: 'owasp-llm-basic',
  format: 'json'
});
```

```python
results = scanner.scan(
    path='./src',
    bundle='owasp-llm-basic',
    format='json'
)
```

### Advanced Scanning Options

```typescript
const results = await scanner.scan({
  path: './src',
  bundle: 'owasp-llm-pro',
  options: {
    mode: 'hybrid',           // 'local', 'remote', 'hybrid'
    severity: 'high',         // 'info', 'low', 'medium', 'high', 'critical'
    includePaths: ['**/*.py', '**/*.js'],
    excludePaths: ['node_modules/**', 'test/**'],
    maxFileSize: '10MB',
    timeout: 300000,          // 5 minutes
    threads: 4
  }
});
```

### Streaming Results

```typescript
const stream = scanner.scanStream({
  path: './large-codebase',
  bundle: 'owasp-llm-basic'
});

for await (const result of stream) {
  console.log(`Found ${result.findings.length} issues in ${result.file}`);
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run OWASP LLM Basic Scan
        uses: tavoai/scan-action@v1
        with:
          bundle: owasp-llm-basic
          path: ./src
          format: sarif
          output: owasp-results.sarif

      - name: Run AI-Enhanced Scan
        uses: tavoai/scan-action@v1
        with:
          bundle: owasp-llm-pro
          api-key: ${{ secrets.TAVOAI_API_KEY }}
          path: ./src
          format: sarif
          output: ai-results.sarif

      - name: Upload OWASP Results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: owasp-results.sarif
          category: owasp-basic

      - name: Upload AI Results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: ai-results.sarif
          category: ai-enhanced
```

### GitLab CI

```yaml
stages:
  - security

security_scan:
  stage: security
  image: tavoai/scanner:latest
  script:
    - tavoai scan --bundle owasp-llm-basic --path . --output results.json
    - tavoai scan --bundle owasp-llm-pro --path . --api-key $TAVOAI_API_KEY --output ai-results.json
  artifacts:
    reports:
      sast: results.json
    paths:
      - ai-results.json
  only:
    - merge_requests
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any

    stages {
        stage('Security Scan') {
            steps {
                sh '''
                    docker run --rm \
                      -v $(pwd):/src \
                      -e TAVOAI_API_KEY=$TAVOAI_API_KEY \
                      tavoai/scanner:latest \
                      --bundle owasp-llm-pro \
                      --path /src \
                      --output results.sarif \
                      --format sarif
                '''

                recordIssues(
                    tool: sarif(pattern: 'results.sarif'),
                    qualityGates: [[threshold: 1, type: 'TOTAL', unstable: true]]
                )
            }
        }
    }
}
```

## Programmatic Usage

### Custom Rule Integration

```typescript
import { TavoAIScanner, RuleEngine } from '@tavoai/sdk';

const scanner = new TavoAIScanner();
const customRules = [
  {
    id: 'custom-sql-injection',
    name: 'Custom SQL Injection Check',
    pattern: 'SELECT * FROM users WHERE id = $USER_INPUT',
    severity: 'high'
  }
];

const results = await scanner.scanWithRules({
  path: './src',
  rules: customRules,
  bundle: 'owasp-llm-basic'  // Combine with existing bundles
});
```

### Result Processing

```typescript
const results = await scanner.scan({
  path: './src',
  bundle: 'owasp-llm-pro'
});

// Filter by severity
const highSeverity = results.findings.filter(
  finding => finding.severity === 'high'
);

// Group by file
const byFile = results.findings.reduce((acc, finding) => {
  acc[finding.file] = acc[finding.file] || [];
  acc[finding.file].push(finding);
  return acc;
}, {});

// Generate summary report
console.log(`Total findings: ${results.findings.length}`);
console.log(`Files scanned: ${results.summary.filesScanned}`);
console.log(`Scan duration: ${results.summary.duration}ms`);
```

### Custom Output Formats

```typescript
class CustomFormatter {
  format(results) {
    return results.findings.map(finding => ({
      file: finding.file,
      line: finding.line,
      rule: finding.ruleId,
      message: finding.message,
      severity: finding.severity,
      remediation: finding.remediation
    }));
  }
}

const results = await scanner.scan({...});
const formatter = new CustomFormatter();
const customOutput = formatter.format(results);
```

## Advanced Configuration

### API Key Management

```bash
# Environment variable
export TAVOAI_API_KEY=your_key_here

# Configuration file
echo "api_key: your_key_here" > ~/.tavoai/config.yaml

# Runtime configuration
tavoai scan --api-key your_key_here ...
```

### Proxy Configuration

```typescript
const scanner = new TavoAIScanner({
  apiKey: 'your_key',
  proxy: {
    host: 'proxy.company.com',
    port: 8080,
    auth: {
      username: 'user',
      password: 'pass'
    }
  }
});
```

### Custom LLM Configuration

```typescript
const scanner = new TavoAIScanner({
  apiKey: 'your_key',
  llm: {
    provider: 'openai',  // 'openai', 'anthropic', 'google'
    model: 'gpt-4',
    temperature: 0.1,
    maxTokens: 2000
  }
});
```

## Troubleshooting

### Common Issues

#### "Bundle not found" Error

```bash
# Check available bundles
tavoai bundles list

# For paid bundles, ensure API key is set
export TAVOAI_API_KEY=your_key_here
tavoai bundles list --show-paid
```

#### API Key Issues

```bash
# Verify API key
tavoai auth status

# Check API key permissions
tavoai auth permissions
```

#### Performance Issues

```typescript
// Enable verbose logging
const scanner = new TavoAIScanner({
  debug: true,
  timeout: 600000  // 10 minutes
});

// Profile scanning performance
const start = Date.now();
const results = await scanner.scan({...});
console.log(`Scan took ${Date.now() - start}ms`);
```

#### Memory Issues with Large Codebases

```bash
# Scan in chunks
tavoai scan --bundle owasp-llm-basic --path ./src --chunk-size 100

# Use streaming for large results
tavoai scan --bundle owasp-llm-basic --path ./src --stream
```

### Debug Mode

```bash
# Enable debug logging
export TAVOAI_DEBUG=1
tavoai scan --bundle owasp-llm-basic --path ./src --verbose
```

```typescript
const scanner = new TavoAIScanner({
  debug: true,
  logLevel: 'debug'
});
```

### Support Resources

- **Documentation**: https://docs.tavoai.com
- **API Reference**: https://docs.tavoai.com/api
- **GitHub Issues**: https://github.com/TavoAI/tavo-rules/issues
- **Community Forum**: https://community.tavoai.com
- **Support**: support@tavoai.com

## Examples

### Security Dashboard Integration

```typescript
class SecurityDashboard {
  async scanRepository(repoPath: string) {
    const scanner = new TavoAIScanner({
      apiKey: process.env.TAVOAI_API_KEY
    });

    // Run multiple scans
    const [basicResults, aiResults] = await Promise.all([
      scanner.scan({ path: repoPath, bundle: 'owasp-llm-basic' }),
      scanner.scan({ path: repoPath, bundle: 'owasp-llm-pro' })
    ]);

    return {
      basic: this.formatResults(basicResults),
      ai: this.formatResults(aiResults),
      summary: this.generateSummary(basicResults, aiResults)
    };
  }

  formatResults(results) {
    return results.findings.map(finding => ({
      id: finding.ruleId,
      title: finding.ruleName,
      severity: finding.severity,
      file: finding.file,
      line: finding.line,
      description: finding.description,
      remediation: finding.remediation
    }));
  }

  generateSummary(basic, ai) {
    return {
      totalFindings: basic.findings.length + ai.findings.length,
      criticalIssues: [...basic.findings, ...ai.findings]
        .filter(f => f.severity === 'critical').length,
      scanTime: Math.max(basic.duration, ai.duration)
    };
  }
}
```

This comprehensive guide covers all aspects of integrating TavoAI security rules into your development workflow. For additional examples and advanced use cases, visit our [documentation site](https://docs.tavoai.com).
