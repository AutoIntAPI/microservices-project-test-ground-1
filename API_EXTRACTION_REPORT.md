# API Call Extraction Report

## Microservices Project - Complete API Communication Mapping

**Generated Date:** October 16, 2025  
**Repository:** microservices-project-test-ground  
**Communication Pattern:** Synchronous REST HTTP API Calls

---

## Summary Statistics

- **Total API Calls Mapped:** 23
- **Direct Service-to-Service Calls:** 3
- **API Gateway Proxy Calls:** 20
- **Services with Outbound Calls:** 3 (api-gateway, order-service, payment-service)
- **Services Receiving Calls:** 5 (user-service, product-service, order-service, payment-service, notification-service)

---

## Call Categories

### 1. Direct Service-to-Service Communication (3 calls)

These are direct HTTP REST calls made between backend services:

| Source | Destination | Endpoint | Purpose |
|--------|-------------|----------|---------|
| order-service | product-service | GET /{product_id} | Product validation during order creation |
| order-service | notification-service | POST /send | Order confirmation notification |
| payment-service | notification-service | POST /send | Payment confirmation notification |

### 2. API Gateway Proxy Calls (20 calls)

The API Gateway acts as a reverse proxy, forwarding client requests to backend services:

#### User Service Routes (6 calls)

- POST /api/users/register → user-service/register
- POST /api/users/login → user-service/login
- GET /api/users/me → user-service/me (authenticated)
- PUT /api/users/me → user-service/me (authenticated)
- GET /api/users/me/addresses → user-service/me/addresses (authenticated)
- POST /api/users/me/addresses → user-service/me/addresses (authenticated)

#### Product Service Routes (5 calls)

- GET /api/products → product-service/
- GET /api/products/{id} → product-service/{id}
- GET /api/products/category/{categoryId} → product-service/category/{categoryId}
- GET /api/products/{id}/reviews → product-service/{id}/reviews
- POST /api/products/{id}/reviews → product-service/{id}/reviews (authenticated)

#### Order Service Routes (4 calls)

- GET /api/orders → order-service/ (authenticated)
- POST /api/orders → order-service/ (authenticated)
- GET /api/orders/{id} → order-service/{id} (authenticated)
- PUT /api/orders/{id}/cancel → order-service/{id}/cancel (authenticated)

#### Payment Service Routes (5 calls)

- POST /api/payments/process → payment-service/process (authenticated)
- GET /api/payments/transactions → payment-service/transactions (authenticated)
- GET /api/payments/transactions/{id} → payment-service/transactions/{id} (authenticated)
- POST /api/payments/methods → payment-service/methods (authenticated)
- GET /api/payments/methods → payment-service/methods (authenticated)

---

## Service Communication Graph

```
┌─────────────────┐
│   API Gateway   │
│    (Port 8000)  │
└────────┬────────┘
         │
         ├──────────────────┬──────────────────┬──────────────────┬──────────────────┐
         │                  │                  │                  │                  │
         ▼                  ▼                  ▼                  ▼                  ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ User Service   │ │Product Service │ │ Order Service  │ │Payment Service │ │Notification    │
│   (Port 3001)  │ │  (Port 3002)   │ │  (Port 3003)   │ │  (Port 3004)   │ │Service (3005)  │
└────────────────┘ └────────┬───────┘ └───┬────────┬───┘ └────────┬───────┘ └────────────────┘
                            ▲              │        │              │
                            │              │        │              │
                            └──────────────┘        └──────────────┘
                            Product Validation      Notifications
```

---

## HTTP Methods Distribution

- **GET:** 12 calls (52%)
- **POST:** 9 calls (39%)
- **PUT:** 2 calls (9%)
- **DELETE:** 0 calls (0%)
- **PATCH:** 0 calls (0%)

---

## Authentication Requirements

- **Authenticated Calls:** 15 (65%)
- **Public Calls:** 8 (35%)

---

## Technology Details

### HTTP Client Libraries Used

- **Python Services:** `requests` library
- **Node.js Services:** `axios` library

### Timeout Configurations

- Direct service-to-service calls: **5 seconds**
- API Gateway proxy calls: **Default (no explicit timeout)**

### Error Handling Patterns

1. **Critical Failures:** Product validation (returns error, blocks order)
2. **Non-Critical Failures:** Notifications (logs warning, continues processing)
3. **Proxy Failures:** Returns 503 Service Unavailable if backend is down

---

## Files Containing API Calls

### Source Files (Making Calls)

1. `services/order-service/app/routes/orders.py` (2 calls)
2. `services/payment-service/app/routes/payments.py` (1 call)
3. `services/api-gateway/src/routes/users.js` (6 calls)
4. `services/api-gateway/src/routes/products.js` (5 calls)
5. `services/api-gateway/src/routes/orders.js` (4 calls)
6. `services/api-gateway/src/routes/payments.js` (5 calls)
7. `services/api-gateway/src/utils/proxy.js` (proxy implementation)

### Destination Files (Receiving Calls)

1. `services/user-service/src/routes/users.js`
2. `services/product-service/src/routes/products.js`
3. `services/order-service/app/routes/orders.py`
4. `services/payment-service/app/routes/payments.py`
5. `services/notification-service/app/routes/notifications.py`

---

## Training Model Recommendations

### Features to Extract from Code

1. **Import Statements:**
   - `import requests` (Python)
   - `const axios = require('axios')` (Node.js)

2. **URL Construction Patterns:**
   - Environment variables: `os.getenv('SERVICE_URL')`
   - Template literals: `f'{SERVICE_URL}/endpoint'`
   - String concatenation

3. **HTTP Method Calls:**
   - `requests.get()`, `requests.post()`, etc.
   - `axios()`, `axios.get()`, `axios.post()`, etc.

4. **Timeout Specifications:**
   - `timeout=5` parameter

5. **Error Handling:**
   - `try/except requests.RequestException`
   - `try/catch error.response`

6. **Proxy Patterns:**
   - Middleware functions forwarding requests
   - Dynamic URL construction from request path

### Validation Metrics

To validate your model's accuracy against this ground truth:

- **Precision:** Correct API calls detected / Total detected
- **Recall:** Correct API calls detected / Total actual (23)
- **F1 Score:** Harmonic mean of precision and recall
- **Service Mapping Accuracy:** Correct source→destination pairs
- **HTTP Method Accuracy:** Correct method identification
- **Endpoint Path Accuracy:** Correct endpoint extraction

### Edge Cases to Test

1. Multi-line API call statements
2. Dynamic endpoint construction with variables
3. Calls with complex payload objects
4. Calls inside conditional blocks
5. Proxy pattern detection
6. Error handling try-catch blocks

---

## Notes

- RabbitMQ infrastructure exists but is NOT used (no message broker calls)
- All communication is synchronous REST HTTP
- No gRPC, WebSockets, or other protocols detected
- Notification calls are fire-and-forget (don't block on failure)
- Product validation calls are blocking (must succeed for order to proceed)

---

## Additional Resources

- Full CSV extraction: `api-calls-extraction.csv`
- Architecture documentation: `ARCHITECTURE.md`
- API documentation: `API.md`
