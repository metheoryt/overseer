from datetime import datetime

from ovs.db import make_source_model
from .schema import RecordSchema
from sqlalchemy.orm import Query


class RecordSource:
    """Источник данных для сверки одной из сторон сверки"""

    NAME = None
    """имя источника. Идентифицирует:
        - имя таблицы в базе кэша
    """

    record_schema = None
    """схема записи источника. 
    Каждая запись источника будет валидироваться этой схемой,
    каждая операция с несвалидироанным содержимым будет TODO где-нибудь помечаться 
    :type: RecordSchema"""

    def fetch_new_data(self, df: datetime, dt: datetime) -> list:
        """Получает (или пытается получить) данные, ограниченные по времени от df до dt
        :return: список словарей, таблица с данными"""
        pass

    def query(self, df: datetime, dt: datetime, q: Query):
        """Применяет фильтры к запросу и возвращает запрос данных для сверки"""
        pass

    def kleek(self, df, dt):
        """
        - забираем сырые данные
        - сохраняем из в соответствующую таблицу

        :param df: дата начала сверки
        :param dt: дата конца сверки
        :return:
        """
        raw_data = self.fetch_new_data(df, dt)
        table = make_source_model(self.NAME, self.columns)




class Overseer:
    """Приложение-сверщик

    app = Overseer(config)

    bob_ds = BobDataSource(session)
    alice_ds = AliceDataSource(session)


    @app.verdict(bob_ds, alice_ds)
    def setVerdict(bob_side, alice_side):
        if bob_side['foo'] != alice_side['bar']:
            return 'Bob\'s "foo" is not equal to Alice\'s "bar"'

        elif bob_side['set'] != 'confident':
            raise NotReconciled('bob is not confident yet')


    """
    pass
