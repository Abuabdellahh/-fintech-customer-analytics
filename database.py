"""
Database operations for Oracle database
"""

import oracledb
import pandas as pd
import logging
from typing import Optional
import os

from .config import DB_CONFIG, DATA_PATHS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OracleDBManager:
    """Oracle database manager for storing review data"""
    
    def __init__(self):
        self.config = DB_CONFIG
        self.connection = None
        
    def connect(self) -> bool:
        """Establish connection to Oracle database"""
        try:
            dsn = f"{self.config['host']}:{self.config['port']}/{self.config['service']}"
            self.connection = oracledb.connect(
                user=self.config['user'],
                password=self.config['password'],
                dsn=dsn
            )
            logger.info("Successfully connected to Oracle database")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Oracle database: {e}")
            return False
    
    def create_schema(self):
        """Create database schema"""
        if not self.connection:
            logger.error("No database connection")
            return False
            
        try:
            cursor = self.connection.cursor()
            
            # Create Banks table
            banks_table_sql = """
            CREATE TABLE banks (
                bank_id VARCHAR2(10) PRIMARY KEY,
                bank_name VARCHAR2(100) NOT NULL,
                app_name VARCHAR2(100),
                app_id VARCHAR2(100),
                created_date DATE DEFAULT SYSDATE
            )
            """
            
            # Create Reviews table
            reviews_table_sql = """
            CREATE TABLE reviews (
                review_id VARCHAR2(100) PRIMARY KEY,
                bank_id VARCHAR2(10),
                review_text CLOB,
                rating NUMBER(1) CHECK (rating BETWEEN 1 AND 5),
                review_date DATE,
                user_name VARCHAR2(100),
                thumbs_up NUMBER DEFAULT 0,
                sentiment_label VARCHAR2(20),
                sentiment_score NUMBER(3,2),
                primary_theme VARCHAR2(50),
                word_count NUMBER,
                created_date DATE DEFAULT SYSDATE,
                FOREIGN KEY (bank_id) REFERENCES banks(bank_id)
            )
            """
            
            try:
                cursor.execute(banks_table_sql)
                logger.info("Banks table created successfully")
            except Exception as e:
                if "name is already used" in str(e):
                    logger.info("Banks table already exists")
                else:
                    raise e
            
            try:
                cursor.execute(reviews_table_sql)
                logger.info("Reviews table created successfully")
            except Exception as e:
                if "name is already used" in str(e):
                    logger.info("Reviews table already exists")
                else:
                    raise e
            
            self.connection.commit()
            cursor.close()
            return True
            
        except Exception as e:
            logger.error(f"Error creating schema: {e}")
            return False
    
    def insert_banks_data(self):
        """Insert bank information"""
        if not self.connection:
            return False
            
        try:
            cursor = self.connection.cursor()
            
            banks_data = [
                ('CBE', 'Commercial Bank of Ethiopia', 'CBE', 'com.cbe.mobile'),
                ('BOA', 'Bank of Abyssinia', 'BOA', 'com.boa.mobile'),
                ('DASHEN', 'Dashen Bank', 'DASHEN', 'com.dashen.mobile')
            ]
            
            cursor.executemany(
                "INSERT INTO banks (bank_id, bank_name, app_name, app_id) VALUES (:1, :2, :3, :4)",
                banks_data
            )
            
            self.connection.commit()
            logger.info("Banks data inserted successfully")
            cursor.close()
            return True
            
        except Exception as e:
            logger.error(f"Error inserting banks data: {e}")
            return False

                                                                    