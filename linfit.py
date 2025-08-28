#!/usr/bin/env python3

import numpy as np
from scipy.odr import *
import ipdb

class linfit:

    def __init__(self, x, y, xerr, yerr, log=False):

        if log == False:
            self.model = Model(self.lin_func)
        else:
            self.model = Model(self.exp_func)
            
        #if log == True:
        #    from uncertainties import unumpy as unp
        #    from uncertainties.unumpy import nominal_values as nvs, std_devs as sds
        #
        #    ux = unp.uarray(x, xerr)
        #    fitx = unp.log10(ux)
        #    uy = unp.uarray(y, yerr)
        #    fity = unp.log10(uy)
        #    
        #    self.data = RealData(nvs(fitx), nvs(fity), sx=sds(fitx), sy=sds(fity))
        #
        #else:
        self.data = RealData(x, y, sx=xerr, sy=yerr)

    
    def run(self, beta0=None):
    
        if beta0 is None: beta0 = [1., 1e5]

        odr = ODR(self.data, self.model, beta0=beta0)
        result = odr.run()

        return result

    
    def lin_func(self, p, x):
        
        m, c = p
        
        return m*x + c


    def exp_func(self, p, x):
        
        m, c = p
        
        return x**m * c


    def lin_invfunc(self, p, y):
        
        m, c = p
        
        return (y-c) / m


    def exp_invfunc(self, p, y):
        
        m, c = p
        
        return (y/c)**(1./m)
