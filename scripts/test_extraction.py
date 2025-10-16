#!/usr/bin/env python3
"""
Test script to validate API extraction results
"""

import json
import csv
from pathlib import Path


def test_extraction():
    """Run basic validation tests on the extracted API calls"""
    print("Running API extraction validation tests...")
    print("=" * 60)
    
    # Get paths
    script_dir = Path(__file__).parent
    repo_path = script_dir.parent
    output_dir = repo_path / 'api_extraction_output'
    
    # Test 1: Check if output files exist
    print("\n1. Checking if output files exist...")
    csv_file = output_dir / 'api_calls.csv'
    json_file = output_dir / 'api_calls.json'
    excel_file = output_dir / 'api_calls.xlsx'
    
    if not csv_file.exists():
        print("   ❌ CSV file not found!")
        return False
    print(f"   ✓ CSV file exists: {csv_file}")
    
    if not json_file.exists():
        print("   ❌ JSON file not found!")
        return False
    print(f"   ✓ JSON file exists: {json_file}")
    
    if excel_file.exists():
        print(f"   ✓ Excel file exists: {excel_file}")
    else:
        print(f"   ⚠ Excel file not found (optional)")
    
    # Test 2: Load and validate CSV
    print("\n2. Validating CSV format...")
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            csv_data = list(reader)
        
        if len(csv_data) == 0:
            print("   ❌ CSV file is empty!")
            return False
        
        print(f"   ✓ CSV loaded successfully with {len(csv_data)} API calls")
        
        # Check required fields
        required_fields = ['source_service', 'http_method', 'endpoint', 
                          'destination_service', 'call_type']
        sample_row = csv_data[0]
        missing_fields = [f for f in required_fields if f not in sample_row]
        
        if missing_fields:
            print(f"   ❌ Missing required fields: {missing_fields}")
            return False
        
        print(f"   ✓ All required fields present")
        
    except Exception as e:
        print(f"   ❌ Error reading CSV: {e}")
        return False
    
    # Test 3: Load and validate JSON
    print("\n3. Validating JSON format...")
    try:
        with open(json_file, 'r') as f:
            json_data = json.load(f)
        
        if not isinstance(json_data, list):
            print("   ❌ JSON should be an array!")
            return False
        
        if len(json_data) == 0:
            print("   ❌ JSON array is empty!")
            return False
        
        print(f"   ✓ JSON loaded successfully with {len(json_data)} API calls")
        
        # Verify JSON and CSV have same count
        if len(json_data) != len(csv_data):
            print(f"   ⚠ Warning: JSON ({len(json_data)}) and CSV ({len(csv_data)}) have different counts")
        else:
            print(f"   ✓ JSON and CSV have matching counts")
        
    except Exception as e:
        print(f"   ❌ Error reading JSON: {e}")
        return False
    
    # Test 4: Validate expected patterns
    print("\n4. Validating expected API call patterns...")
    
    # Check for API Gateway proxy calls
    gateway_calls = [c for c in json_data if c['source_service'] == 'api-gateway']
    if len(gateway_calls) == 0:
        print("   ❌ No API Gateway calls found!")
        return False
    print(f"   ✓ Found {len(gateway_calls)} API Gateway proxy calls")
    
    # Check for inter-service REST calls
    rest_calls = [c for c in json_data if c['call_type'] == 'rest_call']
    if len(rest_calls) == 0:
        print("   ⚠ Warning: No inter-service REST calls found")
    else:
        print(f"   ✓ Found {len(rest_calls)} inter-service REST calls")
    
    # Check for endpoint definitions
    endpoint_defs = [c for c in json_data if c['call_type'] == 'endpoint_definition']
    if len(endpoint_defs) == 0:
        print("   ⚠ Warning: No endpoint definitions found")
    else:
        print(f"   ✓ Found {len(endpoint_defs)} endpoint definitions")
    
    # Test 5: Check for expected services
    print("\n5. Validating service coverage...")
    expected_services = ['api-gateway', 'user-service', 'product-service', 
                        'order-service', 'payment-service', 'notification-service']
    
    found_services = set(c['source_service'] for c in json_data)
    missing_services = [s for s in expected_services if s not in found_services]
    
    if missing_services:
        print(f"   ⚠ Warning: Missing services: {missing_services}")
    else:
        print(f"   ✓ All expected services found: {', '.join(sorted(found_services))}")
    
    # Test 6: Validate HTTP methods
    print("\n6. Validating HTTP methods...")
    http_methods = set(c['http_method'] for c in json_data)
    expected_methods = {'GET', 'POST', 'PUT', 'DELETE'}
    
    found_expected = http_methods & expected_methods
    if not found_expected:
        print("   ❌ No standard HTTP methods found!")
        return False
    
    print(f"   ✓ Found HTTP methods: {', '.join(sorted(http_methods))}")
    
    # Test 7: Sample data inspection
    print("\n7. Sample API call inspection...")
    
    # Show an API Gateway proxy call
    gateway_sample = next((c for c in json_data if c['call_type'] == 'proxy'), None)
    if gateway_sample:
        print("\n   API Gateway Proxy Example:")
        print(f"      {gateway_sample['http_method']} {gateway_sample['endpoint']}")
        print(f"      → {gateway_sample['destination_service']} ({gateway_sample['destination_url']})")
        print(f"      Auth: {gateway_sample['authentication_required']}")
    
    # Show an inter-service REST call
    rest_sample = next((c for c in json_data if c['call_type'] == 'rest_call'), None)
    if rest_sample:
        print("\n   Inter-Service REST Call Example:")
        print(f"      Source: {rest_sample['source_service']}")
        print(f"      {rest_sample['http_method']} {rest_sample['endpoint']}")
        print(f"      → {rest_sample['destination_service']} ({rest_sample['destination_url']})")
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  Total API calls extracted: {len(json_data)}")
    print(f"  - API Gateway proxies: {len([c for c in json_data if c['call_type'] == 'proxy'])}")
    print(f"  - Inter-service REST calls: {len([c for c in json_data if c['call_type'] == 'rest_call'])}")
    print(f"  - Endpoint definitions: {len([c for c in json_data if c['call_type'] == 'endpoint_definition'])}")
    print(f"  Services covered: {len(found_services)}")
    print(f"  HTTP methods used: {len(http_methods)}")
    
    print("\n✅ All validation tests passed!")
    print("=" * 60)
    return True


if __name__ == '__main__':
    success = test_extraction()
    exit(0 if success else 1)
