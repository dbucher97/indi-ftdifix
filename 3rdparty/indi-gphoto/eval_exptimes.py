#! /usr/bin/python3
import os, glob
import PIL.Image as img
import matplotlib.pyplot as plt
from scipy import stats

path = "/home/david/Ekos/Light/" 
N = 5
times = [2, 5, 10, 20, 30, 60, 120, 300, 600]

files = sorted(glob.glob(path+"test*"))
get_exp_time = lambda f: float(os.popen("exiftool -s -S -ShutterSpeed %s" % f).read().strip())
exp_times = list(map(get_exp_time, files))

def reduce_avg(exp_times, n=5):
    s = 0
    for i, exp_time in enumerate(exp_times):
        s += exp_time
        if (i+1)%n == 0:
            print(exp_times[i-n+1:i+1], s/n)
            yield s/n
            s = 0
        
data = list(reduce_avg(exp_times, n=N))

plt.plot(times[:len(data)], data, "o")

params = stats.linregress(times[:len(data)], data)
print(params)

a = 1/params[0]
b = -params[1]/params[0]

print(a, b)

print(list(map(lambda x: a*x+b, data)))

plt.plot(times, list(map(lambda x: params[0]*x+params[1], times)))

plt.show()
