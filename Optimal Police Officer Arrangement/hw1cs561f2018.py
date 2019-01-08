import numpy as np
from itertools import combinations

f = open("input.txt")
lines = f.readlines()
f.close()
output = open("output.txt", "w")
n = int(lines[0])
p = int(lines[1])
s = int(lines[2])
matrix = np.zeros((n, n), dtype=np.int16)
for x in range(3, len(lines)):
    coord = lines[x].split(",")
    row = int(coord[0])
    col = int(coord[1])
    matrix[row, col] += 1

rows = combinations(range(n), p)
rows = list(rows)
res = 0


def dfs(officers, diag1, diag2, row):
    o = len(officers)
    if o == p:
        act = 0
        for x in range(p):
            act += matrix[row[x], officers[x]]
        global res
        res = max(res, act)
        return
    for co in range(n):
        if co in officers or row[o]-co in diag1 or row[o]+co in diag2: continue
        dfs(officers+[co], diag1+[row[o]-co], diag2+[row[o]+co], row)


for x in range(len(rows)):
    dfs([], [], [], rows[x])

output.write('%ld\n' %res)
