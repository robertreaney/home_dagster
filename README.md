# Dagster Data Pipelines

# Production Notes

- standup: `docker compose up --build`
- run: `bash run.sh`

# Folder Structure

```
project-root/
│
├── .vscode
├── data
├── src/ 
│   ├── database/                   ## Database ##
│   │   └── init.sql                # Initialization logic
│   │
│   ├── etl/                        ## Data Pipeline ##
│   │   ├── assets/                 # Dagster code goes here
│   │   │   ├── helloworld.py       # Example asset
│   │   │   └── iris_pipeline.py    # Example pipeline
│   │   │
│   │   ├── sql/                    # Pipeline SQL scripts
│   │   │   └── 0_test.sql
│   │   │
│   │   └── utils/                  # Utility functions
│   │
│   └── tests/                      ## Testing ##
│
├── .env                        
├── .gitignore                    
├── dagster.yaml                  
├── docker-compose.yaml            
├── pyproject.toml                  
├── README.md                       
├── requirements.txt                
├── setup.cfg                      
└── setup.py 
```


# Pipeline Development

## Standup Dagster Locally

1. Create a python virtual env
    
    `python -m venv .venv`

2. Activate env

    `source .venv/bin/activate`

3. Install deps

    `pip install -e ".[dev]"`

4. Start dagster. this will make ui available at `localhost:3000`

    - native: `dagster dev`
    - containerized: `docker compose up --build`


## Creating Jobs

Dagster runs based off "assets" that are 1-to-1 representations of data artifacts (tables, files, etc.)

1. Create an asset
    - Files in `src/etl/assets` will be consumed by dagster to create workflows
2. Materialize and asset
    - Manually from UI with `materialize` button
    - Run script locally to test functionality
    - **Note**: If you create files with dagster jobs, they will be owned by `root` and not your user. This will cause future debugger sessions to fail if they leverage those files.

## Developer Notes

1. Add new python deps to `setup.py`

2. Run tests with `pytest`
    - Note: You need dagster running locally to run test