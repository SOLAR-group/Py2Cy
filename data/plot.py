import importlib
from multiprocessing.connection import wait
from statistics import median
import time
import timeit
from turtle import st
from unittest.mock import patch
import subprocess
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import unchanged as unchanged
import cython25 as cy_25
import cython75 as cy_75
import fib
new = mpl.rc_params().copy()
new["pdf.fonttype"] = 42
new["ps.fonttype"] = 42


# # with open('cython_75.txt', 'w') as file:
# #     json.dump(cython_75, file)

# print("Best Patch: " + best_patch)

# print("Compilation Fails: " + str(compilation_fails//30))
# print("Wrong Values: " + str(wrong//30))
# print("Bug Found: " + str(bugs//30))

def plot():
    cython_25 = []
    python_25 = []
    cython_75 = []
    python_75 = []

    unchanged_25 = []
    unchanged_75 = []
    for i in range(30):
        start = time.time()
        fib.fib(25)
        end = time.time()
        python_25.append(np.log(end-start))

    for i in range(30):
        start = time.time()
        fib.fib(75)
        end = time.time()
        python_75.append(np.log(end-start))

    for i in range(30):
        start = timeit.default_timer()
        unchanged.fib(25)
        unchanged_25.append(np.log(timeit.default_timer() - start))

    for i in range(30):
        start = timeit.default_timer()
        unchanged.fib(75)
        unchanged_75.append(np.log(timeit.default_timer() - start))

    for i in range(30):
        start = timeit.default_timer()
        cy_25.fib(25)
        cython_25.append(np.log(timeit.default_timer() - start))

    for i in range(30):
        start = timeit.default_timer()
        cy_75.fib(75)
        cython_75.append(np.log(timeit.default_timer() - start))

    cython_data = [cython_25, cython_75]
    cython2_data = [unchanged_25, unchanged_75]
    python_data = [python_25, python_75]

    print(cython_data)
    print(cython2_data)
    print(python_data)

    ticks = ['n=25', 'n=75']

    def set_box_color(bp, color):
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['caps'], color=color)
        plt.setp(bp['medians'], color=color)

    with mpl.rc_context(new):
        plt.figure()

        bp1 = plt.boxplot(cython_data, positions=np.array(
            range(len(cython_data)))*3.0-0.6, sym='', widths=0.5)
        bp2 = plt.boxplot(cython2_data, positions=np.array(
            range(len(cython2_data)))*3.0, sym='', widths=0.5)
        bp3 = plt.boxplot(python_data, positions=np.array(
            range(len(python_data)))*3.0+0.6, sym='', widths=0.5)
        # colors are from http://colorbrewer2.org/
        set_box_color(bp1, '#D7191C')
        set_box_color(bp2, '#FFA500')
        set_box_color(bp3, '#2C7BB6')

        # draw temporary red and blue lines and use them to create a legend
        plt.plot([], c='#D7191C', label='Typed Cython')
        plt.plot([], c='#FFA500', label='Untyped Cython')
        plt.plot([], c='#2C7BB6', label='Python')
        plt.legend()

        plt.xticks(range(0, len(ticks) * 2, 3), ticks)
        plt.xlim(-2, len(ticks)*2)
        plt.tight_layout()
        plt.ylabel("Log(Runtime)")
        plt.show()
        # plt.savefig('boxcompare.png')
        print(median(cython_25))
        print(median(cython_75))
        print(median(unchanged_25))
        print(median(unchanged_75))
        print(median(python_25))
        print(median(python_75))

        with open('unchanged_25.txt', 'w') as file:
            json.dump(unchanged_25, file)

        with open('unchanged_75.txt', 'w') as file:
            json.dump(unchanged_75, file)

        with open('cython_unchanged.txt', 'w') as file:
            json.dump(unchanged_25, file)

        with open('cython_75.txt', 'w') as file:
            json.dump(cython_75, file)

        with open('cython_25.txt', 'w') as file:
            json.dump(cython_25, file)


# print("Speedup = {}".format(py_time / cy_time))
if __name__ == "__main__":
    # print(fib_unchanged.fib(10))

    plot()
    # files = ['fib35.pyx', 'fib20.pyx', 'fib173.pyx', 'fib162.pyx', 'fib82.pyx', 'fib90.pyx', 'fib276.pyx', 'fib228.pyx', 'fib82.pyx', 'fib20.pyx', 'fib284.pyx', 'fib19.pyx', 'fib228.pyx', 'fib98.pyx', 'fib53.pyx',
    #          'fib53.pyx', 'fib228.pyx', 'fib228.pyx', 'fib27.pyx', 'fib228.pyx', 'fib292.pyx', 'fib82.pyx', 'fib53.pyx', 'fib148.pyx', 'fib181.pyx', 'fib228.pyx', 'fib162.pyx', 'fib211.pyx', 'fib148.pyx', 'fib228.pyx']
    # seen = {}
    # for file in files:
    #     if file in seen:
    #         seen[file] += 1
    #     else:
    #         seen[file] = 1

    # print(seen)
    # cython_75 = test(75)
