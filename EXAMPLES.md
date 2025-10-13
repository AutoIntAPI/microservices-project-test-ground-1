# Quick Start Examples

This file contains practical examples to test the E-Commerce Microservices API.

## Prerequisites

Make sure all services are running:

```bash
docker-compose up -d
```

Wait for services to be healthy (about 30 seconds), then verify:

```bash
curl http://localhost:8000/health
curl http://localhost:3001/health
curl http://localhost:3002/health
curl http://localhost:3003/health
curl http://localhost:3004/health
curl http://localhost:3005/health
```

## Example Workflow

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePassword123!",
    "name": "John Doe",
    "phone": "+1234567890"
  }'
```

**Expected Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "john.doe@example.com",
    "name": "John Doe",
    "role": "customer"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Save the token for subsequent requests!**

### 2. Login (Alternative to Registration)

```bash
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePassword123!"
  }'
```

### 3. Get User Profile

```bash
# Replace YOUR_TOKEN with the actual token from login/register
export TOKEN="YOUR_TOKEN_HERE"

curl http://localhost:8000/api/users/me \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Add User Address

```bash
curl -X POST http://localhost:8000/api/users/me/addresses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "address_line1": "123 Main Street",
    "address_line2": "Apartment 4B",
    "city": "New York",
    "state": "NY",
    "country": "USA",
    "postal_code": "10001",
    "is_default": true
  }'
```

### 5. Browse Products

```bash
# Get all products
curl http://localhost:8000/api/products

# Search for products
curl "http://localhost:8000/api/products?search=laptop"

# Get products by category
curl http://localhost:8000/api/products/category/1

# Get specific product
curl http://localhost:8000/api/products/1
```

### 6. Get Product Categories

```bash
curl http://localhost:8000/api/products/categories
```

### 7. Add Product Review

```bash
curl -X POST http://localhost:8000/api/products/1/reviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "rating": 5,
    "comment": "Excellent product! Highly recommended."
  }'
```

### 8. Create an Order

```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      },
      {
        "product_id": 2,
        "quantity": 1
      }
    ],
    "shipping_address_id": 1
  }'
```

**Expected Response:**
```json
{
  "message": "Order created successfully",
  "order": {
    "id": 1,
    "user_id": 1,
    "total_amount": 2699.97,
    "status": "pending",
    "payment_status": "pending",
    "created_at": "2024-01-01T12:00:00.000Z"
  }
}
```

### 9. Get User Orders

```bash
curl http://localhost:8000/api/orders \
  -H "Authorization: Bearer $TOKEN"
```

### 10. Get Order Details

```bash
# Replace 1 with your actual order ID
curl http://localhost:8000/api/orders/1 \
  -H "Authorization: Bearer $TOKEN"
```

### 11. Process Payment

```bash
curl -X POST http://localhost:8000/api/payments/process \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "order_id": 1,
    "amount": 2699.97,
    "payment_method": "credit_card"
  }'
```

**Note:** Payment is simulated with 90% success rate

### 12. Get Payment History

```bash
curl http://localhost:8000/api/payments/transactions \
  -H "Authorization: Bearer $TOKEN"
```

### 13. Add Payment Method

```bash
curl -X POST http://localhost:8000/api/payments/methods \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "type": "credit_card",
    "last_four": "4242",
    "card_brand": "Visa",
    "expiry_month": 12,
    "expiry_year": 2025,
    "is_default": true
  }'
```

### 14. Cancel an Order

```bash
curl -X PUT http://localhost:8000/api/orders/1/cancel \
  -H "Authorization: Bearer $TOKEN"
```

## Testing with Sample Data

The database is pre-populated with sample products. You can view them:

```bash
curl http://localhost:8000/api/products | jq
```

Sample products include:
- Laptop ($999.99)
- Smartphone ($699.99)
- T-Shirt ($19.99)
- Jeans ($49.99)
- Novel ($14.99)
- And more...

## Complete Test Script

Here's a complete bash script to test the entire flow:

