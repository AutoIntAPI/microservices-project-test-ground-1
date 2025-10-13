-- Database initialization script for e-commerce microservices

-- Create schemas for each service
CREATE SCHEMA IF NOT EXISTS users;
CREATE SCHEMA IF NOT EXISTS products;
CREATE SCHEMA IF NOT EXISTS orders;
CREATE SCHEMA IF NOT EXISTS payments;

-- Users Service Tables
CREATE TABLE IF NOT EXISTS users.users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(50) DEFAULT 'customer'
);

CREATE TABLE IF NOT EXISTS users.addresses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users.users(id) ON DELETE CASCADE,
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    country VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products Service Tables
CREATE TABLE IF NOT EXISTS products.categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    parent_id INTEGER REFERENCES products.categories(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products.products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    category_id INTEGER REFERENCES products.categories(id) ON DELETE SET NULL,
    stock_quantity INTEGER DEFAULT 0,
    image_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products.product_images (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products.products(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products.reviews (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products.products(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders Service Tables
CREATE TABLE IF NOT EXISTS orders.orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    shipping_address_id INTEGER,
    payment_method VARCHAR(50),
    payment_status VARCHAR(50) DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders.order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders.orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders.order_status_history (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders.orders(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payments Service Tables
CREATE TABLE IF NOT EXISTS payments.transactions (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    payment_method VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    transaction_id VARCHAR(255) UNIQUE,
    gateway_response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payments.payment_methods (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    type VARCHAR(50) NOT NULL,
    last_four VARCHAR(4),
    card_brand VARCHAR(50),
    expiry_month INTEGER,
    expiry_year INTEGER,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payments.refunds (
    id SERIAL PRIMARY KEY,
    transaction_id INTEGER REFERENCES payments.transactions(id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL,
    reason TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users.users(email);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users.users(created_at);
CREATE INDEX IF NOT EXISTS idx_addresses_user_id ON users.addresses(user_id);

CREATE INDEX IF NOT EXISTS idx_products_category_id ON products.products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_sku ON products.products(sku);
CREATE INDEX IF NOT EXISTS idx_products_name ON products.products(name);
CREATE INDEX IF NOT EXISTS idx_reviews_product_id ON products.reviews(product_id);

CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders.orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders.orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders.orders(created_at);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON orders.order_items(order_id);

CREATE INDEX IF NOT EXISTS idx_transactions_order_id ON payments.transactions(order_id);
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON payments.transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_status ON payments.transactions(status);
CREATE INDEX IF NOT EXISTS idx_payment_methods_user_id ON payments.payment_methods(user_id);

-- Insert sample data for testing

-- Sample Categories
INSERT INTO products.categories (name, description) VALUES
    ('Electronics', 'Electronic devices and accessories'),
    ('Clothing', 'Apparel and fashion items'),
    ('Books', 'Books and publications'),
    ('Home & Garden', 'Home improvement and gardening'),
    ('Sports', 'Sports equipment and accessories')
ON CONFLICT (name) DO NOTHING;

-- Sample Products
INSERT INTO products.products (name, description, price, sku, category_id, stock_quantity, image_url) VALUES
    ('Laptop', 'High-performance laptop', 999.99, 'LAPTOP-001', 1, 50, 'https://example.com/laptop.jpg'),
    ('Smartphone', 'Latest smartphone model', 699.99, 'PHONE-001', 1, 100, 'https://example.com/phone.jpg'),
    ('T-Shirt', 'Comfortable cotton t-shirt', 19.99, 'TSHIRT-001', 2, 200, 'https://example.com/tshirt.jpg'),
    ('Jeans', 'Classic blue jeans', 49.99, 'JEANS-001', 2, 150, 'https://example.com/jeans.jpg'),
    ('Novel', 'Bestselling fiction book', 14.99, 'BOOK-001', 3, 75, 'https://example.com/book.jpg'),
    ('Garden Tools Set', 'Complete gardening tools', 89.99, 'GARDEN-001', 4, 30, 'https://example.com/garden.jpg'),
    ('Tennis Racket', 'Professional tennis racket', 129.99, 'TENNIS-001', 5, 40, 'https://example.com/racket.jpg'),
    ('Wireless Mouse', 'Ergonomic wireless mouse', 29.99, 'MOUSE-001', 1, 120, 'https://example.com/mouse.jpg'),
    ('Yoga Mat', 'Non-slip yoga mat', 34.99, 'YOGA-001', 5, 80, 'https://example.com/yoga.jpg'),
    ('Coffee Maker', 'Automatic coffee maker', 79.99, 'COFFEE-001', 4, 60, 'https://example.com/coffee.jpg')
ON CONFLICT (sku) DO NOTHING;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA users TO ecommerce;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA users TO ecommerce;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA products TO ecommerce;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA products TO ecommerce;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA orders TO ecommerce;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA orders TO ecommerce;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA payments TO ecommerce;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA payments TO ecommerce;
