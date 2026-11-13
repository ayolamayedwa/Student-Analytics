class Assessment:
    def __init__(self, name, weight, mark, date_time):
        self.name = name

        if not (0 < weight <= 1):
            raise ValueError(f"weight must be between 0 and 1, got {weight}")
        self.weight = weight

        if mark is not None and not (0 <= mark <= 100):
            raise ValueError(f"mark must be between 0 and 100, or None, got {mark}")
        self.mark = mark

        self.date_time = date_time