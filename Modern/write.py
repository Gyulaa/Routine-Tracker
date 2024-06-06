import os

def Write(input):
    data, records, avgs = input
    if os.path.exists("output.txt"):
        os.remove("output.txt")

    with open("output.txt", 'a', encoding="utf-8") as f:
        f.write(data[0])
        for record in records:
            for attr, value in vars(record).items():
                if value is not None:
                    f.write(str(value))
                f.write("\t")
            f.write("\n")
        f.write(data[len(data) - 1].rstrip('\t') + "\t" + avgs[0] + "\t" + avgs[1] + "\t" + avgs[2] + "\t" + avgs[3])
