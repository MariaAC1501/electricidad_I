import csv
import numpy as np
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

## Aqui empieza el proceso carga-descarga

z_0 = 0.2
v_0 = ocv_value(soc,ocv,z_0)
i_0 = 0
t_0 = 0


z = np.array([z_0])
v = np.array([v_0])
i = np.array([i_0])
t = np.array([t_0])


Q = 3.250
CC_char = -0.5*Q
CC_disc = Q
CV = 4.2
EOC = -0.5 #500 mA
EOD = 3.2 
R_0 = 0.1

index = 0
eta_char = 0.99
eta_disc = 1
Dt = 0.5/3600

## Charging in CC
while v[index] < CV:
    eta = eta_char
    i = np.append(i,CC_char) #es negativo por estar en carga
    z = np.append(z,z[index] - (eta_char*Dt*i[index])/Q)   
    v = np.append(v,ocv_value(soc,ocv,z[index]) - i[index]*R_0) 
    t = np.append(t,t[index]+Dt)
    index += 1

## Charging in CV
while i[index] < EOC:
    eta = eta_char 
    v = np.append(v,CV) #es negativo por estar en carga
    z = np.append(z,z[index] - (eta_char*Dt*i[index])/Q)   
    i = np.append(i,(ocv_value(soc,ocv,z[index]) - v[index])/R_0) 
    t = np.append(t,t[index]+Dt)
    index += 1

## Discharging in CC
while v[index] > EOD:
    eta = eta_disc
    i = np.append(i,CC_disc) #es negativo por estar en carga
    z = np.append(z,z[index] - (eta_char*Dt*i[index])/Q)   
    v = np.append(v,ocv_value(soc,ocv,z[index]) - i[index]*R_0) 
    t = np.append(t,t[index]+Dt)
    index += 1


print(index)
plt.plot(t,v)
plt.show()
plt.plot(t,i)
plt.show()
plt.plot(t,z)
plt.show()