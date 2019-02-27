from datetime import datetime

import marshmallow as ma
import sqlalchemy as sa
from marshmallow import fields as f
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

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

    for k, field in fields.items():
        col = reflect_field_to_column(field)
        columns.append(col)

    return columns


def make_table_from_schema(name, schema: ma.Schema):

    basic_model_columns = (
        sa.Column('pk', sa.String(), primary_key=True, nullable=False, unique=True),
        # если дата вставки и дата обновления отличаются
        # это повод выкинуть операцию в результаты сверки
        sa.Column('date_create', sa.DateTime, default=datetime.now),
        sa.Column('last_update', sa.DateTime, onupdate=datetime.now),
    )

    additional_cols = extract_columns_from_schema(schema)

    table = sa.Table(name, metadata, *basic_model_columns, *additional_cols)

    return table
