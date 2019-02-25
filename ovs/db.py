from itertools import chain

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
import sqlalchemy as sa


metadata = MetaData()
Session = scoped_session(sessionmaker())
Base = declarative_base(metadata=metadata)


def make_source_model(name, additional_cols: list):

    basic_model_columns = (
        sa.Column('shared_id', sa.String(), primary_key=True, nullable=False, unique=True),
        sa.Column('date', sa.DateTime(timezone=False), nullable=False)
    )

    return sa.Table(
        name, metadata,
        chain(basic_model_columns, additional_cols)
    )
