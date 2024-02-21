# OKX Data Engineering
Utilizing Python to ingest data from the OKX provider via API.

## Table of Contents
- [Setup](#setup)
- [Run](#run)
- [CI](#ci)
- [Limitations](#limitations)
- [References](#references)
---

## Setup
1. Clone the repository

2. Go to the project root path:
```
cd okx-data-engineering
```

3. Create a virtual environment:
```
python3 -m venv okx-data-engineering-venv
```

4. Activate the virtual environment:
```
source okx-data-engineering-venv/bin/activate
```

5. Install the dependencies:
```
pip install -r requirements.txt
```

## Run
1. Set up the configuration in `config/base.ini`
    - ingestion_method:
        - `FULL_LOAD`
        - `INCREMENTAL_LOAD`
    - start_id:
        - empty string -> default value
        - User-defined values
    - end_id:
        - empty string -> default value
        - User-defined values
    - instrument_id
        - default value: `XRP-USDT`
        - User-defined values
2. Go to the main
    ```
    cd okx-data-engineering/main.py
    ```
3. Run Python
    ```
    python main.py
    ```

## CI
- After pushing to the main branch or creating a pull request to main on GitHub, the GitHub action will be triggered to start the Continuous Integration (CI) process. This involves setting up the Python environment and automatically running unit tests.

## Limitations
- There are steps to run full load and incremental load consecutively.
- We can define only one instrument ID for each data ingestion time. If we want to ingest another instrument ID, we need to manually remove the file in the `data/raw/` folder directly.
- The instrument ID needs to be configured in the config/base.ini file, referencing the config/instrument_id.csv file.

## References
- [OKX API DOC - Trade History](https://www.okx.com/docs-v5/en/#order-book-trading-market-data-get-trades-history)