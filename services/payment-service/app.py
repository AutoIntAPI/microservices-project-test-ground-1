from flask import Flask
from flask_cors import CORS
from app.routes import payments
from app.utils.logger import logger
import os

app = Flask(__name__)
CORS(app)

app.register_blueprint(payments.bp)

@app.route('/health', methods=['GET'])
def health():
    return {
        'status': 'healthy',
        'service': 'payment-service',
        'timestamp': str(os.times())
    }, 200

@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f'Error: {str(error)}')
    return {'error': str(error)}, 500

if __name__ == '__main__':
    port = int(os.getenv('SERVICE_PORT', 3004))
    logger.info(f'Payment Service starting on port {port}')
    app.run(host='0.0.0.0', port=port)
