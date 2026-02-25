"""
Configuration settings for Neuronet application.
Supports development, testing, and production environments.
"""

import os
from urllib.parse import quote

# Get environment - default to development
FLASK_ENV = os.getenv('FLASK_ENV', 'development')


class Config:
    """Base configuration - shared across all environments"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours in seconds
    
    # Database settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Application settings
    DATABASE_NAME = "AetherVoid"


class DevelopmentConfig(Config):
    """Development configuration"""
    
    DEBUG = True
    TESTING = False
    
    # Development database - try MySQL, fall back to SQLite
    db_password = os.getenv('MYSQL_PASSWORD', '')
    
    if db_password:
        # Use MySQL if password is provided
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://root:{quote(db_password)}@localhost/AetherVoid"
        )
    else:
        # Fall back to SQLite for easy local development
        SQLALCHEMY_DATABASE_URI = "sqlite:///neuronet.db"
    
    print(f"[Config] Using {'MySQL' if db_password else 'SQLite'} database")


class TestingConfig(Config):
    """Testing configuration"""
    
    DEBUG = True
    TESTING = True
    
    # Use in-memory SQLite for tests
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    """Production configuration"""
    
    DEBUG = False
    TESTING = False
    
    # Production must have database configured via environment
    db_password = os.getenv('MYSQL_PASSWORD')
    
    # Only check for password when actually needed
    if not db_password and FLASK_ENV == 'production':
        raise ValueError(
            "MYSQL_PASSWORD environment variable must be set for production!"
        )
    
    if db_password:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://root:{quote(db_password)}@{os.getenv('MYSQL_HOST', 'localhost')}/AetherVoid"
        )
    else:
        # Fallback for non-production environments
        SQLALCHEMY_DATABASE_URI = "sqlite:///neuronet.db"


# Select configuration based on environment
config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

current_config = config_map.get(FLASK_ENV, DevelopmentConfig)
