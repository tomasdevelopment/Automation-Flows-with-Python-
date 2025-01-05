# utils/performance_tester.py

import time
from sqlalchemy import MetaData, Table, text
from .db_manager import DatabaseManager

class QueryPerformanceTester:
    """Class to test and compare query performance between SQLAlchemy and psycopg2"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def run_sqlalchemy_query(self, query_type: str = 'SELECT'):
        """Runs a query using SQLAlchemy and measures performance"""
        start_time = time.time()
        engine = self.db_manager.get_sqlalchemy_engine()
        
        metadata = MetaData(schema=self.db_manager.config['schema'])
        spells_table = Table(
            self.db_manager.config['table_name'],
            metadata,
            autoload_with=engine
        )
        
        with engine.connect() as conn:
            if query_type == 'SELECT':
                result = conn.execute(spells_table.select()).fetchall()
            elif query_type == 'COMPLEX':
                stmt = text("""
                    SELECT type, COUNT(*) as spell_count, AVG(difficulty) as avg_difficulty
                    FROM spells_schema.spells
                    GROUP BY type
                    HAVING AVG(difficulty) > 2
                    ORDER BY avg_difficulty DESC;
                """)
                result = conn.execute(stmt).fetchall()
        
        execution_time = time.time() - start_time
        return len(result), execution_time

    def run_psycopg2_query(self, query_type: str = 'SELECT'):
        """Runs a query using psycopg2 and measures performance"""
        start_time = time.time()
        conn = self.db_manager.get_psycopg2_connection()
        cur = conn.cursor()
        
        if query_type == 'SELECT':
            query = f"""
                SELECT * FROM {self.db_manager.config['schema']}.{self.db_manager.config['table_name']};
            """
        elif query_type == 'COMPLEX':
            query = """
                SELECT type, COUNT(*) as spell_count, AVG(difficulty) as avg_difficulty
                FROM spells_schema.spells
                GROUP BY type
                HAVING AVG(difficulty) > 2
                ORDER BY avg_difficulty DESC;
            """
        
        cur.execute(query)
        result = cur.fetchall()
        execution_time = time.time() - start_time
        return len(result), execution_time
