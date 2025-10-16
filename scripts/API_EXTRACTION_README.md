# API Call Extraction Tool

## Overview

This tool automatically extracts all REST API calls from the microservices codebase and generates comprehensive documentation in multiple formats (CSV, JSON, and Excel).

## Purpose

The extracted API call data can be used to:
- Train AI/ML models on API extraction patterns
- Validate model accuracy against ground truth data
- Document microservices communication patterns
- Analyze inter-service dependencies
- Generate API documentation

## Usage

### Basic Usage

Run the extraction script from the repository root:

```bash
python3 scripts/extract_api_calls.py
```

### Output

The tool generates three output files in the `api_extraction_output/` directory:

1. **api_calls.csv** - CSV format for easy data analysis
2. **api_calls.json** - JSON format for programmatic access
3. **api_calls.xlsx** - Excel format with formatting for human readability

### Output Schema

Each extracted API call contains the following fields:

| Field | Description |
|-------|-------------|
| `source_service` | The service making the API call or exposing the endpoint |
| `source_file` | The file path where the API call or endpoint is defined |
| `http_method` | HTTP method (GET, POST, PUT, DELETE, etc.) |
| `endpoint` | The API endpoint path |
| `destination_service` | The target service receiving the call |
| `destination_url` | The full destination URL |
| `authentication_required` | Whether authentication is required (yes/no/varies/unknown) |
| `call_type` | Type of call (proxy, rest_call, endpoint_definition) |

### Call Types

- **proxy**: API Gateway routes that proxy requests to backend services
- **rest_call**: Direct REST API calls between services
- **endpoint_definition**: Service endpoints that are exposed

## Dependencies

### Required
- Python 3.6+
- Standard library modules (os, re, json, csv, pathlib, typing)

### Optional
- `openpyxl` - For Excel export functionality

Install optional dependencies:
```bash
pip3 install openpyxl
```

## What It Extracts

The tool analyzes the following patterns:

### 1. API Gateway Routes
- Extracts proxy routes from API Gateway that forward requests to backend services
- Identifies authentication middleware
- Maps gateway endpoints to backend services

### 2. Inter-Service Communication
- Detects REST API calls using Python's `requests` library
- Detects REST API calls using Node.js HTTP clients
- Resolves service URLs from environment variables

### 3. Service Endpoints
- Extracts endpoint definitions from Flask blueprints (Python)
- Extracts endpoint definitions from Express routers (Node.js)
- Identifies HTTP methods and paths

## Architecture Coverage

The tool covers all microservices in the project:

- **api-gateway** (Node.js) - Entry point and request routing
- **user-service** (Node.js) - User management
- **product-service** (Node.js) - Product catalog
- **order-service** (Python/Flask) - Order processing
- **payment-service** (Python/Flask) - Payment processing
- **notification-service** (Python/Flask) - Notification delivery

## Example Output

### CSV Format
```csv
source_service,source_file,http_method,endpoint,destination_service,destination_url,authentication_required,call_type
api-gateway,services/api-gateway/src/routes/users.js,GET,/users/me,user-service,http://user-service:3001,yes,proxy
order-service,services/order-service/app/routes/orders.py,GET,{PRODUCT_SERVICE_URL}/{product_id},product-service,http://product-service:3002,unknown,rest_call
```

### JSON Format
```json
[
  {
    "source_service": "api-gateway",
    "source_file": "services/api-gateway/src/routes/users.js",
    "http_method": "GET",
    "endpoint": "/users/me",
    "destination_service": "user-service",
    "destination_url": "http://user-service:3001",
    "authentication_required": "yes",
    "call_type": "proxy"
  }
]
```

## Training ML Models

The extracted data is structured for training machine learning models:

1. **Input Features**: Source code patterns (file content, code structure)
2. **Output Labels**: API call metadata (method, endpoint, destination, etc.)
3. **Validation**: Compare model predictions against this ground truth dataset

### Recommended Workflow

1. Run the extraction tool to generate ground truth data
2. Train your model on code samples
3. Validate model accuracy by comparing predictions to the extracted data
4. Calculate metrics like precision, recall, and F1-score

## Extending the Tool

To add support for additional patterns or languages:

1. Add new service directories to `SERVICE_DIRS` dictionary
2. Implement new extraction methods (e.g., `extract_java_service_calls`)
3. Add pattern matching for specific frameworks or libraries
4. Update the `extract_all()` method to include new extraction methods

## Troubleshooting

### Issue: Missing API calls
- Ensure service directories are correctly configured in `SERVICE_DIRS`
- Check if the code uses non-standard HTTP libraries
- Add custom pattern matching for specific frameworks

### Issue: Unknown destination services
- Verify environment variable patterns in `_parse_destination_python()`
- Add support for additional URL resolution patterns

### Issue: Excel export not working
- Install openpyxl: `pip3 install openpyxl`
- CSV and JSON exports will still work without it

## License

This tool is part of the microservices project and follows the same license.
