import pygrib
import numpy as np
grbs = pygrib.open('sampledata/flux.grb')
for grb in grbs:
    grb['centre']='ecmf'
    grb['subCentre']=99
    grb['values'] = np.ones((grb['Nj'],grb['Ni']),np.float)
    grb.dump_message('flux.grb')
grbs.close()
