import random
from time import time
from sys import getsizeof


random.seed(50)


def is_prime(n):
    """
    Return True if n is prime else False
    """
    for i in range(2, n//2 + 1):
        if n % i == 0:
            return False
    return True


def get_prime(start, count=1, step=1, multiplier=False):
    """
    Returns Prime Number Generator
    :param start: int -- Starting number to find next prime
    :param count: int -- Number of primes required (default 1)
    :param step: int -- Increment number after prime is found, when count > 1 (default 1)
    :param multiplier: boolean -- Step as multiplier or adder (default False)
    :return: Generator -- Prime Number Generator
    """
    i = 0
    number = start
    if is_prime(number):
        number += step
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
    size = len(table)
    collision = [0] * len(data)
    stop_size = size//2
    for i, val in enumerate(data):
        n = 0
        if i > len(table)//2:
            table = [None] * next(get_prime(2*len(table), 1, 1))
            size = len(table)
            stop_size = size//2
            _, prior_collision, _ = quadratic_insert(table, data[:i])
            for index, count in enumerate(prior_collision):
                collision[index] += count
        while stop_size > n:
            key = (val + n*n) % size
            if table[key] is None:
                table[key] = val
                break
            else:
                n += 1
        collision[i] += n
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
    size = len(table)
    collisions = [0] * len(data)
    while True:
        insert_failed = False
        hashed = {}
        next_prime = next(get_prime(size))
        for val in data:
            hashed[val] = [val % size, (val*next_prime) % size]

        table1 = [None] * size
        table2 = [None] * size

        for i, val in enumerate(data):
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
                if count > 2*size:
                    insert_failed = True
                    break
            if insert_failed:
                index = i
                collisions[index] += count
                size = 2 * size
                break
            collisions[i] += count
        if not insert_failed:
            break
    return [table1, table2], collisions, 0


def cuckoo_search(table, element):
    comps = 0
    table_size = len(table[0])
    h1 = element % table_size
    comps += 1
    if table[0][h1] == element:
        return comps, h1, 'F'
    h2 = (element * next(get_prime(table_size))) % table_size
    comps += 1
    if table[1][h2] == element:
        return comps, h2, 'F'
    return comps, -1, 'NF'


def get_time_taken(time_taken_in_sec):
    if time_taken_in_sec < 60:
        return '{:0.2f} S'.format(time_taken_in_sec)

    time_taken_in_min = time_taken_in_sec / 60
    if time_taken_in_min < 60:
        return '{:0.2f} M'.format(time_taken_in_min)

    time_taken_in_hour = time_taken_in_min / 60
    return '{:0.2f} H'.format(time_taken_in_hour)


def get_table_size(table):
    b = getsizeof(table)
    b += sum(getsizeof(i) for i in table)
    if isinstance(table[0], list):
        for tab in table:
            b += sum(getsizeof(i) for i in tab)

    if b < 1024:
        return '{:0.2f} B'.format(b)

    kb = b/1024
    if kb < 1024:
        return '{:0.2f} KB'.format(kb)

    mb = kb/1024
    if mb < 1024:
        return '{:0.2f} MB'.format(mb)

    gb = mb/1024
    return '{:0.2f} GB'.format(gb)


def get_lambda_factor(table):
    table_size = 0
    filled_slots = 0
    if isinstance(table[0], list):
        for tab in table:
            table_size += len(tab)
            filled_slots += sum(1 for i in tab if i is not None)
    else:
        table_size = len(table)
        filled_slots = sum(1 for i in table if i is not None)
    lambda_factor = filled_slots/table_size
    return '{:0.6f}'.format(lambda_factor)


def main():
    hash_methods = [
        ('Linear', linear_insert, linear_search),
        ('Quadratic', quadratic_insert, quadratic_search),
        ('Double Hash', d_hash_insert, d_hash_search),
        ('Rehash', rehash_insert, rehash_search),
        ('Cuckoo', cuckoo_insert, cuckoo_search),
    ]

    for _ in range(90):
        print('-', end='')
    print()
    print('HT:\t\tHashing Technique')
    print('\t\tL = Linear, Q = Quadratic, D = Double, R = Rehash, C = Cuckoo')
    print('TIF:\tTotal Insert Failed')
    print('SR:\t\tSearch Result -> F = Found, NF = Not Found')
    for _ in range(90):
        print('-', end='')
    print()

    print("{:13s}{:3s}{:17s}{:5s}{:10s}{:15s}{:5s}{:14s}{:8s}"
          .format('{:>10s}'.format("Table Size"),
                  '{:>2s}'.format("HT"),
                  '{:>15s}'.format("Collisions"),
                  '{:>3s}'.format("TIF"),
                  '{:>8s}'.format("Time"),
                  '{:>12s}'.format("Search Comps"),
                  '{:>3s}'.format("SR"),
                  '{:>10s}'.format("Mem Size"),
                  '{:>8s}'.format("\u03bb"),
                  ))
    for _ in range(90):
        print('-', end='')
    print()
    for k in get_prime(10, 5, 20, True):
        data = random.sample(set(range(k * 5)), k)
        element_to_search = data[k-1]
        for p, (name, insert_method, search_method) in enumerate(hash_methods):
            table = [None] * k
            start = time()
            table, collision, insert_fail = insert_method(table, data)
            time_taken = time() - start
            comps, index, result = search_method(table, element_to_search)
            if p != 0:
                size = ''
            else:
                size = k
            print("{:13s}{:3s}{:17s}{:5s}{:10s}{:15s}{:5s}{:14s}{:8s}"
                  .format('{:>10s}'.format(str(size)),
                          '{:>2s}'.format(name[0]),
                          '{:>15s}'.format(str(sum(collision))),
                          '{:>3s}'.format(str(insert_fail)),
                          '{:>8s}'.format(get_time_taken(time_taken)),
                          '{:>12s}'.format(str(comps)),
                          '{:>3s}'.format(result),
                          '{:>10s}'.format(get_table_size(table)),
                          '{:>8s}'.format(get_lambda_factor(table)))
                  )
        for _ in range(90):
            print('-', end='')
        print()


if __name__ == '__main__':
    main()
