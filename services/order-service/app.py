from flask import Flask
from flask_cors import CORS
from app.routes import orders
from app.utils.logger import logger
import os

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(orders.bp)

@app.route('/health', methods=['GET'])
def health():
    return {
        'status': 'healthy',
        'service': 'order-service',
        'timestamp': str(os.times())
    }, 200

@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f'Error: {str(error)}')
    return {
        'error': str(error)
    }, 500

if __name__ == '__main__':
    port = int(os.getenv('SERVICE_PORT', 3003))
    logger.info(f'Order Service starting on port {port}')
    app.run(host='0.0.0.0', port=port)
