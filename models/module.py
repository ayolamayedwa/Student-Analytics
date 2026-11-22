class Module:
    def __init__(self,code , name, credits):
        self.code = code
        self.name = name
        self.credits = credits
        self.assessments = []

    # Properties; with consistent rule
    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError(f"Module code is supposed to be a string , got {value}")
        self._code = value.upper()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError(f"Module name is supposed to be a string , got {value}")
        self._name = value

    @property
    def credits(self):
        return self._credits
    @credits.setter
    def credits(self, value):
        if not isinstance(value, int) or not 0 < value < 37:
            raise ValueError(f"Module credit is supposed to be a int , got {value}")
        self._credits = value

    # change methods
    def update_assessment_mark(self, assessment, mark):
        if assessment not in self.assessments:
            return False
        assessment.mark = mark  # the setter validates (raises ValueError if out of range)
        return True

    def add_assessment(self, assessment):
        current_total = 0
        for a in self.assessments:
            current_total += a.weight

        if current_total + assessment.weight > 1 + 0.000001:
            return False
        else:
            self.assessments.append(assessment)
            return True

    def remove_assessment(self, assessment):
        if assessment in self.assessments:
            self.assessments.remove(assessment)
            return True
        else:
            return False

    def is_fully_marked(self):
        if not self.assessments:
            return False
        return all(assessment.mark is not None for assessment in self.assessments)


    def calculate_average(self):
        total_weighted_marks = 0
        total_weight_used = 0

        for assessment in self.assessments:
            if assessment.mark is not None:
                total_weighted_marks += assessment.mark * assessment.weight
                total_weight_used += assessment.weight

        if total_weight_used == 0:
            return None  # no marked assessments yet — nothing to average

        return total_weighted_marks / total_weight_used

    def get_module_credits(self):
        return self.credits