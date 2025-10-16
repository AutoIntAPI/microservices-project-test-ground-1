#!/usr/bin/env python3
"""
Generate a human-readable summary of API calls
"""

import json
from pathlib import Path
from collections import defaultdict


def generate_summary():
    """Generate a markdown summary of API calls"""
    
    script_dir = Path(__file__).parent
    repo_path = script_dir.parent
    output_dir = repo_path / 'api_extraction_output'
    json_file = output_dir / 'api_calls.json'
    
    if not json_file.exists():
        print(f"Error: {json_file} not found. Please run extract_api_calls.py first.")
        return
    
    # Load data
    with open(json_file, 'r') as f:
        api_calls = json.load(f)
    
    # Generate markdown summary
    summary = []
    summary.append("# API Call Extraction Summary\n")
    summary.append(f"**Total API Calls Extracted:** {len(api_calls)}\n")
    summary.append("---\n")
    
    # Group by call type
    by_type = defaultdict(list)
    for call in api_calls:
        by_type[call['call_type']].append(call)
    
    summary.append("## Overview by Call Type\n")
    for call_type, calls in sorted(by_type.items()):
        summary.append(f"- **{call_type.replace('_', ' ').title()}**: {len(calls)} calls\n")
    summary.append("\n")
    
    # API Gateway Proxy Routes
    if 'proxy' in by_type:
        summary.append("## API Gateway Proxy Routes\n")
        summary.append("These routes are exposed to clients via the API Gateway and proxied to backend services.\n\n")
        
        # Group by destination service
        by_dest = defaultdict(list)
        for call in by_type['proxy']:
            by_dest[call['destination_service']].append(call)
        
        for service, calls in sorted(by_dest.items()):
            summary.append(f"### → {service.upper()}\n")
            summary.append("| Method | Endpoint | Auth Required |\n")
            summary.append("|--------|----------|---------------|\n")
            for call in sorted(calls, key=lambda x: (x['http_method'], x['endpoint'])):
                auth = "✓" if call['authentication_required'] == 'yes' else "✗"
                summary.append(f"| {call['http_method']} | `{call['endpoint']}` | {auth} |\n")
            summary.append("\n")
    
    # Inter-Service Communication
    if 'rest_call' in by_type:
        summary.append("## Inter-Service REST API Calls\n")
        summary.append("These are direct REST API calls between microservices.\n\n")
        
        summary.append("| Source Service | Method | Endpoint | Destination Service |\n")
        summary.append("|----------------|--------|----------|--------------------|\n")
        for call in sorted(by_type['rest_call'], 
                          key=lambda x: (x['source_service'], x['http_method'])):
            summary.append(f"| {call['source_service']} | {call['http_method']} | "
                         f"`{call['endpoint']}` | {call['destination_service']} |\n")
        summary.append("\n")
    
    # Service Endpoints
    if 'endpoint_definition' in by_type:
        summary.append("## Service Endpoint Definitions\n")
        summary.append("These are the REST endpoints exposed by each microservice.\n\n")
        
        # Group by service
        by_service = defaultdict(list)
        for call in by_type['endpoint_definition']:
            by_service[call['source_service']].append(call)
        
        for service, calls in sorted(by_service.items()):
            summary.append(f"### {service.upper()}\n")
            
            # Group by method
            by_method = defaultdict(list)
            for call in calls:
                by_method[call['http_method']].append(call)
            
            for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                if method in by_method:
                    endpoints = [c['endpoint'] for c in by_method[method]]
                    for endpoint in sorted(endpoints):
                        summary.append(f"- **{method}** `{endpoint}`\n")
            summary.append("\n")
    
    # Service Dependencies Graph
    summary.append("## Service Dependencies\n")
    summary.append("Shows which services call which other services.\n\n")
    
    dependencies = defaultdict(set)
    for call in api_calls:
        if call['source_service'] != call['destination_service']:
            dependencies[call['source_service']].add(call['destination_service'])
    
    summary.append("```\n")
    for source, destinations in sorted(dependencies.items()):
        for dest in sorted(destinations):
            summary.append(f"{source} --> {dest}\n")
    summary.append("```\n\n")
    
    # HTTP Methods Statistics
    summary.append("## HTTP Methods Distribution\n")
    methods_count = defaultdict(int)
    for call in api_calls:
        methods_count[call['http_method']] += 1
    
    summary.append("| Method | Count |\n")
    summary.append("|--------|-------|\n")
    for method, count in sorted(methods_count.items()):
        summary.append(f"| {method} | {count} |\n")
    summary.append("\n")
    
    # Authentication Statistics
    summary.append("## Authentication Requirements\n")
    auth_stats = defaultdict(int)
    for call in api_calls:
        auth_stats[call['authentication_required']] += 1
    
    summary.append("| Requirement | Count |\n")
    summary.append("|-------------|-------|\n")
    for req, count in sorted(auth_stats.items()):
        summary.append(f"| {req} | {count} |\n")
    summary.append("\n")
    
    # Write to file
    summary_file = output_dir / 'API_CALL_SUMMARY.md'
    with open(summary_file, 'w') as f:
        f.writelines(summary)
    
    print(f"Summary generated: {summary_file}")
    print("\nPreview:")
    print("".join(summary[:20]))
    print("...\n")


if __name__ == '__main__':
    generate_summary()
