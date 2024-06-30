class DailyRecord:
    @staticmethod
    def safe_int_convert(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return value
        
    def __init__(self, date="", school="", work="", fullwork="", incomes="", expenses="", podcast="", 
                 reading="", diet="", workout="", meditation="", mindset="", masturbation="", dopamin="", gaming="", 
                 wake="", bed="", sleep="", score="", note=""):
        self.date = date
        self.school = self.safe_int_convert(school)
        self.work = self.safe_int_convert(work)
        self.fullwork = self.safe_int_convert(fullwork)
        self.incomes = self.safe_int_convert(incomes)
        self.expenses = self.safe_int_convert(expenses)
        self.podcast = self.safe_int_convert(podcast)
        self.reading = self.safe_int_convert(reading)
        self.diet = diet
        self.workout = workout
        self.meditation = meditation
        self.mindset = mindset
        self.masturbation = self.safe_int_convert(masturbation)
        self.dopamin = dopamin
        self.gaming = gaming
        self.wake = wake
        self.bed = bed
        self.sleep = sleep
        self.score = score
        self.note = note

    def morning(self):
        if self.wake == "":
            return None
        elif len(self.wake) == 4:
            return int(self.wake[0]) * 60 + int(self.wake[2:])
        elif len(self.wake) == 5:
            return int(self.wake[:2]) * 60 + int(self.wake[3:])
    
    def night(self):
        if self.bed == "":
            return None
        try:
            hours, minutes = self.bed.split(':')
            if int(hours) >= 15:
                return int(hours) * 60 + int(minutes)
            elif int(hours) < 15:
                return 1440 + int(hours) * 60 + int(minutes)
        except ValueError:
            return None
    
    def sleep_duration(self):
        if self.sleep == "":
            return None
        try:
            hours, minutes, seconds = self.sleep.split(':')
            return int(hours) * 60 + int(minutes)
        except ValueError:
            return None
    
    def score_number(self):
        if self.fullwork == "":
            work_score = 0
        else:
            if self.fullwork < 660:
                work_score = self.fullwork * (37 / 660)
            else:
                work_score = self.fullwork * (37 / 690)

        if self.sleep_duration() is None:
            sleep_score = 0
        else:
            if self.sleep_duration() < 480:
                sleep_score = self.sleep_duration() * (26 / 480)
            else:
                sleep_score = self.sleep_duration() * (26 / 495)

        if self.podcast == "":
            if self.reading == "":
                knowledge_score = 0
            else:
                if self.reading < 120:
                    knowledge_score = self.reading * (3.5 / 60)
                else:
                    knowledge_score = self.reading * (3.5 / 65)
        elif self.reading == "":
            if self.podcast < 120:
                knowledge_score = self.podcast * (3.5 / 60)
            else:
                knowledge_score = self.podcast * (3.5 / 65)
        else:
            knowledge = self.podcast + self.reading
            if knowledge < 120:
                knowledge_score = knowledge * (3.5 / 60)
            else:
                knowledge_score = knowledge * (3.5 / 65)

        diet_score = 6 if self.diet == "1" else 0
        workout_score = 6 if self.workout == "1" else 0
        meditation_score = 4 if self.meditation == "1" else 0
        mindset_score = 3 if self.mindset == "1" else 0
        if self.masturbation == "":
            masturbation_score = 0
        else:
            masturbation_score = self.masturbation * -4
        dopamin_score = 2 if self.dopamin == "0" else 0
        gaming_score = 5 if self.gaming == "0" else 0

        self.score = round(work_score + sleep_score + knowledge_score +
                         diet_score + workout_score + meditation_score + mindset_score +
                         masturbation_score + dopamin_score + gaming_score, 1)
        
        return self.score
