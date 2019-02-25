from datetime import datetime
from .schema import Verdict


class ReconMode:
    """режим сверки

    atm_mode = BobAliceATMMode(bob_ds, alice_ds)

    @atm_mode.verdict
    def find_issue(bob_record: dict, alice_record: dict):
        assert bob_record, 'bob record is missing'  # пометит как несверяемую, прекратит выполнение сверщиков



    app.recon(atm_mode, df=datetime(2019, 1, 1), dt=datetime(2019, 1, 2))

    """

    def __init__(self, *sides):
        self.sides = sides
        self.verdict_handlers = []

    def verdict(self, fn):
        self.verdict_handlers.append(fn)

    def reconcile(self, df: datetime, dt: datetime):
        """Этапы сверки

        - получение данных
        - сохранение полученных данных в кэш
            - проверка shared_id на уникальность - дубликаты как-нибудь помечаются и не участвуют в сверке.
                дубликатам по ходу отдельное место в отчёте
        - запрос сохранённых данных из кэша специально собранным запросом
        """

        data = []
        for side in self.sides:
            raw_data = side.fetch_new_data(df, dt)
            """:type: list[dict]"""
            data.append(raw_data)

        verdict = Verdict()

