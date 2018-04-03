import numpy as np
from verifyKT1 import verify_kt1
from random import shuffle

class KeyGen:
    def get_V5(self):
        V5 = [1, 2, 3, 6, 7, 10, 11, 13, 14, 15, 17, 18, 19, 22, 23, 26, 27, 30, 31, 34, 35]
        np.random.shuffle(V5)
        return V5

    def construct_D(self):
        if np.random.randint(0, 1):
            l2 = np.random.choice([5, 7, 8])
            l1 = np.random.choice([2, 3, 4])
        else:
            l2 = np.random.choice([2, 3, 4])
            l1 = np.random.choice([6, 7, 8])

        #Modify V2
        V2 = [2, 3, 4, 7, 8, 9]
        shuffle(V2)
        if l1 != 6:
            V2.insert(V2.index(l1) + 1, 5)
            V2.insert(V2.index(l2) + 1, 6)
        else:
            V2.insert(V2.index(l2), 6)
            V2.insert(V2.index(l1), 5)

        D = np.zeros(9)
        for i in range(0, 8):
            D[V2[i] - 1] = 4 * V2[i - 1] if i > 0 else 4

        return (D, V2)

    def construct_P(self, V2, V3, D):
        P = np.zeros(27)
        P[2] = 33
        P[6] = 5
        P[8] = 9
        P[14] = 21
        P[17] = 25
        P[23] = 29
        P[19] = 4 * V2[7]
        P[5] = D[7]
        P[12] = D[6]

        temp = {1, 2, 4, 5}
        for i in V3:
            if i in temp:
                l3 = i
                break

        temp2 = {1, 2, 4, 5, 21, 22, 23, 25, 26} - {l3}
        for i in V3:
            if i in temp2:
                l4 = i
                break

        temp3 = {1, 2, 4, 5, 14, 16, 17, 19, 21, 22, 23, 25, 26} - {l3, l4}
        l5 = l6 = -1
        for i in V3:
            if i in temp3:
                if l5 == -1:
                    l5 = i
                else:
                    l6 = i
                    break

        temp4 = {1, 2, 4, 5, 8, 10, 11, 12, 14, 16, 17, 19, 21, 22, 23, 25, 26} - {l3, l4, l5, l6}
        l7 = l8 = -1
        for i in V3:
            if i in temp4:
                if l7 == -1:
                    l7 = i
                else:
                    l8 = i
                    break

        P[l3 - 1] = D[2]
        P[l4 - 1] = D[3]
        P[l5 - 1] = D[4]
        P[l6 - 1] = D[5]
        P[l7 - 1] = D[1]
        P[l8 - 1] = D[8]

        V5 = self.get_V5()
        i = 0
        for j in range(len(P)):
            if P[j] == 0:
                P[j] = V5[i]
                i += 1

        return P

    def choose_alpha(self):
        W = {5, 9, 21, 25, 29, 33}
        alpha = np.random.randint(1, 37)
        return alpha if alpha not in W else alpha + 1

    def gen_key(self):
        V3 = np.arange(1, 37)
        np.random.shuffle(V3)
        D, V2 = self.construct_D()
        P = self.construct_P(V2, V3, D)
        alpha = self.choose_alpha()
        return D, P, alpha

    def gen_valid_key(self):
        while True:
            D, P, alpha = self.gen_key()
            if verify_kt1(D.tolist(), P.tolist(), alpha):
                return D, P, alpha
