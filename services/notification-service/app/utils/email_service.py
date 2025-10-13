import os
from app.utils.logger import logger

class EmailService:
    """Email service for sending notifications"""
    
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.mailtrap.io')
        self.smtp_port = int(os.getenv('SMTP_PORT', 2525))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_pass = os.getenv('SMTP_PASS', '')
        self.email_from = os.getenv('EMAIL_FROM', 'noreply@ecommerce.com')
    
    def send_email(self, to_email, subject, body):
        """Simulate sending an email"""
        # In production, this would use smtplib or a service like SendGrid
        logger.info(f'Sending email to {to_email}')
        logger.info(f'Subject: {subject}')
        logger.info(f'Body: {body[:100]}...')
        
        # Simulate email sent
        return {
            'success': True,
            'message': f'Email sent to {to_email}',
            'subject': subject
        }
    
    def send_welcome_email(self, user_email, user_name):
        """Send welcome email to new user"""
        subject = 'Welcome to E-Commerce Platform!'
        body = f'''
        Hello {user_name},
        
        Welcome to our E-Commerce platform! We're excited to have you on board.
        
        You can now:
        - Browse our product catalog
        - Add items to your cart
        - Place orders
        - Track your purchases
        
        Happy shopping!
        
        Best regards,
        E-Commerce Team
        '''
        return self.send_email(user_email, subject, body)
    
    def send_order_confirmation(self, user_email, order_id, total_amount):
        """Send order confirmation email"""
        subject = f'Order Confirmation - Order #{order_id}'
        body = f'''
        Thank you for your order!
        
        Order ID: {order_id}
        Total Amount: ${total_amount}
        
        We'll send you another email when your order ships.
        
        You can track your order status in your account dashboard.
        
        Best regards,
        E-Commerce Team
        '''
        return self.send_email(user_email, subject, body)
    
    def send_payment_confirmation(self, user_email, transaction_id, amount):
        """Send payment confirmation email"""
        subject = f'Payment Received - Transaction #{transaction_id}'
        body = f'''
        We've received your payment!
        
        Transaction ID: {transaction_id}
        Amount: ${amount}
        Status: Completed
        
        Thank you for your payment.
        
        Best regards,
        E-Commerce Team
        '''
        return self.send_email(user_email, subject, body)
