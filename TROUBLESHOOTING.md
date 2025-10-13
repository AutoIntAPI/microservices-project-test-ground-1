# Troubleshooting Guide

Common issues and their solutions for the E-Commerce Microservices platform.

## Table of Contents

1. [Docker & Compose Issues](#docker--compose-issues)
2. [Service Connection Issues](#service-connection-issues)
3. [Database Issues](#database-issues)
4. [Authentication Issues](#authentication-issues)
5. [Port Conflicts](#port-conflicts)
6. [Performance Issues](#performance-issues)
7. [Development Issues](#development-issues)

---

## Docker & Compose Issues

### Services won't start

**Symptom:** `docker-compose up` fails or services crash immediately

**Solutions:**

1. Check Docker is running:
   ```bash
   docker ps
   ```

2. Rebuild images:
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up
   ```

3. Check logs for specific service:
   ```bash
   docker-compose logs service-name
   ```

### "Port already in use" error

**Symptom:** Error message about port 8000, 3001, 5432, etc. already allocated

**Solution:**

1. Find what's using the port:
   ```bash
   lsof -i :8000
   # or
   netstat -tuln | grep 8000
   ```

2. Stop the conflicting service or change ports in `docker-compose.yml`

### Out of disk space

**Symptom:** Build fails with "no space left on device"

**Solution:**

```bash
# Remove unused Docker resources
docker system prune -a

# Remove all stopped containers
docker container prune

# Remove all unused volumes
docker volume prune
```

---

## Service Connection Issues

### "Service Unavailable" from API Gateway

**Symptom:** 503 error when accessing endpoints

**Possible Causes & Solutions:**

1. **Service not ready yet:**
   - Wait 30-60 seconds after `docker-compose up`
   - Check health: `make health` or `curl http://localhost:3001/health`

2. **Service crashed:**
   ```bash
   docker-compose ps
   docker-compose logs service-name
   ```

3. **Wrong service URL in environment variables:**
   - Check `.env` files in each service
   - Ensure service names match docker-compose service names

### Cannot connect to database

**Symptom:** Services log "connection refused" or "database does not exist"

**Solutions:**

1. Check PostgreSQL is running:
   ```bash
   docker-compose ps postgres
   docker-compose logs postgres
   ```

2. Wait for database initialization:
   ```bash
   docker-compose logs postgres | grep "ready to accept connections"
   ```

3. Verify connection string:
   ```
   DATABASE_URL=postgresql://ecommerce:ecommerce123@postgres:5432/ecommerce
   ```

4. Reset database:
   ```bash
   docker-compose down -v
   docker-compose up -d postgres
   # Wait 10 seconds
   docker-compose up -d
   ```

---

## Database Issues

### Tables not created

**Symptom:** Errors about missing tables or schemas

**Solution:**

1. Check if init script ran:
   ```bash
   docker-compose exec postgres psql -U ecommerce -d ecommerce -c "\dt users.*"
   ```

2. Manually run init script:
   ```bash
   docker-compose exec postgres psql -U ecommerce -d ecommerce -f /docker-entrypoint-initdb.d/init-db.sql
   ```

3. Complete reset:
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

### Sample data not loaded

**Symptom:** No products appear when querying

**Solution:**

Check if products exist:
```bash
docker-compose exec postgres psql -U ecommerce -d ecommerce -c "SELECT COUNT(*) FROM products.products;"
```

If zero, manually insert:
```bash
docker-compose exec postgres psql -U ecommerce -d ecommerce < infrastructure/docker/init-db.sql
```

### Connection pool exhausted

**Symptom:** "sorry, too many clients already"

**Solution:**

Restart the affected service:
```bash
docker-compose restart user-service
```

Or increase pool size in service configuration.

---

## Authentication Issues

### "Invalid token" error

**Symptom:** 401 Unauthorized when using JWT token

**Possible Causes:**

1. **Token expired** (24h default):
   - Login again to get new token

2. **Wrong JWT secret:**
   - Ensure all services use same `JWT_SECRET`
   - Check API Gateway and User Service `.env` files

3. **Malformed token:**
   - Ensure format is: `Authorization: Bearer <token>`
   - No extra spaces or characters

### Cannot login/register

**Symptom:** Registration or login fails with 500 error

**Solutions:**

1. Check User Service logs:
   ```bash
   docker-compose logs user-service
   ```

2. Verify database connection:
   ```bash
   docker-compose exec postgres psql -U ecommerce -d ecommerce -c "SELECT * FROM users.users LIMIT 1;"
   ```

3. Check password hashing:
   - Ensure bcrypt is installed in User Service
   - Check logs for bcrypt errors

---

## Port Conflicts

### Default port already in use

**Solution 1: Stop conflicting service**

Find and stop the service using the port:
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Solution 2: Change ports**

Edit `docker-compose.yml`:
```yaml
api-gateway:
  ports:
    - "8080:8000"  # Changed from 8000:8000
```

Then access at http://localhost:8080

---

## Performance Issues

### Slow API responses

**Possible Causes & Solutions:**

1. **First request after start:**
   - Services need warm-up time
   - First request to each service may be slow

2. **Database not indexed:**
   - Init script includes indexes
   - Verify: Check `infrastructure/docker/init-db.sql`

3. **No caching:**
   - Redis should be running
   - Check: `docker-compose ps redis`

4. **Resource constraints:**
   ```bash
   # Check Docker resource usage
   docker stats
   ```
   
   Increase Docker Desktop resources if needed:
   - Settings → Resources → Advanced
   - Increase CPUs and Memory

### High memory usage

**Solution:**

1. Check which service is using memory:
   ```bash
   docker stats
   ```

2. Restart heavy services:
   ```bash
   docker-compose restart service-name
   ```

3. Limit resources in docker-compose.yml:
   ```yaml
   api-gateway:
     deploy:
       resources:
         limits:
           memory: 512M
   ```

---

## Development Issues

### Hot reload not working

**Symptom:** Code changes don't reflect in running service

**Solution:**

1. Verify using dev docker-compose:
   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

2. Check volume mounts in `docker-compose.dev.yml`:
   ```yaml
   volumes:
     - ./services/user-service:/app
     - /app/node_modules
   ```

3. Restart service:
   ```bash
   docker-compose restart service-name
   ```

### npm install fails in container

**Symptom:** Package installation errors during build

**Solutions:**

1. Clear npm cache:
   ```bash
   docker-compose build --no-cache service-name
   ```

2. Check for package-lock.json conflicts:
   ```bash
   cd services/service-name
   rm package-lock.json
   npm install
   git checkout package-lock.json
   ```

### Python packages not found

**Symptom:** ModuleNotFoundError in Python services

**Solutions:**

1. Rebuild the service:
   ```bash
   docker-compose build --no-cache order-service
   ```

2. Verify requirements.txt:
   ```bash
   cat services/order-service/requirements.txt
   ```

3. Install in container:
   ```bash
   docker-compose exec order-service pip install -r requirements.txt
   ```

---

## Common Error Messages

### "ECONNREFUSED"

**Meaning:** Cannot connect to another service

**Fix:** 
- Check service is running: `docker-compose ps`
- Check service name in URL matches docker-compose.yml
- Wait for service to be healthy

### "relation does not exist"

**Meaning:** Database table not found

**Fix:**
- Run init script: See [Tables not created](#tables-not-created)
- Check schema name is correct (users., products., etc.)

### "password authentication failed"

**Meaning:** Wrong database credentials

**Fix:**
- Check DATABASE_URL in .env files
- Verify postgres service environment variables
- Default: `postgresql://ecommerce:ecommerce123@postgres:5432/ecommerce`

### "CORS error" in browser

**Meaning:** Cross-Origin Resource Sharing blocked

**Fix:**
- API Gateway should have CORS enabled
- Check `cors` middleware in api-gateway/src/index.js
- Ensure request includes proper headers

---

## Getting Help

If you've tried these solutions and still have issues:

1. **Check logs thoroughly:**
   ```bash
   docker-compose logs --tail=100 service-name
   ```

2. **Verify environment:**
   - Docker version: `docker --version` (should be 20.10+)
   - Docker Compose: `docker-compose --version` (should be 2.0+)
   - OS and architecture

3. **Create an issue:**
   - Include error logs
   - Include docker-compose logs
   - Describe what you were trying to do
   - Include your environment details

4. **Reset everything:**
   ```bash
   docker-compose down -v
   docker system prune -af
   ./scripts/setup.sh
   docker-compose up
   ```

---

## Debugging Tips

### Enable debug logging

Add to service .env files:
```
LOG_LEVEL=debug
NODE_ENV=development  # for Node.js
FLASK_DEBUG=1         # for Python
```

### Access container shell

```bash
# Node.js services
docker-compose exec api-gateway sh

# Python services
docker-compose exec order-service sh
```

### Check service configuration

```bash
# View environment variables
docker-compose exec service-name env

# View running processes
docker-compose exec service-name ps aux
```

### Monitor in real-time

```bash
# Watch logs
docker-compose logs -f

# Watch resource usage
docker stats

# Watch network activity
docker-compose exec api-gateway netstat -tuln
```

---

## Preventive Measures

1. **Regular cleanup:**
   ```bash
   docker system prune -f
   ```

2. **Keep Docker updated:**
   - Check for Docker Desktop updates regularly

3. **Monitor resources:**
   - Watch disk space
   - Monitor memory usage
   - Check CPU usage

4. **Backup data:**
   ```bash
   docker-compose exec postgres pg_dump -U ecommerce ecommerce > backup.sql
   ```

5. **Version control:**
   - Commit working configurations
   - Document custom changes

---

Remember: When in doubt, check the logs! 📋
