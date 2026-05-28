const User = require('../models/User');
const jwt = require('jsonwebtoken');
const logger = require('../utils/logger');

const JWT_SECRET = process.env.JWT_SECRET || 'default-secret-change-me';
const JWT_EXPIRY = '24h';

class UserController {
  static async register(req, res) {
    try {
      const { email, password, name } = req.body;

      // Validate input
      if (!email || !password || !name) {
        return res.status(400).json({
          error: 'Missing required fields',
          required: ['email', 'password', 'name']
        });
      }

      // Check if user exists
      const existingUser = await User.findByEmail(email);
      if (existingUser) {
        return res.status(409).json({
          error: 'User already exists'
        });
      }

      // Create user
      const user = await User.create({ email, password, name });
      
      // Generate token
      const token = jwt.sign(
        { id: user.id, email: user.email, role: user.role },
        JWT_SECRET,
        { expiresIn: JWT_EXPIRY }
      );

      logger.info(`User registered: ${user.email}`);

      res.status(201).json({
        message: 'User registered successfully',
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
          role: user.role
        },
        token
      });
    } catch (error) {
      logger.error('Registration error:', error);
      res.status(500).json({ error: 'Registration failed' });
    }
  }

  static async login(req, res) {
    try {
      const { email, password } = req.body;

      if (!email || !password) {
        return res.status(400).json({
          error: 'Email and password are required'
        });
      }

      // Find user
      const user = await User.findByEmail(email);
      if (!user || !user.is_active) {
        return res.status(401).json({
          error: 'Invalid credentials'
        });
      }

      // Verify password
      const isValid = await User.verifyPassword(password, user.password_hash);
      if (!isValid) {
        return res.status(401).json({
          error: 'Invalid credentials'
        });
      }

      // Generate token
      const token = jwt.sign(
        { id: user.id, email: user.email, role: user.role },
        JWT_SECRET,
        { expiresIn: JWT_EXPIRY }
      );

      logger.info(`User logged in: ${user.email}`);

      res.json({
        message: 'Login successful',
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
          role: user.role
        },
        token
      });
    } catch (error) {
      logger.error('Login error:', error);
      res.status(500).json({ error: 'Login failed' });
    }
  }

  static async getProfile(req, res) {
    try {
      const user = await User.findById(req.user.id);
      
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }

      res.json({ user });
    } catch (error) {
      logger.error('Get profile error:', error);
      res.status(500).json({ error: 'Failed to fetch profile' });
    }
  }

  static async updateProfile(req, res) {
    try {
      const updates = req.body;
      const user = await User.update(req.user.id, updates);

      res.json({
        message: 'Profile updated successfully',
        user
      });
    } catch (error) {
      logger.error('Update profile error:', error);
      res.status(500).json({ error: 'Failed to update profile' });
    }
  }

  static async getAddresses(req, res) {
    try {
      const addresses = await User.getAddresses(req.user.id);
      res.json({ addresses });
    } catch (error) {
      logger.error('Get addresses error:', error);
      res.status(500).json({ error: 'Failed to fetch addresses' });
    }
  }

  static async addAddress(req, res) {
    try {
      const address = await User.addAddress(req.user.id, req.body);
      res.status(201).json({
        message: 'Address added successfully',
        address
      });
    } catch (error) {
      logger.error('Add address error:', error);
      res.status(500).json({ error: 'Failed to add address' });
    }
  }
}

module.exports = UserController;
