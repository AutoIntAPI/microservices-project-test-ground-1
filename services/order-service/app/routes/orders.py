from flask import Blueprint, request, jsonify
from app.models.order import Order
from app.utils.logger import logger
import requests
import os

bp = Blueprint('orders', __name__)

PRODUCT_SERVICE_URL = os.getenv('PRODUCT_SERVICE_URL', 'http://product-service:3002')
PAYMENT_SERVICE_URL = os.getenv('PAYMENT_SERVICE_URL', 'http://payment-service:3004')
NOTIFICATION_SERVICE_URL = os.getenv('NOTIFICATION_SERVICE_URL', 'http://notification-service:3005')

def get_user_from_token(request):
    """Extract user ID from Authorization header (handled by API Gateway)"""
    # In production, this would verify JWT or trust the gateway
    return {'id': 1, 'email': 'user@example.com'}

@bp.route('/', methods=['GET'])
def get_orders():
    try:
        user = get_user_from_token(request)
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        orders = Order.get_by_user(user['id'], limit, offset)
        
        return jsonify({
            'orders': orders,
            'count': len(orders)
        }), 200
    except Exception as e:
        logger.error(f'Get orders error: {str(e)}')
        return jsonify({'error': 'Failed to fetch orders'}), 500

@bp.route('/', methods=['POST'])
def create_order():
    try:
        user = get_user_from_token(request)
        data = request.json
        
        items = data.get('items', [])
        shipping_address_id = data.get('shipping_address_id')
        
        if not items:
            return jsonify({'error': 'No items provided'}), 400
        
        # Validate products and calculate total
        total_amount = 0
        order_items = []
        
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            
            # Fetch product details
            try:
                response = requests.get(f'{PRODUCT_SERVICE_URL}/{product_id}', timeout=5)
                if response.status_code != 200:
                    return jsonify({'error': f'Product {product_id} not found'}), 404
                
                data_json = response.json()
                product = data_json.get('item') or data_json.get('product')
                if not product:
                    logger.error(f'Unexpected product payload for {product_id}: {data_json}')
                    return jsonify({'error': f'Invalid product data for {product_id}'}), 500
                
                if product['stock_quantity'] < quantity:
                    return jsonify({'error': f'Insufficient stock for product {product_id}'}), 400
                
                unit_price = float(product['price'])
                subtotal = unit_price * quantity
                total_amount += subtotal
                
                order_items.append({
                    'product_id': product_id,
                    'product_name': product['name'],
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'subtotal': subtotal
                })
            except requests.RequestException as e:
                logger.error(f'Error fetching product {product_id}: {str(e)}')
                return jsonify({'error': 'Failed to validate products'}), 503
        
        # Create order
        order = Order.create(user['id'], order_items, total_amount, shipping_address_id)
        
        logger.info(f'Order created: {order["id"]} for user {user["id"]}')
        
        # Send order confirmation notification (synchronous REST call)
        try:
            notification_payload = {
                'type': 'order_confirmation',
                'recipient': user['email'],
                'payload': {
                    'order_id': order['id'],
                    'total_amount': total_amount
                }
            }
            requests.post(
                f'{NOTIFICATION_SERVICE_URL}/send',
                json=notification_payload,
                timeout=5
            )
            logger.info(f'Order confirmation notification sent for order {order["id"]}')
        except requests.RequestException as e:
            # Log but don't fail the order creation if notification fails
            logger.warning(f'Failed to send order notification: {str(e)}')
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order
        }), 201
        
    except Exception as e:
        logger.error(f'Create order error: {str(e)}')
        return jsonify({'error': 'Failed to create order'}), 500

@bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        user = get_user_from_token(request)
        order = Order.get_by_id(order_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if order['user_id'] != user['id']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        items = Order.get_items(order_id)
        order['items'] = items
        
        return jsonify({'order': order}), 200
    except Exception as e:
        logger.error(f'Get order error: {str(e)}')
        return jsonify({'error': 'Failed to fetch order'}), 500

@bp.route('/<int:order_id>/cancel', methods=['PUT'])
def cancel_order(order_id):
    try:
        user = get_user_from_token(request)
        order = Order.get_by_id(order_id)
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if order['user_id'] != user['id']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        if order['status'] in ['cancelled', 'completed', 'shipped']:
            return jsonify({'error': f'Cannot cancel order with status: {order["status"]}'}), 400
        
        updated_order = Order.update_status(order_id, 'cancelled', 'Cancelled by user')
        
        logger.info(f'Order cancelled: {order_id}')
        
        return jsonify({
            'message': 'Order cancelled successfully',
            'order': updated_order
        }), 200
    except Exception as e:
        logger.error(f'Cancel order error: {str(e)}')
        return jsonify({'error': 'Failed to cancel order'}), 500
