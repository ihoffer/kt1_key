#!/usr/bin/env python
"""
    Provides functions for verifying KT1-compliancy.
    For Cryptanalysis Project T.
    Compatible with Python 2.6+ AND Python 3.x
    Version 3.
    Author: Kwok Yin Cheng, Simon Boehm
"""


def verify_kt1(D, P, alpha, fail_fast=True, verbose=False):
    """
    Verifies if a key is KT1 compliant by executing all check functions.
    Each check function verifies a condition as defined in section B and
    are named according to the order they appear in that section.
    Parameters
    ----------
    D : list of int
        D of key to be verified, function f_D represented as a list with
        D[i] = v equivalent to f_D(i+1) -> v
    P : list of int
        P of key to be verified, function f_P represented as a list with
        P[i] = v equivalent to f_P(i+1) -> v
    alpha : int
        alpha of key to be verified
    fail_fast : bool
        Defaults to True. If True, function will return immediately after
        a check function returns False. If False, all check functions will
        be executed regardless of their returned value.
    verbose : bool
        Defaults to False. If True and fail_fast is True, the name of the
        first check function that returned False will be printed. If True and
        fail_fast is False, the returned value of every check function will
        be printed. If False, nothing will be printed.
    Returns
    -------
    bool
        True if key is KT1-compliant, False otherwise.
    """
    checks = [
        check_c0, check_c1, check_c2, check_c3, check_c4, check_c5, check_c6_c7,
        check_c8, check_c9, check_c10, check_c11, check_c12, check_c13,
        check_c14
    ]
    if fail_fast:
        for check in checks:
            if not check(D, P, alpha):
                if verbose:
                    print("{} returned False".format(check.__name__))
                return False
        return True
    else:
        results = [check(D, P, alpha) for check in checks]
        if verbose:
            print((D, P, alpha))
            for i in range(len(checks)):
                print("{:<15}: {}".format(checks[i].__name__, results[i]))
        return all(results)


#################################################################################
#                            HELPER CHECK FUNCTIONS                             #
#################################################################################
# Each function checks one condition laid out in section B.                     #
# They are named according to the order they appear in the section.             #
# e.g. check_c3 checks if condition 3 is true                                   #
# check_c6_c7 checks both c6 & c7                                               #
# The functions are independent of each other and can be executed in any order. #
#################################################################################


def check_c0(D, P, alpha):
    # CONDITION: D and P are injective AND
    # D : {1-9} -> {0-36}, P : {1-27} -> {1-36} and alpha in {1-36} (section 4.1)
    return (len(D) == len(set(D)) == 9 and len(P) == len(set(P)) == 27 and
            min(P) >= 1 and max(P) <= 36 and min(D) >= 0 and max(D) <= 36 and
            1 <= alpha <= 36)


def check_c1(D, P, alpha):
    # CONDITION: P(3) = 33, P(7) = 5, P(9) = 9, P(15) = 21, P(18) = 25, P(24) = 29
    return P[2] == 33 and P[6] == 5 and P[8] == 9 and P[14] == 21 and P[
        17] == 25 and P[23] == 29


W = [5, 9, 21, 25, 29, 33]


def check_c2(D, P, alpha):
    # CONDITION: For all 1>=i>=9 D(i) not in W
    for i in range(9):
        if D[i] in W:
            return False
    return True


def check_c3(D, P, alpha):
    # CONDITION: alpha not in W
    return alpha not in W


def check_c4(D, P, alpha):
    # CONDITION:
    # T = ({0,1,...,12}\W) INTERSECT ({P(1),P(2),...,P(24)} UNION {D(4),D(5),...,D(9)} UNION {alpha})
    # U = ({13,...,36}\W) INTERSECT ({P(26),P(27)} UNION {D(1),D(2),D(3)})
    # |T\{P(25)}| + |U\{P(25)}| <= 12
    T = set(
        [0, 1, 2, 3, 4, 6, 7, 8, 10, 11, 12]) & set(P[:23] + D[3:8] + [alpha])
    U = set([x for x in range(13, 37) if x not in W]) & set(P[26:28] + D[:3])
    if P[24] in T:
        T.remove(P[24])
    if P[24] in U:
        U.remove(P[24])
    return (len(T) + len(U)) <= 12


def check_c5(D, P, alpha):
    # CONDITION: D(1) = 0
    return D[0] == 0


def check_c6_c7(D, P, alpha):
    # CONDITION:
    # There exist {j1, j2, . . . , j7, j8} a permutation of {2, 3, . . . , 9} which
    # defines D(i) for every i in {2, 3, . . . , 9} as follows:
    # D(j1) = 4, D(j2) = 4*j1, D(j3) = 4*j2, . . . , D(j8) = 4*j7
    # CONDITION: P(20) = 4*j8
    x = D.index(4) + 1
    for _ in range(7):
        try:
            x = D.index(4 * x) + 1
        except ValueError:
            return False
    return P[19] == 4 * x


def check_c8(D, P, alpha):
    # CONDITION: (D(5), D(6)) in {8, 12, 16} x {20, 28, 32} UNION {24, 28, 32} x {8, 12, 16}
    return (D[4] in [8, 12, 16] and D[5] in [20, 28, 32]) or (
        D[4] in [24, 28, 32] and D[5] in [8, 12, 16])


def check_c9(D, P, alpha):
    # CONDITION: P(6) = D(8), P(13) = D(7)
    return P[5] == D[7] and P[12] == D[6]


def check_c10(D, P, alpha):
    # CONDITION: P(27) != 0 mod 4
    return P[26] % 4 != 0


def check_c11(D, P, alpha):
    # CONDITION: For all 1>=l>=9 There exists 1>=i>=26 s.t. P(i) = 4l
    for l in range(1, 10):
        if 4 * l not in P[:26]:
            return False
    return True


def check_c12(D, P, alpha):
    # CONDITION: D(3) in {P(1), P(2), P(4), P(5)}
    return D[2] in [P[0], P[1], P[3], P[4]]


def check_c13(D, P, alpha):
    # CONDITION: D(4) not in {P(14), P(16), P(17), P(19)}
    return D[3] not in [P[13], P[15], P[16], P[18]]


def check_c14(D, P, alpha):
    # CONDITION: {P(8), P(10), P(11), P(12)} INTERSECT {D(4), D(5), D(6)} = EMPTY SET
    return len(set([P[7], P[9], P[10], P[11]]) & set([D[3], D[4], D[5]])) == 0