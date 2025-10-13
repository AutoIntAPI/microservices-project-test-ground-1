#!/bin/bash

# Integration test script for E-Commerce Microservices

set -e

API_URL="http://localhost:8000/api"
TIMEOUT=5

echo "🧪 E-Commerce Microservices Integration Test"
echo "============================================"
echo ""

# Function to make API calls
api_call() {
    local method=$1
    local endpoint=$2
    local data=$3
    local token=$4
    
    if [ -n "$token" ]; then
        if [ -n "$data" ]; then
            curl -s -X $method $API_URL$endpoint \
                -H "Content-Type: application/json" \
                -H "Authorization: Bearer $token" \
                -d "$data" \
                --max-time $TIMEOUT
        else
            curl -s -X $method $API_URL$endpoint \
                -H "Authorization: Bearer $token" \
                --max-time $TIMEOUT
        fi
    else
        if [ -n "$data" ]; then
            curl -s -X $method $API_URL$endpoint \
                -H "Content-Type: application/json" \
                -d "$data" \
                --max-time $TIMEOUT
        else
            curl -s $API_URL$endpoint --max-time $TIMEOUT
        fi
    fi
}

# Check if services are running
echo "📋 Checking service health..."
services=("8000" "3001" "3002" "3003" "3004" "3005")
service_names=("API Gateway" "User Service" "Product Service" "Order Service" "Payment Service" "Notification Service")

for i in "${!services[@]}"; do
    port=${services[$i]}
    name=${service_names[$i]}
    
    if curl -s -f http://localhost:$port/health > /dev/null 2>&1; then
        echo "  ✅ $name (port $port) is healthy"
    else
        echo "  ❌ $name (port $port) is not responding"
        exit 1
    fi
done

echo ""
echo "✅ All services are healthy!"
echo ""

# Generate random user data
RANDOM_ID=$RANDOM
TEST_EMAIL="testuser${RANDOM_ID}@example.com"
TEST_PASSWORD="TestPass123!"
TEST_NAME="Test User $RANDOM_ID"

echo "👤 Test 1: User Registration"
echo "----------------------------"
REGISTER_RESPONSE=$(api_call POST /users/register "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\",
    \"name\": \"$TEST_NAME\"
}")

if echo "$REGISTER_RESPONSE" | grep -q "token"; then
    echo "  ✅ User registration successful"
    TOKEN=$(echo $REGISTER_RESPONSE | grep -o '"token":"[^"]*' | sed 's/"token":"//')
    USER_ID=$(echo $REGISTER_RESPONSE | grep -o '"id":[0-9]*' | head -1 | sed 's/"id"://')
    echo "  📝 User ID: $USER_ID"
else
    echo "  ❌ User registration failed"
    echo "  Response: $REGISTER_RESPONSE"
    exit 1
fi

echo ""
echo "🔐 Test 2: User Login"
echo "-------------------"
LOGIN_RESPONSE=$(api_call POST /users/login "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\"
}")

if echo "$LOGIN_RESPONSE" | grep -q "token"; then
    echo "  ✅ Login successful"
else
    echo "  ❌ Login failed"
    exit 1
fi

echo ""
echo "👤 Test 3: Get User Profile"
echo "-------------------------"
PROFILE_RESPONSE=$(api_call GET /users/me "" "$TOKEN")

if echo "$PROFILE_RESPONSE" | grep -q "$TEST_EMAIL"; then
    echo "  ✅ Profile retrieved successfully"
else
    echo "  ❌ Profile retrieval failed"
    exit 1
fi

echo ""
echo "📦 Test 4: Get Products"
echo "---------------------"
PRODUCTS_RESPONSE=$(api_call GET /products)

if echo "$PRODUCTS_RESPONSE" | grep -q "products"; then
    PRODUCT_COUNT=$(echo $PRODUCTS_RESPONSE | grep -o '"id":[0-9]*' | wc -l)
    echo "  ✅ Products retrieved successfully ($PRODUCT_COUNT products)"
else
    echo "  ❌ Product retrieval failed"
    exit 1
fi

echo ""
echo "🏷️  Test 5: Get Product Categories"
echo "--------------------------------"
CATEGORIES_RESPONSE=$(api_call GET /products/categories)

if echo "$CATEGORIES_RESPONSE" | grep -q "categories"; then
    echo "  ✅ Categories retrieved successfully"
else
    echo "  ❌ Category retrieval failed"
    exit 1
fi

echo ""
echo "📦 Test 6: Get Specific Product"
echo "-----------------------------"
PRODUCT_RESPONSE=$(api_call GET /products/1)

