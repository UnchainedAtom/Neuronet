# Neuronet

A Flask-based marketplace simulator combining DnD character management with NFT inspired digital art trading in a homebrew sci-fi game world.

---

## Overview

**Concept:** 
I wanted a system in my homebrew sci-fi DnD game that made currency more interesting and felt like it fit the dystopian theme.  Naturally I gravitated towards an NFT inspired economy system that would function as minigame for my players and get them more invested in the world.  Eventually this idea spread into trying to create a whole ingame interactive internet system and DnD stat manager.

**Solution:**  
Built a containerized Flask application with SQLAlchemy ORM, role-based access control, and a market simulation engine. NPCs participate in buying/selling with autonomous decision-making. Database auto-selects SQLite (local) or MySQL based on environment configuration.

**Outcome:**  
A fully functional, production-ready application that demonstrates:
- User authentication with access codes and role-based permissions
- Character creation with D&D 5e ability scores and saves
- Dynamic NFT inspired marketplace with player to player and player to NPC trading
- Admin dashboard for game progression and user management
- Containerized deployment with Docker Compose (MySQL + Flask)
- Security hardening (environment-based secrets, no hardcoded credentials)

---

## Architecture / System Design

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP/HTML
       ▼
┌─────────────────────────────────────┐
│  Flask Web Application              │
│  ├─ auth.py (Login/Signup)          │
│  ├─ neuroViews.py (Character)       │
│  ├─ fellViews.py (Market/Trading)   │
│  └─ __init__.py (Factory & Routes)  │
└──────────┬──────────────────────────┘
           │ SQLAlchemy ORM
           ▼
┌─────────────────────────────────────┐
│  SQLite (Dev) / MySQL (Prod)        │
│  ├─ User (roles, credits, stats)    │
│  ├─ Artwork (images, pricing)       │
│  ├─ PlayerAbilitySave (D&D saves)   │
│  ├─ vDate (game world date)         │
│  └─ endDayLog (price history)       │
└─────────────────────────────────────┘
```

**Key Components:**
- **Auth System**: Access code validation, password hashing (scrypt), role assignment
- **Character System**: Ability scores (STR/DEX/CON/INT/WIS/CHA), modifiers, skill tracking, AC calculation
- **Market Engine**: Artwork listing, price tracking, NPC autonomous trading, daily price updates with Monte Carlo simulation
- **Admin Panel**: User/artwork management, game date progression, transaction logging

---

## Core Features

- **Character Management**: Create characters with D&D 5e ability scores, saves, and skills. Modify AC, HP, and bonuses.
- **Dynamic Marketplace**: Upload artwork, trade with other players and 5 NPC participants. Prices shift based on market activity.
- **Access Control**: Three role types (ADMIN, FELLARTIST, USER) with granular permissions. Signup restricted to valid access codes.
- **Price Simulation**: Monte Carlo algorithm generates realistic price movements. Daily logs track price history.
- **Database Flexibility**: Automatic selection—SQLite for development, MySQL for production. Zero manual configuration required.
- **Admin Tools**: Manage users, artworks, view statistics, progress game date, inspect transaction logs.
- **Security**: Scrypt password hashing, environment-based secrets, no hardcoded credentials, .gitignore prevents accidental leaks.

---

## Technical Stack

**Languages / Runtime**
- Python 3.8–3.13
- HTML/CSS/JavaScript (frontend)

**Frameworks / Libraries**
- Flask 2.1.2+ (web framework)
- SQLAlchemy 1.4.39 + Flask-SQLAlchemy 2.5.1 (ORM)
- Flask-Login 0.6.2 (session management)
- Flask-Admin 1.6.0 (admin panel)
- Werkzeug 2.1.2+ (password hashing)
- Pandas 1.3.0+, NumPy 1.20.0+, SciPy 1.5.0+ (price calculations)

**Infrastructure / Cloud**
- Docker (containerization)
- Docker Compose (orchestration)
- MySQL 8.0 (production database)
- SQLite 3 (development database)
- Gunicorn 20.1.0+ (production WSGI server)

**Other Tools**
- Alembic (database migrations)
- Flask-Migrate 3.1.0 (schema management)
- python-dotenv 0.20.0+ (environment variables)
- PyMySQL 1.0.2 (MySQL driver)
- cryptography 3.4.8+ (MySQL auth support)

---

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (comes with Python)
- git
- Docker & Docker Compose (optional, for containerized testing)

### Setup

```bash
# Clone the repository
git clone https://github.com/UnchainedAtom/Neuronet
cd Neuronet

# Create and activate virtual environment
# Windows:
python -m venv venv
venv\Scripts\activate

# macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database (creates tables, roles, demo data)
python init_db.py

