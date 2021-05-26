import csv
import os
import numpy as np
import matplotlib
##matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt


t = np.arange(-1,8,0.01)
vf = (t<1)*0 + ((t>1)&(t<3))*10 + (t>3)*0
vc = (t<1)*0 + ((t>1)&(t<3))*10*(1-np.exp(-(t-1))) + (t>3)*(10*(1-np.exp(-2)))*np.exp(-(t-3))
ic = (t<1)*0 + ((t>1)&(t<3))*10*np.exp(-(t-1)) + (t>3)*-(10*(1-np.exp(-2)))*np.exp(-(t-3))

### Remove the csv file if it exists
try:
    os.remove("resp_comp_RC.csv")
except:
    print("csv file does not exist")
### Open the file, append header, then append data
with open("resp_comp_RC.csv", "ab") as file:
    np.savetxt(file, np.column_stack(['t','vf','vc','ic']) , delimiter = ",", fmt='%s')
    np.savetxt(file, np.column_stack([t,vf,vc,ic]) , delimiter = "," , fmt='%1.4f' )

plt.plot(t,vf,label=r'$v_f(t)$')
plt.plot(t,vc,label=r'$v_c(t)$')
plt.plot(t,ic,label=r'$i_c(t)$')
#plt.xlim([-0.5,5.5])
plt.ylim([-10,10])
plt.legend()
plt.show()