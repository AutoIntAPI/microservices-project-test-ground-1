from app.models.db import execute_query, execute_one
import uuid

class Payment:
    @staticmethod
    def create_transaction(order_id, user_id, amount, payment_method):
        transaction_id = str(uuid.uuid4())
        query = """
            INSERT INTO payments.transactions 
            (order_id, user_id, amount, payment_method, status, transaction_id)
            VALUES (%s, %s, %s, %s, 'pending', %s)
            RETURNING *
        """
        return execute_one(query, (order_id, user_id, amount, payment_method, transaction_id))

    @staticmethod
    def update_transaction_status(transaction_id, status, gateway_response=None):
        query = """
            UPDATE payments.transactions 
            SET status = %s, gateway_response = %s, updated_at = CURRENT_TIMESTAMP
            WHERE transaction_id = %s
            RETURNING *
        """
        return execute_one(query, (status, gateway_response, transaction_id))

    @staticmethod
    def get_by_user(user_id, limit=50, offset=0):
        query = """
            SELECT * FROM payments.transactions 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """
        return execute_query(query, (user_id, limit, offset))

    @staticmethod
    def get_by_id(transaction_id):
        query = "SELECT * FROM payments.transactions WHERE id = %s"
        return execute_one(query, (transaction_id,))

    @staticmethod
    def add_payment_method(user_id, method_data):
        query = """
            INSERT INTO payments.payment_methods 
            (user_id, type, last_four, card_brand, expiry_month, expiry_year, is_default)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        return execute_one(query, (
            user_id,
            method_data.get('type'),
            method_data.get('last_four'),
            method_data.get('card_brand'),
            method_data.get('expiry_month'),
            method_data.get('expiry_year'),
            method_data.get('is_default', False)
        ))

    @staticmethod
    def get_payment_methods(user_id):
        query = """
            SELECT * FROM payments.payment_methods 
            WHERE user_id = %s 
            ORDER BY is_default DESC, created_at DESC
        """
        return execute_query(query, (user_id,))

    @staticmethod
    def simulate_payment(amount, payment_method):
        """Simulate payment processing"""
        # In a real system, this would integrate with Stripe, PayPal, etc.
        import random
        success = random.random() > 0.1  # 90% success rate
        
        if success:
            return {
                'success': True,
                'message': 'Payment processed successfully',
                'gateway_response': f'APPROVED - Transaction ID: {uuid.uuid4()}'
            }
        else:
            return {
                'success': False,
                'message': 'Payment failed',
                'gateway_response': 'DECLINED - Insufficient funds'
            }
