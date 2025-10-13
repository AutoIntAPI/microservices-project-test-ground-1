.PHONY: help setup build start stop restart logs clean test integration-test health

# Default target
help:
	@echo "E-Commerce Microservices - Available Commands"
	@echo "=============================================="
	@echo ""
	@echo "Setup & Build:"
	@echo "  make setup          - Initial setup (copy env files, pull images)"
	@echo "  make build          - Build all Docker images"
	@echo ""
	@echo "Service Management:"
	@echo "  make start          - Start all services"
	@echo "  make stop           - Stop all services"
	@echo "  make restart        - Restart all services"
	@echo "  make dev            - Start services in development mode"
	@echo ""
	@echo "Monitoring:"
	@echo "  make logs           - View logs from all services"
	@echo "  make logs-api       - View API Gateway logs"
	@echo "  make logs-user      - View User Service logs"
	@echo "  make logs-product   - View Product Service logs"
	@echo "  make logs-order     - View Order Service logs"
	@echo "  make logs-payment   - View Payment Service logs"
	@echo "  make logs-notify    - View Notification Service logs"
	@echo "  make health         - Check health of all services"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run all unit tests"
	@echo "  make integration    - Run integration tests"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Stop services and remove volumes"
	@echo "  make clean-all      - Full cleanup including images"
	@echo ""

# Setup
setup:
	@echo "🚀 Setting up E-Commerce Microservices..."
	@./scripts/setup.sh

# Build
build:
	@echo "🔨 Building all services..."
	@docker-compose build

# Start services
start:
	@echo "▶️  Starting all services..."
	@docker-compose up -d
	@echo "✅ Services started!"
	@echo "API Gateway: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/api-docs"

# Stop services
stop:
	@echo "⏸️  Stopping all services..."
	@docker-compose down
	@echo "✅ Services stopped!"

# Restart services
restart: stop start

# Development mode
dev:
	@echo "🔧 Starting services in development mode..."
	@docker-compose -f docker-compose.dev.yml up

# Logs
logs:
	@docker-compose logs -f

logs-api:
	@docker-compose logs -f api-gateway

logs-user:
	@docker-compose logs -f user-service

logs-product:
	@docker-compose logs -f product-service

logs-order:
	@docker-compose logs -f order-service

logs-payment:
	@docker-compose logs -f payment-service

logs-notify:
	@docker-compose logs -f notification-service

logs-db:
	@docker-compose logs -f postgres

logs-redis:
	@docker-compose logs -f redis

# logs-rabbitmq:
# 	@docker-compose logs -f rabbitmq  # DISABLED - RabbitMQ not in use

# Health check
health:
	@echo "🏥 Checking service health..."
	@echo ""
	@echo "API Gateway (8000):"
	@curl -s http://localhost:8000/health | grep -q healthy && echo "  ✅ Healthy" || echo "  ❌ Unhealthy"
	@echo "User Service (3001):"
	@curl -s http://localhost:3001/health | grep -q healthy && echo "  ✅ Healthy" || echo "  ❌ Unhealthy"
	@echo "Product Service (3002):"
	@curl -s http://localhost:3002/health | grep -q healthy && echo "  ✅ Healthy" || echo "  ❌ Unhealthy"
	@echo "Order Service (3003):"
	@curl -s http://localhost:3003/health | grep -q healthy && echo "  ✅ Healthy" || echo "  ❌ Unhealthy"
	@echo "Payment Service (3004):"
	@curl -s http://localhost:3004/health | grep -q healthy && echo "  ✅ Healthy" || echo "  ❌ Unhealthy"
	@echo "Notification Service (3005):"
	@curl -s http://localhost:3005/health | grep -q healthy && echo "  ✅ Healthy" || echo "  ❌ Unhealthy"

# Tests
test:
	@echo "🧪 Running all tests..."
	@./scripts/test-all.sh

integration:
	@echo "🧪 Running integration tests..."
	@./scripts/integration-test.sh

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	@docker-compose down -v
	@echo "✅ Cleanup complete!"

clean-all: clean
	@echo "🧹 Full cleanup (including images)..."
	@docker system prune -af
	@echo "✅ Full cleanup complete!"

# Database
db-shell:
	@docker-compose exec postgres psql -U ecommerce -d ecommerce

db-reset:
	@echo "⚠️  Resetting database..."
	@docker-compose down -v
	@docker-compose up -d postgres
	@sleep 5
	@echo "✅ Database reset complete!"

# Redis
redis-shell:
	@docker-compose exec redis redis-cli

# Quick start (setup, build, start)
quickstart: setup build start
	@echo ""
	@echo "✨ E-Commerce Microservices is ready!"
	@echo ""
	@echo "Try it out:"
	@echo "  curl http://localhost:8000/api/products"
	@echo ""
	@echo "View API docs:"
	@echo "  http://localhost:8000/api-docs"
	@echo ""
	@echo "Run integration tests:"
	@echo "  make integration"
	@echo ""
