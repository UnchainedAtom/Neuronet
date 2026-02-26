# Neuronet

A sci-fi marketplace sim built with Flask where players trade digital art in an in-game economy. It combines character stat management (D&D 5e style) with a dynamic NFT-like trading system. Think "space barter meets tabletop RPG meets online marketplace."

## What's in here

- **Character System**: Create a character, roll stats, manage abilities like in D&D
- **Fellowship Market**: Buy/sell digital artwork with prices that shift based on NPC trading
- **Secure Auth**: Access codes, role-based permissions, proper password handling
- **Admin Tools**: Manage players, artworks, game progression
- **Database Flexibility**: Works with SQLite locally, MySQL in production (zero fuss setup)
- **Docker Support**: Containerized for easy deployment

## Project structure

```
├── app.py              # Entry point (dev server)
├── wsgi.py            # Entry point (production)
├── __init__.py        # Flask app factory & blueprints
├── auth.py            # Login/signup logic
├── neuroViews.py      # Character system
├── fellViews.py       # Market system
├── database.py        # SQLAlchemy models
├── config.py          # Environment/config handling
├── init_db.py         # Database setup script
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container definition
├── docker-compose.yml # Multi-container setup
├── templates/         # HTML templates
│   ├── neuronet/     # Character UI
│   └── fellowship/   # Market UI
└── static/           # CSS, JS, images
```

## Getting started

You need Python 3.8+ and pip. That's it.

**On Windows:**
```bash
git clone https://github.com/UnchainedAtom/Neuronet
cd Neuronet
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python app.py
```

**On Mac/Linux:**
```bash
git clone https://github.com/UnchainedAtom/Neuronet
cd Neuronet
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
python app.py
```

Then open http://localhost:5000. You'll get a login screen. Use one of the demo codes:
- `DEMO-001`, `DEMO-002`, `DEMO-003` - Regular player accounts
- `ADMIN-001` - Admin account (gets access to /admin)

Obviously change these if you're deploying anywhere public.

## Running it

**Development (default):**
```bash
python app.py
```
Uses SQLite, no extra setup needed.

**Production (if you know what you're doing):**
Set environment variables for MySQL and run with Gunicorn:
```bash
export FLASK_ENV=production
export MYSQL_PASSWORD=your_password
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

**With Docker:**
```bash
docker-compose up -d
```
Waits ~30 seconds for MySQL to start, then you're good to go.

## How it works

### Database

Run `python init_db.py` once to set up everything:
- Creates tables for users, artworks, character stats, etc.
- Sets game date to Aether 108:1907
- Adds 5 NPC traders who buy/sell on their own
- Creates the demo access codes above

Uses SQLite by default (lives in `neuronet.db`). Want MySQL? Set `MYSQL_PASSWORD` as an env var and it'll auto-switch.

### The Neuronet character dashboard

After login, you see your character stats (STR, DEX, CON, INT, WIS, CHA) and can tweak things like AC, HP, and bonuses. Straight out of D&D 5e.

### The Fellowship market

Upload artwork, browse what others made, buy/sell pieces. The market's dynamic—NPCs make their own trades, so prices shift based on what's happening.

### Admin panel

If you log in with `ADMIN-001`, you get `/admin` with tools to manage users, see game stats, progress the day/year, and eyeball transaction logs.

## Security stuff

If you're deploying this live:

1. **Generate a real SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Put it in your `.env` or environment before launching.

2. **Use HTTPS.** Always.

3. **Lock down environment variables.** Never push `.env` files or API keys to GitHub.

4. **Change (or remove) the demo access codes** before going public.

See [SECURITY.md](SECURITY.md) for more details on what got fixed.

## Routes

- `/auth/login` - Sign in here
- `/auth/signUp` - Make an account with an access code
- `/` - Your character dashboard (Neuronet home)
- `/baseline` - Detailed character sheet
- `/neurox` - System hub (gateway to subsystems)
- `/fellowship/` - Market home page
- `/fellowship/inventory` - Your items
- `/fellowship/artist` - Upload art (if you have artist role)
- `/admin` - Management tools (ADMIN-001 only)

## Troubleshooting

**The database file got corrupted?**
Delete `neuronet.db` and run `python init_db.py` again.

**Getting import errors?**
Make sure your virtual environment is activated and you've run `pip install -r requirements.txt`.

**Port 5000 in use?**
```bash
PORT=5001 python app.py
```

**MySQL connection failing?**
Make sure MySQL is running and `MYSQL_PASSWORD` is set. For local dev, just delete `neuronet.db` and use SQLite (the default).

**Weird jinja2 errors?**
Refresh the page or clear your browser cache. Flask in debug mode sometimes gets finicky.

## Next steps

Want to extend this? Look at:
- [SETUP.md](SETUP.md) - Installation & deployment guides
- [SECURITY.md](SECURITY.md) - What vulnerabilities got fixed
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Full feature list & DevOps stuff
