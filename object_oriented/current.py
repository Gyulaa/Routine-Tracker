import os
from itertools import zip_longest
from classes import DailyRecord

fileName = "input.txt"
outFileName = "output.txt"

# Read input file
file = open(fileName, "r", encoding="utf-8")
if os.path.exists(outFileName):
    os.remove(outFileName)
outFile = open(outFileName, "x", encoding="utf-8")
adat = file.readlines()

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
    if  all(attr is not None for attr in [record.fullwork, record.sleep, record.podcast, record.reading]):
        score = record.score_number()
        if score is not None:
            score_avg, score_records = ((score_avg * score_records + score) / (score_records + 1), score_records + 1) if score_records > 0 else (score, 1)
    if record.sleep is not None:
        sleep_dur = record.sleep_duration()
        if sleep_dur is not None:
            sleep_dur_avg, sleep_dur_records = ((sleep_dur_avg * sleep_dur_records + sleep_dur) / (sleep_dur_records + 1), sleep_dur_records + 1) if sleep_dur_records > 0 else (sleep_dur, 1)

print(morning_avg, night_avg, sleep_dur_avg, score_avg)

morning_avg = round(morning_avg)
morning_avg = f"{morning_avg // 60}:{morning_avg % 60:02d}"

if isinstance(night_avg, str):
    night_avg = float(night_avg)
night_avg = f"{int(night_avg // 60)}:{int(night_avg % 60):02d}"

sleep_dur_avg = round(sleep_dur_avg)
sleep_dur_avg = f"{sleep_dur_avg // 60}:{sleep_dur_avg % 60:02d}"

score_avg = round(score_avg, 1)

print(morning_avg, night_avg, sleep_dur_avg, score_avg)
        
with open(outFileName, 'a', encoding="utf-8") as f:
    f.write(adat[0])
    for record in records:
        for attr, value in vars(record).items():
            if value is not None:
                f.write(str(value))
            f.write("\t")
        f.write("\n")
    f.write(adat[len(adat) - 1].rstrip('\t') + "\t" + str(morning_avg) + "\t" + str(night_avg) + "\t" + str(sleep_dur_avg) + "\t" + str(score_avg))
