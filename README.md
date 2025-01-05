# Hogwarts Database Performance Testing

A Python project comparing SQLAlchemy and psycopg2 performance using a Harry Potter spells database.

## Project Overview

This project demonstrates database interaction patterns in Python using two popular libraries: SQLAlchemy and psycopg2. It uses a fun Harry Potter themed database to showcase real-world performance differences between these approaches.

## Features

- Azure Function implementation with HTTP triggers
- Performance comparison between SQLAlchemy and psycopg2
- Sample database with Harry Potter spells
- Modular code structure
- Azure AD authentication support
-OOP 
## Project Structure

```
hogwarts_db/
├── config/
│   └── database_config.py      # Database configuration settings
├── utils/
│   ├── __init__.py
│   ├── db_manager.py          # Database connection management
│   └── performance_tester.py   # Query performance testing
├── data/
│   └── sample_data.py         # Sample spells data
├── function_app.py            # Main Azure Function implementation
└── requirements.txt           # Project dependencies
```

## Setup

1. Clone the repository
2. Update database configuration in `config/database_config.py`
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Initialize the database:
```bash
python function_app.py
```

## Usage

### Running Performance Tests

Make HTTP requests to the function endpoint:
```
GET /api/compare_queries?query_type=SELECT
GET /api/compare_queries?query_type=COMPLEX
```

### Sample Response

```json
{
    "query_type": "SELECT",
    "performance_comparison": {
        "sqlalchemy": {
            "execution_time": "0.15 seconds",
            "rows_retrieved": 10
        },
        "psycopg2": {
            "execution_time": "0.10 seconds",
            "rows_retrieved": 10
        },
        "difference": {
            "percentage": "50.0%",
            "faster_method": "Psycopg2"
        }
    }
}
```

## Dependencies

- azure-functions
- sqlalchemy
- psycopg2-binary
- pandas

## Contributing

Feel free to submit issues and enhancement requests!

## License
Open source