```bash
#!/bin/bash

API_URL="http://localhost:8000/api"

echo "1. Registering user..."
REGISTER_RESPONSE=$(curl -s -X POST $API_URL/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "name": "Test User"
  }')

echo $REGISTER_RESPONSE | jq

TOKEN=$(echo $REGISTER_RESPONSE | jq -r '.token')
echo "Token: $TOKEN"

echo -e "\n2. Getting user profile..."
curl -s $API_URL/users/me \
  -H "Authorization: Bearer $TOKEN" | jq

echo -e "\n3. Getting products..."
curl -s $API_URL/products | jq '.products[0:3]'

echo -e "\n4. Creating order..."
ORDER_RESPONSE=$(curl -s -X POST $API_URL/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "items": [
      {"product_id": 1, "quantity": 1},
      {"product_id": 2, "quantity": 1}
    ]
  }')

echo $ORDER_RESPONSE | jq

ORDER_ID=$(echo $ORDER_RESPONSE | jq -r '.order.id')
TOTAL_AMOUNT=$(echo $ORDER_RESPONSE | jq -r '.order.total_amount')

echo -e "\n5. Processing payment..."
curl -s -X POST $API_URL/payments/process \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"order_id\": $ORDER_ID,
    \"amount\": $TOTAL_AMOUNT,
    \"payment_method\": \"credit_card\"
  }" | jq

echo -e "\n6. Getting order details..."
curl -s $API_URL/orders/$ORDER_ID \
  -H "Authorization: Bearer $TOKEN" | jq

echo -e "\nTest completed!"
```

Save this as `test-api.sh`, make it executable with `chmod +x test-api.sh`, and run it!

## Testing Individual Services

### User Service (Direct)
```bash
curl http://localhost:3001/health
```

### Product Service (Direct)
```bash
curl http://localhost:3002/health
curl http://localhost:3002/
```

### Order Service (Direct)
```bash
curl http://localhost:3003/health
```

### Payment Service (Direct)
```bash
curl http://localhost:3004/health
```

### Notification Service (Direct)
```bash
curl http://localhost:3005/health
```

## Debugging

### Check Service Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api-gateway
docker-compose logs -f user-service
docker-compose logs -f product-service
docker-compose logs -f order-service
docker-compose logs -f payment-service
docker-compose logs -f notification-service

# Database logs
docker-compose logs -f postgres
docker-compose logs -f redis
# docker-compose logs -f rabbitmq  # RabbitMQ is disabled
```

### Check Database

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U ecommerce -d ecommerce

# Inside psql:
\dt users.*      # List user service tables
\dt products.*   # List product service tables
\dt orders.*     # List order service tables
\dt payments.*   # List payment service tables

SELECT * FROM products.products;  # View products
SELECT * FROM users.users;        # View users
```

### Check Redis

```bash
docker-compose exec redis redis-cli
# Inside redis-cli:
KEYS *
GET some_key
```

### Check RabbitMQ (Optional - Currently Disabled)

RabbitMQ is available but not currently used. The system uses synchronous REST API communication.

If you need to enable RabbitMQ:
1. Uncomment the rabbitmq service in docker-compose.yml
2. Access RabbitMQ Management UI: http://localhost:15672
   - Username: ecommerce
   - Password: ecommerce123

## API Documentation

Once services are running, access the Swagger documentation:

http://localhost:8000/api-docs

## Troubleshooting

### Services not starting?

```bash
docker-compose down -v
docker-compose up --build
```

### Port conflicts?

Check if ports are already in use:
```bash
lsof -i :8000
lsof -i :3001
lsof -i :3002
# etc.
```

### Database connection issues?

Wait a bit longer for PostgreSQL to initialize:
```bash
docker-compose logs postgres | grep "ready to accept connections"
```

## Production Considerations

When deploying to production:

1. Change all default secrets and passwords
2. Use environment-specific configuration
3. Enable HTTPS/TLS
4. Set up proper monitoring
5. Configure log aggregation
6. Set up database backups
7. Use production-grade message broker
8. Implement proper error tracking
9. Set up CI/CD pipelines
10. Use container orchestration (Kubernetes)

Enjoy testing the E-Commerce Microservices Platform!
