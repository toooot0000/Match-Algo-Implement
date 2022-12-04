from algo import *
from tracker import *
from itertools import repeat
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
from math import ceil


TEST_SCALE = (20, 200, 5)
TEST_FIXED_LENGTH = 100
LETTER_CANDIDATES = ["A", "C", "G", "T"]
PROCESS_NUM = 1


def doDP(s1, s2, q):
    ret = tracker(alignDp, args = (s1, s2))
    ret["method"] = "DP"
    q.put(ret)


def doMemSave(s1, s2, q):
    ret = tracker(alignMemSave, args = (s1, s2))
    ret["method"] = "D&C"
    q.put(ret)


def helperToEvaluate(input, data: mp.Queue):
    for str1, str2 in input:
        q = mp.Queue()
        p1 = mp.Process(target=doDP, args=(str1, str2, q))
        p2 = mp.Process(target=doMemSave, args=(str1, str2, q))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        dpRet, memSaveRet = q.get(), q.get()
        if dpRet["method"] == "D&C":
            dpRet, memSaveRet = memSaveRet, dpRet
        entry = {
            "size": len(str1),
            "time": {
                "dp": dpRet["time"] / 100000,
                "memSave": memSaveRet["time"] / 100000,
            },
            "mem": {"dp": dpRet["mem"], "memSave": memSaveRet["mem"]},
        }
        data.put(entry)


def genData() -> list[dict]:
    data = mp.Queue()
    ret = []
    procs = []
    allInput = list(zip(genInput(), genInput()))
    n = len(allInput)
    inc = ceil(n / PROCESS_NUM)
    for i in range(min(PROCESS_NUM, n)):
        input = allInput[i * inc : (i + 1) * inc]
        procs.append(
            mp.Process(target=helperToEvaluate, args=(input, data), daemon=False)
        )
        procs[-1].start()
    for p in procs:
        p.join()
    ret.extend(data.get() for _ in range(n))
    return ret


def genInput():
    curStr = genRandStr(LETTER_CANDIDATES, TEST_SCALE[0])
    while len(curStr) <= TEST_SCALE[1]:
        yield curStr
        curStr += genRandStr(LETTER_CANDIDATES, TEST_SCALE[2])


def genFixedInput(length = TEST_FIXED_LENGTH):
    return repeat(genRandStr(LETTER_CANDIDATES, TEST_FIXED_LENGTH))
    

def plotTimes(data: list[dict]):
    x = []
    dp = []
    memSave = []
    for entry in data:
        x.append(entry["size"]*2)
        dp.append(entry["time"]["dp"])
        memSave.append(entry["time"]["memSave"])

    fig = plt.figure()
    fig, ax = plt.subplots()
    ax.plot(x, dp, label="Dynamic Programing")  # Plot some data on the axes.
    ax.plot(x, memSave, label="Divide and Conquer")  # Plot more data on the axes...
    ax.set_xlabel("Problem Size")  # Add an x-label to the axes.
    ax.set_ylabel("Time/ms")  # Add a y-label to the axes.
    ax.set_title("CPU Plot")  # Add a title to the axes.
    ax.legend()  # Add a legend.
    plt.savefig("CPUPlot.png")


def plotMem(data: list[dict]):
    x = []
    dp = []
    memSave = []
    for entry in data:
        x.append(entry["size"]*2)
        dp.append(entry["mem"]["dp"])
        memSave.append(entry["mem"]["memSave"])
    pass

    fig = plt.figure()
    fig, ax = plt.subplots()
    ax.plot(x, dp, label="Dynamic Programing")  # Plot some data on the axes.
    ax.plot(x, memSave, label="Divide and Conquer")  # Plot more data on the axes...
    ax.set_xlabel("Problem Size")  # Add an x-label to the axes.
    ax.set_ylabel("Memory/KB")  # Add a y-label to the axes.
    ax.set_title("Memory Plot")  # Add a title to the axes.
    ax.legend()  # Add a legend.
    plt.savefig("MemoryPlot.png")

    fig = plt.figure()
    fig, ax = plt.subplots()
    # ax.plot(x, dp, label="Dynamic Programing")  # Plot some data on the axes.
    ax.plot(x, memSave, label="Divide and Conquer")  # Plot more data on the axes...
    ax.set_xlabel("Problem Size")  # Add an x-label to the axes.
    ax.set_ylabel("Memory/KB")  # Add a y-label to the axes.
    ax.set_title("Memory Plot")  # Add a title to the axes.
    ax.legend()  # Add a legend.
    plt.savefig("MemoryPlot-memSaved version.png")


if __name__ == "__main__":

    # allInput = list(zip(genInput(), genFixedInput()))
    # print(allInput)
    data = genData()
    data.sort(key=lambda x: x["size"])
    # print(data)
    plotTimes(data)
    plotMem(data)
