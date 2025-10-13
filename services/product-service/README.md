# Product Service

Manages product catalog, categories, and reviews.

## Features

- Product catalog management
- Category management
- Product search and filtering
- Product reviews
- Inventory tracking

## Environment Variables

See `.env.example` for configuration.

## Database Schema

Uses the `products` schema in PostgreSQL:
- `products.products` - Product catalog
- `products.categories` - Product categories
- `products.reviews` - Product reviews
- `products.product_images` - Product images

## Running Locally

```bash
npm install
npm run dev
```

## API Endpoints

- `GET /` - Get all products (with filtering)
- `GET /categories` - Get all categories
- `GET /:id` - Get product by ID
- `GET /category/:categoryId` - Get products by category
- `GET /:id/reviews` - Get product reviews
- `POST /:id/reviews` - Add product review (authenticated)

## Testing

```bash
npm test
```
