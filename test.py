import numpy as np
import matplotlib.pyplot as plt


#N = 8
#y = np.zeros(N)
#x1 = np.linspace(0, 10, N, endpoint=True)
#x2 = np.linspace(0, 10, N, endpoint=False)
#plt.figure()
#plt.plot(x1, y, 'o')
#plt.plot(x2, y + 0.5, 'o')
#plt.ylim([-0.5, 1])
#plt.show()
#
#
#y1 = np.random.random(8)
#
#plt.figure()
#plt.plot(x1, y1)
#plt.show()
#
#
#dummy = raw_input("What is the third point in the second graph?")


#x = y = np.arange(0.0,11.0,0.5)
#z = np.array(zip(x,y))
#np.savetxt('dummy.txt', z, delimiter='\t', newline='\r\n', fmt='%.2f', 
#            header='test\tdummy')   # X is an array
#np.savetxt('test.out', (x,y,z))   # x,y,z equal sized 1D arrays
#np.savetxt('test.out', x, fmt='%1.4e')   # use exponential notation


f = open('dummy.edf')
text = f.readlines()
dummy = text[22].split()
value = int(dummy[2])

print value
