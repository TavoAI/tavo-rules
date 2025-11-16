#!/usr/bin/env python3
"""
Vulnerable: ISO 42001 Risk Management - Example 4
Missing risk assessment and management procedures
"""

def deploy_ai_system_4(model_config):
    """VULNERABLE: Deploy AI without risk assessment"""
    
    # VULNERABLE: No risk identification
    # VULNERABLE: No risk analysis
    # VULNERABLE: No risk mitigation planning
    
    model = load_model(model_config)
    
    # VULNERABLE: No monitoring or controls
    start_serving(model)
    
    return "Deployed successfully"

def load_model(config):
    # Stub implementation
    return {"model": "loaded"}

def start_serving(model):
    # Stub implementation
    pass
