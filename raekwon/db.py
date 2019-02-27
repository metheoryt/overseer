from itertools import chain

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
import sqlalchemy as sa
import marshmallow as ma
from marshmallow import fields as f
from datetime import datetime


metadata = MetaData()
Session = scoped_session(sessionmaker())
Base = declarative_base(metadata=metadata)


def reflect_field_to_column(fd: f.Field):
    ct = sa.String()

    if isinstance(fd, f.Decimal):
        ct = sa.Numeric(scale=fd.places, decimal_return_scale=fd.places)
    elif isinstance(fd, f.Bool):
        ct = sa.Boolean()
    elif isinstance(fd, f.DateTime):
        ct = sa.DateTime()
    elif isinstance(fd, f.Date):
        ct = sa.Date()
    elif isinstance(fd, f.Float):
        ct = sa.Float()
    elif isinstance(fd, f.Int):
        ct = sa.Integer()

    return sa.Column(fd.name, ct, nullable=not fd.required, default=fd.default)


def extract_columns_from_schema(schema: ma.Schema):
    fields = schema.fields
    """:type: list[f.Field]"""

    columns = []

    for field in fields:
        col = reflect_field_to_column(field)
        columns.append(col)

    return columns


def make_table_from_schema(name, schema: ma.Schema):

    basic_model_columns = (
        sa.Column('sid', sa.String(), primary_key=True, nullable=False, unique=True),
        # sa.Column('last_update', sa.DateTime, onupdate=datetime.now)
    )

    additional_cols = extract_columns_from_schema(schema)

    table = sa.Table(
        name, metadata,
        chain(basic_model_columns, additional_cols)
    )

    return table
