#import statistics
import datetime

class Student:
    def __init__(self,student_id,name ,email):
        self.name = name
        self.email = email
        self.student_id = student_id
        self.modules = []
        self.sessions = []

#Quick access and changes
    def add_module(self, module):
        self.modules.append(module)

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

    def add_study_session(self, session):
        self.sessions.append(session)

    def get_average(self):
        all_marks = []
        credits = 0
        sumOfCredits = 0
        for module in self.modules:
            average = module.calculate_average()
            if average is not None:
                credits = module.get_module_credits()
                sumOfCredits = sumOfCredits + credits
                all_marks.append(average/100 * credits)
        if sumOfCredits == 0:
            return None

        return sum(all_marks)/sumOfCredits * 100

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