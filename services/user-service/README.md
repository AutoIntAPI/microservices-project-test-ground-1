# User Service

Handles user management, authentication, and authorization.

## Features

- User registration
- User login with JWT
- Password hashing with bcrypt
- Profile management
- Address management
- Role-based access control

## Environment Variables

See `.env.example` for configuration.

## Database Schema

Uses the `users` schema in PostgreSQL:
- `users.users` - User accounts
- `users.addresses` - User addresses

## Running Locally

```bash
npm install
npm run dev
```

## API Endpoints

- `POST /register` - Register new user
- `POST /login` - Login user
- `GET /me` - Get user profile (authenticated)
- `PUT /me` - Update user profile (authenticated)
- `GET /me/addresses` - Get user addresses (authenticated)
- `POST /me/addresses` - Add user address (authenticated)

## Testing

```bash
npm test
```
