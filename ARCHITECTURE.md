# Architecture Documentation

## Overview

This document describes the architecture of the E-Commerce Microservices Platform, designed as a test ground for training AI models on microservices repository projects.

## Architecture Pattern

The platform follows a **Microservices Architecture** pattern with the following key characteristics:

- **Service Independence**: Each service is independently deployable and scalable
- **API Gateway Pattern**: Single entry point for all client requests
- **Database per Service**: Each service manages its own data
- **Event-Driven Communication**: Services communicate asynchronously via message queue
- **Containerization**: All services are containerized with Docker

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Applications                      │
│                    (Web, Mobile, Third-party)                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                         API Gateway (8000)                       │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ - Request Routing                                       │    │
│  │ - Authentication & Authorization (JWT)                 │    │
│  │ - Rate Limiting                                         │    │
│  │ - Request Validation                                    │    │
│  │ - Response Aggregation                                  │    │
│  │ - Load Balancing                                        │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        │                    │                    │
┌───────▼────────┐  ┌───────▼────────┐  ┌───────▼────────┐
│  User Service  │  │Product Service │  │ Order Service  │
│    (3001)      │  │    (3002)      │  │    (3003)      │
│                │  │                │  │                │
│  - User Mgmt   │  │  - Catalog     │  │  - Order Mgmt  │
│  - Auth/Login  │  │  - Inventory   │  │  - Cart        │
│  - Addresses   │  │  - Categories  │  │  - Status      │
│                │  │  - Reviews     │  │                │
└────────┬───────┘  └────────┬───────┘  └────────┬───────┘
         │                   │                   │
         │                   │                   │
┌────────▼────────┐  ┌───────▼────────┐
│Payment Service  │  │Notification Svc│
│    (3004)       │  │    (3005)      │
│                 │  │                │
│  - Payments     │  │  - Emails      │
│  - Refunds      │  │  - Events      │
│  - Methods      │  │  - Webhooks    │
└────────┬────────┘  └────────┬───────┘
         │                    │
         └──────────┬─────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
