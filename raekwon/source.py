from datetime import datetime
from .db import make_table_from_schema
from sqlalchemy.orm import Query
import pandas as pd
from abc import ABCMeta, abstractmethod
from marshmallow import ValidationError
from collections import namedtuple


SourceData = namedtuple('SourceData', ['valid', 'trash'])


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
    raw['_message'] = raw.apply(validate_row, axis=1)
    raw.loc[raw.index.duplicated(keep='last'), '_message'] = 'duplicated'
    raw.loc[raw.index.isna(), '_message'] = 'pk is empty'

    is_trash = ~raw['_message'].isna()

    valid, trash = raw[~is_trash], raw[is_trash]
    valid.drop(columns='_message', inplace=True)

    if trash.empty:
        trash = None

    # ВТОРОЙ ВАРИАНТ, через many=True схемы. По идее должно быть быстрее, но это не так удобно
    # # сериализуем чтобы получить нормальные типы (в частности даты)
    # serialized = json.loads(raw.to_json(orient='index', date_format='iso'))
    # serialized = [{pk_name: k, **v} for k, v in serialized.items()]  # возвращаем pk
    #
    # invalid = []
    # try:
    #     valid = schema.load(serialized, many=True)
    # except ValidationError as e:
    #     valid = e.valid_data
    #     # переносим несвалидированные записи полностью
    #     # помечаем чё с ними не так
    #     for i, k in e.messages.items():
    #         bad_ts = valid[i]
    #         bad_ts['_message'] = str(k)
    #         invalid.append(bad_ts)
    #     # очищаем данные от несвалидированных транзакций
    #     valid = [v for i, v in enumerate(valid) if i not in e.messages.keys()]
    # valid = pd.DataFrame(valid)
    # invalid = pd.DataFrame(invalid)

    return SourceData(valid, trash)


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
    def fetch_data(self, df: datetime, dt: datetime) -> pd.DataFrame:
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
        - забираем сырые данные
        - исключаем дубликаты по индексу

        - сохраняем в именованную таблицу

        :param df: дата начала сверочного периода
        :param dt: дата конца сверочного периода
        :return:
        """
        raw = self.fetch_data(df, dt)
        result = prepare_data(raw, self.pk_name, self.schema)

        table = make_table_from_schema(self.name, self.schema)
        table.create(checkfirst=True)





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
