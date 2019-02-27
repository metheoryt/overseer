import pandas as pd
import marshmallow as ma


def test_data_present(bob_raw_data: pd.DataFrame, bob_schema: ma.Schema):
    assert not bob_raw_data.empty
