class Module:
    def __init__(self,code , name, credits):
        self.code = code
        self.name = name
        self.credits = credits
        self.assessments = []
        self.fully_marked = False

    def add_assessment(self, assessment):
        current_total = 0
        for a in self.assessments:
            current_total += a.weight

        if current_total + assessment.weight > 1:
            return False
        else:
            self.assessments.append(assessment)
            return True

    def remove_assessment(self, assessment):
        if assessment in self.assessments:
            self.assessments.remove(assessment)
    def update_assessment_marks(self, assessment, updated_mark):
        assessment.mark = updated_mark # do error management

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