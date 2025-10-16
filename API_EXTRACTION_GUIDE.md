# API Extraction Tool - Complete Guide

## Overview

This guide provides complete documentation for the API extraction tool created to extract all REST API calls from the microservices codebase. The extracted data can be used to train machine learning models on API extraction patterns and validate their accuracy.

## Problem Statement

**Objective:** Extract all API calls from source to destination services into a table/Excel sheet for:
1. Training ML models on API extraction
2. Validating model accuracy against ground truth data
3. Documenting microservices communication patterns

## Solution

A comprehensive Python-based extraction tool that:
- Analyzes all microservices in the repository
- Extracts API calls from multiple sources
- Generates output in multiple formats (CSV, JSON, Excel)
- Validates extraction accuracy
- Provides human-readable summaries

## Quick Start

### 1. Extract API Calls

```bash
python3 scripts/extract_api_calls.py
```

This will generate:
- `api_extraction_output/api_calls.csv` - CSV format
- `api_extraction_output/api_calls.json` - JSON format
- `api_extraction_output/api_calls.xlsx` - Excel format

### 2. Validate Extraction

```bash
python3 scripts/test_extraction.py
```

This validates:
- File existence and format
- Data completeness
- Expected patterns and services
- HTTP method coverage

### 3. Generate Summary

```bash
python3 scripts/generate_api_summary.py
```

This creates:
- `api_extraction_output/API_CALL_SUMMARY.md` - Human-readable markdown summary

## What Gets Extracted

### 1. API Gateway Proxy Routes (20 calls)

These are client-facing endpoints that the API Gateway proxies to backend services:

**Example:**
```
GET /users/me → user-service (http://user-service:3001)
POST /orders/ → order-service (http://order-service:3003)
```

**Key Information:**
- HTTP method (GET, POST, PUT, DELETE)
- Client-facing endpoint path
- Destination service and URL
- Authentication requirements

### 2. Inter-Service REST API Calls (3 calls)

Direct REST API calls between microservices:

**Example:**
```
order-service → product-service: GET /products/{id}
payment-service → notification-service: POST /send
```

**Why This Matters:**
- Shows service dependencies
- Identifies synchronous communication patterns
- Useful for understanding system architecture

### 3. Service Endpoint Definitions (23 endpoints)

All REST endpoints exposed by each microservice:

**Example:**
```
user-service:
  - GET /me
  - POST /register
  - POST /login
```

**Use Cases:**
- Complete API documentation
- Understanding service capabilities
- API versioning and changes

## Output Schema

Each extracted API call contains:

| Field | Description | Example |
|-------|-------------|---------|
| `source_service` | Service making the call or exposing endpoint | `api-gateway` |
| `source_file` | File path where defined | `services/api-gateway/src/routes/users.js` |
| `http_method` | HTTP method | `GET`, `POST`, `PUT`, `DELETE` |
| `endpoint` | API endpoint path | `/users/me` |
| `destination_service` | Target service | `user-service` |
| `destination_url` | Full destination URL | `http://user-service:3001` |
| `authentication_required` | Auth requirement | `yes`, `no`, `varies`, `unknown` |
| `call_type` | Type of call | `proxy`, `rest_call`, `endpoint_definition` |

## Extraction Statistics

**Total Extracted:** 46 API calls

**Breakdown:**
- **20 API Gateway Proxy Routes**
  - Orders: 4 routes
  - Payments: 5 routes
  - Products: 5 routes
  - Users: 6 routes

- **3 Inter-Service REST Calls**
  - Order → Product: 1 call (product validation)
  - Order → Notification: 1 call (order confirmation)
  - Payment → Notification: 1 call (payment confirmation)

- **23 Service Endpoint Definitions**
  - User Service: 6 endpoints
  - Product Service: 6 endpoints
  - Order Service: 4 endpoints
  - Payment Service: 5 endpoints
  - Notification Service: 2 endpoints

**HTTP Methods:**
- GET: 20 calls
- POST: 18 calls
- PUT: 8 calls

**Authentication:**
- Required: 20 calls
- Not required: 3 calls
- Varies: 23 calls

## Service Coverage

All 6 microservices are covered:

1. **api-gateway** (Node.js/Express)
   - Proxy routing to all backend services
   - Authentication middleware

2. **user-service** (Node.js/Express)
   - User registration and authentication
   - Profile management

3. **product-service** (Node.js/Express)
   - Product catalog
   - Product reviews

4. **order-service** (Python/Flask)
   - Order creation and management
   - Calls Product service for validation
   - Calls Notification service for confirmations

5. **payment-service** (Python/Flask)
   - Payment processing
   - Calls Notification service for confirmations

