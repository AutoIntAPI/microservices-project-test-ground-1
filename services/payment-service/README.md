# Payment Service

Handles payment processing and transaction management.

## Features

- Payment processing (simulated)
- Transaction management
- Payment method storage
- Refund handling
- Transaction history

## Environment Variables

See `.env.example` for configuration.

## Database Schema

Uses the `payments` schema in PostgreSQL:
- `payments.transactions` - Payment transactions
- `payments.payment_methods` - Saved payment methods
- `payments.refunds` - Refund records

## Running Locally

```bash
pip install -r requirements.txt
flask run --port=3004
```

## API Endpoints

- `POST /process` - Process payment (authenticated)
- `GET /transactions` - Get user transactions (authenticated)
- `GET /transactions/:id` - Get transaction details (authenticated)
- `POST /methods` - Add payment method (authenticated)
- `GET /methods` - Get payment methods (authenticated)

## Payment Simulation

The service simulates payment processing with a 90% success rate. In production, integrate with real payment gateways like Stripe or PayPal.

## Testing

```bash
pytest
```
