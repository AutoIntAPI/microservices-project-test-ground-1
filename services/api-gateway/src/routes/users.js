const express = require('express');
const { createServiceProxy } = require('../utils/proxy');
const { authenticate } = require('../middleware/auth');

const router = express.Router();
const USER_SERVICE_URL = process.env.USER_SERVICE_URL || 'http://user-service:3001';

// Public routes
router.post('/register', createServiceProxy('user-service', USER_SERVICE_URL));
router.post('/login', createServiceProxy('user-service', USER_SERVICE_URL));

// Protected routes
router.get('/me', authenticate, createServiceProxy('user-service', USER_SERVICE_URL));
router.put('/me', authenticate, createServiceProxy('user-service', USER_SERVICE_URL));
router.get('/me/addresses', authenticate, createServiceProxy('user-service', USER_SERVICE_URL));
router.post('/me/addresses', authenticate, createServiceProxy('user-service', USER_SERVICE_URL));

module.exports = router;
