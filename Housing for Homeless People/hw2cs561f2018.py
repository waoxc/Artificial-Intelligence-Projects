import time
start_time = time.time()
f = open("input31.txt")
lines = f.readlines()
f.close()
output = open("output.txt", "w")
b = int(lines[0])
p = int(lines[1])
L = int(lines[2])
L_so_far = list()
for x in range(3, 3+L):
    L_so_far.append(lines[x].strip())
S = int(lines[3+L])
S_so_far = list()
for x in range(4+L, 4+L+S):
    S_so_far.append(lines[x].strip())
A = int(lines[4+L+S])
applicants = list()
for x in range(5+L+S, 5+L+S+A):
    applicants.append(lines[x].strip())
bedArrange = ["0000000"]*b
parkArrange = ["0000000"]*p
idToDays = {}
for x in range(A):
    idToDays[applicants[x][:5]] = applicants[x][-7:]


def canArrange1(id, arrangement):
    for i in range(len(arrangement)):
        fit = True
        for j in range(7):
            if arrangement[i][j] != '1' or idToDays[id][j] != '1':
                fit = True
            else:
                fit = False
                break
        if fit:
            return True
    return False


def canArrange2(allids, arrangement):
    for i in range(len(allids)):
        if canArrange1(allids[i], arrangement):
            return True
    return False


def arrange(id, arrangement):
    days = idToDays[id]
    for i in range(len(arrangement)):
        arr1 = int(arrangement[i])
        arr2 = int(days)
        after = str(arr1+arr2)
        while len(after) < 7:
            after = '0'+after
        if after.find('2') >= 0:
            continue
        else:
            arrangement[i] = after
            return


def efficiency(days):
    count = 0
    for i in range(7):
        if days[i] == '1':
            count += 1
    return count


for x in range(L):
    if canArrange1(L_so_far[x], bedArrange):
        arrange(L_so_far[x], bedArrange)
for x in range(S):
    if canArrange1(S_so_far[x], parkArrange):
        arrange(S_so_far[x], parkArrange)

ava_to_LAHSA = list()
ava_to_SPLA = list()
for x in range(len(applicants)):
    id = applicants[x][:5]
    if id in L_so_far or id in S_so_far:
        continue
    gender = applicants[x][5:6]
    age = int(applicants[x][6:9])
    pets = applicants[x][9:10]
    med = applicants[x][10:11]
    car = applicants[x][11:12]
    license = applicants[x][12:13]

    if gender == 'F' and age > 17 and pets == 'N':
        ava_to_LAHSA.append(id)
    if car == 'Y' and license == 'Y' and med == 'N':
        ava_to_SPLA.append(id)

first = ''


def dfs(SPLA_ava, LAHSA_ava, SPLA_arrange, LAHSA_arrange, SPLAeff, LAHSAeff, isSPLA):
    if isSPLA:
        if not canArrange2(SPLA_ava, SPLA_arrange) and not canArrange2(LAHSA_ava, LAHSA_arrange):
            return [SPLAeff, LAHSAeff]
        elif not canArrange2(SPLA_ava, SPLA_arrange):
            return dfs(SPLA_ava, LAHSA_ava, SPLA_arrange, LAHSA_arrange, SPLAeff, LAHSAeff, not isSPLA)
        res = [SPLAeff, LAHSAeff]
        finalpick = ''
        for x in range(len(SPLA_ava)):
            pick = SPLA_ava[x]
            if not canArrange1(pick, SPLA_arrange):
                continue
            newSPLA_ava = list(SPLA_ava)
            newSPLA_ava.remove(pick)
            newLAHSA_ava = list(LAHSA_ava)
            if pick in newLAHSA_ava:
                newLAHSA_ava.remove(pick)
            newSPLA_arrange = list(SPLA_arrange)
            arrange(pick, newSPLA_arrange)
            next = dfs(newSPLA_ava, newLAHSA_ava, newSPLA_arrange, LAHSA_arrange, SPLAeff + efficiency(idToDays[pick]), LAHSAeff, not isSPLA)
            if next[0] > res[0]:
                res[0] = next[0]
                res[1] = next[1]
                finalpick = pick
        global first
        first = finalpick
        return res
    else:
        if not canArrange2(SPLA_ava, SPLA_arrange) and not canArrange2(LAHSA_ava, LAHSA_arrange):
            return [SPLAeff, LAHSAeff]
        elif not canArrange2(LAHSA_ava, LAHSA_arrange):
            return dfs(SPLA_ava, LAHSA_ava, SPLA_arrange, LAHSA_arrange, SPLAeff, LAHSAeff, not isSPLA)
        res = [SPLAeff, LAHSAeff]
        finalpick = ''
        for x in range(len(LAHSA_ava)):
            pick = LAHSA_ava[x]
            if not canArrange1(pick, LAHSA_arrange):
                continue
            newLAHSA_ava = list(LAHSA_ava)
            newLAHSA_ava.remove(pick)
            newSPLA_ava = list(SPLA_ava)
            if pick in newSPLA_ava:
                newSPLA_ava.remove(pick)
            newLAHSA_arrange = list(LAHSA_arrange)
            arrange(pick, newLAHSA_arrange)
            next = dfs(newSPLA_ava, newLAHSA_ava, SPLA_arrange, newLAHSA_arrange, SPLAeff , LAHSAeff + efficiency(idToDays[pick]), not isSPLA)
            if next[1] > res[1]:
                res[0] = next[0]
                res[1] = next[1]
        return res


print dfs(ava_to_SPLA, ava_to_LAHSA, parkArrange, bedArrange, 0, 0, True)
print first
output.write(first)
print("--- %s seconds ---" % (time.time() - start_time))

