# Order Service

Handles order creation, management, and tracking.

## Features

- Order creation
- Order status tracking
- Cart management
- Order history
- Integration with Product and Payment services

## Environment Variables

See `.env.example` for configuration.

## Database Schema

Uses the `orders` schema in PostgreSQL:
- `orders.orders` - Order records
- `orders.order_items` - Order line items
- `orders.order_status_history` - Order status changes

## Running Locally

```bash
pip install -r requirements.txt
flask run --port=3003
```

## API Endpoints

- `GET /` - Get user orders (authenticated)
- `POST /` - Create new order (authenticated)
- `GET /:id` - Get order details (authenticated)
- `PUT /:id/cancel` - Cancel order (authenticated)

## Testing

```bash
pytest
```

## Technology Stack

- Python 3.11
- Flask
- PostgreSQL
- Redis
- RabbitMQ