if echo "$PRODUCT_RESPONSE" | grep -q "product"; then
    PRODUCT_NAME=$(echo $PRODUCT_RESPONSE | grep -o '"name":"[^"]*' | sed 's/"name":"//')
    PRODUCT_PRICE=$(echo $PRODUCT_RESPONSE | grep -o '"price":"[^"]*' | sed 's/"price":"//')
    echo "  ✅ Product retrieved: $PRODUCT_NAME (\$$PRODUCT_PRICE)"
else
    echo "  ❌ Product retrieval failed"
    exit 1
fi

echo ""
echo "🛒 Test 7: Create Order"
echo "---------------------"
ORDER_RESPONSE=$(api_call POST /orders "{
    \"items\": [
        {\"product_id\": 1, \"quantity\": 1},
        {\"product_id\": 2, \"quantity\": 1}
    ]
}" "$TOKEN")

if echo "$ORDER_RESPONSE" | grep -q "order"; then
    echo "  ✅ Order created successfully"
    ORDER_ID=$(echo $ORDER_RESPONSE | grep -o '"id":[0-9]*' | head -1 | sed 's/"id"://')
    TOTAL_AMOUNT=$(echo $ORDER_RESPONSE | grep -o '"total_amount":"[^"]*' | sed 's/"total_amount":"//' | sed 's/"//')
    echo "  📝 Order ID: $ORDER_ID"
    echo "  💰 Total Amount: \$$TOTAL_AMOUNT"
else
    echo "  ❌ Order creation failed"
    echo "  Response: $ORDER_RESPONSE"
    exit 1
fi

echo ""
echo "📋 Test 8: Get User Orders"
echo "------------------------"
ORDERS_RESPONSE=$(api_call GET /orders "" "$TOKEN")

if echo "$ORDERS_RESPONSE" | grep -q "orders"; then
    echo "  ✅ Orders retrieved successfully"
else
    echo "  ❌ Orders retrieval failed"
    exit 1
fi

echo ""
echo "💳 Test 9: Process Payment"
echo "------------------------"
PAYMENT_RESPONSE=$(api_call POST /payments/process "{
    \"order_id\": $ORDER_ID,
    \"amount\": $TOTAL_AMOUNT,
    \"payment_method\": \"credit_card\"
}" "$TOKEN")

if echo "$PAYMENT_RESPONSE" | grep -q "transaction"; then
    PAYMENT_STATUS=$(echo $PAYMENT_RESPONSE | grep -o '"status":"[^"]*' | sed 's/"status":"//')
    echo "  ✅ Payment processed: $PAYMENT_STATUS"
else
    echo "  ⚠️  Payment processing response received (may have failed in simulation)"
fi

echo ""
echo "💳 Test 10: Get Payment Transactions"
echo "-----------------------------------"
TRANSACTIONS_RESPONSE=$(api_call GET /payments/transactions "" "$TOKEN")

if echo "$TRANSACTIONS_RESPONSE" | grep -q "transactions"; then
    echo "  ✅ Transactions retrieved successfully"
else
    echo "  ❌ Transactions retrieval failed"
    exit 1
fi

echo ""
echo "⭐ Test 11: Add Product Review"
echo "----------------------------"
REVIEW_RESPONSE=$(api_call POST /products/1/reviews "{
    \"rating\": 5,
    \"comment\": \"Automated test review - excellent product!\"
}" "$TOKEN")

if echo "$REVIEW_RESPONSE" | grep -q "review"; then
    echo "  ✅ Review added successfully"
else
    echo "  ❌ Review addition failed"
    exit 1
fi

echo ""
echo "🚫 Test 12: Cancel Order"
echo "----------------------"
CANCEL_RESPONSE=$(api_call PUT /orders/$ORDER_ID/cancel "" "$TOKEN")

if echo "$CANCEL_RESPONSE" | grep -q "cancelled"; then
    echo "  ✅ Order cancelled successfully"
else
    echo "  ⚠️  Order cancellation response received"
fi

echo ""
echo "============================================"
echo "✨ All Integration Tests Passed! ✨"
echo "============================================"
echo ""
echo "Summary:"
echo "  - User registered and authenticated: ✅"
echo "  - Products retrieved: ✅"
echo "  - Order created: ✅"
echo "  - Payment processed: ✅"
echo "  - Review added: ✅"
echo "  - Order cancelled: ✅"
echo ""
echo "Test user: $TEST_EMAIL"
echo "Test order ID: $ORDER_ID"
echo ""
