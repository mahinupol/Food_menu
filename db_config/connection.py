"""
Database Connection Configuration for Smart Digital Food Menu
Handles connection setup for both SQLite and MySQL databases
"""

import os
import sqlite3
from typing import Optional

# Try to import MySQL connector
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    mysql = None
    print("MySQL connector not available, falling back to SQLite")


class DatabaseConfig:
    """Database configuration and connection management"""
    
    # SQLite Configuration (Development/Testing)
    SQLITE_CONFIG = {
        'database': 'smart_food_menu.db'
    }
    
    # MySQL Configuration (Production)
    MYSQL_CONFIG = {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'port': int(os.getenv('MYSQL_PORT', 3306)),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DATABASE', 'smart_food_menu'),
        'charset': 'utf8mb4',
        'autocommit': True
    }
    
    # Environment-based database selection
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')  # 'mysql' or 'sqlite'
    
    @classmethod
    def get_sqlite_connection(cls) -> Optional[sqlite3.Connection]:
        """Create and return SQLite database connection"""
        try:
            # Use check_same_thread=False to allow usage across threads
            connection = sqlite3.connect(cls.SQLITE_CONFIG['database'], check_same_thread=False)
            connection.row_factory = sqlite3.Row  # Enable dict-like access to rows
            print("Successfully connected to SQLite database")
            return connection
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite: {e}")
            return None
    
    @classmethod
    def get_mysql_connection(cls):
        """Create and return MySQL database connection"""
        if not MYSQL_AVAILABLE or mysql is None:
            print("MySQL not available, falling back to SQLite")
            return None
            
        try:
            connection = mysql.connector.connect(**cls.MYSQL_CONFIG)
            print("Successfully connected to MySQL database")
            return connection
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    @classmethod
    def get_connection(cls):
        """Get database connection based on environment configuration"""
        if cls.DATABASE_TYPE == 'mysql' and MYSQL_AVAILABLE:
            conn = cls.get_mysql_connection()
            if conn:
                return conn
            else:
                print("Falling back to SQLite")
                return cls.get_sqlite_connection()
        else:
            return cls.get_sqlite_connection()
    
    @classmethod
    def close_connection(cls, connection):
        """Close database connection"""
        if connection:
            try:
                connection.close()
                print("Database connection closed")
            except Exception as e:
                print(f"Error closing connection: {e}")