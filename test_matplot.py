import matplotlib.pyplot as plt
# contains a calculation function to be called from another file.

def plot_xy(option='Linear', numpnts = 10):
    xx=[]
    yy=[]
    for ii in range(1, numpnts):  
        if option.startswith('Line'): # linear
            x0 = ii
            y0 = ii*2
        if option.startswith('Exp'): # exponential
            x0 = ii
            y0 = ii**2
        xx.append(x0)
        yy.append(y0)
    plt.plot(xx, yy) 
    plt.ylabel('y-values')
    plt.xlabel('x-values')
    plt.show()

