const db = require('./db');

class Product {
  static async getAll(filters = {}) {
    let query = `
      SELECT p.*, c.name as category_name 
      FROM products.products p 
      LEFT JOIN products.categories c ON p.category_id = c.id 
      WHERE p.is_active = true
    `;
    const params = [];
    
    if (filters.category_id) {
      params.push(filters.category_id);
      query += ` AND p.category_id = $${params.length}`;
    }
    
    if (filters.search) {
      params.push(`%${filters.search}%`);
      query += ` AND (p.name ILIKE $${params.length} OR p.description ILIKE $${params.length})`;
    }
    
    query += ' ORDER BY p.created_at DESC';
    
    if (filters.limit) {
      params.push(filters.limit);
      query += ` LIMIT $${params.length}`;
    }
    
    if (filters.offset) {
      params.push(filters.offset);
      query += ` OFFSET $${params.length}`;
    }
    
    const result = await db.query(query, params);
    return result.rows;
  }

  static async getById(id) {
    const result = await db.query(
      `SELECT p.*, c.name as category_name 
       FROM products.products p 
       LEFT JOIN products.categories c ON p.category_id = c.id 
       WHERE p.id = $1 AND p.is_active = true`,
      [id]
    );
    return result.rows[0];
  }

  static async getByCategory(categoryId) {
    const result = await db.query(
      `SELECT p.*, c.name as category_name 
       FROM products.products p 
       LEFT JOIN products.categories c ON p.category_id = c.id 
       WHERE p.category_id = $1 AND p.is_active = true 
       ORDER BY p.created_at DESC`,
      [categoryId]
    );
    return result.rows;
  }

  static async getReviews(productId) {
    const result = await db.query(
      'SELECT * FROM products.reviews WHERE product_id = $1 ORDER BY created_at DESC',
      [productId]
    );
    return result.rows;
  }

  static async addReview(productId, userId, reviewData) {
    const { rating, comment } = reviewData;
    const result = await db.query(
      'INSERT INTO products.reviews (product_id, user_id, rating, comment) VALUES ($1, $2, $3, $4) RETURNING *',
      [productId, userId, rating, comment]
    );
    return result.rows[0];
  }

  static async updateStock(productId, quantity) {
    const result = await db.query(
      'UPDATE products.products SET stock_quantity = stock_quantity + $1, updated_at = CURRENT_TIMESTAMP WHERE id = $2 RETURNING *',
      [quantity, productId]
    );
    return result.rows[0];
  }

  static async getCategories() {
    const result = await db.query(
      'SELECT * FROM products.categories ORDER BY name'
    );
    return result.rows;
  }
}

module.exports = Product;
