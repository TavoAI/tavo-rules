#!/usr/bin/env python3
"""
Safe: LLM02 - Insecure Output Handling
Proper validation and sanitization of LLM outputs
"""

import openai
import html
import ast
import os
import re

def safe_code_execution(llm_response):
    """SAFE: Validate and sandbox LLM-generated code"""
    
    # Ask LLM to generate code
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user", 
            "content": "Generate Python code to list files in current directory"
        }]
    )
    
    code = response.choices[0].message.content
    
    # SAFE: Parse and validate code structure
    try:
        tree = ast.parse(code)
        # Only allow safe operations
        allowed_functions = ['os.listdir', 'print']
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = getattr(node.func, 'id', None)
                if func_name and func_name not in allowed_functions:
                    return "Code contains disallowed operations"
                    
    except SyntaxError:
        return "Invalid Python syntax"
    
    # SAFE: Execute in restricted environment
    safe_globals = {'__builtins__': {'print': print, 'len': len}}
    exec(code, safe_globals)
    
    return "Code executed safely"

def safe_html_output(user_query):
    """SAFE: Sanitize LLM output for HTML"""
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_query}]
    )
    
    html_content = response.choices[0].message.content
    
    # SAFE: Sanitize HTML output
    sanitized = html.escape(html_content)
    
    return f"<div>{sanitized}</div>"

def safe_file_operation(llm_instruction):
    """SAFE: Validate LLM instructions for file operations"""
    
    # Define allowed files and operations
    allowed_files = ['temp.txt', 'cache.dat']
    allowed_operations = ['delete', 'create', 'read']
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user", 
            "content": f"What file operation should I perform? {llm_instruction}"
        }]
    )
    
    instruction = response.choices[0].message.content.strip().lower()
    
    # SAFE: Validate operation and file
    if 'delete' in instruction:
        # Only allow deletion of specific temp files
        for filename in allowed_files:
            if filename in instruction and os.path.exists(filename):
                os.remove(filename)
                return f"Safely deleted {filename}"
    
    return "Operation not allowed or file not found"
EOF && cat > llm03_training_poisoning.py << 'EOF'
#!/usr/bin/env python3
"""
Safe: LLM03 - Training Data Poisoning
Proper validation and sanitization of training data sources
"""

import requests
import pandas as pd
import hashlib
import re
from urllib.parse import urlparse

def safe_web_scraping_training():
    """SAFE: Validate and sanitize web-scraped training data"""
    
    # SAFE: Only trusted, verified sources
    trusted_domains = [
        "trusted-research.org",
        "academic-dataset.edu",
        "government-data.gov"
    ]
    
    training_data = []
    
    for url in [
        "https://trusted-research.org/data.csv",
        "https://academic-dataset.edu/reviews.csv"
    ]:
        domain = urlparse(url).netloc
        if domain not in trusted_domains:
            continue
            
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # SAFE: Validate data format and content
            data = response.json()
            
            for item in data:
                # SAFE: Sanitize and validate each item
                if validate_training_item(item):
                    training_data.append(item)
                    
        except (requests.RequestException, ValueError):
            continue  # SAFE: Skip invalid sources
    
    return training_data

def safe_user_feedback_loop():
    """SAFE: Validate user feedback before incorporation"""
    
    user_feedback = [
        {"text": "This product is great!", "sentiment": "positive"},
        {"text": "Terrible service", "sentiment": "negative"}
    ]
    
    # SAFE: Validate and sanitize all feedback
    validated_feedback = []
    
    for item in user_feedback:
        if validate_feedback_item(item):
            # SAFE: Additional sanitization
            clean_item = {
                'text': sanitize_text(item['text']),
                'sentiment': item['sentiment'] if item['sentiment'] in ['positive', 'negative', 'neutral'] else 'neutral'
            }
            validated_feedback.append(clean_item)
    
    return validated_feedback

def safe_api_data_ingestion():
    """SAFE: Validate API data sources"""
    
    # SAFE: Authenticated, verified APIs only
    api_configs = [
        {
            'url': 'https://verified-api.com/data',
            'api_key': os.getenv('VERIFIED_API_KEY'),
            'expected_format': 'json'
        }
    ]
    
    all_data = []
    
    for config in api_configs:
        try:
            headers = {'Authorization': f'Bearer {config["api_key"]}'} if config['api_key'] else {}
            
            response = requests.get(config['url'], headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # SAFE: Validate data structure and content
            if validate_api_response(data, config['expected_format']):
                all_data.extend(data)
                
        except (requests.RequestException, ValueError, KeyError):
            continue  # SAFE: Skip failed validations
    
    return all_data

def validate_training_item(item):
    """Validate a training data item"""
    required_fields = ['text', 'label']
    if not all(field in item for field in required_fields):
        return False
    
    # Check for malicious patterns
    malicious_patterns = [r'<script', r'javascript:', r'on\w+\s*=']
    text = item.get('text', '')
    
    for pattern in malicious_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    
    return True

def validate_feedback_item(item):
    """Validate user feedback item"""
    if not isinstance(item, dict):
        return False
    
    text = item.get('text', '')
    if len(text) > 10000:  # Reasonable length limit
        return False
    
    return True

def sanitize_text(text):
    """Sanitize text content"""
    # Remove potentially dangerous characters
    text = re.sub(r'[<>]', '', text)
    # Limit length
    return text[:1000]

def validate_api_response(data, expected_format):
    """Validate API response format"""
    if expected_format == 'json':
        if not isinstance(data, list):
            return False
        
        # Validate each item in the list
        for item in data[:10]:  # Sample validation
            if not validate_training_item(item):
                return False
    
    return True
