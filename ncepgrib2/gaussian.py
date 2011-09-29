"""
module for computing gaussian latitudes

derived from fortran CCM3 code.

Jeff Whitaker <jeffrey.s.whitaker@noaa.gov>
"""
import numpy as N
import math, sys

# 1st 50 zeros of the bessel function.
bz=N.array([2.4048255577,   5.5200781103,
    8.6537279129,  11.7915344391,  14.9309177086,  18.0710639679,
   21.2116366299,  24.3524715308,  27.4934791320,  30.6346064684,
   33.7758202136,  36.9170983537,  40.0584257646,  43.1997917132,
   46.3411883717,  49.4826098974,  52.6240518411,  55.7655107550,
   58.9069839261,  62.0484691902,  65.1899648002,  68.3314693299,
   71.4729816036,  74.6145006437,  77.7560256304,  80.8975558711,
   84.0390907769,  87.1806298436,  90.3221726372,  93.4637187819,
   96.6052679510,  99.7468198587, 102.8883742542, 106.0299309165,
  109.1714896498, 112.3130502805, 115.4546126537, 118.5961766309,
  121.7377420880, 124.8793089132, 128.0208770059, 131.1624462752,
  134.3040166383, 137.4455880203, 140.5871603528, 143.7287335737,
  146.8703076258, 150.0118824570, 153.1534580192, 156.2950342685],'d')
  
pi = math.pi
eps = 1.e-15
  
def lats(k):
    """
 Calculate latitudes for gaussian quadrature.
 The algorithm is described in Davis and Rabinowitz,
 Journal of Research of the NBS, V 56, Jan 1956.
 The zeros of the bessel function j0, which are obtained from bsslzr,
 are used as a first guess for the abscissa.


 Input:   k (number of latitudes pole to pole)
 Output:  gaussian latitudes in degress (N to S).
    """
# The value eps, used for convergence tests in the iterations,
# can be changed.  Newton iteration is used to find the abscissas.
    c = (1.-(2./pi)**2)*0.25
    fk = float(k)
    kk = k/2
    sinlat = bsslzr(kk)
    for i in range(kk):
        xz = N.cos(sinlat[i]/math.sqrt((fk+0.5)**2+c))
# This is the first approximation to xz
        iter = 0
        while 1:
           pkm2 = 1.
           pkm1 = xz
           iter = iter + 1
           if iter > 10:
# Error exit
               raise ValueError, 'gaulats: No convergence in 10 iterations'
# Computation of the legendre polynomial
           for n in range(2,k+1):
             fn = float(n)
             pk = ((2.*fn-1.)*xz*pkm1-(fn-1.)*pkm2)/fn
             pkm2 = pkm1
             pkm1 = pk
           pkm1 = pkm2
           pkmrk = (fk*(pkm1-xz*pk))/(1.-xz**2)
           sp = pk/pkmrk
           xz = xz - sp
           avsp = math.fabs(sp)
           if avsp < eps: break
           sinlat[i] = xz
    lats = N.zeros(n,'d')
# Complete the latitudes, using the symmetry.
    lats[0:kk] = (180./pi)*N.arcsin(sinlat[0:kk])
    lats[k-kk:k] = -lats[0:kk][::-1]
    return lats


def bsslzr(n):
    """
 Return n zeros (or if n>50, approximate zeros), of the Bessel function
 j0, in the array bes. The first 50 zeros will be given exactly, and the
 remaining zeros are computed by extrapolation, and therefore not exact.
    """
    nn = n
    bes = N.zeros(n,'d')
    if n > 50:
      bes[49] = bz[49]
      for j in range(50,n):
          bes[j] = bes[j-1] + pi
      nn = 49
    bes[0:nn] = bz[0:nn]
    return bes
