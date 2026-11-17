from models.module import Module
from models.assessment import Assessment
import datetime
import json

ComputerScience = Module("CSC01A1", "ComputerScience", 180)

date_written = datetime.datetime.strptime("2026-11-20 09:00", "%Y-%m-%d %H:%M")
SemesterTestOne = Assessment("SemesterTestOne", 0.4, 50, date_written)

date_written2 = datetime.datetime.strptime("2026-11-20 09:00", "%Y-%m-%d %H:%M")
SemesterTestTwo = Assessment("SemesterTestTwo", 0.4, 60, date_written2)

date_written3 = datetime.datetime.strptime("2026-11-20 09:00", "%Y-%m-%d %H:%M")
SemesterTestThree = Assessment("SemesterTestThree", 0.3, 70, date_written3)

ComputerScience.add_assessment(SemesterTestOne)
ComputerScience.add_assessment(SemesterTestTwo)

moduleInfo = { "name": "ComputerScience", "code": "CSC01A1", "credits": 180}

with open("data/moduleData.json", "w") as f:
    json.dump(moduleInfo, f, indent=4)


ComputerScience.add_assessment(SemesterTestThree)

