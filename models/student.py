import datetime

class Student:
    def __init__(self, student_id, year, name, email):
        self.name = name
        self.email = email
        self.student_id = student_id
        self.modules = []
        self.sessions = []
        self.year_of_study = year
        self.num_of_modules = 0

#Quick access and changes
    def add_module(self, module):
        self.modules.append(module)
        number_of_modules = len(self.modules)

    def get_modules(self):
        return self.modules

    def remove_module(self, module):
        if module in self.modules:
            self.modules.remove(module)

    def get_student_id(self):
        return self.student_id

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email
    def update_year_of_study(self, year):
        if 0 < year < 8:
            self.year_of_study = year
            return True
        return False

    def add_study_session(self, session):
        for module in self.modules:
            if session.module_code == module.code:
                self.sessions.append(session)
                return True
        return False

    def get_module_study_time(self, code):
        total = 0
        for session in self.sessions:
            if session.module_code == code:
                total += session.duration
        return total

    def get_module_average(self, code):
        if len(self.modules) == 0:
            return False
        for module in self.modules:
            if module.code == code:
                return module.calculate_average()
        return None # Module not found

    def get_weighted_average(self):
        all_credits = []
        sum_of_credits = 0
        for module in self.modules:
            average = module.calculate_average()
            if average is not None:
                module_credits = module.get_module_credits()
                sum_of_credits = sum_of_credits + module_credits
                all_credits.append(average/100 * module_credits)
        if sum_of_credits == 0:
            return None

        return sum(all_credits)/sum_of_credits * 100

    def get_average_marks(self):
        all_marks = []
        for module in self.modules:
            average = module.calculate_average()
            if average is not None:
                all_marks.append(average)
        if all_marks == []:
            return None
        return sum(all_marks) / len(all_marks)

    def get_total_study_time(self):
        temp = 0
        for session in self.sessions:
            temp = temp + session.duration
        return temp

    # This function returns an array of assessments that are still yet to be written.
    def get_upcoming_assessments(self):
        remaining = []
        now = datetime.datetime.now()
        for module in self.modules:
            for assessment in module.assessments:
                if assessment.date_time > now:
                    remaining.append(assessment)
        return remaining