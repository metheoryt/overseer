import pytest
import pandas as pd
from datetime import datetime as dt
import marshmallow as ma
from marshmallow import fields as f


df = pd.DataFrame([
    [1, 10.01, 'eagle', dt(2019, 1, 1, 12, 40, 0)],
    [2, 12.3, None, dt(2019, 1, 1, 13, 42, 11)],
    [3, None, 'bull', dt(2019, 1, 1, 14, 2, 37)],
    [4, None, None, None],
    [5, 100, 'mouse', dt(2019, 1, 2, 14, 2, 22)],
    [5, 100, 'mouse', dt(2019, 1, 2, 18, 3, 44)],
    [None, 101, 'tiger', dt(2019, 1, 2, 18, 3, 44)],
], columns=['id', 'sum', 'name', 'date'])


@pytest.fixture(scope='session')
def bob_raw_data():
    return df


class BobSchema(ma.Schema):

    id = f.String(required=True)
    sum = f.Decimal(places=2)
    name = f.String()
    date = f.DateTime()


@pytest.fixture(scope='session')
def bob_schema():
    return BobSchema()
