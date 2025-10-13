# API Gateway

Entry point for all client requests to the e-commerce microservices platform.

## Features

- Request routing to microservices
- JWT authentication and authorization
- Rate limiting
- API documentation (Swagger)
- Error handling and logging
- Request/response transformation

## Environment Variables

See `.env.example` for all configuration options.

## Running Locally

```bash
npm install
npm run dev
```

## Running with Docker

```bash
docker build -t api-gateway .
docker run -p 8000:8000 --env-file .env api-gateway
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/api-docs
- Health check: http://localhost:8000/health

## Endpoints

- `GET /health` - Health check
- `POST /api/users/register` - User registration (proxied to user-service)
- `POST /api/users/login` - User login (proxied to user-service)
- `GET /api/products` - Get products (proxied to product-service)
- `POST /api/orders` - Create order (proxied to order-service)
- And more...

## Testing

```bash
npm test
```

## Technology Stack

- Node.js 18
- Express.js
- http-proxy-middleware
- jsonwebtoken
- redis
- winston (logging)
