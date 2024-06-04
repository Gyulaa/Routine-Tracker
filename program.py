import os
from itertools import zip_longest

fileName = "input.txt"

outFileName = "output.txt"

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
                 reading=None, diet=None, workout=None, meditation=None, masturbation=None, music=None, gaming=None, 
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
        self.masturbation = self.safe_int_convert(masturbation)
        self.music = music
        self.gaming = gaming
        self.wake = wake
        self.bed = bed
        self.sleep = sleep
        self.score = score
        self.note = note

    def morning(self):
        if len(self.wake) == 4:
            return int(self.wake[0])*60 + int(self.wake[2:])
        elif len(self.wake) == 5:
            return int(self.wake[:2])*60 + int(self.wake[3:])

    def night(self):
        hours, minutes = self.bed.split(':')
        if int(hours) >= 15:
            return int(hours)*60 + int(minutes)
        elif int(hours) < 15:
            return 1440 + int(hours)*60 + int(minutes)
    
    def sleep_duration(self):
        hours, minutes, seconds = self.sleep.split(':')
        return int(hours)*60+int(minutes)
    
    def score_number(self):
        multiplier = 0.0415
        nerfed_mulitplier = 0.0375

        if self.fullwork < 660:
            work_score = self.fullwork * multiplier
        else:
            work_score = self.fullwork * nerfed_mulitplier

        if  self.sleep_duration() < 540:
            sleep_score = self.sleep_duration() * multiplier
        else:
            sleep_score = self.sleep_duration() * nerfed_mulitplier

        if self.podcast < 75:
            podcast_score = self.podcast * multiplier
        else:
            podcast_score = self.podcast * nerfed_mulitplier
        
        if self.reading < 75:
            reading_score = self.reading * multiplier
        else:
            reading_score = self.reading * nerfed_mulitplier

        diet_score = 5 if self.diet != "0" else 0
        workout_score = 7 if self.workout != "0" else 0
        meditation_score = 5 if self.meditation != "0" else 0
        masturbation_score = 15 if self.masturbation == 0 else 0
        music_score = 3 if self.music == "0" else 0
        gaming_score = 5 if self.gaming == "0" else 0

        self.score = int(work_score + sleep_score + podcast_score + reading_score +
                diet_score + workout_score + meditation_score +
                masturbation_score + music_score + gaming_score)
        return self.score

db = []
records = []
for i in range(1, len(adat) - 1):
    line = adat[i]
    values = line.strip().split('\t')
    keys = ['date', 'school', 'work', 'fullwork', 'incomes', 'expenses', 'podcast', 'reading', 'diet', 'workout', 
            'meditation', 'masturbation', 'music', 'gaming', 'wake', 'bed', 'sleep', 'score', 'note']
    variables = dict(zip_longest(keys, values, fillvalue=None))

    record = DailyRecord(**variables)
    
    records.append(record)

    line = line.strip().split('\t')
    db.append(line)

print(adat[0])

morning_avg = morning_records = night_avg = night_records = sleep_dur_avg = sleep_dur_records = score_avg = score_records =  0
for i in range(1, len(records)-1, 1):
    record = records[i]
    morning_avg, morning_records = ((morning_avg * morning_records + record.morning()) / (morning_records + 1), morning_records + 1) if morning_records > 0 else (record.morning(), 1)
    night_avg, night_records = ((night_avg * night_records + record.night()) / (night_records + 1), night_records + 1) if night_records > 0 else (record.night(), 1)
    score_avg, score_records = ((score_avg * score_records + record.score_number()) / (score_records + 1), score_records + 1) if score_records > 0 else (record.score_number(), 1)
    sleep_dur_avg, sleep_dur_records = ((sleep_dur_avg * sleep_dur_records + record.sleep_duration()) / (sleep_dur_records + 1), sleep_dur_records + 1) if sleep_dur_records > 0 else (record.sleep_duration(), 1)

morning_avg = str(int(morning_avg/60))+":"+str(int(morning_avg%60))
night_avg = str(int(night_avg/60))+":"+str(int(night_avg%60))
sleep_dur_avg = str(int(sleep_dur_avg/60))+":"+str(int(sleep_dur_avg%60))
score_avg = str(int(score_avg))
print(morning_avg, night_avg, sleep_dur_avg, score_avg)
        
with open(outFileName, 'a', encoding="utf-8") as f:
    f.write(adat[0])
    for record in records:
        for attr, value in vars(record).items():
            f.write(str(value)+"\t")
        f.write("\n")
    f.write(adat[len(adat)-1].rstrip('\t') + "\t" + str(morning_avg) + "\t" + str(night_avg) + "\t" + str(sleep_dur_avg) + "\t" + str(score_avg))