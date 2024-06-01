import os

fileName = input("Input File Name> ")
outFileName = input("Output File Name> ")
file = open(fileName, "r", encoding="utf-8")
if os.path.exists(outFileName):
  os.remove(outFileName)
outFile = open(outFileName, "x", encoding="utf-8")
adat = file.readlines()

db = []
for line in adat:
    line = line.strip().split('\t')
    db.append(line)

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