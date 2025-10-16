# API Extraction Ground Truth - Usage Guide

## Overview

This directory contains comprehensive ground truth data for all API calls in the microservices project. These files are designed to help you train and validate machine learning models for API call extraction from source code.

## Generated Files

### 1. **api-calls-extraction.csv**

- **Format:** CSV (Comma-Separated Values)
- **Best for:** Excel, Google Sheets, data analysis tools
- **Contains:** 23 API calls with 13 columns of metadata
- **Columns:**
  - Call ID
  - Source Service
  - Source File
  - Source Line
  - HTTP Method
  - Destination Service
  - Destination Endpoint
  - Purpose
  - Request Type
  - Response Expected
  - Authentication Required
  - Timeout (seconds)
  - Error Handling

### 2. **api-calls-extraction.json**

- **Format:** JSON (JavaScript Object Notation)
- **Best for:** Programmatic access, ML pipelines, automated validation
- **Contains:**
  - Detailed metadata for all 23 API calls
  - Source code snippets
  - Service statistics
  - Environment variables
  - Error handling patterns

### 3. **API_EXTRACTION_REPORT.md**

- **Format:** Markdown
- **Best for:** Human reading, documentation
- **Contains:**
  - Executive summary
  - Service communication graph
  - Statistics and distributions
  - Training recommendations
  - Validation metrics

## How to Use for Model Training

### Step 1: Understand the Ground Truth

```bash
# Open the CSV in Excel or any spreadsheet tool
start api-calls-extraction.csv

# Or view the report
cat API_EXTRACTION_REPORT.md
```

### Step 2: Extract Features from Source Code

Your model should learn to identify these patterns:

**Python (requests library):**

```python
# Pattern 1: Simple GET
response = requests.get(f'{SERVICE_URL}/{resource_id}', timeout=5)

# Pattern 2: POST with payload
requests.post(f'{SERVICE_URL}/endpoint', json=payload, timeout=5)
```

**JavaScript (axios library):**

```javascript
// Pattern 1: Proxy pattern
router.get('/endpoint', createServiceProxy('service-name', SERVICE_URL))

// Pattern 2: Direct axios call
const response = await axios.get(`${SERVICE_URL}/endpoint`)
```

### Step 3: Train Your Model

**Input Features to Extract:**

1. HTTP client library imports (`requests`, `axios`)
2. Service URL environment variables
3. HTTP method calls (`.get()`, `.post()`, etc.)
4. URL construction patterns
5. Authentication middleware
6. Timeout specifications

**Output Labels (Ground Truth):**

- Source service name
- Destination service name
- HTTP method
- Endpoint path
- Authentication requirement

### Step 4: Validate Against Ground Truth

```python
import json
import pandas as pd

# Load ground truth
with open('api-calls-extraction.json') as f:
    ground_truth = json.load(f)

# Or use CSV
df_truth = pd.read_csv('api-calls-extraction.csv')

# Your model predictions
predictions = your_model.extract_api_calls(codebase)

# Calculate metrics
precision = correct_predictions / total_predictions
recall = correct_predictions / 23  # Total ground truth calls
f1_score = 2 * (precision * recall) / (precision + recall)
```

## Validation Metrics

### Exact Match Metrics

- **Call Detection:** Did you find the API call? (Binary)
- **Service Pair:** Did you identify source→destination correctly?
- **HTTP Method:** Did you extract the correct method (GET, POST, etc.)?
- **Endpoint Path:** Did you extract the correct URL path?

### Partial Match Metrics

- **Service Name Similarity:** Edit distance between predicted and actual service names
- **Endpoint Similarity:** Matching patterns in URL paths (e.g., param vs hardcoded)

### Example Validation Code

```python
def validate_extraction(predicted, ground_truth):
    """
    Validate a single API call extraction
    """
    score = {
        'source_match': predicted['source'] == ground_truth['source']['service'],
        'destination_match': predicted['destination'] == ground_truth['destination']['service'],
        'method_match': predicted['method'] == ground_truth['request']['method'],
        'endpoint_match': predicted['endpoint'] == ground_truth['destination']['endpoint'],
        'auth_match': predicted['auth'] == ground_truth['request']['authentication']
    }
    
    return sum(score.values()) / len(score)

# Calculate average accuracy
accuracies = [validate_extraction(pred, truth) 
              for pred, truth in zip(predictions, ground_truth['api_calls'])]
average_accuracy = sum(accuracies) / len(accuracies)
print(f"Average Accuracy: {average_accuracy:.2%}")
```