┌───▼────┐    ┌────▼─────┐   ┌────▼──────┐
│PostgreSQL│    │  Redis   │   │ RabbitMQ  │
│  (5432) │    │  (6379)  │   │  (5672)   │
└─────────┘    └──────────┘   └───────────┘
```

## Services Description

### 1. API Gateway (Node.js/Express)

**Responsibilities:**
- Single entry point for all client requests
- Request routing to appropriate microservices
- JWT token validation and authentication
- Rate limiting and throttling
- Request/response transformation
- API documentation (Swagger UI)
- Circuit breaking and retry logic

**Technology Stack:**
- Runtime: Node.js 18
- Framework: Express.js
- Proxy: http-proxy-middleware
- Auth: jsonwebtoken
- Documentation: swagger-ui-express

**Port:** 8000

### 2. User Service (Node.js/Express)

**Responsibilities:**
- User registration and authentication
- JWT token generation
- User profile management
- Address management
- Password hashing (bcrypt)

**Technology Stack:**
- Runtime: Node.js 18
- Framework: Express.js
- Database: PostgreSQL (users schema)
- Cache: Redis
- Auth: bcryptjs, jsonwebtoken

**Port:** 3001

**Database Schema:**
- `users.users`: User accounts
- `users.addresses`: User addresses

### 3. Product Service (Node.js/Express)

**Responsibilities:**
- Product catalog management
- Category management
- Product search and filtering
- Inventory tracking
- Product reviews

**Technology Stack:**
- Runtime: Node.js 18
- Framework: Express.js
- Database: PostgreSQL (products schema)
- Cache: Redis

**Port:** 3002

**Database Schema:**
- `products.products`: Product catalog
- `products.categories`: Product categories
- `products.reviews`: Product reviews
- `products.product_images`: Product images

### 4. Order Service (Python/Flask)

**Responsibilities:**
- Order creation and management
- Order status tracking
- Cart management
- Order history
- Order validation

**Technology Stack:**
- Runtime: Python 3.11
- Framework: Flask
- Database: PostgreSQL (orders schema)
- Cache: Redis
- Message Queue: RabbitMQ (pika)

**Port:** 3003

**Database Schema:**
- `orders.orders`: Order records
- `orders.order_items`: Order line items
- `orders.order_status_history`: Order status changes

**External Dependencies:**
- Product Service (for product validation)
- Payment Service (for payment processing)
- User Service (for user validation)

### 5. Payment Service (Python/Flask)

**Responsibilities:**
- Payment processing (simulated)
- Transaction management
- Payment method storage
- Refund handling
- Transaction history

**Technology Stack:**
- Runtime: Python 3.11
- Framework: Flask
- Database: PostgreSQL (payments schema)
- Cache: Redis
- Message Queue: RabbitMQ

**Port:** 3004

**Database Schema:**
- `payments.transactions`: Payment transactions
- `payments.payment_methods`: Saved payment methods
- `payments.refunds`: Refund records

**Payment Processing:**
- Simulated gateway (90% success rate)
- In production: Integrate with Stripe, PayPal, etc.

### 6. Notification Service (Python/Flask)

**Responsibilities:**
- Email notifications
- Event-driven notifications
- Welcome emails
- Order confirmations
- Payment confirmations

**Technology Stack:**
- Runtime: Python 3.11
- Framework: Flask
- Cache: Redis
- Message Queue: RabbitMQ
- Email: SMTP (simulated)

**Port:** 3005

**Notification Types:**
- User registration (welcome email)
- Order confirmation
- Payment confirmation
- Custom notifications

## Data Layer

### PostgreSQL

**Purpose:** Primary data store for all services

**Schemas:**
- `users`: User service data
- `products`: Product service data
- `orders`: Order service data
- `payments`: Payment service data

**Characteristics:**
- ACID compliance
- Relational data model
- Schema per service (logical separation)
- Indexed for performance

### Redis

**Purpose:** Caching and session storage

**Use Cases:**
- Session management
- API response caching
- Rate limiting counters
- Temporary data storage

### RabbitMQ

**Purpose:** Asynchronous messaging and event bus

**Use Cases:**
- Order notifications
- Payment events
- Email queue
- Service-to-service async communication

**Exchange Types:**
- Direct: For specific routing
- Topic: For pattern-based routing
- Fanout: For broadcasting

## Communication Patterns

### Synchronous Communication (REST)

- **Client → API Gateway**: HTTPS/REST
- **API Gateway → Services**: HTTP/REST
- **Service → Service**: HTTP/REST (when needed)

**Characteristics:**
- Request-response pattern
- Immediate response expected
- Used for queries and commands requiring immediate feedback

### Asynchronous Communication (Message Queue)

- **Service → RabbitMQ → Service**: AMQP
- Event publishing for cross-service updates
- Email notifications

**Characteristics:**
- Fire-and-forget pattern
- Eventual consistency
- Decoupled services
- Resilient to service failures

## Security

### Authentication

- **JWT (JSON Web Tokens)**: Stateless authentication
- **Token Expiry**: 24 hours (configurable)
- **Password Hashing**: bcrypt with salt rounds

### Authorization

- **Role-Based Access Control (RBAC)**
- Roles: customer, admin
- Enforced at API Gateway and service level

### Network Security

- **API Gateway**: Single entry point
- **Service Isolation**: Services not directly accessible
- **Environment Variables**: Secrets stored in env vars
- **HTTPS**: In production (TLS/SSL)

### Best Practices

- Input validation on all endpoints
- SQL injection prevention (parameterized queries)
- XSS protection
- CORS configuration
- Rate limiting

## Scalability

### Horizontal Scaling

Each service can be scaled independently:

```yaml
docker-compose up --scale user-service=3 --scale product-service=2
```

### Load Balancing

- API Gateway handles load distribution
- Docker Compose automatic service discovery
- In production: Kubernetes or cloud load balancers

### Database Scaling

- Read replicas for PostgreSQL
- Redis clustering
- Connection pooling

## Resilience

### Health Checks

Each service exposes `/health` endpoint:
- Database connectivity
- Service status
- Uptime information

### Circuit Breaker

API Gateway implements circuit breaker pattern:
- Prevents cascading failures
- Automatic retry with backoff
- Service degradation

### Graceful Shutdown

All services handle SIGTERM:
- Complete in-flight requests
- Close database connections
- Clean resource cleanup

## Monitoring and Logging

### Logging

- **Structured Logging**: JSON format
- **Log Levels**: DEBUG, INFO, WARN, ERROR
- **Centralized**: All logs to stdout/stderr
- **Log Aggregation**: Can be integrated with ELK stack

### Metrics

Each service can expose:
- `/metrics`: Prometheus format
- Request count
- Response time
- Error rate
- Custom business metrics

### Health Monitoring

- Docker health checks
- Service-level health endpoints
- Database connectivity checks

## Deployment

### Development

```bash
docker-compose -f docker-compose.dev.yml up
```

Features:
- Hot reload
- Debug ports exposed
- Volume mounts for code

### Production

```bash
docker-compose up -d
```

Features:
- Optimized images
- Multi-stage builds
- Health checks
- Restart policies

### CI/CD

GitHub Actions workflow:
1. Lint code
2. Run unit tests
3. Build Docker images
4. Run integration tests
5. Push to registry
6. Deploy to environment

## Future Enhancements

1. **Service Mesh**: Istio or Linkerd
2. **Kubernetes**: Production orchestration
3. **gRPC**: For service-to-service communication
4. **GraphQL**: Alternative API layer
5. **Saga Pattern**: Distributed transactions
6. **CQRS**: Command Query Responsibility Segregation
7. **Event Sourcing**: Event-based state management
8. **API Versioning**: Support multiple API versions
9. **WebSockets**: Real-time updates
10. **Metrics Dashboard**: Grafana + Prometheus

## Design Patterns Used

1. **API Gateway Pattern**: Centralized entry point
2. **Database per Service**: Service autonomy
3. **Circuit Breaker**: Fault tolerance
4. **Service Registry**: Service discovery
5. **Event-Driven**: Asynchronous communication
6. **CQRS**: Command Query separation (partial)
7. **Retry Pattern**: Transient fault handling
8. **Health Check Pattern**: Service monitoring

## Technology Decisions

### Why Node.js for API Gateway and User/Product Services?

- Fast I/O operations
- Large ecosystem
- Non-blocking architecture
- Good for API services

### Why Python for Order/Payment/Notification Services?

- Excellent for business logic
- Rich libraries
- Easy integration with external services
- Good for data processing

### Why PostgreSQL?

- ACID compliance
- Complex queries support
- JSON support
- Mature and reliable

### Why Redis?

- Fast in-memory operations
- Excellent for caching
- Session management
- Rate limiting

### Why RabbitMQ?

- Reliable message delivery
- Flexible routing
- Easy to set up
- Good documentation

## Conclusion

This architecture provides a solid foundation for a production-grade e-commerce platform while serving as an excellent test ground for AI model training on microservices patterns, best practices, and real-world scenarios.
