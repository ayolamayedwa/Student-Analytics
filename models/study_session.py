import datetime


class StudySession:
    def __init__(self, module_code, duration, date):
        self.module_code = module_code
        self.duration = duration
        self.date = date

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value): # The units will be hours, should specify in application side.
        if value <= 0 or value > 24:
            if not isinstance(value, (int, float)):
                raise TypeError(f"duration must be int or float, got {value}")
            raise ValueError(f"Duration must be greater than 0 and less than or equal to 24, got {value}")
        self._duration = value

    @property
    def module_code(self):
        return self._module_code

    @module_code.setter
    def module_code(self, code):
        if not isinstance(code, str) or not code:
            raise ValueError(f"Module code is supposed to be a string , got {code}")
        self._module_code = code.upper()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
            raise ValueError(f"date must be datetime.date, got {value}")
        self._date = value