import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'workspace.db')
    N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL', '')
    N8N_TIMEOUT = int(os.getenv('N8N_TIMEOUT', '30'))


class TestConfig(Config):
    TESTING = True
    DATABASE_PATH = ':memory:'


def get_config(config_name=None):
    configs = {
        'default': Config,
        'testing': TestConfig,
    }
    return configs.get(config_name, Config)
