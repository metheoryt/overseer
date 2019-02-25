import marshmallow as ma
from marshmallow import fields as f


class Verdict:

    def __init__(self, reconciled: bool=None, verdict: str=None):
        self.reconciled = reconciled
        self.verdicts = []
        if verdict:
            self.verdicts.append(verdict)

    def __str__(self):
        return f'<Verdict / {"reconciled" if self.reconciled else "non-reconciled"} ({"; ".join(self.verdicts)})'


class RecordSchema(ma.Schema):

    shared_id = f.Str(required=True)
    """Единственное поле, требуемое от записи"""

    date = f.DateTime(required=True)
    """Второе важное поле, по которому можно будет фильтровать по времени. Должно быть всегда"""
