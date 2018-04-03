import time
from multiprocessing import Pool, cpu_count

from KT1gen import KeyGen


def do_gen(num):
    keygen = KeyGen()
    for i in range(num):
        keygen.gen_valid_key()


if __name__ == '__main__':
    cpus = cpu_count()
    single_job = int(100000 / cpus)
    p = Pool(cpus)

    t = time.time()
    p.map(do_gen, [single_job] * cpus)
    print(time.time() - t)
