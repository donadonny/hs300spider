# Kalman filter example demo in Python

# A Python implementation of the example given in pages 11-15 of "An
# Introduction to the Kalman Filter" by Greg Welch and Gary Bishop,
# University of North Carolina at Chapel Hill, Department of Computer
# Science, TR 95-041,
# http://www.cs.unc.edu/~welch/kalman/kalmanIntro.html

# by Andrew D. Straw

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (10, 8)



def KF(z):
    # intial parameters
    n_iter = len(z)
    sz = (n_iter,) # size of array
    
    #x = -0.37727 # truth value (typo in example at top of p. 13 calls this z)
    #z = np.random.normal(x,0.1,size=sz) # observations (normal about x, sigma=0.1)
    
    Q = 1e-5 # process variance
    
    # allocate space for arrays
    xhat=np.zeros(sz)      # a posteri estimate of x
    P=np.zeros(sz)         # a posteri error estimate
    xhatminus=np.zeros(sz) # a priori estimate of x
    Pminus=np.zeros(sz)    # a priori error estimate
    K=np.zeros(sz)         # gain or blending factor
    
    R = 0.005 # estimate of measurement variance, change to see effect
    
    # intial guesses
    xhat[0] = 0.0
    P[0] = 1.0
    
    for k in range(1,n_iter):
        # time update
        xhatminus[k] = xhat[k-1]
        Pminus[k] = P[k-1]+Q
    
        # measurement update
        K[k] = Pminus[k]/( Pminus[k]+R )
        xhat[k] = xhatminus[k]+K[k]*(z[k]-xhatminus[k])
        P[k] = (1-K[k])*Pminus[k]
    return xhat[n_iter-1]

def KF2(z):
    return sum(z)/len(z)
    
'''
x = -0.37727 # truth value (typo in example at top of p. 13 calls this z)
z = np.random.normal(x,0.1,size=(50,)) # observations (normal about x, sigma=0.1)

print KF(z)
'''


# average price every-day
d = []
with open('/home/xiaofeng/source/hs300spider/s.txt') as fd:
    for line in fd:
        (idx, low, high)=  line[:-1].split(',')
        (low,high) = (float(low),float(high))
        d.append((low+high)/2)


t1=[0 for i in d]

for i in range(1,len(d)):
    t1[i] = (d[i]-d[i-1])/d[i-1]
    
ratio = []


for RANGE in range(2,90):
    # price price every day
    dhat = d[:]
    t2=[0 for item in d]
    for i in range(RANGE,len(d)):
        dhat[i] = KF(d[i-RANGE:i])
        t2[i] = (dhat[i]-d[i-1])/d[i-1]    

    
    
    r = 0.0
    for i in range(RANGE,len(d)):
        x = (t2[i]-t1[i])
        r += abs(x)
    
    r/=(len(d)-RANGE-1)
    
    ratio.append(r)
    
plt.figure()
plt.plot(ratio)
plt.plot(t1)
plt.show()

'''
plt.plot(z,'k+',label='noisy measurements')
plt.plot(xhat,'b-',label='a posteri estimate')
plt.axhline(x,color='g',label='truth value')
plt.legend()
plt.title('Estimate vs. iteration step', fontweight='bold')
plt.xlabel('Iteration')
plt.ylabel('Voltage')

plt.figure()
valid_iter = range(1,n_iter) # Pminus not valid at step 0
plt.plot(valid_iter,Pminus[valid_iter],label='a priori error estimate')
plt.title('Estimated $\it{\mathbf{a \ priori}}$ error vs. iteration step', fontweight='bold')
plt.xlabel('Iteration')
plt.ylabel('$(Voltage)^2$')
plt.setp(plt.gca(),'ylim',[0,.01])
plt.show()

'''