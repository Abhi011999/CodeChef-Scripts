import os
import sys
import math
import random
from collections import defaultdict, Counter, deque
from itertools import permutations, combinations
from itertools import groupby, accumulate
from bisect import bisect_left, bisect_right
from functools import lru_cache

# sys.setrecursionlimit(200000000)
# MOD = 1000000000 + 7
PROFILE = False

input = lambda: sys.stdin.readline().rstrip("\r\n")
# print = lambda *args: sys.stdout.write(f"{args}\n")
_n = lambda: int(input())
_t = lambda: range(_n())
_in = lambda: list(map(int, input().split()))

###################################################################


def tc():
    pass


def main():
    for _ in _t():
        tc()


###################################################################


def init(profile=False):
    if profile:
        from pyinstrument import Profiler

        profiler = Profiler()
        profiler.start()

        main()

        profiler.stop()
        profiler.print(color=True, timeline=True)
    else:
        main()


try:
    # os.system("online_judge.py")
    sys.stdin = open("in.txt", "r")
    sys.stdout = open("out.txt", "w")
    sys.stderr = sys.stdout
    # from _in import *
except:
    pass


if __name__ == "__main__":
    init(PROFILE)
