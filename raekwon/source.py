from datetime import datetime

from raekwon.db import Session
from .db import make_table_from_schema
from sqlalchemy.orm import Query
import pandas as pd
from abc import ABCMeta, abstractmethod
from marshmallow import ValidationError
from collections import namedtuple


SourceData = namedtuple('SourceData', ['valid', 'invalid', 'trash'])


def prepare_data(raw: pd.DataFrame, schema):
    """
    исключает дубликаты, записи без pk, и записи, не прошедшие валидацию по схеме

    :param raw: сырой фрейм
    :return: SourceData с валидными и невалидными данными
    """

    def validate_row(row):
        try:
            # преобразование в строку для обхода datetime64
            schema.loads(row.to_json(date_format='iso'))
        except ValidationError as e:
            return str(e.messages)

    # отгружаем в отбросы дубликаты (один оставляем),
    # записи с пустыми идентификаторами и провалившие валидацию

    is_dup = raw.index.duplicated(keep='last')
    is_na = raw.index.isna()

    dups, na_pks, raw = raw[is_dup], raw[is_na], raw[~(is_dup | is_na)]
    dups.loc[:, '__msg'] = 'duplicated'
    na_pks.loc[:, '__msg'] = 'pk missing'

    raw.loc[:, '__msg'] = raw.apply(validate_row, axis=1)
    is_invalid = ~raw['__msg'].isna()
    invalid, raw = raw[is_invalid], raw[~is_invalid]

    trash = pd.concat([dups, na_pks])

    if trash.empty:
        trash = None

    if invalid.empty:
        invalid = None

    raw.drop(columns='__msg', inplace=True)

    return SourceData(raw, invalid, trash)


class RecordSource(metaclass=ABCMeta):
    """Источник данных для сверки одной из сторон сверки"""

    name = None
    """уникальное имя источника данных"""

    schema = None
    """Схема данных. Какие поля, какого формата, обязательны ли.
    Несвалидированные по правилам этой схемы данные смержатся с остальными, 
    но будут уже с пометкой "не сверено" и не будут участвовать в валидации цепочки
    :type: ma.Schema
    """

    pk_name = 'id'
    """Название поля с уникальным "публичным" идентификатором записи"""

    date_name = 'date'
    """Название поля с датой операции. Служит идентификатором записи на временной шкале. 
    Точность роли не играет, но важно чтобы за одну единицу времени всегда забирался полный набор операций.
    Напрмер, если в качестве единицы времени будет выступать один день "2019-02-27", забирать операции 
    за сегодня нельзя, потому что 
    если сверщик уже один раз забрал данные за конкретный минимальный промежуток времени,
    повторно за этот промежуток он операции не вставит 
    """

    @abstractmethod
    def fetch_data(self, dfrom: datetime, dto: datetime) -> pd.DataFrame:
        """Получает (или пытается получить) данные, ограниченные по времени от df до dt
        :return: датафрейм
        """
        pass

    @abstractmethod
    def query(self, df: datetime, dt: datetime, q: Query):
        """Применяет фильтры к запросу и возвращает запрос данных для сверки"""
        pass

    def kleek(self, df, dt):
        """
        - получаем сырые данные
        - чистим
        - сохраняем в личную таблицу

        :param df: дата начала сверочного периода
        :param dt: дата конца сверочного периода
        :return:
        """
        raw = self.fetch_data(df, dt)
        raw.set_index(self.pk_name, drop=True, inplace=True)

        result = prepare_data(raw, self.schema)

        # это основная таблица. В ней будут лежать данные этой конкретной коллекции
        table = make_table_from_schema(self.name, self.schema)
        table.create(checkfirst=True)

        # пора экспортировать данные
        # чё, просто наложением писать? пофиг ведь наверное
        s = Session()
        table.bind.executemany(table.insert(), result.valid.to_dict(orient='records'))
        s.commit()
        return table


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
