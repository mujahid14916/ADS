import random
from time import time


# random.seed(50)


def is_prime(n):
    for i in range(2, n//2 + 1):
        if n % i == 0:
            return False
    return True


def get_prime(start, count=1, step=1, multiplier=False):
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
        while size > n:
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


def linear_search(table, element):
    n = 0
    size = len(table)
    while size > n:
        key = (element + n) % size
        if table[key] == element:
            return n+1, key, 'F'
        else:
            n += 1
    return n, -1, 'NF'


def quadratic_insert(table, data):
    insert_fail = 0
    collision = []
    size = len(table)
    stop_size = size//2
    for val in data:
        n = 0
        while stop_size > n:
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


def quadratic_search(table, element):
    n = 0
    size = len(table)
    while size > n:
        key = (element + n * n) % size
        if table[key] == element:
            return n+1, key, 'F'
        else:
            n += 1
    return n, -1, 'NF'


def d_hash_insert(table, data):
    insert_fail = 0
    collision = []
    size = len(table)
    prime = next(get_prime(size, 1, -1))
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


def d_hash_search(table, element):
    size = len(table)
    n = 0
    prime = next(get_prime(size, 1, -1))

    key = element % size
    if table[key] == element:
        return n+1, key, 'F'
    else:
        n = 1
        offset = prime - element % prime
        while size > n:
            key = (key + offset) % size
            if table[key] == element:
                return n+1, key, 'F'
            else:
                n += 1
    return n, -1, 'NF'


def rehash_insert(table, data):
    collision = []
    size = len(table)
    stop_size = size//2
    i = 0
    for val in data:
        n = 0
        if i > len(table)//2:
            table = [None] * next(get_prime(2*len(table), 1, 1))
            size = len(table)
            stop_size = size//2
            _, collision, _ = quadratic_insert(table, data[:i])
            # n = sum(c)
        while stop_size > n:
            key = (val + n*n) % size
            if table[key] is None:
                table[key] = val
                break
            else:
                n += 1
        collision.append(n)
        i += 1
    return table, collision, 0


def rehash_search(table, element):
    n = 0
    size = len(table)
    while size > n:
        h = (element + n*n) % size
        if table[h] == element:
            return n+1, h, 'F'
        n += 1
    return n, -1, 'NF'


def cuckoo_insert(table, data):
    m = 2*len(table)
    while True:
        m = 2*m
        # TODO: Actual Collisions
        collisions = []
        insert_failed = False
        hashed = {}
        next_prime = next(get_prime(m))
        for val in data:
            hashed[val] = [val % m, (val*next_prime) % m]

        table1 = [None] * m
        table2 = [None] * m

        for val in data:
            element_to_insert = val
            count = 0
            while element_to_insert:
                first = hashed[element_to_insert][0]
                if table1[first] is None:
                    table1[first] = element_to_insert
                    element_to_insert = None
                else:
                    count += 1
                    element_to_insert, table1[first] = table1[first], element_to_insert
                    second = hashed[element_to_insert][1]
                    if table2[second] is None:
                        table2[second] = element_to_insert
                        element_to_insert = None
                    else:
                        count += 1
                        element_to_insert, table2[second] = table2[second], element_to_insert
                if count > m:
                    insert_failed = True
                    break
            if insert_failed:
                break
            collisions.append(count)
        if not insert_failed:
            break
    return [table1, table2], collisions, 0


def cuckoo_search(table, val):
    comps = 0
    table_size = len(table[0])
    h1 = val % table_size
    comps += 1
    if table[0][h1] == val:
        return comps, h1, 'F'
    h2 = (val*get_prime(table_size)) % table_size
    comps += 1
    if table[1][h2] == val:
        return comps, h2, 'F'
    return comps, -1, 'NF'


def main():
    hash_methods = {
        'Linear': linear_insert,
        'Quadratic': quadratic_insert,
        'Double Hash': d_hash_insert,
        'Rehash': rehash_insert,
        'Cuckoo': cuckoo_insert,
    }

    for _ in range(91):
        print('-', end='')
    print()
    print('A: Table Size')
    print('B: Total Collisions')
    print('C: Total Insert Failed')
    print('D: Total Time Taken')
    print("{:13s}{:30s}{:7s}{:15s}".format('{:>10s}'.format("A"),
                                           '{:>27s}'.format("B"),
                                           '{:>5s}'.format("C"),
                                           '{:>12s}'.format("D")))
    for _ in range(91):
        print('-', end='')
    print()
    for k in get_prime(10, 5, 20, True):
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
            print("{:13s}{:30s}{:7s}{:15s}"
                  .format('{:>10s}'.format(str(size)),
                          '{:12s}'.format(name) + '{:>15s}'.format(str(sum(collision))),
                          '{:>5s}'.format(str(insert_fail)),
                          '{:>12s}'.format('{:0.4f}'.format(t) + ' s'))
                  )
        for _ in range(91):
            print('-', end='')
        print()


if __name__ == '__main__':
    main()
