# E-Commerce Microservices Project Test Ground

A comprehensive microservices-based e-commerce application built with best practices for training AI models on microservices repository projects. This monorepo demonstrates modern microservices architecture, containerization, orchestration, and CI/CD pipelines.

## Architecture Overview

This project implements a microservices architecture for an e-commerce platform with the following services:

```
┌─────────────────────────────────────────────────────────────┐
│                         API Gateway                          │
│                    (Port: 8000)                              │
└────────────┬────────────────────────────────────────────────┘
             │
    ┌────────┴────────┬────────────┬───────────┬──────────────┐
    │                 │            │           │              │
┌───▼────┐    ┌──────▼─────┐  ┌──▼─────┐  ┌──▼────┐   ┌────▼──────┐
│ User   │    │  Product   │  │ Order  │  │Payment│   │Notification│
│Service │    │  Service   │  │Service │  │Service│   │  Service   │
│(3001)  │    │   (3002)   │  │ (3003) │  │(3004) │   │   (3005)   │
└───┬────┘    └──────┬─────┘  └───┬────┘  └───┬───┘   └────┬───────┘
    │                │            │            │            │
    └────────┬───────┴────────────┴────────────┴────────────┘
             │
    ┌────────▼─────────┐      ┌──────────────┐
    │    PostgreSQL    │      │    Redis     │
    │    (Port: 5432)  │      │ (Port: 6379) │
    └──────────────────┘      └──────────────┘
```

## Services

### 1. API Gateway (Port 8000)
- Entry point for all client requests
- Route management and load balancing
- Authentication and authorization
- Rate limiting and request validation

### 2. User Service (Port 3001)
- User registration and authentication
- User profile management
- JWT token generation and validation
- Password hashing and security

### 3. Product Service (Port 3002)
- Product catalog management
- Product search and filtering
- Inventory management
- Product categories and tags

### 4. Order Service (Port 3003)
- Order creation and management
- Order status tracking
- Cart management
- Order history

### 5. Payment Service (Port 3004)
- Payment processing simulation
- Payment method management
- Transaction history
- Refund handling

### 6. Notification Service (Port 3005)
- Email notifications
- Order confirmation emails (triggered by Order Service)
- Payment confirmation emails (triggered by Payment Service)
- User registration emails
- REST API-based notifications

## Technology Stack

- **Languages**: Python (Flask), Node.js (Express)
- **Databases**: PostgreSQL, Redis
- **Communication**: Synchronous REST API calls (HTTP/JSON)
- **Containerization**: Docker, Docker Compose
- **API Gateway**: Node.js/Express
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus, Grafana (configuration included)

## Communication Pattern

This project uses **synchronous REST API communication** between microservices:
- All services communicate via HTTP REST APIs
- Order Service → Product Service (product validation)
- Order Service → Notification Service (order confirmations)
- Payment Service → Notification Service (payment confirmations)
- API Gateway → All Services (request routing)

RabbitMQ infrastructure is available but not currently used, allowing for future async patterns if needed.

## Project Structure

```
.
├── services/
│   ├── api-gateway/          # API Gateway service
│   ├── user-service/         # User management service
│   ├── product-service/      # Product catalog service
│   ├── order-service/        # Order management service
│   ├── payment-service/      # Payment processing service
│   └── notification-service/ # Notification service
├── shared/
│   ├── proto/                # Protocol buffers (if using gRPC)
│   ├── utils/                # Shared utilities
│   └── config/               # Shared configuration
├── infrastructure/
│   ├── docker/               # Docker configurations
│   └── k8s/                  # Kubernetes manifests (optional)
├── scripts/
│   ├── setup.sh              # Setup script
│   ├── start-all.sh          # Start all services
│   └── test-all.sh           # Run all tests
├── .github/
│   └── workflows/            # CI/CD pipelines
├── docker-compose.yml        # Docker Compose orchestration
├── docker-compose.dev.yml    # Development environment
└── README.md                 # This file
```

## Prerequisites

- Docker (v20.10+)
- Docker Compose (v2.0+)
- Node.js (v16+) - for local development
- Python (v3.9+) - for local development
- Git

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/AutoIntAPI/microservices-project-test-ground.git
cd microservices-project-test-ground
```

### 2. Start all services with Docker Compose

```bash
# Start all services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### 3. Access the services

- API Gateway: http://localhost:8000
- User Service: http://localhost:3001
- Product Service: http://localhost:3002
- Order Service: http://localhost:3003
- Payment Service: http://localhost:3004
- Notification Service: http://localhost:3005

### 4. Test the API

```bash
# Register a new user
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123", "name": "John Doe"}'

# Login
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Get products
curl http://localhost:8000/api/products

# Create an order (requires authentication token)
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"items": [{"product_id": 1, "quantity": 2}]}'
```

## Development

### Running services individually

Each service can be run independently for development:

```bash
# User Service
cd services/user-service
npm install  # or pip install -r requirements.txt
npm run dev  # or python app.py

# Product Service
cd services/product-service
npm install
npm run dev

# And so on for other services...
```

### Running tests

```bash
# Run all tests
./scripts/test-all.sh

# Run tests for a specific service
cd services/user-service
npm test  # or pytest
```

### Database migrations

```bash
# Run migrations for all services
docker-compose exec user-service npm run migrate
docker-compose exec product-service npm run migrate
docker-compose exec order-service npm run migrate
```

## CI/CD Pipeline

The project includes GitHub Actions workflows for:

- **Continuous Integration**: Automated testing on push/PR
- **Code Quality**: Linting and code style checks
- **Docker Build**: Build and push Docker images
- **Deployment**: Automated deployment to staging/production

Workflow files are located in `.github/workflows/`.

## API Documentation

API documentation is available at:
- Swagger UI: http://localhost:8000/api-docs
- Each service also exposes its own API docs at `/api-docs`

## Environment Variables

Each service requires specific environment variables. Example `.env` files are provided in each service directory as `.env.example`.

Key environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `JWT_SECRET`: Secret for JWT token generation
- `SERVICE_PORT`: Port for the service to listen on
- `NOTIFICATION_SERVICE_URL`: Notification service URL (for order/payment services)
- `PRODUCT_SERVICE_URL`: Product service URL (for order service)
- `USER_SERVICE_URL`: User service URL (for API gateway)

## Monitoring and Logging

- **Logs**: All services log to stdout/stderr (accessible via `docker-compose logs`)
- **Prometheus**: Metrics endpoint available at each service's `/metrics` endpoint
- **Health Checks**: Each service exposes a `/health` endpoint

## Best Practices Implemented

1. **Containerization**: Each service has its own Dockerfile
2. **Service Independence**: Each service has its own database schema
3. **API Gateway Pattern**: Centralized entry point
4. **Environment Configuration**: Environment-based configuration
5. **Health Checks**: Kubernetes-ready health check endpoints
6. **Graceful Shutdown**: Proper signal handling
7. **Logging**: Structured logging with log levels
8. **Error Handling**: Consistent error response format
9. **Security**: JWT authentication, password hashing, input validation
10. **Testing**: Unit and integration tests for each service
11. **Documentation**: API documentation with Swagger/OpenAPI
12. **CI/CD**: Automated testing and deployment pipelines

## Contributing

This is a test ground project for training AI models. Contributions are welcome to add more features, improve architecture, or enhance documentation.

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please open an issue on GitHub.