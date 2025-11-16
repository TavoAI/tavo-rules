# MIT AI Risk Repository Sync

This document explains how to sync the latest risks from the [MIT AI Risk Repository](https://airisk.mit.edu) into TavoAI rule format.

## Overview

The MIT AI Risk Repository is a comprehensive database of over 1600 AI risks, categorized by domain, entity, intent, and timing. The `sync-mit-ai-risks.py` script automatically pulls the latest version and converts each risk into a TavoAI hybrid rule.

## Prerequisites

1. **Python Packages**:
   ```bash
   pip install gspread oauth2client pandas pyyaml requests
   ```

2. **Google Sheets API Access** (Optional):
   - For full API access, create a Google Cloud service account
   - Enable Google Sheets API
   - Download service account JSON key

## Usage

### Basic Usage (Public Access)

The script can download the MIT database using public access:

```bash
cd scripts/
python sync-mit-ai-risks.py
```

### Testing with Mock Data

For development and testing, use mock data:

```bash
python sync-mit-ai-risks.py --mock-data --limit 5 --validate
```

### With Google API Key

For faster access and full functionality:

```bash
python sync-mit-ai-risks.py --api-key path/to/service-account.json
```

### Testing with Limited Risks

To test with a small subset:

```bash
python sync-mit-ai-risks.py --limit 10 --validate
```

### Full Options

```bash
python sync-mit-ai-risks.py \
    --api-key path/to/service-account.json \
    --sheet-id 1zbIPiSIAu6v9MI98HtB4gyM_sI4JsOSuAlVLWAIqw_U \
    --output-dir bundles/ai-enhanced/mit-ai-risk-repo/rules \
    --limit 100 \
    --validate
```

## How It Works

### 1. Data Source

The script accesses the MIT AI Risk Database Google Sheet:
- **Sheet ID**: `1zbIPiSIAu6v9MI98HtB4gyM_sI4JsOSuAlVLWAIqw_U`
- **Public URL**: https://docs.google.com/spreadsheets/d/1zbIPiSIAu6v9MI98HtB4gyM_sI4JsOSuAlVLWAIqw_U/copy

### 2. Risk Parsing

Each risk record contains:
- **ID**: Unique risk identifier
- **Risk**: Risk description
- **Domain**: One of 7 domains (Discrimination & Toxicity, Privacy & Security, etc.)
- **Subdomain**: More specific categorization
- **Entity**: Who/what causes the risk (AI, Human, Other)
- **Intent**: Intentional vs Unintentional
- **Timing**: Pre-deployment vs Post-deployment
- **Source**: Academic paper or framework reference

### 3. Rule Generation

For each risk, the script generates:

#### Rule Structure
```yaml
version: "1.0"
id: "tavoai-mit-risk-{risk_id}"
name: "MIT AI Risk: {risk_description}"
category: "{mapped_category}"
subcategory: "{mapped_subdomain}"
severity: "{calculated_severity}"
rule_type: "hybrid"
```

#### Domain Mappings

| MIT Domain | TavoAI Category | TavoAI Subcategory | Severity |
|------------|-----------------|-------------------|----------|
| Discrimination & Toxicity | ethics | discrimination | high |
| Privacy & Security | security | security-privacy | high |
| Misinformation | ethics | misinformation | medium |
| Malicious Actors | security | malicious-use | critical |
| Human-Computer Interaction | ethics | human-computer-interaction | medium |
| Sociotechnical Harms | ethics | sociotechnical-risks | high |
| AI Harms to the Environment | ethics | environmental | medium |

#### Standards Mappings

Each rule includes relevant standards:
- **ISO 42001**: AI management system sections
- **NIST AI RMF**: AI risk management framework functions
- **CWE**: Common Weakness Enumeration
- **CAPEC**: Common Attack Pattern Enumeration

#### Heuristics Generation

The script generates heuristics based on:
- Domain-specific patterns
- Keyword extraction from risk descriptions
- Common AI security patterns

#### AI Analysis Prompts

Each rule includes a customized AI analysis prompt that:
- References the specific MIT risk
- Includes causal factors (entity, intent, timing)
- Provides context from the source material
- Guides analysis toward the specific risk characteristics

### 4. Output

Generated rules are saved as:
```
bundles/ai-enhanced/mit-ai-risk-repo/rules/tavoai-mit-risk-{id}.yaml
```

## Examples

### Generated Rule Example

```yaml
version: "1.0"
id: "tavoai-mit-risk-R001"
name: "MIT AI Risk: AI systems that create unfair discrimination"
category: "ethics"
subcategory: "discrimination"
severity: "high"
rule_type: "hybrid"

standards:
  mit_ai_risk: ["discrimination-and-toxicity"]
  iso_42001: ["6.2.2", "7.7.1"]
  nist_ai_rmf: ["MEASURE-2.2"]
  cwe: ["CWE-710"]
  capec: ["CAPEC-183"]

heuristics:
  - type: "semgrep"
    languages: ["python"]
    pattern: "model\\.fit\\(.*\\).*gender|race|age"
    message: "Potential discriminatory model training"
    severity: "high"

ai_analysis:
  trigger: ["always"]
  prompt_template: |
    Analyze this AI system for the following MIT AI Risk Repository risk:
    Risk: AI systems that create unfair discrimination
    Domain: Discrimination & Toxicity
    Entity: AI
    Intent: Unintentional
    Timing: Post-deployment
    # ... detailed analysis prompt

sarif_output:
  rule_id: "tavoai-mit-risk-R001"
  rule_name: "MIT AI Risk: AI systems that create unfair discrimination"
  short_description: "AI systems that create unfair discrimination"
  help_uri: "https://airisk.mit.edu/risk/R001"
  tags: ["mit-ai-risk", "discrimination", "ai-risk-repository"]
```

## Integration with TavoAI

### Automatic Updates

Set up a cron job for regular updates:

```bash
# Daily sync at 2 AM
0 2 * * * cd /path/to/tavo-rules && python scripts/sync-mit-ai-risks.py --validate
```

### CI/CD Integration

Add to your CI pipeline:

```yaml
- name: Sync MIT AI Risks
  run: |
    cd scripts/
    python sync-mit-ai-risks.py --validate
    git add bundles/ai-enhanced/mit-ai-risk-repo/rules/
    git commit -m "chore: sync latest MIT AI risks" || true
```

### Validation

The script includes automatic validation:

```bash
python sync-mit-ai-risks.py --validate
```

This runs the existing `validate-rules.py` script to ensure generated rules conform to the TavoAI schema.

## Status

### ✅ **Working Features**

- **CSV Download**: Successfully downloads MIT AI Risk Database via public access
- **Risk Parsing**: Parses CSV data into structured risk records
- **Rule Generation**: Converts MIT risks into TavoAI hybrid rule format
- **Standards Mapping**: Maps MIT domains to ISO 42001, NIST AI RMF, CWE, CAPEC
- **Heuristics Generation**: Creates semantic patterns based on risk content
- **AI Analysis Prompts**: Generates contextual analysis prompts for each risk
- **Validation Integration**: Integrates with existing TavoAI validation scripts

### 🔧 **Known Limitations**

1. **Google Sheets Access**: Public CSV download may have rate limits or access issues
2. **Data Completeness**: Only processes risks that can be successfully parsed
3. **Rule Quality**: Generated heuristics and prompts may need manual refinement

### 📊 **Test Results**

Successfully tested with mock data:
- Generated 3 sample rules covering different MIT risk domains
- Rules include proper YAML structure, standards mappings, and AI analysis
- Validation script integration working correctly

## Troubleshooting

### Common Issues

1. **Google Sheets Access**:
   - Public access should work without API key
   - For full functionality, set up Google Sheets API

2. **Rate Limiting**:
   - Google Sheets API has rate limits
   - Use `--limit` for testing

3. **Large Dataset**:
   - 1600+ risks may take time to process
   - Use `--limit` for smaller batches

### Manual Inspection

After sync, inspect generated rules:

```bash
# Check a few generated rules
head -50 bundles/ai-enhanced/mit-ai-risk-repo/rules/tavoai-mit-risk-*.yaml

# Validate all rules
python scripts/validate-rules.py --rules-dir bundles/ai-enhanced/mit-ai-risk-repo/rules/
```

## Future Enhancements

### Planned Features

1. **Incremental Updates**: Only sync changed risks
2. **Risk Prioritization**: Focus on high-impact risks
3. **Custom Mappings**: User-defined domain mappings
4. **Risk Correlations**: Link related risks
5. **Historical Tracking**: Track risk evolution over time

### Contributing

To improve the sync script:

1. **Better Heuristics**: Enhance pattern generation algorithms
2. **Improved Prompts**: Refine AI analysis prompts
3. **Additional Standards**: Map to more security frameworks
4. **Performance**: Optimize for large datasets

## References

- [MIT AI Risk Repository](https://airisk.mit.edu)
- [AI Risk Database Google Sheet](https://docs.google.com/spreadsheets/d/1zbIPiSIAu6v9MI98HtB4gyM_sI4JsOSuAlVLWAIqw_U/copy)
- [TavoAI Rule Format Specification](./hybrid-format-spec.md)
- [MIT AI Risk Research Paper](https://doi.org/10.48550/arXiv.2408.12622)
- [Semgrep Rules Repository](https://github.com/returntocorp/semgrep-rules)
- [Open Policy Agent Library](https://github.com/open-policy-agent/library)
- [YARA Rules Repository](https://github.com/Yara-Rules/rules)
- [Sigma Rules Repository](https://github.com/SigmaHQ/sigma)
