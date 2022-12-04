import random

# Hard-code MISMATCH cost
MISMATCH = {
    "A": {
        "A": 0,
        "C": 110,
        "G": 48,
        "T": 94,
    },
    "C": {
        "A": 110,
        "C": 0,
        "G": 118,
        "T": 48,
    },
    "G": {
        "A": 48,
        "C": 118,
        "G": 0,
        "T": 110,
    },
    "T": {"A": 94, "C": 48, "G": 110, "T": 0},
}
# Hard-code GAP cost
GAP = 30


def alignDp(str1: str, str2: str):
    m, n = len(str1), len(str2)
    memo = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1, 1):
        memo[i][0] = GAP * i
    for j in range(1, n + 1, 1):
        memo[0][j] = GAP * j
    for i in range(1, m + 1, 1):
        for j in range(1, n + 1, 1):
            memo[i][j] = min(
                memo[i - 1][j - 1] + MISMATCH[str1[i - 1]][str2[j - 1]],
                memo[i - 1][j] + GAP,
                memo[i][j - 1] + GAP,
            )
    # print(memo[-1])
    i, j = m, n
    ret = []
    while i > 0 or j > 0:
        ret.append((i, j))
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        elif memo[i][j] == memo[i - 1][j - 1] + MISMATCH[str1[i - 1]][str2[j - 1]]:
            i, j = i - 1, j - 1
        elif memo[i][j] == memo[i - 1][j] + GAP:
            i = i - 1
        else:
            j = j - 1
    ret.append((0, 0))
    return (ret[::-1], memo[-1][-1])


# solve String Alignment problem using less memory
def alignMemSave(str1: str, str2: str):

    # Calculate the optimal value of the instance space from (l1, l2) to (r1, r2)
    # Return the final optimal value
    # Corresponding to the alignDP(str1[l1:r1], str2[l2:r2])
    # PRE: r1!=l1
    def optMemSave(l1, r1, l2, r2, str1, str2) -> list[int]:
        # The length of return array
        n = abs(r2 - l2) + 1
        # Incremental direction
        inc = (r1 - l1) // abs(r1 - l1)
        if inc < 0:
            l1, r1, l2, r2 = l1 - 1, r1 - 1, l2 - 1, r2 - 1
        # return array
        memo = [i * GAP for i in range(n)]
        for i in range(l1, r1, inc):
            oldMemo = memo.copy()
            memo[0] = GAP * (abs(i - l1) + 1)
            for j in range(l2, r2, inc):
                k = abs(j - l2)
                memo[k + 1] = min(
                    oldMemo[k] + MISMATCH[str1[i]][str2[j]],
                    oldMemo[k + 1] + GAP,
                    memo[k] + GAP,
                )
        return memo

    # explore the searching space from (l1, l2) to (r1, r2)
    def simpleDp(l1, r1, l2, r2, str1, str2) -> list[tuple[int, int]]:
        n, m = r2 - l2, r1 - l1
        memo = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            memo[i][0] = GAP * i
        for j in range(n + 1):
            memo[0][j] = GAP * j
        for i in range(m):
            for j in range(n):
                memo[i + 1][j + 1] = min(
                    memo[i][j] + MISMATCH[str1[i + l1]][str2[j + l2]],
                    memo[i][j + 1] + GAP,
                    memo[i + 1][j] + GAP,
                )
        i, j = m, n
        temp = []
        while i > 0 or j > 0:
            temp.append((l1 + i, l2 + j))
            if i == 0:
                j -= 1
            elif j == 0:
                i -= 1
            elif (
                memo[i][j]
                == memo[i - 1][j - 1] + MISMATCH[str1[l1 + i - 1]][str2[l2 + j - 1]]
            ):
                i, j = i - 1, j - 1
            elif memo[i][j] == memo[i - 1][j] + GAP:
                i = i - 1
            else:
                j = j - 1
        temp.append((l1 + i, l2 + j))
        return temp[::-1]

    # divide&conquer the instance space of (l1, l2) to (r1, r2)
    def divAndCon(l1, r1, l2, r2, str1, str2, ret: list[tuple[int, int]]):
        if l1 + 1 >= r1:
            ret.extend(simpleDp(l1, r1, l2, r2, str1, str2)[1:])
            return
        mid = l1 + (r1 - l1) // 2
        mForward = optMemSave(l1, mid, l2, r2, str1, str2)
        mBackward = optMemSave(r1, mid, r2, l2, str1, str2)[::-1]
        mn = float("inf")
        ind = l2
        for i, e in enumerate(zip(mForward, mBackward)):
            if mn > e[0] + e[1]:
                mn = e[0] + e[1]
                ind = i + l2
        divAndCon(l1, mid, l2, ind, str1, str2, ret)
        divAndCon(mid, r1, ind, r2, str1, str2, ret)

    swapped = False
    if len(str1) < len(str2):
        str1, str2 = str2, str1
        swapped = True

    res = [(0, 0)]
    divAndCon(0, len(str1), 0, len(str2), str1, str2, res)

    if swapped:
        res = [(j, i) for i, j in res]
        str1, str2 = str2, str1

    res.sort(key=lambda x: x[1])
    res.sort(key=lambda x: x[0])
    # print(res)
    cost = 0
    for i in range(1, len(res), 1):
        if res[i - 1][0] + 1 == res[i][0] and res[i - 1][1] + 1 == res[i][1]:
            cost += MISMATCH[str1[res[i][0] - 1]][str2[res[i][1] - 1]]
        else:
            cost += GAP

    return (res, cost)


# expand string on the given position
def expandStr(base: str, position: int):
    return base[: position + 1] + base + base[position + 1 :]


# calculate alignment string
def getAlignment(str1, str2, path: list[tuple[int, int]]) -> tuple[str, str]:
    o1, o2 = [], []
    for prev, cur in zip(path[:-1], path[1:]):
        o1.append(str1[cur[0] - 1] if cur[0] == prev[0] + 1 else "_")
        o2.append(str2[cur[1] - 1] if cur[1] == prev[1] + 1 else "_")
    return ("".join(o1), "".join(o2))


# generate random string from given letters and of the given length
def genRandStr(letters: list[str], length: int) -> str:
    ret = []
    for i in range(length):
        ret.append(letters[random.randrange(0, len(letters))])
    return "".join(ret)


# Testing codes.
if __name__ == "__main__":
    # str1, str2 = "ACACTGACT", "TATTATACGCTATTATACGCGACGCGGACGCG"
    # m, n = len(str1), len(str2)
    # mid = m // 2
    # path = alignMemSave(str1, str2)[0]
    # print(getAlignment(str1, str2, path))
    # print(alignDp(str1, str2))
    # print(alignMemSave(str1, str2))
    cur = "ACTG"
    cur = expandStr(cur, 3)
    cur = expandStr(cur, 6)
    cur = expandStr(cur, 1)
    print(cur)
