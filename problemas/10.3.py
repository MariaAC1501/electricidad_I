import numpy as np
import matplotlib
import matplotlib.pyplot as plt

t = np.arange(0,5,1e-3)

#vx = 5*(t<1) - 10*(t>2) + 5*(t>3)
#ix = 1e-3*(t>4) - 0.5e-3*(t<1)
vx = np.array([5,0,-10,-5,-5])
ix = np.array([-0.5,0,0,0,1])  #mA
t0 = np.array([0,1,2,3,4]) #initial times
vinf = np.zeros(5)
v0 = np.zeros(5)
v0[0] = -2 
vc = (t>=0)*0

for i in range(5):
    vinf[i] = (-10*ix[i] + vx[i])/2
    if i < 4:
        vc = vc + ((t>t0[i])&(t<=t0[i+1]))*(vinf[i] + (v0[i]-vinf[i])*np.exp(-4*(t-t0[i])))
        v0[i+1] = vc[int(t0[i+1]/1e-3)]
    else:
        vc = vc + (t>t0[i])*(vinf[i] + (v0[i]-vinf[i])*np.exp(-4*(t-t0[i])))

ic = np.zeros_like(vc)
for j in range(len(vc)):
    ic[j] = 50e-6*((vc[j-1]-vc[j])/(t[j-1]-t[j]))


print(vinf)
print(v0)


# vc = (t<=1)*(5-7*np.exp(-4*t)) #+ (t>1)*(266.002*np.exp(-4*t))
# vc = vc + (t>1)*(vc[int(1/1e-3)]*np.exp(-4*(t-1)))

#print(vc[int(1/1e-3)])

# Plot results
#plt.plot(t,vx,label="v_x(t)")

plt.plot(t,vc,label="v_c(t)")
plt.xlim([0,5])
plt.ylim([-12,12])
plt.legend()
plt.show()

plt.plot(t,ic,label="i_c(t)")
plt.xlim([0,5])
plt.ylim([-2e-3,2e-3])
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