import sys, importlib as impl
#rootdir = '/home/tanio/Sync/review/'
rootdir = '/Users/tanio/Sync/review/'
sys.path.insert(0, rootdir+'fslcat/')

from fslcat import fslcat
impl.reload(sys.modules['fslcat'])
from fslcat import fslcat

cat = fslcat(rootdir+'FSL_catalog_v4.csv')

linelist = ['[OIII]52', '[OI]63', '[OIII]88', '[NII]122', '[CII]158', '[OI]146', '[NII]205', '[CI]370', '[CI]609'] #, '[NIII]57'

# Line deficits as a function of LFIR

#for line in linelist: cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum',line], '2':['LFIR_LIR','','/']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
# Corrected for magnification
#for line in linelist: cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum',line], '2':['LFIR_LIR','','/']}, xlims=[1e9, 5e14, 'log'], ylims=[5e-8,5e-1, 'log'])

#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OIII]52'], '2':['LFIR_LIR','','/']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
##cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[NIII]57]', '2':['LFIR_LIR','','/']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OI]63'], '2':['LFIR_LIR','','/']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OIII]88'], '2':['LFIR_LIR','','/']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[NII]122'], '2':['LFIR_LIR','','/']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[CII]158'], '2':['LFIR_LIR','','/']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OI]146'], '2':['LFIR_LIR','','/']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[NII]205'], '2':['LFIR_LIR','','/']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[CI]370'], '2':['LFIR_LIR','','/']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[CI]609'], '2':['LFIR_LIR','','/']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])

################################################

# Line deficits as a function of LFIR color-coded by z

#for line in linelist: cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum',line], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
# Corrected for magnification
#for line in linelist: cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum',line,''], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, xlims=[1e9, 5e14, 'log'], ylims=[5e-8,5e-1, 'log'])

#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OIII]52'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
##cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[NIII]57'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OI]63'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OIII]88'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[NII]122'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[CII]158'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OI]146'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[NII]205'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[CI]370'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[CI]609'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])

################################################

# Line deficits as a function of LFIR color-coded by type

#for line in linelist: cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum',line], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
# Corrected for magnification
#for line in linelist: cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum',line,''], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']}, xlims=[1e9, 5e14, 'log'], ylims=[5e-8,5e-1, 'log'])

#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OIII]52'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
##cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[NIII]57'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OI]63'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OIII]88'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[NII]122'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[CII]158'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OI]146'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[NII]205'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[CI]370'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[CI]609'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']}, xlims=[2e9, 2e15, 'log'], ylims=[5e-8,5e-1, 'log'])

###############################################

# Line deficits as a function of FWHM color-coded by z

#for line in linelist: cat.plot(xkeyws={'1':['FWHM',line]}, ykeyws={'1':['Lum',line], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, ylims=[5e-8,5e-1, 'log'])

#cat.plot(xkeyws={'1':['FWHM','[OIII]52']}, ykeyws={'1':['Lum','[OIII]52'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, ylims=[5e-8,5e-1, 'log'])
##cat.plot(xkeyws={'1':['FWHM','[NIII]57']}, ykeyws={'1':['Lum','[NIII]57'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['FWHM','[OI]63']}, ykeyws={'1':['Lum','[OI]63'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['FWHM','[OIII]88']}, ykeyws={'1':['Lum','[OIII]88'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['FWHM','[NII]122']}, ykeyws={'1':['Lum','[NII]122'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['FWHM','[CII]158']}, ykeyws={'1':['Lum','[CII]158'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['FWHM','[OI]146']}, ykeyws={'1':['Lum','[OI]146'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['FWHM','[NII]205']}, ykeyws={'1':['Lum','[NII]205'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['FWHM','[CI]370']}, ykeyws={'1':['Lum','[CI]370'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, ylims=[5e-8,5e-1, 'log'])
#cat.plot(xkeyws={'1':['FWHM','[CI]609']}, ykeyws={'1':['Lum','[CI]609'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']}, ylims=[5e-8,5e-1, 'log'])

###############################################

#for line in linelist: cat.plot(xkeyws={'1':['FWHM',line]}, ykeyws={'1':['Lum',line,'Flux']}, zkeyws={'1':['z','']})

