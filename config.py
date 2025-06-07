"""Configuration settings for the project"""

import os
from dotenv import load_dotenv

load_dotenv()

# Bank app configurations
BANKS_CONFIG = {
    'CBE': {
        'name': 'Commercial Bank of Ethiopia',
        'app_id': 'com.cbe.mobile',
        'full_name': 'CBE Mobile Banking'
    },
    'BOA': {
        'name': 'Bank of Abyssinia',
        'app_id': 'com.boa.mobile',
        'full_name': 'BOA Mobile Banking'
    },
    'DASHEN': {
        'name': 'Dashen Bank',
        'app_id': 'com.dashen.mobile',
        'full_name': 'Dashen Mobile Banking'
    }
}

# Database configuration
DB_CONFIG = {
    'host': os.getenv('ORACLE_HOST', 'localhost'),
    'port': int(os.getenv('ORACLE_PORT', 1521)),
    'service': os.getenv('ORACLE_SERVICE', 'XE'),
    'user': os.getenv('ORACLE_USER'),
    'password': os.getenv('ORACLE_PASSWORD')
}

# Scraping configuration
SCRAPING_CONFIG = {
    'max_reviews_per_bank': int(os.getenv('MAX_REVIEWS_PER_BANK', 400)),
    'delay_between_requests': int(os.getenv('DELAY_BETWEEN_REQUESTS', 1)),
    'language': 'en',
    'country': 'et'
}

# File paths
DATA_PATHS = {
    'raw_data': 'data/raw/',
    'processed_data': 'data/processed/',
    'output': 'output/',
    'reports': 'reports/'
}
