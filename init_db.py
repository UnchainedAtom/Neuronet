"""
Initialize Neuronet Database with Default Data

This script creates the database tables and populates them with
initial data needed for the application to function.

Usage:
    python init_db.py
"""

import sys
import os
from pathlib import Path

# Add current directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from __init__ import create_app
from database import db, AccessCode, vDate, WebsiteRole, User
from werkzeug.security import generate_password_hash
from auth import createStats


def init_database():
    """Initialize database with tables and initial data"""
    
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("Initializing Neuronet Database")
        print("="*60)
        
        # Create all tables
        print("\n[1/4] Creating database tables...")
        try:
            db.create_all()
            print("     ✓ Tables created successfully")
        except Exception as e:
            print(f"     ✗ Error creating tables: {e}")
            sys.exit(1)
        
        # Create initial vDate if it doesn't exist
        print("\n[2/4] Setting up game date...")
        try:
            existing_date = vDate.query.get(1)
            if not existing_date:
                initial_date = vDate(id=1, year=1907, day=108, indexDate=1907)
                db.session.add(initial_date)
                db.session.commit()
                print("     ✓ Initial game date set (Aether Date 108:1907)")
            else:
                print("     ℹ Game date already initialized")
        except Exception as e:
            print(f"     ✗ Error setting up date: {e}")
            sys.exit(1)
        
        # Create default roles
        print("\n[3/4] Setting up user roles...")
        try:
            existing_roles = WebsiteRole.query.all()
            if not existing_roles:
                roles = [
                    WebsiteRole(role='ADMIN'),
                    WebsiteRole(role='FELLARTIST'),
                    WebsiteRole(role='USER'),
                ]
                db.session.add_all(roles)
                db.session.commit()
                print("     ✓ Roles created: ADMIN, FELLARTIST, USER")
            else:
                print("     ℹ Roles already exist")
        except Exception as e:
            print(f"     ✗ Error creating roles: {e}")
            sys.exit(1)
        
        # Create sample access codes
        print("\n[4/4] Creating sample access codes...")
        try:
            existing_codes = AccessCode.query.all()
            if not existing_codes:
                sample_codes = [
                    AccessCode(code='DEMO-001'),
                    AccessCode(code='DEMO-002'),
                    AccessCode(code='DEMO-003'),
                    AccessCode(code='ADMIN-001'),
                ]
                db.session.add_all(sample_codes)
                db.session.commit()
                print("     ✓ Sample access codes created:")
                print("       - DEMO-001")
                print("       - DEMO-002")
                print("       - DEMO-003")
                print("       - ADMIN-001")
            else:
                print("     ℹ Access codes already exist")
        except Exception as e:
            print(f"     ✗ Error creating access codes: {e}")
            sys.exit(1)
        
        # Create NPC market participants
        print("\n[5/5] Creating NPC market participants...")
        try:
            npc_names = [
                'Collector_Vex',
                'TradeMaster_Zyn',
                'Investor_Kael',
                'GalleryScan_IX',
                'Curator_Nyx'
            ]
            
            existing_npcs = User.query.filter(User.userName.in_(npc_names)).count()
            if existing_npcs < len(npc_names):
                newly_created = []
                for npc_name in npc_names:
                    existing_npc = User.query.filter_by(userName=npc_name).first()
                    if not existing_npc:
                        # Create NPC with a dummy password, starting credits
                        npc = User(userName=npc_name, password=generate_password_hash('npc_bot_account'))
                        npc.currentCredits = 5000.00  # Starting budget for NPC buyers
                        db.session.add(npc)
                        newly_created.append(npc_name)
                db.session.commit()
                
                # Now initialize stats for all NPCs
                for npc_name in newly_created:
                    npc_user = User.query.filter_by(userName=npc_name).first()
                    if npc_user:
                        createStats(npc_user)
                db.session.commit()
                
                print("     ✓ NPC market participants created:")
                for npc_name in npc_names:
                    print(f"       - {npc_name}")
            else:
                print("     ℹ NPC participants already exist")
        except Exception as e:
            print(f"     ✗ Error creating NPCs: {e}")
            sys.exit(1)
        
        print("\n" + "="*60)
        print("✓ Database initialization complete!")
        print("="*60)
        print("\nYou can now:")
        print("  1. Start the application: python app.py")
        print("  2. Sign up using one of the access codes above")
        print("  3. Access admin panel at /admin (if given ADMIN role)\n")


if __name__ == '__main__':
    init_database()
