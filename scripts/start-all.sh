#!/bin/bash

# Start all microservices

set -e

echo "🚀 Starting all microservices..."

# Start services
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service health
services=("api-gateway:8000" "user-service:3001" "product-service:3002" "order-service:3003" "payment-service:3004" "notification-service:3005")

for service in "${services[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if curl -f http://localhost:$port/health &> /dev/null; then
        echo "  ✅ $name is healthy"
    else
        echo "  ⚠️  $name is not responding"
    fi
done

echo ""
echo "✨ Services are running!"
echo ""
echo "API Gateway: http://localhost:8000"
echo "API Documentation: http://localhost:8000/api-docs"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
