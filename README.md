# FastAPI Channel Stats API

This project is a FastAPI-based API for retrieving channel statistics from time series data stored in a Parquet file. It uses Polars for efficient data loading and xarray for time series operations.
Technical challenge by NNergix and GE.

## Features

- Retrieve available channels with optional type filtering
- Calculate statistics (mean, std, min, max, count) for specified channels
- Filter statistics by date range
- Efficient data handling with Polars and xarray

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- Polars
- pytest

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/belochenko/channelstats-api
   cd channelstats-api
   ```

2. Create a virtual environment and activate it:
   ```
   python3.10 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration
0. Bring your parquet data into `data` folder and rename Parquet file into `data/service_data.parquet`
1. Create a `.env` file in the project root and set the path to your Parquet file:
   ```
   DATA_FILE=data/service_data.parquet
   ```

# Documentation
Detailed documentation for the API and its components can be found in the source code itself.
Each module contains docstrings that explain its purpose, usage, and parameters.

## Running the Application

To run the application locally:

Preferably
```
fastapi dev app/main.py
```

OR

```
uvicorn app.main:app --reload
```


The API will be available at `http://localhost:8000`.

## API Endpoints

1. Get Channels
   - Endpoint: `/channels`
   - Method: GET
   - Query Parameters:
     - `channel_type` (optional): Filter channels by type

2. Get Statistics
   - Endpoint: `/stats`
   - Method: GET
   - Query Parameters:
     - `channels` (optional): List of channel names to calculate stats for
     - `start_date` (optional): Start date for the stats calculation (format: YYYY-MM-DD)
     - `end_date` (optional): End date for the stats calculation (format: YYYY-MM-DD)

## Running Tests

To run the test suite:

```
pytest
```

For a coverage report:

```
pytest --cov=app --cov-report=term-missing
```

OR
```
python -m coverage report
```

Test coverage:

```
➜ python -m coverage report
Name                           Stmts   Miss  Cover
--------------------------------------------------
app/__init__.py                    0      0   100%
app/config.py                      4      0   100%
app/main.py                        8      0   100%
app/routes/channels.py            11      0   100%
app/routes/stats.py               30      2    93%
app/services/data_service.py      41      4    90%
tests/test_channels.py            19      0   100%
tests/test_config.py               6      0   100%
tests/test_data_service.py        15      0   100%
tests/test_main.py                 6      0   100%
tests/test_stats.py               71      0   100%
--------------------------------------------------
TOTAL                            211      6    97%
```
