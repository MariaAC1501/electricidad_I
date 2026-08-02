import csv
import numpy as np
import matplotlib.pyplot as plt

title = np.array(['','','',''])
t = np.array([])
vc = np.array([])
ic = np.array([])
#data = np.array([0,0,0,0])

with open("resp_comp_RC.csv", mode="r")as file:
    read = csv.reader(file)
    row_count = 0
    for row in read:
        if row_count == 0:
            title = row
            row_count += 1
        #elif row_count == 1:
         #   data = row
        #     row_count += 1
        else:
            t = np.append(t,float(row[0]))
            vc = np.append(vc,float(row[2]))
            ic = np.append(ic,float(row[3]))
print("Las columnas son:")
print(title)

plt.plot(t,vc,t,ic)
plt.show()