#cat.plot(xkeyws={'1':['Lum','[CII]158','Flux']}, ykeyws={'1':['FWHM','[CII]158']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['Lum','[CI]370','Flux']}, ykeyws={'1':['FWHM','[CI]370']}, zkeyws={'1':['z','']})

#cat.plot(xkeyws={'1':['FWHM','[CII]158']}, ykeyws={'1':['Lum','[CII]158','MagCorr']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['FWHM','[CI]370']}, ykeyws={'1':['Lum','[CI]370','MagCorr']}, zkeyws={'1':['Type','Simplified']})

#cat.plot(xkeyws={'1':['FWHM','[CII]158']}, ykeyws={'1':['Lum','[CII]158'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']}, ylims=[1e-6,5e-1, 'log'])
#cat.plot(xkeyws={'1':['FWHM','[CI]370']}, ykeyws={'1':['Lum','[CI]370'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']}, ylims=[1e-6,5e-1, 'log'])

#for line in linelist: cat.plot(xkeyws={'1':['FWHM',line]}, ykeyws={'1':['Lum',line,'Flux','MagCorr']}, zkeyws={'1':['Type','Simplified']})
#for line in linelist: cat.plot(xkeyws={'1':['FWHM',line]}, ykeyws={'1':['Lum',line,'MagCorr']}, zkeyws={'1':['Type','Simplified']})
#for line in linelist: cat.plot(xkeyws={'1':['FWHM',line]}, ykeyws={'1':['Lum',line,'MagCorr']}, zkeyws={'1':['z','']})

#cat.plot(xkeyws={'1':['FWHM','[CII]158']}, ykeyws={'1':['Lum','[CII]158','Flux','MagCorr']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['FWHM','[CII]158']}, ykeyws={'1':['Lum','[CII]158','Flux','MagCorr']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['FWHM','[CI]370']}, ykeyws={'1':['Lum','[CI]370','Flux','MagCorr']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['FWHM','[CI]370']}, ykeyws={'1':['Lum','[CI]370','Flux','MagCorr']}, zkeyws={'1':['z','']})
##cat.plot(xkeyws={'1':['FWHM','[CI]609']}, ykeyws={'1':['Lum','[CI]609','Flux','MagCorr']}, zkeyws={'1':['z','']})

#for line in linelist: cat.plot(xkeyws={'1':['Lum',line,'Flux'], '2':['Cont',line,'/']}, ykeyws={'1':['Lum',line], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']})

#for line in linelist: cat.plot(xkeyws={'1':['Lum',line,'Flux'], '2':['Cont',line,'/']}, ykeyws={'1':['Lum',line], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']})

#cat.plot(xkeyws={'1':['Lum','[CII]158','Flux'], '2':['Cont','[CII]158','/']}, ykeyws={'1':['Lum','[CII]158'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['Lum','[CI]370','Flux'], '2':['Cont','[CI]370','/']}, ykeyws={'1':['Lum','[CI]370'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']})

#for line in linelist: cat.plot(xkeyws={'1':['Lum',line,'Flux'], '2':['Cont',line,'/']}, ykeyws={'1':['Lum',line], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']})

#cat.plot(xkeyws={'1':['Lum','[CII]158','Flux'], '2':['Cont','[CII]158','/']}, ykeyws={'1':['Lum','[CII]158'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['Lum','[CI]370','Flux'], '2':['Cont','[CI]370','/']}, ykeyws={'1':['Lum','[CI]370'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']})

###############################################

# Line ratios as a function of LFIR cc as Type

for line1 in linelist:
    for line2 in linelist:
        if line1 != line2:
            pass
            #print(line1,line2)
            #cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum',line1], '2':['Lum',line2,'/']}, zkeyws={'1':['Type','Simplified']})
            #cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum',line1], '2':['Lum',line2,'/']}, zkeyws={'1':['Type','Simplified']})
            #cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum',line1], '2':['Lum',line2,'/']}, zkeyws={'1':['z','']})
            #cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum',line1], '2':['Lum',line2,'/']}, zkeyws={'1':['z','']})
            
#cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[CII]158'], '2':['Lum','[NII]205','/']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[CI]370'], '2':['Lum','[CI]609','/']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[NII]122'], '2':['Lum','[NII]205','/']}, zkeyws={'1':['Type','Simplified']})
##cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[OIII]52'], '2':['Lum','[OIII]88','/']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[OI]63'], '2':['Lum','[OI]146','/']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[OIII]88'], '2':['Lum','[NII]122','/']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[OIII]88'], '2':['Lum','[CII]158','/']}, zkeyws={'1':['Type','Simplified']})
##cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[CII]158'], '2':['Lum','[CI]370','/']}, zkeyws={'1':['Type','Simplified']})

# Line ratios as a function of LFIR cc as z
#cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[CII]158'], '2':['Lum','[NII]205','/']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[CI]370'], '2':['Lum','[CI]609','/']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[NII]122'], '2':['Lum','[NII]205','/']}, zkeyws={'1':['z','']})
##cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[OIII]52'], '2':['Lum','[OIII]88','/']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[OI]63'], '2':['Lum','[OI]146','/']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[OIII]88'], '2':['Lum','[NII]122','/']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[OIII]88'], '2':['Lum','[CII]158','/']}, zkeyws={'1':['z','']})

#cat.plot(xkeyws={'1':['Lum','[CII]158','MagCorr']}, ykeyws={'1':['Lum','[CI]370','MagCorr']}, fit=True, hist=True)
#cat.plot(xkeyws={'1':['Lum','[CII]158','MagCorr']}, ykeyws={'1':['Lum','[CI]370','MagCorr']}, zkeyws={'1':['Type','Simplified']}, fit=True, hist=True)
#cat.plot(xkeyws={'1':['Lum','[CII]158']}, ykeyws={'1':['Lum','[CI]370']}, zkeyws={'1':['Type','Simplified']}, fit=True)
#cat.plot(xkeyws={'1':['Lum','[CII]158','MagCorr']}, ykeyws={'1':['Lum','[CI]370','MagCorr']}, zkeyws={'1':['Lum','[NII]205']}, fit=True)
#cat.plot(xkeyws={'1':['Lum','[CII]158']}, ykeyws={'1':['Lum','[CI]370']}, zkeyws={'1':['z','']}, fit=True)

###############################################

#cat.plot(xkeyws={'1':['Cont','[CII]158'], '2':['Cont','[CI]370','/']}, ykeyws={'1':['Lum','[CII]158'], '2':['Lum','[CI]370','/']}, zkeyws={'1':['Type','Simplified']})

#cat.plot(xkeyws={'1':['Lum','[CII]158'], '2':['Lum','[NII]122','/']}, ykeyws={'1':['Lum','[OIII]88'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['Lum','[CII]158'], '2':['Lum','[NII]122','/']}, ykeyws={'1':['Lum','[OIII]88'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']})



from fslcat_4CII158_NII205 import fslcat_4CII158_NII205
impl.reload(sys.modules['fslcat_4CII158_NII205'])
from fslcat_4CII158_NII205 import fslcat_4CII158_NII205

cat = fslcat_4CII158_NII205(rootdir+'FSL_catalog_v4.csv')

cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[CII]158'], '2':['Lum','[NII]205','/']}, zkeyws={'1':['Type','Simplified']})


#from fslcat_4CI370_CI609 import fslcat_4CI370_CI609
#impl.reload(sys.modules['fslcat_4CI370_CI609'])
#from fslcat_4CI370_CI609 import fslcat_4CI370_CI609

#cat = fslcat_4CI370_CI609(rootdir+'FSL_catalog_v4.csv')

#cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[CI]370'], '2':['Lum','[CI]609','/']}, zkeyws={'1':['Type','Simplified']})


#from fslcat_4NII122_NII205 import fslcat_4NII122_NII205
#impl.reload(sys.modules['fslcat_4NII122_NII205'])
#from fslcat_4NII122_NII205 import fslcat_4NII122_NII205

#cat = fslcat_4NII122_NII205(rootdir+'FSL_catalog_v4.csv')

#cat.plot(xkeyws={'1':['LFIR_LIR','MagCorr']}, ykeyws={'1':['Lum','[NII]122'], '2':['Lum','[NII]205','/']}, zkeyws={'1':['Type','Simplified']})
