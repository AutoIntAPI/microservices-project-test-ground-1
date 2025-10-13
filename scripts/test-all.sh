#!/bin/bash

# Run tests for all services

set -e

echo "🧪 Running tests for all services..."

# Test Node.js services
node_services=("api-gateway" "user-service" "product-service")

for service in "${node_services[@]}"; do
    echo ""
    echo "Testing $service..."
    cd "services/$service"
    npm install
    npm test || echo "⚠️  Tests failed for $service"
    cd ../..
done

# Test Python services
python_services=("order-service" "payment-service" "notification-service")

for service in "${python_services[@]}"; do
    echo ""
    echo "Testing $service..."
    cd "services/$service"
    pip install -r requirements.txt
    pip install pytest
    pytest || echo "⚠️  Tests failed for $service"
    cd ../..
done

echo ""
echo "✨ All tests completed!"
