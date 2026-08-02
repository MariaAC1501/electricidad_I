import csv
import os
import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt


t = np.arange(-1,9,0.01)
ifu = (t<1)*5 + ((t>1)&(t<4))*10 + (t>4)*5
il = (t<1)*5 + ((t>1)&(t<4))*10*(1-0.5*np.exp(-(t-1))) + (t>4)*(5 + ((10*(1-0.5*np.exp(-3))) - 5)*np.exp(-(t-4)))
vl = (t<1)*0 + ((t>1)&(t<4))*5*np.exp(-(t-1)) + (t>4)*-((10*(1-0.5*np.exp(-3)))-5)*np.exp(-(t-4))

### Remove the csv file if it exists
try:
    os.remove("resp_comp_RL.csv")
except:
    print("csv file does not exist")
### Open the file, append header, then append data
with open("resp_comp_RL.csv", "ab") as file:
    np.savetxt(file, np.column_stack(['t','if','il','vl']) , delimiter = ",", fmt='%s')
    np.savetxt(file, np.column_stack([t,ifu,il,vl]) , delimiter = "," , fmt='%1.4f' )

plt.plot(t,ifu,label=r'$i_f(t)$')
plt.plot(t,il,label=r'$i_l(t)$')
plt.plot(t,vl,label=r'$v_l(t)$')
#plt.xlim([-0.5,5.5])
plt.ylim([-10,10])
plt.legend()
plt.show()