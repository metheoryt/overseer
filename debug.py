from datetime import datetime as dt

from raekwon.source import RecordSource
import marshmallow as ma
from marshmallow import fields as f
import pandas as pd
from raekwon import configure


configure(dsn='postgresql+psycopg2://postgres:postgres@localhost/postgres', echo=True)


class BobRecords(RecordSource):

    class BobRecordSchema(ma.Schema):

        id = f.Str()
        sum = f.Decimal(places=2)
        name = f.Str()
        date = f.DateTime()

    name = 'bob'

    pk_name = 'id'

    date_name = 'date'

    schema = BobRecordSchema()

    def fetch_data(self, dfrom: dt, dto: dt):
        return pd.DataFrame([
            [1, 10.01, 'eagle', dt(2019, 1, 1, 12, 40, 0)],
            [2, 12.3, None, dt(2019, 1, 1, 13, 42, 11)],
            [3, None, 'bull', dt(2019, 1, 1, 14, 2, 37)],
            [4, None, None, None],
            [5, 100, 'mouse', dt(2019, 1, 2, 14, 2, 22)],
            [5, 100, 'mouse', dt(2019, 1, 2, 18, 3, 44)],
            [None, 101, 'tiger', dt(2019, 1, 2, 18, 3, 44)],
        ], columns=['id', 'sum', 'name', 'date'])

    def query(self, dfrom: dt, dto: dt, q):
        return q
