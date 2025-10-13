const express = require('express');
const { createServiceProxy } = require('../utils/proxy');
const { authenticate } = require('../middleware/auth');

const router = express.Router();
const PAYMENT_SERVICE_URL = process.env.PAYMENT_SERVICE_URL || 'http://payment-service:3004';

// All payment routes require authentication
router.use(authenticate);

router.post('/process', createServiceProxy('payment-service', PAYMENT_SERVICE_URL));
router.get('/transactions', createServiceProxy('payment-service', PAYMENT_SERVICE_URL));
router.get('/transactions/:id', createServiceProxy('payment-service', PAYMENT_SERVICE_URL));
router.post('/methods', createServiceProxy('payment-service', PAYMENT_SERVICE_URL));
router.get('/methods', createServiceProxy('payment-service', PAYMENT_SERVICE_URL));

module.exports = router;
