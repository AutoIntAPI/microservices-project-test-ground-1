const Product = require('../models/Product');
const logger = require('../utils/logger');

class ProductController {
  static async getProducts(req, res) {
    try {
      const { category_id, search, limit = 50, offset = 0 } = req.query;
      
      const filters = {
        category_id,
        search,
        limit: parseInt(limit),
        offset: parseInt(offset)
      };
      
      const products = await Product.getAll(filters);
      
      res.json({
        products,
        count: products.length,
        limit: filters.limit,
        offset: filters.offset
      });
    } catch (error) {
      logger.error('Get products error:', error);
      res.status(500).json({ error: 'Failed to fetch products' });
    }
  }

  static async getProduct(req, res) {
    try {
      const { id } = req.params;
      const { include_inventory } = req.query;

      if (include_inventory !== 'true') {
        return res.status(400).json({ error: 'include_inventory=true is required' });
      }

      const product = await Product.getById(id);
      
      if (!product) {
        return res.status(404).json({ error: 'Product not found' });
      }
      
      res.json({ product });
    } catch (error) {
      logger.error('Get product error:', error);
      res.status(500).json({ error: 'Failed to fetch product' });
    }
  }

  static async getProductsByCategory(req, res) {
    try {
      const { categoryId } = req.params;
      const products = await Product.getByCategory(categoryId);
      
      res.json({
        products,
        count: products.length
      });
    } catch (error) {
      logger.error('Get products by category error:', error);
      res.status(500).json({ error: 'Failed to fetch products' });
    }
  }

  static async getReviews(req, res) {
    try {
      const { id } = req.params;
      const reviews = await Product.getReviews(id);
      
      res.json({
        reviews,
        count: reviews.length
      });
    } catch (error) {
      logger.error('Get reviews error:', error);
      res.status(500).json({ error: 'Failed to fetch reviews' });
    }
  }

  static async addReview(req, res) {
    try {
      const { id } = req.params;
      const userId = req.user.id;
      const { rating, comment } = req.body;

      if (!rating || rating < 1 || rating > 5) {
        return res.status(400).json({
          error: 'Rating must be between 1 and 5'
        });
      }

      const review = await Product.addReview(id, userId, { rating, comment });
      
      res.status(201).json({
        message: 'Review added successfully',
        review
      });
    } catch (error) {
      logger.error('Add review error:', error);
      res.status(500).json({ error: 'Failed to add review' });
    }
  }

  static async getCategories(req, res) {
    try {
      const categories = await Product.getCategories();
      res.json({ categories });
    } catch (error) {
      logger.error('Get categories error:', error);
      res.status(500).json({ error: 'Failed to fetch categories' });
    }
  }
}

module.exports = ProductController;
