from flask import Blueprint, request, jsonify
from app.utils.email_service import EmailService
from app.utils.logger import logger

bp = Blueprint('notifications', __name__)
email_service = EmailService()

@bp.route('/send', methods=['POST'])
def send_notification():
    try:
        data = request.json
        
        notification_type = data.get('type')
        recipient = data.get('recipient')
        priority = data.get('priority', 'normal')
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
        
        logger.info(f'Notification sent: {notification_type} to {recipient} with priority {priority}')
        
        return jsonify({
            'message': 'Notification sent successfully',
            'priority': priority,
            'result': result
        }), 200
        
    except Exception as e:
        logger.error(f'Send notification error: {str(e)}')
        return jsonify({'error': 'Failed to send notification'}), 500

@bp.route('/audit', methods=['POST'])
def record_audit_event():
    try:
        data = request.json
        event = data.get('event')
        source = data.get('source', 'unknown')
        details = data.get('details', {})
        
        if not event:
            return jsonify({'error': 'Missing required fields'}), 400
        
        logger.info(f'Audit event recorded: {event} from {source}')
        
        return jsonify({
            'message': 'Audit event recorded successfully',
            'event': event,
            'source': source,
            'details': details
        }), 200
        
    except Exception as e:
        logger.error(f'Audit event error: {str(e)}')
        return jsonify({'error': 'Failed to record audit event'}), 500
