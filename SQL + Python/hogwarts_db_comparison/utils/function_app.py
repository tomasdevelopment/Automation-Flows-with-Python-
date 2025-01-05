# function_app.py

import azure.functions as func
import logging
import json
from sqlalchemy import MetaData, Table, Column, Integer, String, Text
from config.database_config import HOGWARTS_DB_CONFIG
from utils.db_manager import DatabaseManager
from utils.performance_tester import QueryPerformanceTester
from data.sample_data import SAMPLE_SPELLS

app = func.FunctionApp()

@app.function_name(name="compare_spell_queries")
@app.route(route="compare_queries")
def compare_spell_queries(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger function that compares query performance between SQLAlchemy and psycopg2"""
    try:
        # Initialize database manager
        db_manager = DatabaseManager(HOGWARTS_DB_CONFIG)
        
        # Initialize performance tester
        tester = QueryPerformanceTester(db_manager)
        
        # Get query type from request (default to 'SELECT')
        query_type = req.params.get('query_type', 'SELECT')
        
        # Run performance tests
        sa_rows, sa_time = tester.run_sqlalchemy_query(query_type)
        pg_rows, pg_time = tester.run_psycopg2_query(query_type)
        
        # Calculate performance difference
        time_diff = sa_time - pg_time
        percentage_diff = abs(time_diff / pg_time * 100)
        
        # Prepare response
        response_data = {
            'query_type': query_type,
            'performance_comparison': {
                'sqlalchemy': {
                    'execution_time': f"{sa_time:.2f} seconds",
                    'rows_retrieved': sa_rows
                },
                'psycopg2': {
                    'execution_time': f"{pg_time:.2f} seconds",
                    'rows_retrieved': pg_rows
                },
                'difference': {
                    'percentage': f"{percentage_diff:.1f}%",
                    'faster_method': 'Psycopg2' if time_diff > 0 else 'SQLAlchemy'
                }
            }
        }
        
        return func.HttpResponse(
            body=json.dumps(response_data),
            mimetype="application/json",
            status_code=200
        )
        
    except Exception as e:
        error_message = f"Error in query comparison: {str(e)}"
        logging.error(error_message)
        return func.HttpResponse(
            body=json.dumps({"error": error_message}),
            mimetype="application/json",
            status_code=500
        )
    finally:
        if 'db_manager' in locals():
            db_manager.cleanup()

def initialize_spells_table():
    """Helper function to initialize the spells table with sample data"""
    db_manager = DatabaseManager(HOGWARTS_DB_CONFIG)
    engine = db_manager.get_sqlalchemy_engine()
    
    # Create schema if it doesn't exist
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {HOGWARTS_DB_CONFIG['schema']};"))
    
    # Define the spells table
    metadata = MetaData(schema=HOGWARTS_DB_CONFIG['schema'])
    spells_table = Table(
        HOGWARTS_DB_CONFIG['table_name'],
        metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(100), nullable=False, unique=True),
        Column('incantation', String(100)),
        Column('effect', Text),
        Column('type', String(50)),
        Column('difficulty', Integer),
        Column('creator', String(100))
    )
    
    # Create table and insert sample data
    metadata.create_all(engine)
    
    with engine.connect() as conn:
        for spell in SAMPLE_SPELLS:
            conn.execute(
                spells_table.insert().values(**spell)
            )
        conn.commit()
    
    db_manager.cleanup()

if __name__ == "__main__":
    # Initialize the database with sample data
    initialize_spells_table()
