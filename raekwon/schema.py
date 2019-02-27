

class Verdict:

    def __init__(self, reconciled: bool=None, verdict: str=None):
        self.reconciled = reconciled
        self.verdicts = []
        if verdict:
            self.verdicts.append(verdict)

    def __str__(self):
        return f'<Verdict / {"reconciled" if self.reconciled else "non-reconciled"} ({"; ".join(self.verdicts)})'


