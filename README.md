# Neuronet - In-Game Economy Trading Platform

A Flask-based web application that simulates an internet within a sci-fi D&D game setting. Players can trade artwork (NFT-like assets) in the "Fellowship" market and manage character statistics through the "Neuronet" system.

## Features

- **User Authentication**: Secure login and signup with access code verification
- **Fellowship Market**: Buy and sell artwork with dynamic pricing
- **Neuronet System**: Character stat management (D&D 5e inspired)
- **Admin Panel**: Manage users, artworks, and game data
- **Role-Based Access**: Support for different user roles (Admin, Artist, etc.)
- **Database Flexibility**: Supports both SQLite (development) and MySQL (production)

## Project Structure

```
├── app.py                 # Application entry point
├── init_db.py            # Database initialization script
├── wsgi.py              # Production WSGI entry point
├── requirements.txt       # Python dependencies
├── config.py             # Configuration management
├── __init__.py           # Flask app factory
├── auth.py              # Authentication routes
├── neuroViews.py        # Neuronet character system
├── fellViews.py         # Fellowship market system
├── database.py          # SQLAlchemy models
├── migrations/          # Alembic database migrations
├── Dockerfile           # Container image definition
├── docker-compose.yml   # Multi-container orchestration
├── templates/           # HTML templates
│   ├── neuronet/       # Neuronet UI templates
│   └── fellowship/     # Fellowship market templates
└── static/             # CSS and JavaScript
    ├── styles/
    └── javascript/
```

## Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   cd Neuronet
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional, uses SQLite by default)
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your settings (optional for development)
   ```

5. **Initialize the database**
   ```bash
   python init_db.py
   ```
   This creates default tables, roles, and demo access codes.

6. **Access the application**
   - Open your browser to `http://localhost:5000`
   - Default access: Login page (need to create account with access code)

## Development vs Production

### Development (Default)

Uses SQLite database for easy local development with no setup required.

```bash
FLASK_ENV=development python app.py
```

### Production (MySQL)

For production deployment, configure MySQL:

1. **Set environment variables**:
   ```bash
   export FLASK_ENV=production
   export MYSQL_PASSWORD=your_password
   export MYSQL_HOST=your_host
   export SECRET_KEY=your-secure-key
   ```

2. **Initialize the database**:
   ```bash
   python init_db.py
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

## Database Initialization

### Quick Setup
```bash
python init_db.py
```

This creates:
- Database tables from SQLAlchemy models
- Game date (Aether Date 108:1907)
- User roles (ADMIN, FELLARTIST, USER)
- Demo access codes (DEMO-001/002/003, ADMIN-001)
- NPC market participants (5 traders with starting credits)

### Database Selection
- **Development (Default)**: Uses SQLite, automatically created
- **Production**: Uses MySQL when `MYSQL_PASSWORD` environment variable is set

## Database Migrations

After schema changes, run:
```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

## Features Overview

### Neuronet System
- Character creation and management
- D&D 5e-inspired ability scores and saves
- Skill tracking
- Equipment management
- Ship ownership and crew management

### Fellowship Market
- Artist registration for art uploads
- Artwork marketplace with pricing
- Buy/sell transactions
- Inventory management
- Sales history and analytics

### Admin Panel
- User management
- Artwork moderation
- Game-wide statistics
- Date/game-time management
- Transaction logs

## Security Considerations

⚠️  **Before deploying to production:**

1. **Change the SECRET_KEY**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Set this value in your `.env` or environment variables

2. **Use HTTPS** with a proper SSL certificate

3. **Configure CORS** headers appropriately

4. **Use environment variables** for all sensitive data (never hardcode credentials)

5. **Implement rate limiting** on authentication endpoints

6. **Regular backups** of database

## API Usage

The application provides web pages rather than traditional REST APIs. Interactions happen through form submissions and JSON endpoints.

### Key Routes

- `/auth/login` - User login
- `/auth/signUp` - User registration
- `/` - Neuronet home (character dashboard)
- `/fellowship/` - Fellowship market
- `/fellowship/market` - Browse artworks
- `/fellowship/inventory` - User's owned items
- `/fellowship/artist` - Upload artwork (if artist role)
- `/admin` - Admin dashboard (admin role required)

## Troubleshooting

### "Cannot import neuronet" error
Make sure you're in the correct directory and the virtual environment is activated.

### Database connection errors
For development: No action needed, SQLite is auto-created
For production: Verify MySQL is running and `MYSQL_PASSWORD` is set

### Port already in use
```bash
PORT=5001 python app.py
```

### Module not found errors
```bash
pip install -r requirements.txt
```

## Contributing

This is a portfolio project. For modifications or improvements:
1. Create a feature branch
2. Make changes
3. Test locally
4. Submit a pull request

## License

Private project - for portfolio use

## Future Improvements

- [ ] REST API endpoints
- [ ] WebSocket support for real-time updates
- [ ] Enhanced analytics dashboard
- [ ] Mobile-responsive UI overhaul
- [ ] Docker containerization
- [ ] Kubernetes deployment configs
- [ ] CI/CD pipeline
- [ ] Automated testing suite

## Contact & Support

This is a portfolio project by UnchainedAtom. For questions or issues, refer to the GitHub repository.

---

**Last Updated**: February 2026
**Status**: Portfolio Ready
