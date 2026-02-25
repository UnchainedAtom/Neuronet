# Neuronet - Setup Guide

Follow these steps to get Neuronet running on your system.

## Quick Start (Windows)

### Method 1: Local Development (Recommended for Quick Testing)

This uses SQLite and requires no database setup.

```powershell
# 1. Open PowerShell and navigate to project
cd e:\TECH\Neuronet

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database and create demo data
python init_db.py

# 5. Run the application
python app.py
```

Then open your browser to `http://localhost:5000`

**Demo Access Codes** (created by init_db.py):
- DEMO-001
- DEMO-002
- DEMO-003
- ADMIN-001

---

## Method 2: Docker (Recommended for Portfolio Display)

Demonstrates containerization and orchestration skills.

### Prerequisites
- Docker Desktop installed and running
- (optional) Docker Compose

### Steps

```powershell
# 1. Navigate to project directory
cd e:\TECH\Neuronet

# 2. Build and start containers
docker-compose up -d

# This will:
# - Create a MySQL database container
# - Build and run the Flask application
# - Expose the app on port 5000
```

Wait 30-40 seconds for the database to fully start, then:
- Open browser to `http://localhost:5000`
- Database automatically initializes on first run

To stop:
```powershell
docker-compose down
```

---

## Method 3: Production Setup with MySQL

For deploying to a web server.

### Prerequisites
- MySQL Server installed and running
- Python 3.8+

### Steps

```powershell
# 1. Navigate to project
cd e:\TECH\Neuronet

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
# Option A: Create .env file
copy .env.example .env
# Edit .env with your MySQL password and secret key

# Option B: Set via PowerShell
$env:MYSQL_PASSWORD = "your_password"
$env:SECRET_KEY = "your-secure-key"
$env:FLASK_ENV = "production"

# 5. Initialize database
python init_db.py

# 6. Run with Gunicorn (for production)
gunicorn --bind 0.0.0.0:8000 --workers 4 wsgi:app

# Or for development
python app.py
```

---

## Testing the Application

### 1. Create an Account
- Go to `/auth/signUp`
- Use one of the demo codes: DEMO-001, DEMO-002, DEMO-003
- Fill in username and password (min 8 chars)

### 2. View Neuronet
- After login, you'll see the character dashboard
- This shows D&D-style character stats
- Go to `/baseline` to see more detailed stats

### 3. View Fellowship Market
- Click on "Fellowship" in navigation
- View uploaded artwork
- Browse inventory and market

### 4. Access Admin Panel (with ADMIN-001 code)
- Go to `/admin`
- Manage users, artwork, game data
- Change the game date

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'neuronet'"
**Solution**: Make sure you're in the `Neuronet` directory and virtual environment is activated.

### "No MYSQL_PASSWORD environment variable"
**Solution**: For dev, this is fine - it uses SQLite automatically. For production, set the environment variable.

### Port 5000 already in use
**Solution**: 
```powershell
# Use a different port
$env:PORT = "5001"
python app.py
```

### Database is locked (SQLite)
**Solution**: Delete `neuronet.db` and run `python init_db.py` again

### Docker containers won't start
**Solution**:
```powershell
docker-compose down -v  # Remove volumes
docker-compose up -d    # Start fresh
```

### Templates not found
**Solution**: Make sure you're running from the project root directory

---

## Environment Variables Explained

| Variable | Purpose | Required | Default |
|----------|---------|----------|---------|
| `FLASK_ENV` | dev/test/prod mode | No | development |
| `FLASK_HOST` | Server address | No | 127.0.0.1 |
| `PORT` | Server port | No | 5000 |
| `SECRET_KEY` | Session encryption | Recommended | dev-key |
| `MYSQL_PASSWORD` | MySQL password | Prod only | None |
| `MYSQL_HOST` | MySQL server | Prod only | localhost |

---

## Next Steps for Portfolio

After getting it running, consider:

1. **Deploy to a server** (AWS, DigitalOcean, Heroku)
   - Document the deployment process
   - Show CI/CD pipeline

2. **Add GitHub Actions** for testing
   - Create `.github/workflows/test.yml`

3. **Improve security**
   - Add CORS headers
   - Implement rate limiting
   - Add input validation tests

4. **Write API documentation**
   - Swagger/OpenAPI for endpoints
   - Postman collection

5. **Add monitoring**
   - Application logs
   - Error tracking (Sentry)
   - Performance metrics

---

## Common Interview Questions This Setup Addresses

> "Walk me through how you'd deploy this application"
- ✓ Docker setup provided
- ✓ Environment configuration explained
- ✓ Database initialization documented

> "How would you handle secrets?"
- ✓ Environment variables instead of hardcoding
- ✓ .env.example shows best practices
- ✓ Production vs dev config separation

> "Show me you understand scaling"
- ✓ Gunicorn with multiple workers
- ✓ Docker Compose for orchestration
- ✓ Separation of application and database

---

**Need help?** Check the main [README.md](README.md) for more documentation.
