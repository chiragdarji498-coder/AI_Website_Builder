import os


class Config:
    """Base configuration"""

    SECRET_KEY = "default-dev-secret-key"

    DEBUG = False
    TESTING = False

    # Groq API Key
    GROQ_API_KEY = "YOUR_GROQ_API_KEY"

    # Web3Forms Key
    WEB3FORMS_KEY = "YOUR_PUBLIC_API_KEY_HERE"

    # Paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    GENERATED_DIR = os.path.join(BASE_DIR, "static", "generated")


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = "change-this-secret-key"


config_by_name = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig
}
