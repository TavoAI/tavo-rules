# TavoAI Rules Usage Examples

This document provides practical examples of using TavoAI security rules in various scenarios and environments.

## Table of Contents

- [Command Line Usage](#command-line-usage)
- [CI/CD Examples](#ci-cd-examples)
- [IDE Integration](#ide-integration)
- [Custom Scripts](#custom-scripts)
- [Advanced Workflows](#advanced-workflows)

## Command Line Usage

### Basic Scanning

```bash
# Scan a directory with free OWASP rules
tavoai scan --bundle owasp-llm-basic --path ./src

# Scan with AI-enhanced analysis (requires API key)
export TAVOAI_API_KEY=your_key_here
tavoai scan --bundle owasp-llm-pro --path ./src

# Scan specific file types
tavoai scan --bundle owasp-llm-basic --path ./src --include "**/*.py" "**/*.js"

# Exclude test files and dependencies
tavoai scan --bundle owasp-llm-basic --path ./src \
  --exclude "test/**" "node_modules/**" "**/*.test.js"
```

### Output Formats

```bash
# JSON output (default)
tavoai scan --bundle owasp-llm-basic --path ./src --output results.json

# SARIF for GitHub Security tab
tavoai scan --bundle owasp-llm-basic --path ./src \
  --format sarif \
  --output owasp-results.sarif

# JUnit XML for CI systems
tavoai scan --bundle owasp-llm-basic --path ./src \
  --format junit \
  --output security-tests.xml

# HTML report
tavoai scan --bundle owasp-llm-basic --path ./src \
  --format html \
  --output security-report.html
```

### Multiple Bundles

```bash
# Combine free and paid bundles
tavoai scan \
  --bundle owasp-llm-basic \
  --bundle iso-42001-compliance \
  --path ./src

# Mix with external rules
tavoai scan \
  --bundle owasp-llm-basic \
  --bundle github:semgrep/semgrep-rules/python \
  --path ./src
```

### Performance Optimization

```bash
# Limit scan depth
tavoai scan --bundle owasp-llm-basic --path ./src --max-depth 3

# Scan only modified files (Git integration)
tavoai scan --bundle owasp-llm-basic --path ./src --git-diff

# Parallel scanning
tavoai scan --bundle owasp-llm-basic --path ./src --threads 8

# Memory limits
tavoai scan --bundle owasp-llm-basic --path ./src --max-file-size 10MB
```

## CI/CD Examples

### GitHub Actions - Complete Security Pipeline

```yaml
name: Security & Compliance Pipeline
on: [push, pull_request]

env:
  TAVOAI_API_KEY: ${{ secrets.TAVOAI_API_KEY }}

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0  # Full git history for diff scanning

      - name: Setup TavoAI
        uses: tavoai/setup-action@v1

      - name: Fast OWASP LLM Scan
        run: |
          tavoai scan \
            --bundle owasp-llm-basic \
            --path . \
            --format sarif \
            --output owasp-basic.sarif \
            --git-diff

      - name: AI-Enhanced Security Scan
        run: |
          tavoai scan \
            --bundle owasp-llm-pro \
            --path . \
            --format sarif \
            --output owasp-pro.sarif \
            --severity high

      - name: Compliance Check
        run: |
          tavoai scan \
            --bundle iso-42001-compliance \
            --path . \
            --format sarif \
            --output compliance.sarif

      - name: Upload Basic Results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: owasp-basic.sarif
          category: owasp-basic

      - name: Upload Pro Results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: owasp-pro.sarif
          category: owasp-pro

      - name: Upload Compliance Results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: compliance.sarif
          category: compliance

      - name: Comment PR with Summary
        if: github.event_name == 'pull_request'
        uses: tavoai/comment-action@v1
        with:
          results: owasp-basic.sarif,owasp-pro.sarif,compliance.sarif
          summary-only: true

  quality-gate:
    needs: security-scan
    runs-on: ubuntu-latest
    steps:
      - name: Check Quality Gates
        run: |
          # Fail build if critical issues found
          if jq '.runs[0].results[] | select(.level == "error") | length > 0' owasp-pro.sarif; then
            echo "❌ Critical security issues found"
            exit 1
          fi

          # Allow some warnings for non-critical PRs
          warning_count=$(jq '[.runs[0].results[] | select(.level == "warning")] | length' owasp-pro.sarif)
          if [ "$warning_count" -gt 10 ]; then
            echo "⚠️  Too many warnings: $warning_count"
            exit 1
          fi

          echo "✅ Quality gates passed"
```

### GitLab CI - Parallel Scanning

```yaml
stages:
  - security

variables:
  TAVOAI_API_KEY: $TAVOAI_API_KEY

security_scan:
  stage: security
  image: tavoai/scanner:latest
  parallel:
    matrix:
      - BUNDLE: owasp-llm-basic
        OUTPUT: owasp-basic.json
      - BUNDLE: owasp-llm-pro
        OUTPUT: owasp-pro.json
      - BUNDLE: iso-42001-compliance
        OUTPUT: compliance.json
  script:
    - echo "Scanning with bundle: $BUNDLE"
    - tavoai scan --bundle $BUNDLE --path . --output $OUTPUT --format json
    - echo "Results saved to $OUTPUT"
  artifacts:
    reports:
      sast: $OUTPUT
    paths:
      - "*.json"
    expire_in: 1 week
  only:
    - merge_requests

compliance_summary:
  stage: security
  image: tavoai/scanner:latest
  script:
    - echo "Generating compliance summary..."
    - tavoai report --input owasp-basic.json owasp-pro.json compliance.json --format html --output compliance-summary.html
    - echo "Compliance summary generated"
  artifacts:
    paths:
      - compliance-summary.html
    expire_in: 1 week
  dependencies:
    - security_scan
  only:
    - merge_requests
```

### Jenkins Pipeline - Enterprise Setup

```groovy
pipeline {
    agent any

    environment {
        TAVOAI_API_KEY = credentials('tavoai-api-key')
        DOCKER_IMAGE = 'tavoai/scanner:latest'
    }

    stages {
        stage('Security Scan') {
            parallel {
                stage('OWASP Basic') {
                    steps {
                        script {
                            docker.image(env.DOCKER_IMAGE).inside {
                                sh '''
                                    tavoai scan \
                                      --bundle owasp-llm-basic \
                                      --path . \
                                      --output owasp-basic.sarif \
                                      --format sarif
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            sarif(failOnError: false, pattern: 'owasp-basic.sarif')
                        }
                    }
                }

                stage('AI Enhanced') {
                    steps {
                        script {
                            docker.image(env.DOCKER_IMAGE).inside {
                                sh '''
                                    tavoai scan \
                                      --bundle owasp-llm-pro \
                                      --path . \
                                      --output owasp-pro.sarif \
                                      --format sarif \
                                      --timeout 600
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            sarif(failOnError: false, pattern: 'owasp-pro.sarif')
                        }
                    }
                }

                stage('Compliance') {
                    steps {
                        script {
                            docker.image(env.DOCKER_IMAGE).inside {
                                sh '''
                                    tavoai scan \
                                      --bundle iso-42001-compliance \
                                      --path . \
                                      --output compliance.sarif \
                                      --format sarif
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            sarif(failOnError: false, pattern: 'compliance.sarif')
                        }
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    def criticalCount = sh(
                        script: "jq '[.runs[0].results[] | select(.level == \"error\")] | length' owasp-pro.sarif",
                        returnStdout: true
                    ).trim() as Integer

                    if (criticalCount > 0) {
                        error "❌ ${criticalCount} critical security issues found"
                    }

                    def warningCount = sh(
                        script: "jq '[.runs[0].results[] | select(.level == \"warning\")] | length' owasp-pro.sarif",
                        returnStdout: true
                    ).trim() as Integer

                    echo "⚠️  ${warningCount} warnings found"

                    if (warningCount > 20) {
                        unstable "Too many warnings: ${warningCount}"
                    }
                }
            }
        }

        stage('Generate Report') {
            steps {
                script {
                    docker.image(env.DOCKER_IMAGE).inside {
                        sh '''
                            tavoai report \
                              --input owasp-basic.sarif owasp-pro.sarif compliance.sarif \
                              --format html \
                              --output security-report.html \
                              --title "Jenkins Security Scan Report"
                        '''
                    }
                }
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'security-report.html',
                        reportName: 'Security Scan Report'
                    ])
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '*.sarif,*.html', allowEmptyArchive: true
        }
        failure {
            slackSend(
                channel: '#security',
                color: 'danger',
                message: "Security scan failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
    }
}
```

## IDE Integration

### VS Code Extension

```json
// .vscode/settings.json
{
  "tavoai.scanOnSave": true,
  "tavoai.bundles": ["owasp-llm-basic"],
  "tavoai.apiKey": "${workspaceFolder}/.tavoai-key",
  "tavoai.severityFilter": "medium",
  "tavoai.excludePatterns": [
    "node_modules/**",
    "dist/**",
    "**/*.test.*"
  ]
}
```

```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "TavoAI Security Scan",
      "type": "shell",
      "command": "tavoai",
      "args": [
        "scan",
        "--bundle", "owasp-llm-basic",
        "--path", "${workspaceFolder}",
        "--format", "json"
      ],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": [
        {
          "pattern": [
            {
              "regexp": "^(.*):(\\d+):(\\d+):\\s*(error|warning|info)\\s*(.*)$",
              "file": 1,
              "line": 2,
              "column": 3,
              "severity": 4,
              "message": 5
            }
          ],
          "owner": "tavoai"
        }
      ]
    }
  ]
}
```

### Pre-commit Hooks

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running TavoAI security scan..."

# Run fast scan on staged files
tavoai scan \
  --bundle owasp-llm-basic \
  --path . \
  --git-staged-only \
  --format json \
  --output /tmp/security-scan.json

# Check for critical issues
critical_count=$(jq '[.findings[] | select(.severity == "critical")] | length' /tmp/security-scan.json)

if [ "$critical_count" -gt 0 ]; then
    echo "❌ $critical_count critical security issues found!"
    echo "Please fix these issues before committing."
    jq '.findings[] | select(.severity == "critical") | "\(.file):\(.line) \(.message)"' /tmp/security-scan.json
    exit 1
fi

echo "✅ No critical security issues found"
```

### ESLint Integration

```javascript
// .eslintrc.js
module.exports = {
  plugins: ['tavoai'],
  rules: {
    'tavoai/owasp-llm-basic': 'error',
    'tavoai/iso-42001-compliance': 'warn'
  },
  settings: {
    tavoai: {
      apiKey: process.env.TAVOAI_API_KEY,
      bundles: ['owasp-llm-basic'],
      severity: 'medium'
    }
  }
};
```

## Custom Scripts

### Python Security Dashboard

```python
#!/usr/bin/env python3
"""
Security Dashboard - Automated security scanning with TavoAI
"""

import os
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from tavoai import TavoAIScanner


class SecurityDashboard:
    def __init__(self):
        self.scanner = TavoAIScanner(
            api_key=os.getenv('TAVOAI_API_KEY')
        )
        self.results_dir = Path('.security')
        self.results_dir.mkdir(exist_ok=True)

    async def run_full_scan(self, path: str) -> Dict[str, Any]:
        """Run comprehensive security scan"""
        print("🔍 Running comprehensive security scan...")

        # Run multiple scans in parallel
        scans = [
            self.scanner.scan(path=path, bundle='owasp-llm-basic'),
            self.scanner.scan(path=path, bundle='owasp-llm-pro'),
            self.scanner.scan(path=path, bundle='iso-42001-compliance')
        ]

        results = await asyncio.gather(*scans)

        # Combine results
        combined = {
            'timestamp': datetime.utcnow().isoformat(),
            'path': path,
            'scans': {
                'owasp_basic': results[0],
                'owasp_pro': results[1],
                'iso42001': results[2]
            }
        }

        return combined

    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate HTML security report"""
        html = f"""
        <html>
        <head>
            <title>Security Scan Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .summary {{ background: #f0f0f0; padding: 10px; border-radius: 5px; }}
                .finding {{ margin: 10px 0; padding: 10px; border-left: 4px solid; }}
                .critical {{ border-color: #dc3545; background: #f8d7da; }}
                .high {{ border-color: #fd7e14; background: #fff3cd; }}
                .medium {{ border-color: #ffc107; background: #fff3cd; }}
                .low {{ border-color: #28a745; background: #d4edda; }}
            </style>
        </head>
        <body>
            <h1>Security Scan Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p>Scanned: {results['path']}</p>
                <p>Timestamp: {results['timestamp']}</p>
        """

        for scan_name, scan_results in results['scans'].items():
            findings = scan_results.get('findings', [])
            html += f"<p>{scan_name}: {len(findings)} findings</p>"

        html += "</div><h2>Findings</h2>"

        for scan_name, scan_results in results['scans'].items():
            findings = scan_results.get('findings', [])
            if findings:
                html += f"<h3>{scan_name.upper()}</h3>"
                for finding in findings:
                    severity = finding.get('severity', 'medium')
                    html += f"""
                    <div class="finding {severity}">
                        <strong>{finding.get('rule_name', 'Unknown')}</strong><br>
                        File: {finding.get('file', 'Unknown')}<br>
                        Line: {finding.get('line', 'Unknown')}<br>
                        Severity: {severity}<br>
                        Message: {finding.get('message', 'No message')}
                    </div>
                    """

        html += "</body></html>"
        return html

    async def run_dashboard(self, path: str):
        """Run the complete security dashboard"""
        # Run scan
        results = await self.run_full_scan(path)

        # Save JSON results
        json_file = self.results_dir / f"scan-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2)

        # Generate HTML report
        html_report = self.generate_report(results)
        html_file = json_file.with_suffix('.html')
        with open(html_file, 'w') as f:
            f.write(html_report)

        print(f"📊 Results saved to: {json_file}")
        print(f"📄 Report saved to: {html_file}")

        # Print summary
        total_findings = sum(
            len(scan.get('findings', []))
            for scan in results['scans'].values()
        )
        print(f"🔍 Total findings: {total_findings}")


async def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python security_dashboard.py <path-to-scan>")
        sys.exit(1)

    path = sys.argv[1]
    dashboard = SecurityDashboard()
    await dashboard.run_dashboard(path)


if __name__ == "__main__":
    asyncio.run(main())
```

### Node.js Security Monitor

```javascript
#!/usr/bin/env node
/**
 * Security Monitor - Continuous security monitoring with TavoAI
 */

const { TavoAIScanner } = require('@tavoai/sdk');
const fs = require('fs').promises;
const path = require('path');
const { watch } = require('fs');

class SecurityMonitor {
  constructor(options = {}) {
    this.scanner = new TavoAIScanner({
      apiKey: process.env.TAVOAI_API_KEY,
      ...options
    });

    this.watchPaths = options.watchPaths || ['src', 'lib'];
    this.bundles = options.bundles || ['owasp-llm-basic'];
    this.lastScan = new Map();
    this.scanInterval = options.interval || 5000; // 5 seconds
  }

  async scanFile(filePath) {
    try {
      const results = await this.scanner.scan({
        path: filePath,
        bundle: this.bundles[0], // Use first bundle for quick scans
        format: 'json'
      });

      const findings = results.findings || [];
      const fileFindings = findings.filter(f => f.file === filePath);

      if (fileFindings.length > 0) {
        console.log(`🚨 Security issues in ${filePath}:`);
        fileFindings.forEach(finding => {
          const level = this.getSeverityIcon(finding.severity);
          console.log(`  ${level} ${finding.message}`);
          console.log(`     Rule: ${finding.ruleId}`);
          console.log(`     Line: ${finding.line}`);
        });
      } else {
        console.log(`✅ ${filePath} - No issues found`);
      }

      this.lastScan.set(filePath, Date.now());
    } catch (error) {
      console.error(`❌ Scan failed for ${filePath}:`, error.message);
    }
  }

  getSeverityIcon(severity) {
    const icons = {
      critical: '🔴',
      high: '🟠',
      medium: '🟡',
      low: '🟢',
      info: 'ℹ️'
    };
    return icons[severity] || '⚪';
  }

  async startMonitoring() {
    console.log('🔍 Starting security monitoring...');
    console.log(`📁 Watching paths: ${this.watchPaths.join(', ')}`);
    console.log(`📦 Using bundles: ${this.bundles.join(', ')}`);

    // Initial scan of all files
    for (const watchPath of this.watchPaths) {
      await this.scanDirectory(watchPath);
    }

    // Set up file watchers
    for (const watchPath of this.watchPaths) {
      this.watchDirectory(watchPath);
    }

    console.log('✅ Security monitoring active');
  }

  async scanDirectory(dirPath) {
    try {
      const files = await this.getSourceFiles(dirPath);
      console.log(`📂 Scanning ${files.length} files in ${dirPath}...`);

      for (const file of files) {
        await this.scanFile(file);
      }
    } catch (error) {
      console.error(`❌ Failed to scan directory ${dirPath}:`, error.message);
    }
  }

  watchDirectory(dirPath) {
    watch(dirPath, { recursive: true }, async (eventType, filename) => {
      if (!filename) return;

      const filePath = path.join(dirPath, filename);

      // Check if it's a source file
      if (!this.isSourceFile(filePath)) return;

      // Debounce scans
      const now = Date.now();
      const lastScanTime = this.lastScan.get(filePath) || 0;

      if (now - lastScanTime < this.scanInterval) return;

      console.log(`📝 File changed: ${filePath}`);
      await this.scanFile(filePath);
    });
  }

  async getSourceFiles(dirPath) {
    const files = [];
    const extensions = ['.js', '.ts', '.py', '.java', '.go', '.rs'];

    async function scanDir(currentPath) {
      const items = await fs.readdir(currentPath, { withFileTypes: true });

      for (const item of items) {
        const fullPath = path.join(currentPath, item.name);

        if (item.isDirectory() && !item.name.startsWith('.') && item.name !== 'node_modules') {
          await scanDir(fullPath);
        } else if (item.isFile() && extensions.some(ext => item.name.endsWith(ext))) {
          files.push(fullPath);
        }
      }
    }

    await scanDir(dirPath);
    return files;
  }

  isSourceFile(filePath) {
    const extensions = ['.js', '.ts', '.py', '.java', '.go', '.rs'];
    return extensions.some(ext => filePath.endsWith(ext));
  }
}

// CLI usage
if (require.main === module) {
  const monitor = new SecurityMonitor({
    watchPaths: process.argv[2] ? [process.argv[2]] : ['src'],
    bundles: ['owasp-llm-basic'],
    interval: 2000
  });

  monitor.startMonitoring().catch(console.error);
}

module.exports = { SecurityMonitor };
```

## Advanced Workflows

### Multi-Repository Security Orchestration

```bash
#!/bin/bash
# multi-repo-security-scan.sh

REPOS=(
    "https://github.com/company/api-server"
    "https://github.com/company/web-client"
    "https://github.com/company/mobile-app"
)

BUNDLES=("owasp-llm-basic" "owasp-llm-pro" "iso-42001-compliance")
OUTPUT_DIR="./security-reports"

mkdir -p "$OUTPUT_DIR"

for repo in "${REPOS[@]}"; do
    repo_name=$(basename "$repo" .git)
    echo "🔍 Scanning $repo_name..."

    # Clone or update repo
    if [ ! -d "$repo_name" ]; then
        git clone "$repo" "$repo_name"
    else
        cd "$repo_name"
        git pull
        cd ..
    fi

    # Run scans in parallel
    for bundle in "${BUNDLES[@]}"; do
        echo "  📦 Scanning with $bundle..."

        tavoai scan \
            --bundle "$bundle" \
            --path "$repo_name" \
            --output "$OUTPUT_DIR/${repo_name}-${bundle}.sarif" \
            --format sarif \
            --threads 4 &
    done

    # Wait for all scans to complete
    wait

    echo "✅ Completed scanning $repo_name"
done

# Generate consolidated report
echo "📊 Generating consolidated security report..."
tavoai report \
    --input "$OUTPUT_DIR"/*.sarif \
    --format html \
    --output "$OUTPUT_DIR/consolidated-report.html" \
    --title "Multi-Repository Security Report"

echo "🎉 Security scan complete! Reports available in $OUTPUT_DIR"
```

### Compliance as Code

```yaml
# compliance-pipeline.yaml
version: '1.0'

pipelines:
  security-compliance:
    stages:
      - scan:
          name: "OWASP LLM Compliance"
          bundle: "owasp-llm-pro"
          severity_threshold: "high"
          fail_on_findings: true

      - compliance:
          name: "ISO 42001 Governance"
          bundle: "iso-42001-compliance"
          required_controls:
            - "6.1.1"  # Risk management
            - "8.1.1"  # Documentation
            - "9.1.1"  # Monitoring

      - ethics:
          name: "AI Ethics Review"
          bundle: "ai-ethics"
          frameworks:
            - "fairness"
            - "transparency"
            - "accountability"

    gates:
      - quality:
          max_critical_findings: 0
          max_high_findings: 5
          compliance_score_min: 85

      - deployment:
          requires_approval: true
          approvers: ["security-team", "compliance-officer"]
```

These examples demonstrate the flexibility and power of TavoAI security rules across different environments and use cases. For more examples and advanced configurations, visit our [documentation site](https://docs.tavoai.com/examples).
