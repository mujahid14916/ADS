import random
from time import time


random.seed(50)


def is_prime(n):
    for i in range(2, n//2 + 1):
        if n % i == 0:
            return False
    return True


def get_prime(start, count=1, step=1, multiplier=True):
    i = 0
    number = start
    while count > i:
        while True:
            if number < 2:
                return
            if is_prime(number):
                i += 1
                yield number
                if multiplier:
                    number = number * step + 1
                else:
                    number += step
                break
            if multiplier:
                number += 1
            else:
                number += step


def linear_insert(table, data):
    insert_fail = 0
    collision = []
    size = len(table)
    for val in data:
        n = 0
        while n < size:
            key = (val + n) % size
            if table[key] is None:
                table[key] = val
                break
            else:
                n += 1
        else:
            insert_fail += 1
        collision.append(n)
    return table, collision, insert_fail


def quadratic_insert(table, data):
    insert_fail = 0
    collision = []
    size = len(table)
    stop_size = size//2
    for val in data:
        n = 0
        while n < stop_size:
            key = (val + n*n) % size
            if table[key] is None:
                table[key] = val
                break
            else:
                n += 1
        else:
            insert_fail += 1
        collision.append(n)
    return table, collision, insert_fail


def d_hash_insert(table, data):
    insert_fail = 0
    collision = []
    size = len(table)
    prime = next(get_prime(size, 1, -1, False))
    for val in data:
        n = 0
        key = val % size
        if table[key] is None:
            table[key] = val
        else:
            n = 1
            offset = prime - val % prime
            while n < size:
                key = (key + offset) % size
                if table[key] is None:
                    table[key] = val
                    break
                else:
                    n += 1
            else:
                insert_fail += 1
        collision.append(n)
    return table, collision, insert_fail


def rehash_insert(table, data):
    collision = []
    size = len(table)
    stop_size = size//2
    i = 0
    for val in data:
        n = 0
        if i > len(table)//2:
            table = [None] * next(get_prime(2*len(table), 1, 1, False))
            _, c, _ = quadratic_insert(table, data[:i])
            n = sum(c)
        while n < stop_size:
            key = (val + n*n) % size
            if table[key] is None:
                table[key] = val
                break
            else:
                n += 1
        collision.append(n)
        i += 1
    return table, collision, 0


def main():
    hash_methods = {
        'Linear': linear_insert,
        'Quadratic': quadratic_insert,
        'Double Hash': d_hash_insert,
        'Rehash': rehash_insert
    }

    for _ in range(91):
        print('-', end='')
    print()
    print("{:15s}{:35s}{:25s}{:25s}".format("Table Size",
                                            "Total Collisions",
                                            "Total Insert Failed",
                                            "Total Time Taken"))
    for _ in range(91):
        print('-', end='')
    print()
    for k in get_prime(10, 5, 20):
        data = random.sample(set(range(k * 5)), k)
        for p, (name, method) in enumerate(hash_methods.items()):
            table = [None] * k
            start = time()
            table, collision, insert_fail = method(table, data)
            t = time() - start
            if p != 0:
                size = ''
            else:
                size = k
            print("{:15s}{:35s}{:25s}{:25s}"
                  .format('{:>10s}'.format(str(size)),
                          '{:12s}'.format(name) + '{:>15s}'.format(str(sum(collision))),
                          '{:>10s}'.format(str(insert_fail)),
                          '{:>12s}'.format('{:0.4f}'.format(t) + ' s'))
                  )
        for _ in range(91):
            print('-', end='')
        print()


if __name__ == '__main__':
    main()
