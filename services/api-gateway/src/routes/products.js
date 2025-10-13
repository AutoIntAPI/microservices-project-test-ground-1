const express = require('express');
const { createServiceProxy } = require('../utils/proxy');
const { authenticate } = require('../middleware/auth');

const router = express.Router();
const PRODUCT_SERVICE_URL = process.env.PRODUCT_SERVICE_URL || 'http://product-service:3002';

// Public routes
router.get('/', createServiceProxy('product-service', PRODUCT_SERVICE_URL));
router.get('/:id', createServiceProxy('product-service', PRODUCT_SERVICE_URL));
router.get('/category/:categoryId', createServiceProxy('product-service', PRODUCT_SERVICE_URL));
router.get('/:id/reviews', createServiceProxy('product-service', PRODUCT_SERVICE_URL));

// Protected routes
router.post('/:id/reviews', authenticate, createServiceProxy('product-service', PRODUCT_SERVICE_URL));

module.exports = router;
