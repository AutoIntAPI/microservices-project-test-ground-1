# API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### User Service

#### Register User
```http
POST /api/users/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "phone": "+1234567890"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "customer"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Login
```http
POST /api/users/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Get User Profile
```http
GET /api/users/me
Authorization: Bearer <token>
```

#### Update User Profile
```http
PUT /api/users/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "John Updated",
  "phone": "+0987654321"
}
```

#### Get User Addresses
```http
GET /api/users/me/addresses
Authorization: Bearer <token>
```

#### Add User Address
```http
POST /api/users/me/addresses
Authorization: Bearer <token>
Content-Type: application/json

{
  "address_line1": "123 Main St",
  "address_line2": "Apt 4B",
  "city": "New York",
  "state": "NY",
  "country": "USA",
  "postal_code": "10001",
  "is_default": true
}
```

---

### Product Service

#### Get All Products
```http
GET /api/products?limit=50&offset=0&search=laptop&category_id=1
```

**Query Parameters:**
- `limit` (optional): Number of products to return (default: 50)
- `offset` (optional): Offset for pagination (default: 0)
- `search` (optional): Search term for product name/description
- `category_id` (optional): Filter by category ID

#### Get Product by ID
```http
GET /api/products/1
```

#### Get Products by Category
```http
GET /api/products/category/1
```

#### Get Product Reviews
```http
GET /api/products/1/reviews
```

#### Add Product Review
```http
POST /api/products/1/reviews
Authorization: Bearer <token>
Content-Type: application/json

{
  "rating": 5,
  "comment": "Excellent product!"
}
```

#### Get Categories
```http
GET /api/products/categories
```

---

### Order Service

#### Get User Orders
```http
GET /api/orders?limit=50&offset=0
Authorization: Bearer <token>
```

#### Create Order
```http
POST /api/orders
Authorization: Bearer <token>
Content-Type: application/json

{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 1
    }
  ],
  "shipping_address_id": 1
}
```

#### Get Order Details
```http
GET /api/orders/1
Authorization: Bearer <token>
```

#### Cancel Order
```http
PUT /api/orders/1/cancel
Authorization: Bearer <token>
```

---

### Payment Service

#### Process Payment
```http
POST /api/payments/process
Authorization: Bearer <token>
Content-Type: application/json

{
  "order_id": 1,
  "amount": 99.99,
  "payment_method": "credit_card"
}
```

#### Get User Transactions
```http
GET /api/payments/transactions?limit=50&offset=0
Authorization: Bearer <token>
```

#### Get Transaction Details
```http
GET /api/payments/transactions/1
Authorization: Bearer <token>
```

#### Add Payment Method
```http
POST /api/payments/methods
Authorization: Bearer <token>
Content-Type: application/json

{
  "type": "credit_card",
  "last_four": "1234",
  "card_brand": "Visa",
  "expiry_month": 12,
  "expiry_year": 2025,
  "is_default": true
}
```

#### Get Payment Methods
```http
GET /api/payments/methods
Authorization: Bearer <token>
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Missing required fields",
  "required": ["email", "password"]
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid token"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error"
}
```

### 503 Service Unavailable
```json
{
  "error": "Service Unavailable",
  "message": "user-service is not responding"
}
```

---

## Rate Limiting

The API Gateway implements rate limiting:
- **Window**: 60 seconds
- **Max Requests**: 100 per window per IP

When rate limit is exceeded:
```json
{
  "error": "Too many requests from this IP, please try again later."
}
```

---

## Testing the API

### Using cURL

```bash
# Register
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}'

# Login
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Get products (no auth required)
curl http://localhost:8000/api/products

# Create order (requires token)
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"items":[{"product_id":1,"quantity":2}],"shipping_address_id":1}'
```

### Using Postman

1. Import the Postman collection (if available)
2. Set the base URL to `http://localhost:8000/api`
3. Create an environment variable for the JWT token
4. Test each endpoint

---

## WebSocket Support

WebSocket support for real-time updates is planned for future releases.

---

## API Versioning

Currently using v1 (implicit). Future versions will use explicit versioning:
- `/api/v1/users`
- `/api/v2/users`
