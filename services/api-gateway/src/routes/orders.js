const express = require('express');
const { createServiceProxy } = require('../utils/proxy');
const { authenticate } = require('../middleware/auth');

const router = express.Router();
const ORDER_SERVICE_URL = process.env.ORDER_SERVICE_URL || 'http://order-service:3003';

// All order routes require authentication
router.use(authenticate);

router.get('/', createServiceProxy('order-service', ORDER_SERVICE_URL));
router.post('/', createServiceProxy('order-service', ORDER_SERVICE_URL));
router.get('/:id', createServiceProxy('order-service', ORDER_SERVICE_URL));
router.put('/:id/cancel', createServiceProxy('order-service', ORDER_SERVICE_URL));

module.exports = router;
