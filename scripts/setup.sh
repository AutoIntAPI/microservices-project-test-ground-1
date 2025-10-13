#!/bin/bash

# Setup script for the microservices project

set -e

echo "🚀 Setting up E-Commerce Microservices Project..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create .env files from examples if they don't exist
echo "📝 Creating environment files..."

for service in api-gateway user-service product-service order-service payment-service notification-service; do
    if [ -f "services/$service/.env.example" ] && [ ! -f "services/$service/.env" ]; then
        cp "services/$service/.env.example" "services/$service/.env"
        echo "  ✓ Created .env for $service"
    fi
done

# Pull required Docker images
echo "📦 Pulling Docker images..."
docker-compose pull postgres redis rabbitmq

# Build services
echo "🔨 Building services..."
docker-compose build

echo ""
echo "✨ Setup complete!"
echo ""
echo "To start all services, run:"
echo "  docker-compose up -d"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop all services:"
echo "  docker-compose down"
