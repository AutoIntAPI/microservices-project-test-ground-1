# API Extraction Files - Quick Reference

## 📊 Summary

I've extracted all API calls from the microservices codebase and created comprehensive ground truth data for training your ML model.

## 📁 Files Created

| File | Format | Size | Purpose | Best For |
|------|--------|------|---------|----------|
| `api-calls-extraction.csv` | CSV | 5.2 KB | Tabular data with 23 API calls | Excel, data analysis, spreadsheets |
| `api-calls-extraction.json` | JSON | 18.6 KB | Structured data with code snippets | Programmatic access, ML pipelines |
| `API_EXTRACTION_REPORT.md` | Markdown | 8.0 KB | Human-readable report | Documentation, reading |
| `API_EXTRACTION_GUIDE.md` | Markdown | 9.1 KB | Training & validation guide | Model training, testing |

## 🎯 Quick Stats

- **Total API Calls Extracted:** 23
- **Direct Service-to-Service:** 3 calls
- **API Gateway Proxies:** 20 calls
- **Services Making Calls:** 3 (api-gateway, order-service, payment-service)
- **Services Receiving Calls:** 5 (all services)
- **HTTP Methods:** GET (12), POST (9), PUT (2)
- **Authentication:** 15 calls require auth, 8 are public

## 🔍 What Was Extracted

### Direct Service-to-Service Calls (3)

1. **order-service → product-service**
   - Method: `GET /{product_id}`
   - Purpose: Validate product and check stock
   - File: `services/order-service/app/routes/orders.py:57`

2. **order-service → notification-service**
   - Method: `POST /send`
   - Purpose: Send order confirmation
   - File: `services/order-service/app/routes/orders.py:96`

3. **payment-service → notification-service**
   - Method: `POST /send`
   - Purpose: Send payment confirmation
   - File: `services/payment-service/app/routes/payments.py:55`

### API Gateway Proxy Calls (20)

- **User Service:** 6 routes (register, login, profile, addresses)
- **Product Service:** 5 routes (list, get, category, reviews)
- **Order Service:** 4 routes (list, create, get, cancel)
- **Payment Service:** 5 routes (process, transactions, methods)

## 📈 How to Use

### 1. **For Training Data** → Use `api-calls-extraction.json`

```python
import json
with open('api-calls-extraction.json') as f:
    ground_truth = json.load(f)
    
# Each call has: source, destination, method, endpoint, code_snippet
for call in ground_truth['api_calls']:
    print(f"{call['source']['service']} -> {call['destination']['service']}")
```

### 2. **For Validation** → Use `api-calls-extraction.csv`

```python
import pandas as pd
df = pd.read_csv('api-calls-extraction.csv')

# Validate your model predictions
accuracy = (your_predictions == df['HTTP Method']).sum() / len(df)
```

### 3. **For Understanding** → Read `API_EXTRACTION_REPORT.md`

- Human-readable summary
- Service communication graphs
- Statistics and distributions

### 4. **For Implementation** → Follow `API_EXTRACTION_GUIDE.md`

- Step-by-step training instructions
- Code examples for validation
- Common pitfalls to avoid

## 🎓 Model Training Checklist

- [ ] Load ground truth data (CSV or JSON)
- [ ] Extract features from source code:
  - [ ] Import statements (`requests`, `axios`)
  - [ ] HTTP method calls (`.get()`, `.post()`)
  - [ ] URL construction patterns
  - [ ] Service URL environment variables
  - [ ] Authentication middleware
- [ ] Train your model on the patterns
- [ ] Validate against ground truth (23 calls)
- [ ] Calculate metrics: Precision, Recall, F1-Score
- [ ] Test edge cases:
  - [ ] Multi-line statements
  - [ ] Proxy patterns
  - [ ] Dynamic URLs
  - [ ] Template literals/f-strings

## 🔑 Key Patterns to Detect

### Python (requests)

```python
# Pattern 1: GET with timeout
response = requests.get(f'{SERVICE_URL}/{id}', timeout=5)

# Pattern 2: POST with JSON payload
requests.post(f'{SERVICE_URL}/endpoint', json=payload, timeout=5)
```

### JavaScript (axios via proxy)

```javascript
// Pattern: Proxy middleware
router.get('/endpoint', authenticate, createServiceProxy('service', URL))
```

## 📊 Validation Metrics

Test your model's accuracy on:

1. **Call Detection:** Find all 23 API calls
2. **Service Mapping:** Correct source → destination pairs
3. **HTTP Method:** Correct GET/POST/PUT identification
4. **Endpoint Path:** Correct URL path extraction
5. **Authentication:** Identify protected vs public endpoints

**Target Accuracy:**

- Minimum: 80% (19/23 calls correct)
- Good: 90% (21/23 calls correct)
- Excellent: 95%+ (22+/23 calls correct)

## 🚀 Next Steps

1. **Review the data:**

   ```bash
   # Open CSV in Excel
   start api-calls-extraction.csv
   
   # Read the report
   code API_EXTRACTION_REPORT.md
   ```

2. **Train your model** using the JSON file as ground truth

3. **Validate predictions** against the CSV file

4. **Iterate** based on accuracy metrics

## 📞 Need Help?

- **Understand the architecture:** See `ARCHITECTURE.md`
- **API details:** See `API.md`
- **Full report:** See `API_EXTRACTION_REPORT.md`
- **Training guide:** See `API_EXTRACTION_GUIDE.md`

---

**Generated:** October 16, 2025  
**Repository:** microservices-project-test-ground  
**Total API Calls:** 23  
**Files Created:** 4
