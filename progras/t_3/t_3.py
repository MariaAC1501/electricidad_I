import csv
import os
import numpy as np
import matplotlib
# matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt

title = np.array(['',''])
soc = np.array([])
ocv = np.array([])

with open("OCV(z).csv", mode="r")as file:
    read = csv.reader(file)
    row_count = 0
    for row in read:
        if row_count == 0:
            title = row
            row_count += 1
        else:
            soc = np.append(soc,float(row[0]))
            ocv = np.append(ocv,float(row[1]))


print("Las columnas son:")
print(title)
plt.plot(soc,ocv)
plt.show()

isc = 1.05
imp = 1
vmp = 3.8
voc = 4

v_plot = np.arange(0,voc,1e-3)
ips_plot = (v_plot<=vmp)*((imp-isc)*(v_plot/vmp)+isc) + ((v_plot>vmp)&(v_plot<=voc))*(imp*((v_plot-vmp)/(vmp-voc))+imp)
plt.plot(v_plot,ips_plot,label=r'$v_f(t)$')
# # plt.plot(t,vc,label=r'$v_c(t)$')
# # plt.plot(t,ic,label=r'$i_c(t)$')
plt.xlim([0,5])
plt.ylim([0,1.5])
plt.legend()
plt.show()

def ocv_value(soc_values, ocv_values, input_soc):
    "devuelve el valor del OCV para cualquier SOC"
    output_ocv = 0
    for i in range(len(soc_values)):
        if input_soc <= soc_values[i]:
            if soc_values[i-1] == soc_values[i]:
                output_ocv = ocv_values[i]
                break
            output_ocv = ocv_values[i-1] + (ocv_values[i]-ocv_values[i-1])*((input_soc - soc_values[i-1])/(soc_values[i] - soc_values[i-1]))
            break
    return output_ocv


def ips_value(v_value, isc, imp, vmp, voc):
    'devuelve la corriente del panel para cualquier voltaje'
    output_ips = 0
    if v_value <= vmp:
        output_ips = (imp-isc)*(v_value/vmp)+isc
    if (v_value > vmp) & (v_value <= voc):
        output_ips = imp*((v_value-vmp)/(vmp-voc))+imp
    return output_ips


## Aqui empieza el proceso carga-descarga

Q = 3.250
R_0 = 0.1
index = 0
eta_char = 0.99
Dt = 1/3600

z_0 = 0.2
i_0 = -1.0037935526315789
v_0 = ocv_value(soc,ocv,z_0) - i_0*R_0
t_0 = 0

z = np.array([z_0])
v = np.array([v_0])
i = np.array([i_0])
t = np.array([t_0])



## Charging with panel
while i[index] < -0.1:
    eta = eta_char
    ips = ips_value(v[index],isc,imp,vmp,voc)
    i = np.append(i,-ips) #es negativo por estar en carga
    z = np.append(z,z[index] - (eta_char*Dt*i[index])/Q)   
    v = np.append(v,ocv_value(soc,ocv,z[index]) - i[index]*R_0) 
    t = np.append(t,t[index]+Dt)
    index += 1


plt.plot(t,v)
plt.show()
plt.plot(t,i)
plt.show()
plt.plot(t,z)
plt.show()
print(i[1])    
print(index)

# ### Remove the csv file if it exists
# try:
#     os.remove("resp_comp_RC.csv")
# except:
#     print("csv file does not exist")
# ### Open the file, append header, then append data
# with open("resp_comp_RC.csv", "ab") as file:
#     np.savetxt(file, np.column_stack(['t','vf','vc','ic']) , delimiter = ",", fmt='%s')
#     np.savetxt(file, np.column_stack([t,vf,vc,ic]) , delimiter = "," , fmt='%1.4f' )

