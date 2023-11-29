from dagster import MaterializeResult
from pathlib import Path
from datetime import datetime

from ...etl.assets.helloworld import helloworld

def test_helloworld():
    assert helloworld() == MaterializeResult(
        metadata={
            'timestamp': datetime.now().strftime('%Y-%m-%d'),
            'cwd': str(Path.cwd())
        }
    )
    assert Path('data/helloworld.json').exists()

if __name__ == '__main__':
    test_helloworld()