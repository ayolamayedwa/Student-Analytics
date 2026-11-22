import datetime
class Assessment:
    def __init__(self, name, weight, mark, date_time):
        self.name = name
        self.weight = weight
        self.mark = mark
        self.date_time = date_time

    # use of python property to have one rule of validation
    @property
    def mark(self):
        return self._mark

    @mark.setter
    def mark(self, value):
        if value is not None and not (0 <= value <= 100):
            raise ValueError(f"mark must be between 0 and 100, or None, got {value}")
        self._mark = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if not (0 < value <= 1):
            raise ValueError(f"weight must be between 0 and 1, got {value}")
        self._weight = value

    @property
    def date_time(self):
        return self._date_time
    @date_time.setter
    def date_time(self, date):
        if date is not datetime.datetime:
            raise ValueError(f"date_time must be datetime, got {date}")
        self._date_time = date