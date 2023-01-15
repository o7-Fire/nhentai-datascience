import requests
import time

counter = None
averageCounter = None
averageCounterN = 1
fansCounter = open("cdnlogger.txt", "a")

try:
    while True:
        time.sleep(1)
        beforeCounter = counter
        counter = requests.get("https://cdn.mindustry.me/research/botindex").text.count("\n")
        if beforeCounter is None:
            beforeCounter = counter
        diff = counter - beforeCounter

        if averageCounter is None and diff != 0:
            averageCounter = diff
        elif averageCounter is not None:
            averageCounter = (averageCounter * averageCounterN + diff) / (averageCounterN+1)
            averageCounterN = averageCounterN + 1

        if diff != 0:
            fansCounter.write(str(counter)+"\n")
            fansCounter.flush()
        print(diff, "/s")
        if averageCounter is not None:
            print(round(averageCounter, 2), "/s avg")
except Exception as e:
    print(e)
    print("SAVING")
    

fansCounter.close()
