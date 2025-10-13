# Notification Service

Handles notifications via email and other channels.

## Features

- Email notifications
- Event-driven notifications
- Welcome emails
- Order confirmations
- Payment confirmations
- Batch notifications

## Environment Variables

See `.env.example` for configuration.

## Running Locally

```bash
pip install -r requirements.txt
flask run --port=3005
```

## API Endpoints

- `POST /send` - Send notification
- `POST /batch` - Send batch notifications

## Notification Types

- `welcome` - Welcome email for new users
- `order_confirmation` - Order confirmation email
- `payment_confirmation` - Payment confirmation email
- `custom` - Custom notification

## Email Simulation

The service simulates email sending. In production, integrate with SMTP servers or services like SendGrid, Mailgun, or AWS SES.

## Testing

```bash
pytest
```

## Technology Stack

- Python 3.11
- Flask
- Redis
- RabbitMQ
