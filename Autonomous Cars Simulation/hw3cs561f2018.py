import numpy as np
import time

start_time = time.time()
f = open("input.txt")
lines = f.readlines()
f.close()

s = int(lines[0])
n = int(lines[1])
o = int(lines[2])
obstacles = []
carStart = []
carEnd = []
for x in range(o):
    obstacles.append(lines[3+x])
for x in range(n):
    carStart.append(lines[3+o+x])
for x in range(n):
    carEnd.append(lines[3+o+n+x])

grid = np.full((s, s), -1, dtype=int)
for x in range(o):
    temp = obstacles[x].split(',')
    grid[int(temp[1])][int(temp[0])] = -101


def iteration(r, gamma, finish):
    n = len(r)
    u = np.zeros((n, n), dtype=np.float64)
    uprime = np.zeros((n, n), dtype=np.float64)
    delta = 1.0
    while delta >= finish:
        u = np.copy(uprime)
        delta = 0
        for i in range(n):
            for j in range(n):
                if r[j][i] == 99:
                    uprime[j][i] = float(99)
                    continue
                up = u[j-1][i] if j >= 1 else u[j][i]
                down = u[j+1][i] if j < n-1 else u[j][i]
                left = u[j][i-1] if i >= 1 else u[j][i]
                right = u[j][i+1] if i < n-1 else u[j][i]
                u_up = 0.7 * up + 0.1 * down + 0.1 * left + 0.1 * right
                u_down = 0.1 * up + 0.7 * down + 0.1 * left + 0.1 * right
                u_left = 0.1 * up + 0.1 * down + 0.7 * left + 0.1 * right
                u_right = 0.1 * up + 0.1 * down + 0.1 * left + 0.7 * right
                maxi = max(u_up, u_down, u_left, u_right)
                uprime[j][i] = r[j][i] + gamma * maxi
                delta = abs(uprime[j][i]-u[j][i]) if abs(uprime[j][i]-u[j][i]) > delta else delta
    return u


def turn_left(m):
    if m == '^':
        return '<'
    elif m == 'V':
        return '>'
    elif m == '>':
        return '^'
    elif m == '<':
        return 'V'


def turn_right(m):
    if m == '^':
        return '>'
    elif m == 'V':
        return '<'
    elif m == '>':
        return 'V'
    elif m == '<':
        return '^'


def afterMove(pos, m):
    temp = pos.split(',')
    i = int(temp[1])
    j = int(temp[0])
    if m == '<':
        j = j - 1 if j > 0 else j
    elif m == '>':
        j = j + 1 if j < s - 1 else j
    elif m == '^':
        i = i - 1 if i > 0 else i
    elif m == 'V':
        i = i + 1 if i < s - 1 else i
    return str(j) + ',' + str(i)


out = []
for x in range(n):
    R = np.copy(grid)
    temp = carEnd[x].split(',')
    R[int(temp[1])][int(temp[0])] = 99

    U = iteration(R, 0.9, 0.1*0.1/0.9)

    direc = np.zeros((s, s), dtype=str)
    for i in range(s):
        for j in range(s):
            if R[j][i] == 99:
                direc[j][i] = 'D'
            else:
                up = U[j - 1][i] if j >= 1 else U[j][i]
                down = U[j + 1][i] if j < s - 1 else U[j][i]
                left = U[j][i - 1] if i >= 1 else U[j][i]
                right = U[j][i + 1] if i < s - 1 else U[j][i]
                u_up = 0.7 * up + 0.1 * down + 0.1 * left + 0.1 * right
                u_down = 0.1 * up + 0.7 * down + 0.1 * left + 0.1 * right
                u_left = 0.1 * up + 0.1 * down + 0.7 * left + 0.1 * right
                u_right = 0.1 * up + 0.1 * down + 0.1 * left + 0.7 * right
                maxi = max(u_up, u_down, u_right, u_left)
                diff = u_up - u_left
                if maxi == u_up:
                    direc[j][i] = '^'
                elif maxi == u_down:
                    direc[j][i] = 'V'
                elif maxi == u_right:
                    direc[j][i] = '>'
                elif maxi == u_left:
                    direc[j][i] = '<'

    total = 0
    for j in range(10):
        pos = carStart[x]
        np.random.seed(j)
        swerve = np.random.random_sample(1000000)
        k = 0
        rSoFar = 0
        while pos != carEnd[x].strip():
            temp = pos.split(',')
            move = direc[int(temp[1])][int(temp[0])]
            if swerve[k] > 0.7:
                if swerve[k] > 0.8:
                    if swerve[k] > 0.9:
                        move = turn_right(turn_right(move))
                    else:
                        move = turn_right(move)
                else:
                    move = turn_left(move)
            k += 1
            pos = afterMove(pos, move)
            temp = pos.split(',')
            rSoFar += R[int(temp[1])][int(temp[0])]
        total += rSoFar
    simu = int(np.floor(float(total)/10))
    print simu
    out.append(simu)

output = open("output.txt", "a")
for x in range(len(out)):
    output.write('%ld\n' % out[x])
output.close()
print("--- %s seconds ---" % (time.time() - start_time))
