import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from threading import Thread
from tkinter.scrolledtext import ScrolledText
from hashing import *
import numpy as np


def disable_buttons():
    global plt_btn, sim_btn, prime_btn
    plt_btn['state'] = DISABLED
    sim_btn['state'] = DISABLED
    prime_btn['state'] = DISABLED


def enable_buttons():
    global plt_btn, sim_btn, prime_btn
    plt_btn['state'] = NORMAL
    sim_btn['state'] = NORMAL
    prime_btn['state'] = NORMAL


def plot_close(evt):
    enable_buttons()


def plot_graph():
    global plt_btn, collisions, collisions_cum_sum
    if len(collisions_cum_sum):
        disable_buttons()
        fig = plt.figure('Random Graph')
        fig.canvas.mpl_connect('close_event', plot_close)
        x_labels = len(collisions_cum_sum[0])
        plt.xlabel('Items Inserted')
        plt.ylabel('Collisions')
        for i, c in enumerate(collisions_cum_sum):
            plt.plot(list(range(1, x_labels+1)), c, label=hash_methods[i][0])
        plt.legend(loc=1)
        plt.show()


def display_result(text):
    global result
    result.config(state=NORMAL)
    # result.delete('1.0', END)
    result.insert(INSERT, text)
    result.config(state=DISABLED)


def simulate_thread():
    global collisions, sim_btn, collisions_cum_sum, table_size, hash_methods
    disable_buttons()
    collisions_cum_sum = []
    data = random.sample(set(range(table_size * 5)), table_size)
    element_to_search = data[table_size - 1]
    message = ''
    message += '*' * 106 + '\n'
    message += 'Table Size: {}'.format(table_size) + '\n'
    message += '-' * 106 + '\n'
    message += "{:12s}{:17s}{:15s}{:10s}{:15s}{:15s}{:14s}{:8s}"\
        .format("Method",
                '{:>15s}'.format("Collisions"),
                '{:>13s}'.format("Insert Failed"),
                '{:>8s}'.format("Time"),
                '{:>12s}'.format("Search Comps"),
                '{:>13s}'.format("Search Result"),
                '{:>10s}'.format("Mem Size"),
                '{:>8s}'.format("\u03bb"),
                )
    message += '\n' + '-' * 106 + '\n'
    display_result(message)
    message = ''
    for p, (name, insert_method, search_method) in enumerate(hash_methods):
        table = [None] * table_size
        start = time()
        table, collision, insert_fail = insert_method(table, data)
        time_taken = time() - start
        collisions_cum_sum.append(np.cumsum(collision, dtype=np.uint32))
        comps, index, r = search_method(table, element_to_search)

        message += "{:12s}{:17s}{:15s}{:10s}{:15s}{:15s}{:14s}{:8s}"\
            .format(name,
                    '{:>15s}'.format(str(sum(collision))),
                    '{:>13s}'.format(str(insert_fail)),
                    '{:>8s}'.format(get_time_taken(time_taken)),
                    '{:>12s}'.format(str(comps)),
                    '{:>13s}'.format(r),
                    '{:>10s}'.format(get_table_size(table)),
                    '{:>8s}'.format(get_lambda_factor(table)))
        message += '\n'
        display_result(message)
        message = ''
    message += '*' * 106 + '\n' + '\n'
    display_result(message)
    enable_buttons()


def simulate():
    global table_size, prime
    try:
        table_size = int(prime.get())
        print(table_size)
    except ValueError as e:
        print("Invalid Size")
        return
    t = Thread(target=simulate_thread)
    t.start()


def fill_with_prime():
    global prime
    try:
        start = int(prime.get()) + 1
        prime.set(next(get_prime(start)))
    except ValueError as e:
        prime.set(2)
        print("Exception")


hash_methods = [
    ('Linear', linear_insert, linear_search),
    ('Quadratic', quadratic_insert, quadratic_search),
    ('Double Hash', d_hash_insert, d_hash_search),
    ('Rehash', rehash_insert, rehash_search),
    ('Cuckoo', cuckoo_insert, cuckoo_search),
]


collisions_cum_sum = []
collisions = []
table_size = 11
root = Tk()
# root.resizable(False, False)
root.title('Hashing Techniques Comparisons')

frame = ttk.Frame(root)
frame.pack(pady=5)

label = ttk.Label(frame, text='Table Size: ')
label.pack(side=LEFT)

prime = StringVar()
entry = ttk.Entry(frame, width=40, textvariable=prime)
entry.pack(side=LEFT, padx=5)

prime_btn = ttk.Button(frame, text="Get Closest Prime", command=fill_with_prime)
prime_btn.pack(side=LEFT, padx=5)


sim_btn = ttk.Button(root, text="Simulate", width=20, command=simulate)
sim_btn.pack()

plt_btn = ttk.Button(root, text="Comparison Graph", width=20, command=plot_graph)
plt_btn.pack(pady=5)

result = ScrolledText(root, width=106, height=15, wrap='none')
result.pack(padx=10, pady=10)
result.config(state=DISABLED)

root.mainloop()
