import os, sys, copy
#sys.path.insert(1, '/Users/tanio/Sync/pywork/pys')
import pdb, ipdb
from tqdm import tqdm
import numpy as np
import numpy.ma as ma
import pandas as pd
import importlib as imp

import scipy.ndimage
from scipy import stats
from astropy import units as u
from astropy import constants as c
from astropy.stats import sigma_clip
from astropy.coordinates import SkyCoord
from astropy.io import ascii
from astropy.table import Table

from astropy.cosmology import FlatLambdaCDM

import matplotlib as mpl, matplotlib.backends.backend_pdf, matplotlib.pyplot as plt, matplotlib.cm as cm
from matplotlib.colors import Normalize, LogNorm

import axis
imp.reload(axis)


line_list = ['[OIII]52um', '[NIII]57um', '[OI]63um', '[OIII]88um', '[NII]122um','[CII]158um', '[OI]145um', '[NII]205um', '[CI]370um', '[CI]609um']


class fslcat:

    def __init__(self, cat_name):

        self.fslcat = pd.read_csv(cat_name, skiprows=[1])
        self.fslcat['RA'] = [i.replace('"','') if type(i) == str else i for i in self.fslcat['RA'].values]
        self.fslcat['Dec'] = [i.replace('"','') if type(i) == str else i for i in self.fslcat['Dec'].values]



    def get_filename(self, xkeyws, ykeyws, zkeyws=None):
        
        plotname = ''.join(ykeyws['1'])
        if '2' in ykeyws.keys(): plotname += ''.join(ykeyws['2'])
        plotname += '_vs_'        
        plotname += ''.join(xkeyws['1'])
        if '2' in xkeyws.keys(): plotname += ''.join(xkeyws['2'])
        if zkeyws != None:
            plotname += '_sort_'        
            plotname += ''.join(zkeyws['1'])
            if '2' in zkeyws.keys(): plotname += ''.join(zkeyws['2'])

        return plotname



    def pre_selection(self, pre_select):

        # Start from a fresh copy of the catalog
        fslcat_select = self.fslcat.copy()

        for key, value in pre_select.items():
            if type(value) == list:
                fslcat_select = fslcat_select[(fslcat_select[key] >= value[0]) & (fslcat_select[key] <= value[1])]
            else:
                fslcat_select = fslcat_select[(fslcat_select[key] == value)]

        return fslcat_select



    def check_scale_ir(self, ax):

        if ax.keyws[1] == 'LFIR_LIR':
            lir_inds = ax.cat['LFIR_LIR_type'].values == 'LIR'
            ax.data[lir_inds] *= 0.5
            ax.err[lir_inds] *= 0.5
        elif ax.keyws[1] == 'LIR_LFIR':
            lfir_inds = ax.cat['LIR_LFIR_type'].values == 'LFIR'
            ax.data[lfir_inds] *= 2.
            ax.err[lfir_inds] *= 2.
            
        return ax



    def write_table(self, xax, xkeyws, yax, ykeyws, zax, zkeyws, plotname):

        tbl = Table()
        
        tbl['Source'] = xax.cat['Source']
        tbl['RA'] = xax.cat['RA']
        tbl['Dec'] = xax.cat['Dec']
        tbl['z'] = xax.cat['z']
        tbl['LDist'] = xax.cat['LDist']
        xhead = [''.join(val) for key, val in xkeyws.items()][0]
        tbl[xhead] = xax.data
        tbl[xhead+'_err'] = xax.err
        tbl[xhead+'_lim'] = xax.lim
        yhead = [''.join(val) for key, val in ykeyws.items()][0]
        tbl[yhead] = yax.data
        tbl[yhead+'_err'] = yax.err
        tbl[yhead+'_lim'] = yax.lim
        if zax is not None:
            zhead = [''.join(val) for key, val in zkeyws.items()][0]
            tbl[zhead] = zax.data
            tbl[zhead+'_err'] = zax.err
            tbl[zhead+'_lim'] = zax.lim
            ascii.write(tbl, plotname+'.ecsv', overwrite=True, format='fixed_width', delimiter='', formats={'Source':'%s', 'RA':'%s', 'Dec':'%s', 'z':'%.4f', 'LDist':'%.1f',
                                                                        xhead:'%.2e', xhead+'_err':'%.2e', xhead+'_lim':'%.0f', yhead:'%.2e', yhead+'_err':'%.2e', yhead+'_lim':'%.0f',
                                                                        zhead:'%.2e', zhead+'_err':'%.2e', zhead+'_lim':'%.0f'})
        else:
            ascii.write(tbl, plotname+'.ecsv', overwrite=True, formats={'Source':'%s', 'RA':'%s', 'Dec':'%s', 'z':'%.4f', 'LDist':'%.1f',
                                                                        xhead:'%.2e', xhead+'_err':'%.2e', xhead+'_lim':'%.0f', yhead:'%.2e', yhead+'_err':'%.2e', yhead+'_lim':'%.0f'})



    def generate_axis(self, keyws, pre_select, r_cross, **kwargs):

        # AXIS1
        print('Generating catalog for axis'+list(keyws.keys())[0])
        ax_pre_select = {'Valid':'S', **pre_select, 'Line':keyws['1'][0]+'um'} if keyws['1'][0]+'um' in line_list else {'Valid':'S', **pre_select}
        # Select on the line, if any, and on other properties, if any
        ax_cat = self.pre_selection(ax_pre_select)
        # Build the data dictionary of the axis
        ax = axis.axis(keyws['1'], ax_cat, **kwargs)
        ax = self.check_scale_ir(ax)

        # AXIS2
        if '2' in keyws.keys():
            print('Generating catalog for axis'+list(keyws.keys())[1])
            ax2_pre_select = {'Valid':'S', **pre_select, 'Line':keyws['2'][0]+'um'} if keyws['2'][0]+'um' in line_list  else {'Valid':'S', **pre_select}
            ax2_cat = self.pre_selection(ax2_pre_select)
            ax2 = axis.axis(keyws['2'], ax2_cat, **kwargs)
            ax2 = self.check_scale_ir(ax2)

            print('Cross matching 1 and 2-axes')
            cross_ids, ids = axis.cross_corr(ax.cat, ax2.cat, ax.keyws, ax2.keyws, r_cross=r_cross,  **kwargs)
            ax.update(cross_ids)
            ax2.update(ids)
            
            ax = ax.operate(ax2, operator=keyws['2'][2])

        return ax


    def plot(self, xkeyws={'1':['', 'LFIR']}, ykeyws={'1':['[CII]158', 'Lum'], '2':['','LFIR','/']}, zkeyws=None, pre_select={}, outdir='./', r_cross=0.01, color='red', **kwargs):
        """
        The axis keywords specify the quantity to be ploted in the x, y (and optionally z) axes.
        Each quantity is constructed from one or two parameters from the catalog.
        If two parameters are chosen, an operator must be passed, which will sum, subtract, multiply or divide the two.
        The parameter of each axis keyword is given via a list.
        The first element of the list specifies an emission line, the second the type of measurement, and the third the operator (in the case two parameters are given)
        """
        
        # XAXIS
        self.x = self.generate_axis(xkeyws, pre_select, r_cross)
        # YAXIS
        self.y = self.generate_axis(ykeyws, pre_select, r_cross)
        # Z-AXIS1
        if zkeyws is not None:
            self.z = self.generate_axis(zkeyws, pre_select, r_cross)
        else:
            self.z = None
            
        print('Cross matching x and y-axes')
        xids, yids = axis.cross_corr(self.x.cat, self.y.cat, self.x.keyws, self.y.keyws, r_cross=r_cross, **kwargs)
        print('Updating x and y-axes')
        self.x.update(xids)
        self.y.update(yids)

        if zkeyws is not None:
            print('Cross matching x and z-axes')
            # Here we cross match but we keep all the entries in the x/y-axis even if they have NaN values in the z-axis
            xids, zids = axis.cross_corr(self.x.cat, self.z.cat, self.x.keyws, self.z.keyws, keep_all=True, r_cross=r_cross, **kwargs)
            print('Updating z-axis')
            self.z.update(zids, self.x.cat)
            
            
            
        # PLOT
        print('Generating plot')
        plotname = outdir + self.get_filename(xkeyws, ykeyws, zkeyws=zkeyws)
        pdfname = mpl.backends.backend_pdf.PdfPages(plotname+'.pdf')
        fig, axs = plt.subplots(figsize=(11.,8.5))
        plt.subplots_adjust(left=0.12, bottom=0.1, right=1.0, top=0.98)

        # Set up axes
        axs.minorticks_on()
        for side in axs.spines.keys(): axs.spines[side].set_linewidth(1.5)
        axs.tick_params(axis='both', which='both', direction='in', top=True, right=True, labelsize=20, pad=10.)
        axs.tick_params(axis='both', which='major', length=8, width=2.0)
        axs.tick_params(axis='both', which='minor', length=4, width=2.0)

        axs.set_xlabel(self.x.label[0]+' '+self.x.label[1], fontsize=20)
        axs.set_ylabel(self.y.label[0]+' '+self.y.label[1], fontsize=20)
        #axs.set_xlabel(r'x', fontsize=20)
        #axs.set_ylabel(r'y', fontsize=20)

        axs.set(xlim=[np.nanmin(self.x.data)/2., np.nanmax(self.x.data)*2.], xscale='log')
        axs.set(ylim=[np.nanmin(self.y.data)/2., np.nanmax(self.y.data)*2.], yscale='log')

        #ax2 = ax.twiny()
        #ax2.set_xlim(ax.get_xlim())
        #ax2.set_xticks(ax.get_xticks()[1:-1], np.round(cosmo.age(ax.get_xticks()[1:-1]).value,1), size=14)
        #ax2.set_xlabel(r'Age of the Universe [Gyr]', size=16, labelpad=10)
        
        self.x.err[self.x.lim != 0] = self.x.data[self.x.lim != 0] * np.log10(np.nanmax(self.x.data)/np.nanmin(self.x.data)*4.) / 20.
        self.y.err[self.y.lim != 0] = self.y.data[self.y.lim != 0] * np.log10(np.nanmax(self.y.data)/np.nanmin(self.y.data)*4.) / 20.
        axs.errorbar(self.x.data, self.y.data, xerr=self.x.err, yerr=self.y.err,
                     uplims = self.y.lim == -1., lolims = self.y.lim == 1., xuplims = self.x.lim == -1., xlolims = self.x.lim == 1.,
                     fmt='o', alpha=1., mfc='none', ms=15., mec='black', mew=1., ecolor='gray', elinewidth=1., linestyle='none')
    
        if zkeyws is not None:
            colors = plt.cm.get_cmap('rainbow')
            # Plot the color
            if np.nanmax(self.z.data) > 10:
                sc = plt.scatter(self.x.data, self.y.data, c=self.z.data, cmap=colors, alpha=1., marker='o', s=15**2, edgecolors='none', norm=mpl.colors.LogNorm(vmin=np.nanmin(self.z.data), vmax=np.nanmax(self.z.data)))
            else:               
                sc = plt.scatter(self.x.data, self.y.data, c=self.z.data, cmap=colors, alpha=1., marker='o', s=15**2, edgecolors='none')

            cbar = plt.colorbar(sc, aspect=30, pad=0.02)
            cbar.ax.tick_params(labelsize=18, length=4, width=2.)
            cbar.set_label(self.z.label[0]+' '+self.z.label[1], rotation=90, size=20, labelpad=10.)
            cbar.outline.set_linewidth(1.5)
        else:
            sc = plt.scatter(self.x.data, self.y.data, c=self.z.data, cmap=color, alpha=1., marker='o', s=15**2, edgecolors='none')

        pdfname.savefig(fig)
        #plt.close()
        pdfname.close()

                            
        # Write data table
        self.write_table(self.x, xkeyws, self.y, ykeyws, self.z, zkeyws, plotname)

