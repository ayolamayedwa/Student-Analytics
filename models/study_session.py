class StudySession:
    def __init__(self, module_code, duration, date):
        self.module_code = module_code
        if duration <= 0 or duration > 24: # The units will be hours, should specify in application side.
            raise ValueError(f"Duration must be greater than 0 and less than or equal to 24, got {duration}")
        self.duration = duration
        self.date = date