import os
from itertools import zip_longest

fileName = input("Input File Name> ")
outFileName = input("Output File Name> ")
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

db = []
records = []
for line in adat:
    values = line.strip().split('\t')
    keys = ['date', 'school', 'work', 'fullwork', 'incomes', 'expenses', 'podcast', 'reading', 'diet', 'workout', 
            'meditation', 'masturbation', 'music', 'gaming', 'wake', 'bed', 'sleep', 'score', 'note']
    variables = dict(zip_longest(keys, values, fillvalue=None))

    record = DailyRecord(**variables)
    
    records.append(record)

    line = line.strip().split('\t')
    db.append(line)

print(records[17].sleep_duration())
print(records[17].sleep)
print(records[17].night())
print(records[18].night())

morning_avg = 0
morning_records = 0
night_avg = 0
night_records = 0
sleep_dur_avg = 0
sleep_dur_records = 0
score_avg = 0
score_records = 0

for i in range(len(records), 1, 1):
    record = records[i]

    multiplier = 0.0415
    nerfed_mulitplier = 0.0375

    score = 0

    if record.fullwork < 660:
        work_score = record.fullwork * multiplier
    else:
        work_score = record.fullwork * nerfed_mulitplier

    if  record.sleep < 540:
        sleep_score = record.sleep * multiplier
    else:
        sleep_score = record.sleep * nerfed_mulitplier

    if record.podcast < 75:
        podcast_score = record.podcast * multiplier
    else:
        podcast_score = record.podcast * nerfed_mulitplier
    
    if record.reading < 75:
        reading_score = record.reading * multiplier
    else:
        reading_score = record.reading * nerfed_mulitplier
    
    score = work_score + sleep_score + podcast_score + reading_score

    if record.diet != 0:
        score += 5
    if record.workout != 0:
        score += 7
    if record.meditation != 0:
        score += 5
    if record.masturbation == 0:
        score += 15
    if record.music == 0:
        score += 3
    if record.gaming == 0:
        score += 5


mornings = 0
nightTimes = []
nights = 0
sleeps = 0
allScore = 0
validDays = 0

for i in range(len(db)-1):
    if len(db[i]) >= 15 and i > 0 and db[i][15] != '' and db[i][14] != '' and db[i][3] != '':
        validDays += 1
        score = 0
        date = db[i][0]
        workTime = int(db[i][3])
        podcastTime = int(db[i][6])
        readingTime = int(db[i][7])
        properlyEating = int(db[i][8])
        workout = int(db[i][9])
        visualization = int(db[i][10])
        masturbation = int(db[i][11])
        music = int(db[i][12])
        gaming = int(db[i][13])
        morning = db[i][14]
        night = db[i][15]

        # Calculate morning, night and sleeping
        if len(morning) == 4:
            morningTime = int(morning[0])*60 + int(morning[2:])
        else:
            morningTime = int(morning[:2])*60 + int(morning[3:])
        mornings += morningTime
        if len(night) == 5:
            nightTime = int(night[:2])*60 + int(night[3:])
            nights += nightTime
            nightTimes.append(nightTime)
            if len(nightTimes) > 1:
                if nightTimes[len(nightTimes) - 1] < 600:
                    sleepTime = (morningTime - nightTimes[len(nightTimes) - 1]) + (1440 - nightTime)
                else:
                    sleepTime = morningTime + (1440 - nightTime)
            else:
                sleepTime = morningTime + (1440 - nightTime)
            sleeps += sleepTime
        else:
            nightTime = int(night[:1])*60 + int(night[2:])
            nights += nightTime + 1440
            nightTimes.append(nightTime)
            if len(nightTimes) > 1:
                if nightTimes[len(nightTimes) - 1] < 600:
                    sleepTime = morningTime - nightTimes[len(nightTimes) - 1]
                else:
                    sleepTime = morningTime
            else:
                sleepTime = morningTime
            sleeps += sleepTime

        
        # Calculate Score
        print(date)
        if workTime < 660:
            workSCR = workTime * 0.0415
        else:
            workSCR = workTime * 0.0375
        score += workSCR
        
        if sleepTime < 540:
            sleepSCR = sleepTime * 0.0415
        else:
            sleepSCR = sleepTime * 0.0375
        score += sleepSCR
        
        if podcastTime < 75:
            podcastSCR = podcastTime * 0.0415
        else:
            podcastSCR = podcastTime * 0.0375
        score += podcastSCR

        if readingTime < 75:
            readSCR = readingTime * 0.0415
        else:
            readSCR += readingTime * 0.0375
        score += readSCR
        
        currentSCR = score

        if properlyEating != 0:
            score += 5
        if workout != 0:
            score += 7
        if visualization != 0:
            score += 5
        if masturbation == 0:
            score += 15
        if music == 0:
            score += 3
        if gaming == 0:
            score += 5

        allScore += score

        if score < 100:
            db[i][17] = str(score)[:2]
        else:
            db[i][17] = str(score)[:3]


# Add time avarages
avgMorning = str(mornings / validDays // 60)[0] + ":" + str(mornings / validDays % 60)[:2]
db[len(db)-1].append(avgMorning)

avgNight = str(nights / validDays // 60)[:2] + ":" + str(nights / validDays % 60)[:2]
db[len(db)-1].append(avgNight)

avgSleep = str(sleeps / validDays // 60)[0] + ":" + str(sleeps / validDays % 60)[:2]
db[len(db)-1].append(avgSleep)

avgScore = str(allScore / validDays)[:2]
db[len(db)-1].append(avgScore)
        
with open(outFileName, 'a', encoding="utf-8") as f:
    for i in range(len(db)):
        for j in range(len(db[i])):
            f.write(str(db[i][j]) + "\t")
        f.write("\n")  # Write newline after each line
    print("Task finished.")