const db = require('./db');
const bcrypt = require('bcryptjs');

class User {
  static async create(userData) {
    const { email, password, name, phone } = userData;
    const passwordHash = await bcrypt.hash(password, 10);
    
    const result = await db.query(
      'INSERT INTO users.users (email, password_hash, name, phone) VALUES ($1, $2, $3, $4) RETURNING id, email, name, phone, created_at, role',
      [email, passwordHash, name, phone || null]
    );
    
    return result.rows[0];
  }

  static async findByEmail(email) {
    const result = await db.query(
      'SELECT * FROM users.users WHERE email = $1',
      [email]
    );
    return result.rows[0];
  }

  static async findById(id) {
    const result = await db.query(
      'SELECT id, email, name, phone, created_at, updated_at, role FROM users.users WHERE id = $1 AND is_active = true',
      [id]
    );
    return result.rows[0];
  }

  static async update(id, updates) {
    const { name, phone } = updates;
    const result = await db.query(
      'UPDATE users.users SET name = COALESCE($1, name), phone = COALESCE($2, phone), updated_at = CURRENT_TIMESTAMP WHERE id = $3 RETURNING id, email, name, phone, updated_at',
      [name, phone, id]
    );
    return result.rows[0];
  }

  static async verifyPassword(plainPassword, hashedPassword) {
    return bcrypt.compare(plainPassword, hashedPassword);
  }

  static async getAddresses(userId) {
    const result = await db.query(
      'SELECT * FROM users.addresses WHERE user_id = $1 ORDER BY is_default DESC, created_at DESC',
      [userId]
    );
    return result.rows;
  }

  static async addAddress(userId, addressData) {
    const { address_line1, address_line2, city, state, country, postal_code, is_default } = addressData;
    
    // If setting as default, unset other defaults
    if (is_default) {
      await db.query('UPDATE users.addresses SET is_default = false WHERE user_id = $1', [userId]);
    }
    
    const result = await db.query(
      'INSERT INTO users.addresses (user_id, address_line1, address_line2, city, state, country, postal_code, is_default) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING *',
      [userId, address_line1, address_line2 || null, city, state || null, country, postal_code, is_default || false]
    );
    
    return result.rows[0];
  }
}

module.exports = User;
