const express = require('express');
const cors = require('cors');
const productRoutes = require('./routes/products');
const logger = require('./utils/logger');

const app = express();
const PORT = process.env.SERVICE_PORT || 3002;

app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    service: 'product-service',
    timestamp: new Date().toISOString()
  });
});

app.use('/', productRoutes);

app.use((err, req, res, next) => {
  logger.error(err.message, { stack: err.stack });
  res.status(err.status || 500).json({
    error: err.message || 'Internal Server Error'
  });
});

const server = app.listen(PORT, () => {
  logger.info(`Product Service running on port ${PORT}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully');
  server.close(() => {
    logger.info('Server closed');
    process.exit(0);
  });
});

module.exports = app;
