import csv
import os
import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt


ttau = np.arange(-0.5,5.5,0.001)
mag = (ttau>0)*np.exp(-ttau)+(ttau<0)*1
### Remove the csv file if it exists
try:
    os.remove("resp_nat.csv")
except:
    print("csv file does not exist")
### Open the file, append header, then append data
with open("resp_nat.csv", "ab") as file:
    np.savetxt(file, np.column_stack(['t','mag']) , delimiter = ",", fmt='%s')
    np.savetxt(file, np.column_stack([ttau,mag]) , delimiter = "," , fmt='%1.4f' )

plt.plot(ttau,mag,label=r'$\frac{v(t)}{v(0)}$')
plt.plot([-0.5,1],[np.exp(-1),np.exp(-1)],'-.')
plt.xlim([-0.5,5.5])
plt.ylim([-0.05,1.05])
plt.legend()
plt.show()
# t = np.arange(-0.5,5.5,0.001)
# plt.plot(t,t>0)
# plt.plot(t,(t>0)*(1-np.exp(-t)))


# plt.grid('on')
# plt.xlabel(r'$t/\tau$',fontsize=16)
# plt.suptitle('Unit step response of an RC filter with time constant $\\tau=RC$',
#              fontsize=12)
# plt.legend(['$V_{in}$','$V_{out}$'],'best',fontsize=16)
# plt.show