pParament = 4.
moveDelayTime = 10
moveDelayMin = 4
moveDelayMax = 100
weight_smooth = 0.1
tolerance = 0.00001

# def smooth(path, fix, weight_data=0.0, weight_smooth=0.1, tolerance=0.00001):
#     #
#     # Enter code here.
#     # The weight for each of the two new equations should be 0.5 * weight_smooth
#     #
#     newpath = deepcopy(path)
#     error = tolerance
#     while error >= tolerance:
#         error = 0.0
#         for i in range(len(path)):
#             for j in range(len(path[0])):
#                 if not fix[i]:
#                     aux = newpath[i][j]
#                     newpath[i][j] += weight_smooth * (newpath[(i - 1) % len(path)][j] + newpath[(i + 1) % len(path)][j] - 2.0*newpath[i][j])\
#                          + (weight_smooth / 2.0) * (2.0 * newpath[(i - 1) % len(path)][j] - newpath[(i - 2) % len(path)][j] - newpath[i][j])+ \
#                          (weight_smooth / 2.0) * (2.0 * newpath[(i + 1) % len(path)][j] - newpath[(i + 2) % len(path)][j] - newpath[i][j])
#                     error += abs(newpath[i][j] - aux)
#     return newpath


# path = []
new_path = []
flexible = []
accelerate_limit = 0.5
max_rotation = 180

for i in range(max_rotation):
    # path.append(0)
    new_path.append(0)
    flexible.append(0)

def PathInitialize():
    for i in range(max_rotation):
        new_path[i] = 0
        flexible[i] = 0

def Smooth():
    error = tolerance
    while error >= tolerance:
        error = 0.0
        for i in range(max_rotation):
            if flexible[i] == 1:
                aux = new_path[i]
                new_path[i] += (weight_smooth * (new_path[i - 1] + new_path[i + 1] - 2 * new_path[i]) +
                                (weight_smooth / 2) * (2 * new_path[i - 1] - new_path[i - 2] - new_path[i]) +
                                (weight_smooth / 2) * (2 * new_path[i + 1] - new_path[i + 2] - new_path[i]))
                error += abs(new_path[i] - aux)


def ComputeParameter(targetAngle, currentAngle):
    PathInitialize()
    scala = abs(currentAngle - targetAngle)
    for i in range(0, scala):
        new_path[i] = 1.0
    for i in range(2, scala - 2):
        flexible[i] = 1
    mid_index = int(scala / 2)
    mid_value = 1.0 - float(mid_index) * accelerate_limit / moveDelayTime
    if (mid_value < float(moveDelayMin) /  moveDelayTime):
        mid_value = float(moveDelayMin) /  moveDelayTime
    new_path[mid_index] = mid_value
    flexible[mid_index] = 0
    Smooth()


def ComputeParament(parament, targetAngle, k, currentAngle):
    scala = abs(currentAngle - targetAngle);
    if (targetAngle >= k):
        parament = 1. - (float(targetAngle) - k) / scala;
    else:
        parament = 1. - (float(k) - targetAngle) / scala;
    # print parament, ','
    if (parament < 0.5):
        parament = 1 - parament;
    # print parament, ','
    parament -= 1.0;
    parament *= pParament;
    parament += 1.0;

    if (parament < 4. / moveDelayTime):
        parament = 4. / moveDelayTime;
    if (parament > 100. / moveDelayTime):
        parament = 100 / moveDelayTime;
    # print parament, ','
    return parament;

def main():
    currentAngle = 0
    targetAngle = 10;
    parament = 0;
    # for k in range(currentAngle,targetAngle):
        # parament = ComputeParament(parament, targetAngle, k, currentAngle);
        # print parament, ','
    ComputeParameter(targetAngle, currentAngle)
    print  new_path

main()