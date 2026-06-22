import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key')
    DEBUG = False
    TESTING = False
    
    # AI API Keys
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    WEB3FORMS_KEY = os.environ.get('WEB3FORMS_KEY', 'YOUR_PUBLIC_API_KEY_HERE')
    
    # Paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    GENERATED_DIR = os.path.join(BASE_DIR, 'static', 'generated')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Ensure strong secret key in production
    SECRET_KEY = os.environ.get('SECRET_KEY')

# Dictionary to easily select environments
config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)