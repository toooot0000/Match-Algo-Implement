from algo import *
from IO import *
from tracker import *
import multiprocessing as mp
import sys


def doDP(str1, str2, queue: mp.Queue):
    ret = tracker(alignDp, args = (str1, str2))
    ret["method"] = "Dynamic Programming"
    ret["align"] = getAlignment(str1, str2, ret["ret"][0])
    queue.put(ret)


def doMemSave(str1, str2, queue: mp.Queue):
    ret = tracker(alignMemSave, args = (str1, str2))
    ret["method"] = "Divide and Conquer"
    ret["align"] = getAlignment(str1, str2, ret["ret"][0])
    queue.put(ret)


def executeAlgo(algo):
    filename = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
    output = "output.txt" if len(sys.argv) < 3 else sys.argv[2]
    try:
        str1, str2 = handleInput(filename)
        # print(str1, str2)
        ret = tracker(algo, args = (str1, str2))
        ret["align"] = getAlignment(str1, str2, ret["ret"][0])
        ret["method"] = ""
        handleOutput([ret], pretty=False, output=output)
    except OSError:
        print("File not found!\n Filename: %s"%filename)


if __name__ == "__main__":
    filename = "input.txt" if len(sys.argv) == 1 else sys.argv[1]
    # print("Current input : %s"%filename)
    try:
        str1, str2 = handleInput(filename)
        q = mp.Queue()
        proc1 = mp.Process(target=doDP, args=(str1, str2, q))
        proc2 = mp.Process(target=doMemSave, args=(str1, str2, q))
        proc1.start()
        proc2.start()
        proc1.join()
        proc2.join()
        dpRet, memSaveRet = q.get(), q.get()
        if dpRet["method"] == "Divide and Conquer":
            dpRet, memSaveRet = memSaveRet, dpRet
        handleOutput([dpRet, memSaveRet])
    except OSError:
        print("File not found! Filename = %s"%filename)