6. **notification-service** (Python/Flask)
   - Email notifications
   - Receives calls from Order and Payment services

## Using for ML Model Training

### Training Workflow

1. **Extract Ground Truth Data**
   ```bash
   python3 scripts/extract_api_calls.py
   ```

2. **Prepare Training Data**
   - Use source files as input features
   - Use extracted API calls as labels
   - Split into training/validation sets

3. **Train Your Model**
   - Input: Source code patterns
   - Output: API call metadata (method, endpoint, destination, etc.)

4. **Validate Accuracy**
   ```bash
   python3 scripts/test_extraction.py
   ```
   - Compare model predictions to extracted ground truth
   - Calculate precision, recall, F1-score

### Example Use Case

**Goal:** Train a model to identify inter-service REST API calls

**Ground Truth (from extraction):**
```csv
source_service,http_method,endpoint,destination_service
order-service,GET,{PRODUCT_SERVICE_URL}/{product_id},product-service
order-service,POST,{NOTIFICATION_SERVICE_URL}/send,notification-service
payment-service,POST,{NOTIFICATION_SERVICE_URL}/send,notification-service
```

**Model Training:**
1. Input: Code snippets containing `requests.get()`, `requests.post()`
2. Expected Output: HTTP method, destination service, endpoint pattern
3. Validation: Compare against the 3 inter-service calls in ground truth

## Technical Details

### Supported Patterns

**Node.js/Express:**
- `router.get('/path', ...)` - Route definitions
- `router.post('/path', ...)` - Route definitions
- `authenticate` middleware - Authentication detection

**Python/Flask:**
- `@bp.route('/path', methods=['GET'])` - Route definitions
- `requests.get(url)` - REST API calls
- `requests.post(url, json=data)` - REST API calls
- `os.getenv('SERVICE_URL', 'default')` - URL resolution

### Environment Variable Resolution

The tool automatically resolves service URLs from environment variables:

```python
# In code:
PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://product-service:3002')
response = requests.get(f'{PRODUCT_SERVICE_URL}/{product_id}')

# Extracted:
{
  "endpoint": "{PRODUCT_SERVICE_URL}/{product_id}",
  "destination_service": "product-service",
  "destination_url": "http://product-service:3002"
}
```

## Limitations and Future Enhancements

### Current Limitations

1. **Static Analysis Only**: Does not execute code or follow dynamic calls
2. **Pattern-Based**: Relies on recognizing specific code patterns
3. **No Type Resolution**: Does not perform deep type analysis

### Potential Enhancements

1. **Add More Languages**: Support for Java, Go, etc.
2. **GraphQL Support**: Extract GraphQL queries/mutations
3. **Async Patterns**: Detect message queue communications (RabbitMQ, Kafka)
4. **Dynamic Analysis**: Use instrumentation for runtime call detection
5. **Visualization**: Generate architecture diagrams from extracted data

## File Structure

```
scripts/
├── extract_api_calls.py        # Main extraction script
├── test_extraction.py          # Validation tests
├── generate_api_summary.py     # Summary generator
└── API_EXTRACTION_README.md    # Detailed documentation

api_extraction_output/          # Generated output (gitignored)
├── api_calls.csv               # CSV format
├── api_calls.json              # JSON format
├── api_calls.xlsx              # Excel format
└── API_CALL_SUMMARY.md         # Human-readable summary
```

## Dependencies

**Required:**
- Python 3.6+
- Standard library (os, re, json, csv, pathlib, typing)

**Optional:**
- `openpyxl` - For Excel export (install via `pip3 install openpyxl`)

## Troubleshooting

### No API calls extracted for a service

**Check:**
- Service directory path in `SERVICE_DIRS` dictionary
- File patterns match your service structure
- Code uses supported HTTP libraries

### Destination service showing as "unknown"

**Check:**
- Environment variable naming conventions
- URL patterns in code
- `_parse_destination_python()` method

### Excel export not working

**Solution:**
```bash
pip3 install openpyxl
```
CSV and JSON exports work without it.

## Contributing

To extend the tool:

1. Add new patterns to extraction methods
2. Update `SERVICE_DIRS` for new services
3. Enhance URL resolution logic
4. Add new output formats

## Support

For issues or questions:
1. Check the detailed README: `scripts/API_EXTRACTION_README.md`
2. Review the code comments in `scripts/extract_api_calls.py`
3. Run validation tests: `python3 scripts/test_extraction.py`

## License

This tool is part of the microservices-project-test-ground repository and follows the same license.

---

**Last Updated:** 2025-10-16
**Version:** 1.0.0
