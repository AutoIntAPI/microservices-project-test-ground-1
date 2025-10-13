const express = require('express');
const ProductController = require('../controllers/productController');

const router = express.Router();

// Mock auth middleware for reviews (since auth is handled at gateway)
const authenticate = (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (authHeader && authHeader.startsWith('Bearer ')) {
    // In production, verify JWT here or trust the gateway
    req.user = { id: 1 }; // Mock user for now
  }
  next();
};

router.get('/', ProductController.getProducts);
router.get('/categories', ProductController.getCategories);
router.get('/category/:categoryId', ProductController.getProductsByCategory);
router.get('/:id', ProductController.getProduct);
router.get('/:id/reviews', ProductController.getReviews);
router.post('/:id/reviews', authenticate, ProductController.addReview);

module.exports = router;
