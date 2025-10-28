import os, re, csv
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np

def get_matcher(s):
    return f"p\\d-t\\d-s{s}.csv"

e = {
    "like": 0,
    "heart": 1,
    "yay": 2,
    "haha": 3,
    "sad": 4,
    "angry": 5
}

props = fm.FontProperties(fname="../NotoColorEmoji-Regular.ttf")

emoji = "👍❤️😊😆😥😡"

def make_matrix(s):
    contents = os.listdir("../raw-data")
    relevant_files = []
    for name in contents:
        if re.match(get_matcher(s), name):
            relevant_files.append(name)
    arr = [[],[],[],[],[],[]]
    for i in range(6):
        arr[i] = [0] * 6
    error_count = 0
    for file in relevant_files:
        with open(f"../raw-data/{file}") as f:
            reader = csv.reader(f)
            for row in reader:
                i1 = e[row[0]]
                i2 = e[row[1]]
                arr[i1][i2] += 1
                if i1 != i2:
                    error_count += 1
    return arr

def make_heatmap(arr):
    na = np.array(arr)
    plt.imshow(na, cmap='gray', interpolation='nearest', vmin=0, vmax=24)
    #plt.xlabel(emoji, fontproperties=props)
    #plt.ylabel(emoji, fontproperties=props)
    plt.show()

make_heatmap(make_matrix(1))