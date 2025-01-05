# utils/performance_tester.py

import time
import logging
from sqlalchemy import MetaData, Table, select
from .db_manager import DatabaseManager

class QueryPerformanceTester:
    """Simple class to test query performance between SQLAlchemy and psycopg2"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def compare_queries(self):
        """Runs simple SELECT ALL queries and compares performance"""
        results = {}
        
        try:
            # 1. SQLAlchemy Query
            start_time = time.time()
            engine = self.db_manager.get_sqlalchemy_engine()
            
            metadata = MetaData(schema=self.db_manager.config['schema'])
            table = Table(
                self.db_manager.config['table_name'],
                metadata,
                autoload_with=engine
            )
            stmt = select(table)
            
            with engine.connect() as connection:
                sa_result = connection.execute(stmt).fetchall()
            sqlalchemy_time = time.time() - start_time
            results['sqlalchemy'] = {
                'time': sqlalchemy_time,
                'rows': len(sa_result)
            }

            # 2. Psycopg2 Query
            conn = self.db_manager.get_psycopg2_connection()
            start_time = time.time()
            cur = conn.cursor()
            query = f"""
                SELECT * FROM {self.db_manager.config['schema']}.{self.db_manager.config['table_name']}
            """
            cur.execute(query)
            pg_result = cur.fetchall()
            psycopg2_time = time.time() - start_time
            results['psycopg2'] = {
                'time': psycopg2_time,
                'rows': len(pg_result)
            }

            # Calculate difference
            time_diff = sqlalchemy_time - psycopg2_time
            percentage_diff = abs(time_diff / psycopg2_time * 100)
            
            results['comparison'] = {
                'difference_percentage': percentage_diff,
                'faster_method': 'Psycopg2' if time_diff > 0 else 'SQLAlchemy'
            }

            # Log results
            logging.info("\n=== Query Performance Comparison ===")
            logging.info(f"SQLAlchemy Time: {sqlalchemy_time:.2f} seconds")
            logging.info(f"Psycopg2 Time: {psycopg2_time:.2f} seconds")
            logging.info(f"Difference: {percentage_diff:.1f}%")
            logging.info(f"Faster Method: {results['comparison']['faster_method']}")
            logging.info(f"Rows Retrieved: {results['psycopg2']['rows']}")

            return results

        except Exception as e:
            logging.error(f"Error in performance comparison: {str(e)}")
            raise
