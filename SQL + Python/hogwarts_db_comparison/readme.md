# Python SQL Performance Testing

A practical comparison of SQLAlchemy and psycopg2 performance with real-world data.

## Overview

This project demonstrates a real-world performance comparison between two popular Python SQL libraries using a dataset of 30,000 rows. The comparison showcases the trade-offs between raw performance and developer convenience.

## Performance Results

From our tests with 30,000 rows:
```
=== Query Performance Comparison (SELECT ALL) ===
SQLAlchemy Query Time: 59.67 seconds
Psycopg2 Query Time: 51.36 seconds
Psycopg2 was faster by 16.2%
```

## Project Structure

```
SQL_Python/
└── hogwarts_db_comparison/
    ├── config/
    │   └── database_config.py        # Database configuration
    ├── utils/
    │   ├── __init__.py
    │   ├── db_manager.py            # Connection management
    │   └── performance_tester.py     # Simplified performance testing
    └── function_app.py              # Azure Function implementation
```

## Features

- Simple performance comparison between SQLAlchemy and psycopg2
- Real-world testing with large datasets
- Azure Function implementation
- Clean, modular code structure

## Setup

1. Clone the repository
2. Update database configuration:
```python
# config/database_config.py
db_config = {
    'user': 'your_user',
    'host': 'your_host',
    'port': '5432',
    'dbname': 'your_db'
}
```
3. Install dependencies:

pip install azure-functions sqlalchemy psycopg2-binary
```

## Usage

Make a request to the Azure Function endpoint:
```
GET /api/compare_spells
```

Sample Response:
```json
{
    "comparison_results": {
        "sqlalchemy": "59.67 seconds",
        "psycopg2": "51.36 seconds",
        "difference": "16.2%",
        "faster_method": "Psycopg2",
        "rows_retrieved": 30000
    }
}
```

## Dependencies
- azure-functions
- sqlalchemy
- psycopg2-binary

## License
Open Source License
