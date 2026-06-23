from app.models.db import execute_query, execute_one
import os
import requests

# Adjust product-service response schema: map 'item' to 'product' for compatibility
_PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://product-service:3002')
_original_requests_get = requests.get

def _patched_requests_get(url, *args, **kwargs):
    resp = _original_requests_get(url, *args, **kwargs)
    try:
        if url.startswith(_PRODUCT_SERVICE_URL):
            data = resp.json()
            if isinstance(data, dict) and 'product' not in data and 'item' in data:
                # expose product key for downstream code
                resp.json = lambda: {'product': data['item']}
    except Exception:
        pass
    return resp

# Apply monkey-patch
requests.get = _patched_requests_get

class Order:
    @staticmethod
    def create(user_id, items, total_amount, shipping_address_id):
        # Create order
        order_query = """
            INSERT INTO orders.orders (user_id, total_amount, shipping_address_id, status, payment_status)
            VALUES (%s, %s, %s, 'pending', 'pending')
            RETURNING *
        """
        order = execute_one(order_query, (user_id, total_amount, shipping_address_id))
        
        # Add order items
        for item in items:
            item_query = """
                INSERT INTO orders.order_items 
                (order_id, product_id, product_name, quantity, unit_price, subtotal)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            execute_query(
                item_query,
                (order['id'], item['product_id'], item['product_name'], 
                 item['quantity'], item['unit_price'], item['subtotal']),
                fetch=False
            )
        
        # Add status history
        status_query = """
            INSERT INTO orders.order_status_history (order_id, status, notes)
            VALUES (%s, 'pending', 'Order created')
        """
        execute_query(status_query, (order['id'],), fetch=False)
        
        return order

    @staticmethod
    def get_by_user(user_id, limit=50, offset=0):
        query = """
            SELECT * FROM orders.orders 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        return execute_query(query, (user_id, limit, offset))

    @staticmethod
    def get_by_id(order_id):
        query = "SELECT * FROM orders.orders WHERE id = %s"
        return execute_one(query, (order_id,))

    @staticmethod
    def get_items(order_id):
        query = "SELECT * FROM orders.order_items WHERE order_id = %s"
        return execute_query(query, (order_id,))

    @staticmethod
    def update_status(order_id, status, notes=None):
        # Update order status
        update_query = """
            UPDATE orders.orders 
            SET status = %s, updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s
            RETURNING *
        """
        order = execute_one(update_query, (status, order_id))
        
        # Add to status history
        history_query = """
            INSERT INTO orders.order_status_history (order_id, status, notes)
            VALUES (%s, %s, %s)
        """
        execute_query(history_query, (order_id, status, notes), fetch=False)
        
        return order

    @staticmethod
    def update_payment_status(order_id, payment_status):
        query = """
            UPDATE orders.orders 
            SET payment_status = %s, updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s
            RETURNING *
        """
        return execute_one(query, (payment_status, order_id))
