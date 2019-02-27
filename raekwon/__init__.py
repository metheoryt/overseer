from sqlalchemy import create_engine


def configure(dsn: str, echo=False):
    # движок нашей базы
    engine = create_engine(dsn, echo=echo, use_batch_mode=True)

    # конфигурим!
    from .db import metadata, Session
    Session.configure(bind=engine)
    metadata.bind = engine
