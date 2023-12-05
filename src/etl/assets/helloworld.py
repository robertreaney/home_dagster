from dagster import asset
import logging
import json
from pathlib import Path
from datetime import datetime

from dagster import MaterializeResult

@asset(group_name="demo", compute_kind="Python")
def helloworld() -> None:
    logging.info('Hello World')
    Path('data').mkdir(exist_ok=True, parents=True)
    with open('data/helloworld.json', 'w') as f:
        json.dump({'hello': 'world!', 'timestamp': datetime.now().strftime('%Y-%m-%d')}, f)

    # this return object provides more information to the workflow
    return MaterializeResult(
        metadata={
            'timestamp': datetime.now().strftime('%Y-%m-%d'),
            'cwd': str(Path.cwd())
        }
    )

if __name__ == '__main__':
    helloworld()