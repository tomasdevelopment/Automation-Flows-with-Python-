# utils/db_manager.py

import logging
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import psycopg2

class DatabaseManager:
    """Manager for database connections and operations"""
    
    def __init__(self, config: Dict[str, Any], access_token: Optional[str] = None):
        self.config = config
        self.access_token = access_token
        self._engine = None
        self._psycopg_conn = None

    def get_sqlalchemy_engine(self) -> Engine:
        """Creates SQLAlchemy engine with proper configuration"""
        if not self._engine:
            connection_string = (
                f"postgresql+psycopg2://{self.config['user']}:{self.access_token or 'password'}"
                f"@{self.config['host']}:{self.config['port']}/{self.config['dbname']}"
            )
            self._engine = create_engine(
                connection_string,
                connect_args={"sslmode": "require"}
            )
        return self._engine

    def get_psycopg2_connection(self):
        """Creates psycopg2 connection with proper configuration"""
        if not self._psycopg_conn:
            self._psycopg_conn = psycopg2.connect(
                dbname=self.config['dbname'],
                user=self.config['user'],
                password=self.access_token or 'password',
                host=self.config['host'],
                port=self.config['port'],
                sslmode='require'
            )
        return self._psycopg_conn

    def set_role(self, role: str) -> None:
        """Sets PostgreSQL role for the current connection"""
        with self.get_sqlalchemy_engine().connect() as conn:
            conn.execute(text(f"SET ROLE {role};"))
            logging.info(f"Role set to '{role}' successfully.")

    def cleanup(self):
        """Closes all database connections"""
        if self._engine:
            self._engine.dispose()
        if self._psycopg_conn:
            self._psycopg_conn.close()
