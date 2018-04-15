def j_from_D(D):
    j = []
    if 4 in D:
        j.append(D.index(4) + 1)
    else:
        raise RuntimeError('Cannot compute j')
    for i in range(1, 8):
        tmp = 4 * j[-1]
        if tmp in D:
            j.append(D.index(tmp) + 1)
        else:
            raise RuntimeError('Cannot compute j')
    if max(j) != 9 or min(j) != 2 or len(set(j)) != 8:
        raise RuntimeError('Cannot compute j')
    return j