## Common Pitfalls to Avoid

### 1. Proxy Pattern Detection

❌ **Wrong:** Detecting only direct HTTP calls  
✅ **Correct:** Also detect proxy middleware patterns

```javascript
// This is also an API call!
router.get('/endpoint', createServiceProxy('service', URL))
```

### 2. Multi-line Statements

❌ **Wrong:** Only parsing single-line calls  
✅ **Correct:** Handle multi-line function calls

```python
# Multi-line call
requests.post(
    f'{NOTIFICATION_SERVICE_URL}/send',
    json=notification_payload,
    timeout=5
)
```

### 3. Dynamic URL Construction

❌ **Wrong:** Missing calls with complex URL building  
✅ **Correct:** Detect template literals and f-strings

```python
# Python f-string
url = f'{SERVICE_URL}/{resource_id}'
response = requests.get(url, timeout=5)

# JavaScript template literal
const url = `${SERVICE_URL}/endpoint`;
```

### 4. Environment Variables

❌ **Wrong:** Hardcoding service URLs  
✅ **Correct:** Track environment variable usage

```python
SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://product-service:3002')
# Your model should extract both the env var name and default value
```

## Statistics Summary

| Metric | Value |
|--------|-------|
| Total API Calls | 23 |
| Direct Service-to-Service | 3 |
| API Gateway Proxies | 20 |
| GET Requests | 12 (52%) |
| POST Requests | 9 (39%) |
| PUT Requests | 2 (9%) |
| Authenticated Calls | 15 (65%) |
| Python Services | 3 calls |
| JavaScript Services | 20 calls |
| Services Making Calls | 3 |
| Services Receiving Calls | 5 |

## Service Communication Map

```
order-service (2 calls)
├─→ product-service (GET) [product validation]
└─→ notification-service (POST) [order confirmation]

payment-service (1 call)
└─→ notification-service (POST) [payment confirmation]

api-gateway (20 calls)
├─→ user-service (6 calls) [authentication, profiles, addresses]
├─→ product-service (5 calls) [catalog, reviews]
├─→ order-service (4 calls) [order management]
└─→ payment-service (5 calls) [payment processing, methods]
```

## Advanced Use Cases

### 1. Pattern Recognition Training

Use the JSON file to train on code patterns:

```python
patterns = [call['code_snippet'] for call in ground_truth['api_calls']]
# Train your model to recognize these patterns
```

### 2. Service Dependency Graph

Build a dependency graph from the data:

```python
edges = [(call['source']['service'], call['destination']['service']) 
         for call in ground_truth['api_calls']]
# Create directed graph for visualization
```

### 3. Authentication Analysis

Analyze which calls require authentication:

```python
auth_required = [call for call in ground_truth['api_calls'] 
                 if call['request'].get('authentication', False)]
```

### 4. Error Handling Classification

Classify error handling strategies:

```python
critical = [call for call in ground_truth['api_calls'] 
            if call.get('error_handling') == 'critical']
non_critical = [call for call in ground_truth['api_calls'] 
                if call.get('error_handling') == 'non_critical']
```

## Testing Your Model

### Minimum Viable Test

```python
# Your model should at least detect:
assert len(your_predictions) >= 20  # Should find most calls
assert 'order-service' in [p['source'] for p in your_predictions]
assert 'notification-service' in [p['destination'] for p in your_predictions]
```

### Comprehensive Test

```python
# Load ground truth
with open('api-calls-extraction.json') as f:
    gt = json.load(f)

# Test each type
assert any(c['request']['method'] == 'GET' for c in your_predictions)
assert any(c['request']['method'] == 'POST' for c in your_predictions)
assert any(c['request']['authentication'] == True for c in your_predictions)
assert any(c['source']['language'] == 'python' for c in your_predictions)
assert any(c['source']['language'] == 'javascript' for c in your_predictions)
```

## Questions or Issues?

If you find discrepancies or have questions about the ground truth data:

1. Check the actual source files referenced in the extraction
2. Verify line numbers (they may shift if code changes)
3. Review the `API_EXTRACTION_REPORT.md` for context
4. Cross-reference with `ARCHITECTURE.md` for system design

## License

This ground truth data is part of the microservices-project-test-ground repository and follows the same license.

---

**Generated:** October 16, 2025  
**Version:** 1.0  
**Total API Calls:** 23
