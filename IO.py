from algo import expandStr


def handleInput(filename: str = "input.txt"):
    try:
        actions = [i[:-1] if i[-1] == "\n" else i for i in open(filename).readlines()]
        str1 = actions[0]
        i = 1
        while actions[i].isdigit():
            str1 = expandStr(str1, int(actions[i]))
            i += 1
        str2 = actions[i]
        i += 1
        while i < len(actions) and actions[i]:
            str2 = expandStr(str2, int(actions[i]))
            i += 1
        return (str1, str2)
    except OSError:
        raise


def outputSingleResult(f, result):
    f.write(result["align"][0][:50] + " " + result["align"][0][-50:] + "\n")
    f.write(result["align"][1][:50] + " " + result["align"][1][-50:] + "\n")
    f.write("%.1f\n"%(result["ret"][1]))
    f.write("%.3f\n"%(result["time"] / (10 ** 9)))
    f.write("%.1f\n"%(result["mem"]))


def outputSingleResultPretty(f, result: dict):
    f.write("Method             : %s\n" % result["method"])
    f.write("Actual alignment   :\n")
    if len(result["align"][0]) > 100:
        f.write(
            "    " + result["align"][0][:50] + "..." + result["align"][0][-50:] + "\n"
        )
        f.write(
            "    " + result["align"][1][:50] + "..." + result["align"][1][-50:] + "\n"
        )
    else:
        f.write("    " + result["align"][0] + "\n")
        f.write("    " + result["align"][1] + "\n")

    f.write("Total cost         : %d\n" % result["ret"][1])
    f.write("Time usage         : %d μs\n" % (result["time"] / 1000))
    f.write("Mem usage          : %6.3f MB\n" % result["mem"])
    f.write("\n")


def handleOutput(results: list[dict], pretty=True, output="output.txt"):
    with open(output, mode="w") as f:
        for res in results:
            if pretty:
                outputSingleResultPretty(f, res)
            else:
                outputSingleResult(f, res)


if __name__ == "__main__":
    print(handleInput())
