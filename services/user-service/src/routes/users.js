const express = require('express');
const UserController = require('../controllers/userController');
const { authenticate } = require('../middleware/auth');

const router = express.Router();

// Public routes
router.post('/register', UserController.register);
router.post('/login', UserController.login);

// Protected routes
router.get('/me', authenticate, UserController.getProfile);
router.put('/me', authenticate, UserController.updateProfile);
router.get('/me/addresses', authenticate, UserController.getAddresses);
router.post('/me/addresses', authenticate, UserController.addAddress);

module.exports = router;
