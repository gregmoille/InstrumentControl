import sys
import scipy.io as io
import numpy as np
# import ipdb

from numpy import NaN, Inf, arange, isscalar, asarray, array
c = 299792458

def FindPeaks(v, delta, x=None):
    maxtab = []
    mintab = []
    if x is None:
        x = arange(len(v))
    v = asarray(v)
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN
    lookformax = True
    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)


if __name__ == "__main__":
    from matplotlib.pyplot import plot, scatter, show
    series = [0, 0, 0, 2, 0, 0, 0, -2, 0, 0, 0, 2, 0, 0, 0, -2, 0]
    maxtab, mintab = peakdet(series, .3)
    plot(series)
    scatter(array(maxtab)[:, 0], array(maxtab)[:, 1], color='blue')
    scatter(array(mintab)[:, 0], array(mintab)[:, 1], color='red')
    show()


def MZCalibrate(data, FSR):
    tdaq = data['tdaq']
    MZ = data['MZ'][:]
    ind = np.where(np.diff(np.signbit(MZ-MZ.mean())))[0]
    f_stop = 1e9*c/data['lbd_stop'][:][0]
    f_start = 1e9*c/data['lbd_start'][:][0]
    FSR = 2*(f_start-f_stop)/ind.size
    print(ind.size)
    freq = f_start - 0.5*FSR*np.arange(ind.size)
    lbd_cal = c/freq
    T_cal = data['T'][:][ind]
    # cs = CubicSpline(tdaq[ind], freq)
    # f = cs(tdaq)
    T_cal = T_cal/T_cal.max()

    return freq, T_cal