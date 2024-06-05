import os
from itertools import zip_longest

fileName = "input.txt"
outFileName = "output.txt"

# Read input file
file = open(fileName, "r", encoding="utf-8")
if os.path.exists(outFileName):
    os.remove(outFileName)
outFile = open(outFileName, "x", encoding="utf-8")
adat = file.readlines()

class DailyRecord:
    @staticmethod
    def safe_int_convert(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return value
        
    def __init__(self, date=None, school=None, work=None, fullwork=None, incomes=None, expenses=None, podcast=None, 
                 reading=None, diet=None, workout=None, meditation=None, mindset=None, masturbation=None, dopamin=None, gaming=None, 
                 wake=None, bed=None, sleep=None, score=None, note=None):
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
        if self.wake is None:
            return None
        if len(self.wake) == 4:
            return int(self.wake[0]) * 60 + int(self.wake[2:])
        elif len(self.wake) == 5:
            return int(self.wake[:2]) * 60 + int(self.wake[3:])
    
    def night(self):
        if self.bed is None:
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
        if self.sleep is None:
            return None
        try:
            hours, minutes, seconds = self.sleep.split(':')
            return int(hours) * 60 + int(minutes)
        except ValueError:
            return None
    
    def score_number(self):
        if any(attr is None for attr in [self.fullwork, self.sleep, self.podcast, self.reading]):
            return None
        if self.fullwork < 660:
            work_score = self.fullwork * (37 / 660)
        else:
            work_score = self.fullwork * (37 / 690)

        if self.sleep_duration() < 480:
            sleep_score = self.sleep_duration() * (26 / 480)
        else:
            sleep_score = self.sleep_duration() * (26 / 490)

        if self.podcast < 60:
            podcast_score = self.podcast * (3.5 / 60)
        else:
            podcast_score = self.podcast * (3.5 / 65)
        
        if self.reading < 60:
            reading_score = self.reading * (3.5 / 60)
        else:
            reading_score = self.reading * (3.5 / 65)

        diet_score = 6 if self.diet != "0" else 0
        workout_score = 6 if self.workout != "0" else 0
        meditation_score = 4 if self.meditation != "0" else 0
        mindset_score = 3 if self.mindset != "0" else 0
        masturbation_score = self.masturbation * 4
        dopamin_score = 2 if self.dopamin == "0" else 0
        gaming_score = 5 if self.gaming == "0" else 0

        self.score = int(work_score + sleep_score + podcast_score + reading_score +
                         diet_score + workout_score + meditation_score +
                         masturbation_score + dopamin_score + gaming_score)
        return self.score

db = []
records = []
for i in range(1, len(adat) - 1):
    line = adat[i]
    values = line.strip().split('\t')
    keys = ['date', 'school', 'work', 'fullwork', 'incomes', 'expenses', 'podcast', 'reading', 'diet', 'workout', 
            'meditation', 'mindset', 'masturbation', 'dopamin', 'gaming', 'wake', 'bed', 'sleep', 'score', 'note']
    variables = dict(zip_longest(keys, values, fillvalue=None))
    record = DailyRecord(**variables)
    records.append(record)

morning_avg = morning_records = night_avg = night_records = sleep_dur_avg = sleep_dur_records = score_avg = score_records =  0
for record in records:
    if record.wake is not None:
        morning = record.morning()
        if morning is not None:
            morning_avg, morning_records = ((morning_avg * morning_records + morning) / (morning_records + 1), morning_records + 1) if morning_records > 0 else (morning, 1)
    if record.bed is not None:
        night = record.night()
        if night is not None:
            night_avg, night_records = ((night_avg * night_records + night) / (night_records + 1), night_records + 1) if night_records > 0 else (night, 1)
    if all(attr is not None for attr in [record.fullwork, record.sleep, record.podcast, record.reading]):
        score = record.score_number()
        if score is not None:
            score_avg, score_records = ((score_avg * score_records + score) / (score_records + 1), score_records + 1) if score_records > 0 else (score, 1)
    if record.sleep is not None:
        sleep_dur = record.sleep_duration()
        if sleep_dur is not None:
            sleep_dur_avg, sleep_dur_records = ((sleep_dur_avg * sleep_dur_records + sleep_dur) / (sleep_dur_records + 1), sleep_dur_records + 1) if sleep_dur_records > 0 else (sleep_dur, 1)

morning_avg = str(int(morning_avg / 60)) + ":" + str(int(morning_avg % 60))
night_avg = str(int(night_avg / 60)) + ":" + str(int(night_avg % 60))
sleep_dur_avg = str(int(sleep_dur_avg / 60)) + ":" + str(int(sleep_dur_avg % 60))
score_avg = str(int(score_avg))
print(morning_avg, night_avg, sleep_dur_avg, score_avg)
        
with open(outFileName, 'a', encoding="utf-8") as f:
    f.write(adat[0])
    for record in records:
        for attr, value in vars(record).items():
            f.write(str(value) + "\t")
        f.write("\n")
    f.write(adat[len(adat) - 1].rstrip('\t') + "\t" + morning_avg + "\t" + night_avg + "\t" + sleep_dur_avg + "\t" + score_avg)
