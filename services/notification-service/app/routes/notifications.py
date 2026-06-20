from flask import Blueprint, request, jsonify
from app.utils.email_service import EmailService
from app.utils.logger import logger

bp = Blueprint('notifications', __name__)
email_service = EmailService()

@bp.route('/deliver', methods=['POST'])
def send_notification():
    try:
        data = request.json
        
        notification_type = data.get('type')
        recipient = data.get('recipient')
        payload = data.get('payload', {})
        
        if not notification_type or not recipient:
            return jsonify({'error': 'Missing required fields'}), 400
        
        result = None
        
        if notification_type == 'welcome':
            result = email_service.send_welcome_email(
                recipient,
                payload.get('user_name', 'User')
            )
        elif notification_type == 'order_confirmation':
            result = email_service.send_order_confirmation(
                recipient,
                payload.get('order_id'),
                payload.get('total_amount')
            )
        elif notification_type == 'payment_confirmation':
            result = email_service.send_payment_confirmation(
                recipient,
                payload.get('transaction_id'),
                payload.get('amount')
            )
        elif notification_type == 'custom':
            result = email_service.send_email(
                recipient,
                payload.get('subject', 'Notification'),
                payload.get('body', '')
            )
        else:
            return jsonify({'error': f'Unknown notification type: {notification_type}'}), 400
        
        logger.info(f'Notification sent: {notification_type} to {recipient}')
        
        return jsonify({
            'message': 'Notification sent successfully',
            'result': result
        }), 200
        
    except Exception as e:
        logger.error(f'Send notification error: {str(e)}')
        return jsonify({'error': 'Failed to send notification'}), 500

@bp.route('/batch', methods=['POST'])
def send_batch_notifications():
    try:
        data = request.json
        notifications = data.get('notifications', [])
        
        if not notifications:
            return jsonify({'error': 'No notifications provided'}), 400
        
        results = []
        for notification in notifications:
            try:
                # Process each notification
                # This is simplified; in production, you'd use a queue
                results.append({
                    'recipient': notification.get('recipient'),
                    'status': 'sent'
                })
            except Exception as e:
                results.append({
                    'recipient': notification.get('recipient'),
                    'status': 'failed',
                    'error': str(e)
                })
        
        return jsonify({
            'message': 'Batch notifications processed',
            'results': results,
            'total': len(results)
        }), 200
        
    except Exception as e:
        logger.error(f'Batch notification error: {str(e)}')
        return jsonify({'error': 'Failed to process batch notifications'}), 500
