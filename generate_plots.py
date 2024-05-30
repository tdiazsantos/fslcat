import sys, importlib as impl
sys.path.insert(0, '/Users/tanio/Sync/review/fslcat/')

from fslcat import fslcat
impl.reload(sys.modules['fslcat'])
from fslcat import fslcat

cat = fslcat('/Users/tanio/Sync/review/FSL_catalog_vFinal.csv')

# Line deficits as a function of LFIR
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

# Line deficits as a function of LFIR color-coded by type
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

# Line deficits as a function of LFIR color-coded by z
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

# Line deficits as a function of FWHM color-coded by z
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

#cat.plot(xkeyws={'1':['Lum','[CII]158','Flux']}, ykeyws={'1':['FWHM','[CII]158']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['Lum','[CI]370','Flux']}, ykeyws={'1':['FWHM','[CI]370']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['FWHM','[CII]158']}, ykeyws={'1':['Lum','[CII]158','Flux']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['FWHM','[CI]370']}, ykeyws={'1':['Lum','[CI]370']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['Lum','[CII]158','Flux'], '2':['Cont','[CII]158','/']}, ykeyws={'1':['Lum','[CII]158'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['Lum','[CII]158','Flux'], '2':['Cont','[CII]158','/']}, ykeyws={'1':['Lum','[CII]158'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['Lum','[CI]370','Flux'], '2':['Cont','[CI]370','/']}, ykeyws={'1':['Lum','[CI]370'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['Lum','[CI]370','Flux'], '2':['Cont','[CI]370','/']}, ykeyws={'1':['Lum','[CI]370'], '2':['LFIR_LIR','','/']}, zkeyws={'1':['z','']})

# Line ratios as a function of LFIR cc as Type
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[CII]158'], '2':['Lum','[NII]205','/']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[CI]370'], '2':['Lum','[CI]609','/']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OIII]52'], '2':['Lum','[OIII]88','/']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OIII]88'], '2':['Lum','[NII]122','/']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[CII]158'], '2':['Lum','[CI]370','/']}, zkeyws={'1':['Type','Simplified']})
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OIII]88'], '2':['Lum','[CII]158','/']}, zkeyws={'1':['Type','Simplified']})

# Line ratios as a function of LFIR cc as z
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[CII]158'], '2':['Lum','[NII]205','/']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[CI]370'], '2':['Lum','[CI]609','/']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OIII]52'], '2':['Lum','[OIII]88','/']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OIII]88'], '2':['Lum','[NII]122','/']}, zkeyws={'1':['z','']})
#cat.plot(xkeyws={'1':['LFIR_LIR','']}, ykeyws={'1':['Lum','[OIII]88'], '2':['Lum','[CII]158','/']}, zkeyws={'1':['z','']})