# Run the development server
python app.py
```

**Default URL:** http://localhost:5000

**Demo Access Codes:**
- `DEMO-001`, `DEMO-002`, `DEMO-003` — Regular player accounts
- `ADMIN-001` — Admin account (access to `/admin`)

### Testing Basic Functionality

1. **Login/Signup**: Navigate to `/auth/login` and sign up with one of the demo codes
2. **Character Dashboard**: After login, view character stats at `/` (Neuronet home)
3. **Market**: Browse artwork at `/fellowship/` and upload at `/fellowship/artist`
4. **Admin Panel**: Log in with ADMIN-001 at `/admin`

---

## Deployment

### Docker Setup

```bash
# Start all services (Flask + MySQL)
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

The setup automatically:
- Initializes the MySQL database
- Runs `python init_db.py` on startup
- Configures Flask with MySQL connection
- Exposes the app on http://localhost:5000

### Manual Production Deployment

```bash
# Set environment variables
export FLASK_ENV=production
export MYSQL_PASSWORD=your_password
export MYSQL_HOST=your_mysql_host
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 60 wsgi:app
```

---

## Testing

### Test Scenario: Character Creation & Trading

1. Sign up with `DEMO-001`
2. View character dashboard at `/`
3. Note starting ability scores and AC
4. Navigate to `/fellowship/` market
5. Upload an image at `/fellowship/artist`
6. Verify artwork appears in inventory
7. Sell artwork from inventory, it moves to market
7. Check `/fellowship/market`, will see owned artwork, and any other artwork for sale
8. If the day is incremented by ADMIN, there is a chance an NPC will buy artwork while on the market
9. Once artwork is bought, credits are transferred to profile, and artwork is transferred to NPC
10. Admin: Log in with `ADMIN-001` and check `/admin` for transaction logs
11. Admin: `/fellowship/admin` can increment days, which triggers NPC artwork buy logic

### Expected Outcomes

- Character loads with D&D ability scores
- Images upload successfully (max 16MB due to MEDIUMBLOB)
- Prices update daily based on NPC trading
- Admin panel shows user and transaction data

---

## Reliability / Operational Considerations

**Password Security**
- Uses Werkzeug scrypt hashing (high entropy, slow-to-compute)
- Passwords stored at 255-char column width (accommodates modern hash algorithms)

**Database Selection**
- Detects `MYSQL_PASSWORD` env var; uses MySQL if set, otherwise SQLite
- No manual database selection required—automatic fallback ensures dev works without setup

**Data Persistence**
- SQLite: Single file (`neuronet.db`)
- Docker: MySQL volume mounted at `db_data/` (survives container restart)
- Demo data auto-installed via `init_db.py`

**Environmental Isolation**
- All secrets (database passwords, Flask SECRET_KEY) read from environment variables
- `.env` file excluded via `.gitignore`
- `.env.example` provided as configuration template

**Image Storage**
- Artwork stored as MEDIUMBLOB (16MB limit per image)
- Binary data handled correctly across SQLite and MySQL
- Mimetype tracked for proper rendering

**Price Simulation**
- Monte Carlo algorithm with daily randomization
- NPC buying behavior prevents prices from stagnating
- Daily logs archive price history for auditing

---

## Known Limitations

- **Single-threaded Market**: NPC decisions calculated during day progression; no concurrent trading logic.
- **Artwork Size**: Maximum 16MB per image due to MySQL MEDIUMBLOB. Larger files require LONGBLOB or cloud storage.
- **NPCs Limited**: Five hardcoded NPC participants; scaling to dynamic NPCs would require redesigned trading logic.
- **No Rate Limiting**: Authentication endpoints lack rate limiting; open to brute force until implemented.
- **Not Officially Web Hosted**: Demo only currently, not officially hosted on a domain webpage.

---

## Future Improvements

**Features**
- [ ] WebSocket support for real-time price updates
- [ ] Mobile-responsive UI overhaul (current: desktop-focused)
- [ ] Search/filtering in marketplace
- [ ] Player-to-player messaging system
- [ ] More ingame interactive webpages

**Infrastructure**
- [ ] Kubernetes deployment manifests
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Structured logging (JSON format)

**Scaling**
- [ ] Database read replicas
- [ ] Async job queue (Celery) for NPC market updates
- [ ] Load balancing for horizontal scaling

**Security**
- [ ] Input validation hardening

---

## Notes

**Purpose**: Built as a creative project for home DnD game, upgraded to demo for a portfolio project to demonstrate full-stack Flask development, database design, Docker containerization, and DevOps practices.

**Highlights**:
- Security-first approach (no hardcoded secrets, environment-based configuration)
- Database flexibility (SQLite ↔ MySQL toggle via single env var)
- Containerized from the start (Docker Compose, Gunicorn)

**Design Decisions**:
- SQLAlchemy ORM over raw SQL for type safety and migration support
- Blueprint-based routing for modularity and testability
- NPC buying logic to simulate dynamic market
- Access codes for controlled signup 



