from flask import Blueprint, request, jsonify
from app.models.payment import Payment
from app.utils.logger import logger
import requests
import os

bp = Blueprint('payments', __name__)

NOTIFICATION_SERVICE_URL = os.getenv('NOTIFICATION_SERVICE_URL', 'http://notification-service:3005')

def get_user_from_token(request):
    """Extract user ID from Authorization header"""
    return {'id': 1, 'email': 'user@example.com'}

@bp.route('/process', methods=['POST'])
def process_payment():
    try:
        user = get_user_from_token(request)
        data = request.json
        
        order_id = data.get('order_id')
        amount = data.get('amount')
        payment_method = data.get('payment_method', 'credit_card')
        
        if not order_id or not amount:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create transaction
        transaction = Payment.create_transaction(order_id, user['id'], amount, payment_method)
        
        # Simulate payment processing
        result = Payment.simulate_payment(amount, payment_method)
        
        # Update transaction status
        status = 'completed' if result['success'] else 'failed'
        updated_transaction = Payment.update_transaction_status(
            transaction['transaction_id'],
            status,
            result['gateway_response']
        )
        
        logger.info(f'Payment processed: {transaction["transaction_id"]} - Status: {status}')
        
        # Send payment confirmation notification (synchronous REST call)
        if result['success']:
            try:
                notification_payload = {
                    'type': 'payment_confirmation',
                    'recipient': user['email'],
                    'payload': {
                        'transaction_id': transaction['transaction_id'],
                        'amount': amount
                    }
                }
                requests.post(
                    f'{NOTIFICATION_SERVICE_URL}/{transaction["transaction_id"]}',
                    json=notification_payload,
                    timeout=5
                )
                logger.info(f'Payment confirmation notification sent for transaction {transaction["transaction_id"]}')
            except requests.RequestException as e:
                # Log but don't fail the payment if notification fails
                logger.warning(f'Failed to send payment notification: {str(e)}')
        
        if result['success']:
            return jsonify({
                'message': 'Payment processed successfully',
                'transaction': updated_transaction
            }), 200
        else:
            return jsonify({
                'error': 'Payment failed',
                'message': result['message'],
                'transaction': updated_transaction
            }), 402
            
    except Exception as e:
        logger.error(f'Process payment error: {str(e)}')
        return jsonify({'error': 'Payment processing failed'}), 500

@bp.route('/transactions', methods=['GET'])
def get_transactions():
    try:
        user = get_user_from_token(request)
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        transactions = Payment.get_by_user(user['id'], limit, offset)
        
        return jsonify({
            'transactions': transactions,
            'count': len(transactions)
        }), 200
    except Exception as e:
        logger.error(f'Get transactions error: {str(e)}')
        return jsonify({'error': 'Failed to fetch transactions'}), 500

@bp.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    try:
        user = get_user_from_token(request)
        transaction = Payment.get_by_id(transaction_id)
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        if transaction['user_id'] != user['id']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({'transaction': transaction}), 200
    except Exception as e:
        logger.error(f'Get transaction error: {str(e)}')
        return jsonify({'error': 'Failed to fetch transaction'}), 500

@bp.route('/methods', methods=['POST'])
def add_payment_method():
    try:
        user = get_user_from_token(request)
        data = request.json
        
        method = Payment.add_payment_method(user['id'], data)
        
        logger.info(f'Payment method added for user {user["id"]}')
        
        return jsonify({
            'message': 'Payment method added successfully',
            'method': method
        }), 201
    except Exception as e:
        logger.error(f'Add payment method error: {str(e)}')
        return jsonify({'error': 'Failed to add payment method'}), 500

@bp.route('/methods', methods=['GET'])
def get_payment_methods():
    try:
        user = get_user_from_token(request)
        methods = Payment.get_payment_methods(user['id'])
        
        return jsonify({
            'methods': methods,
            'count': len(methods)
        }), 200
    except Exception as e:
        logger.error(f'Get payment methods error: {str(e)}')
        return jsonify({'error': 'Failed to fetch payment methods'}), 500
