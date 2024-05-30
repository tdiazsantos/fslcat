import os, sys, copy
#sys.path.insert(1, '/Users/tanio/Sync/pywork/pys')
import pdb, ipdb
from tqdm import tqdm
import numpy as np
import numpy.ma as ma
import pandas as pd
import importlib as impl

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

#import nicePlot
#imp.reload(nicePlot)
import axis
impl.reload(axis)


line_list = ['[OIII]52um', '[NIII]57um', '[OI]63um', '[OIII]88um', '[NII]122um','[CII]158um', '[OI]146um', '[NII]205um', '[CI]370um', '[CI]609um']
color_list = ['dodgerblue', 'limegreen', 'lightseagreen', 'dodgerblue', 'green', 'red',  'lightseagreen',  'green',      'violet',    'violet']

#'[CII]', '[NIII]', '[OIV]', '[NII]', '[OIII]', '[NeV]', '[NeIII]', '[NeII]', '[SiII]', '[SIII]', '[ArV]', '[ArIII]', '[ArII]'
#'red','limegreen','deepskyblue','green','dodgerblue','coral','orange','gold','silver','darkviolet','indigo','darkslateblue','navy'

class fslcat:

    def __init__(self, cat_name):

        self.fslcat = pd.read_csv(cat_name, skiprows=[1])
        self.fslcat['RA'] = [i.replace('"','') if type(i) == str else i for i in self.fslcat['RA'].values]
        self.fslcat['Dec'] = [i.replace('"','') if type(i) == str else i for i in self.fslcat['Dec'].values]



    def get_filename(self, xkeyws, ykeyws, zkeyws=None):
        
        plotname = ''.join(ykeyws['1'][0:2])
        if '2' in ykeyws.keys(): plotname += '-'+''.join(ykeyws['2'][0:2])
        plotname += '_vs_'        
        plotname += ''.join(xkeyws['1'][0:2])
        if '2' in xkeyws.keys(): plotname += '-'+''.join(xkeyws['2'][0:2])
        if zkeyws != None:
            plotname += '_sort_'        
            plotname += ''.join(zkeyws['1'][0:2])
            if '2' in zkeyws.keys(): plotname += '-'+''.join(zkeyws['2'][0:2])

        return plotname



    def pre_select(self, pre_select):

        # Start from a fresh copy of the catalog
        fslcat_select = self.fslcat.copy()

        for key, value in pre_select.items():
            if type(value) == list:
                fslcat_select = fslcat_select[(fslcat_select[key] >= value[0]) & (fslcat_select[key] <= value[1])]
            else:
                fslcat_select = fslcat_select[(fslcat_select[key] == value)]

        return fslcat_select



    def check_scale(self, ax):

        if ax.keyws[0] == 'LFIR_LIR':
            lir_inds = ax.cat['LFIR_LIR_type'].values == 'LIR'
            ax.data[lir_inds] *= 0.5
            ax.err[lir_inds] *= 0.5
        elif ax.keyws[0] == 'LIR_LFIR':
            lfir_inds = ax.cat['LIR_LFIR_type'].values == 'LFIR'
            ax.data[lfir_inds] *= 2.
            ax.err[lfir_inds] *= 2.
        # The continua is transformed to rest-frame
        elif ax.keyws[0] == 'Cont':
            ax.data /= (1+ax.cat['z'].values)
            ax.err /= (1+ax.cat['z'].values)
        
        # The Flux, when obtained from the Luminosity, is transformed to rest-frame
        if len(ax.keyws) == 3:
            if ax.keyws[0] == 'Lum' and ax.keyws[2] == 'Flux':
                ax.data *= 961.54 / ax.cat['LDist'].values**2 / (ax.cat['Line_rf'].values / (1+ax.cat['z'].values)) / (1+ax.cat['z'].values)  # Sdv = L * 961.54 / DL^2 / nu_obs
                ax.err *= 961.54 / ax.cat['LDist'].values**2 / (ax.cat['Line_rf'].values / (1+ax.cat['z'].values)) / (1+ax.cat['z'].values)


        return ax



    def write_table(self, xax, xkeyws, yax, ykeyws, zax, zkeyws, plotname):

        tbl = Table()
        
        tbl['Source'] = xax.cat['Source']
        tbl['RA'] = xax.cat['RA']
        tbl['Dec'] = xax.cat['Dec']
        tbl['z'] = xax.cat['z']
        tbl['LDist'] = xax.cat['LDist']
        tbl['Instrument'] = xax.cat['Instrument']
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

            if isinstance(zax.data[0], float):
                ascii.write(tbl, plotname+'.ecsv', overwrite=True, format='fixed_width', delimiter='', formats={'Source':'%s', 'RA':'%s', 'Dec':'%s', 'z':'%.4f', 'LDist':'%.1f',
                                                                                                                xhead:'%.2e', xhead+'_err':'%.2e', xhead+'_lim':'%.0f', yhead:'%.2e', yhead+'_err':'%.2e', yhead+'_lim':'%.0f',
                                                                                                                zhead:'%.2e', zhead+'_err':'%.2e', zhead+'_lim':'%.0f'})
            else:
                ascii.write(tbl, plotname+'.ecsv', overwrite=True, format='fixed_width', delimiter='', formats={'Source':'%s', 'RA':'%s', 'Dec':'%s', 'z':'%.4f', 'LDist':'%.1f',
                                                                                                                xhead:'%.2e', xhead+'_err':'%.2e', xhead+'_lim':'%.0f', yhead:'%.2e', yhead+'_err':'%.2e', yhead+'_lim':'%.0f',
                                                                                                                zhead:'%s', zhead+'_err':'%s', zhead+'_lim':'%s'})
                
        else:
            ascii.write(tbl, plotname+'.ecsv', overwrite=True, formats={'Source':'%s', 'RA':'%s', 'Dec':'%s', 'z':'%.4f', 'LDist':'%.1f',
                                                                        xhead:'%.2e', xhead+'_err':'%.2e', xhead+'_lim':'%.0f', yhead:'%.2e', yhead+'_err':'%.2e', yhead+'_lim':'%.0f'})



    def generate_axis(self, keyws, pre_select, r_cross, **kwargs):

        if '[' in keyws['1'][1] and keyws['1'][1]+'um' not in line_list: raise ValueError('Emission line not available in the catalog')

        # AXIS1
        print('Generating catalog for axis'+list(keyws.keys())[0])
        ax_pre_selection = {'Valid':'S', **pre_select, 'Line':keyws['1'][1]+'um'} if keyws['1'][1]+'um' in line_list else {'Valid':'S', **pre_select}
        # Select on the line, if any, and on other properties, if any
        ax_cat = self.pre_select(ax_pre_selection)
        # Build the data dictionary of the axis
        ax = axis.axis(keyws['1'], cat=ax_cat, **kwargs)
        ax = self.check_scale(ax)

        # AXIS2
        if '2' in keyws.keys():
            print('Generating catalog for axis'+list(keyws.keys())[1])
            ax2_pre_selection = {'Valid':'S', **pre_select, 'Line':keyws['2'][1]+'um'} if keyws['2'][1]+'um' in line_list  else {'Valid':'S', **pre_select}
            ax2_cat = self.pre_select(ax2_pre_selection)
            if len(keyws['2']) < 3:
                raise ValueError('An operator is needed for one of the axes. Check it tout.')
            else:            
                ax2 = axis.axis(keyws['2'], cat=ax2_cat, op=keyws['2'][2], **kwargs)
                ax2 = self.check_scale(ax2)
            
                print('Cross matching 1 and 2-axes')
                cross_ids, ids = axis.cross_corr(ax.cat, ax2.cat, ax.keyws, ax2.keyws, r_cross=r_cross,  **kwargs)
                ax.update(cross_ids)
                ax2.update(ids)
                
                ax = ax.operate(ax2)
        
        else:
            ax.keyws = {'1':ax.keyws}

        return ax

    

    def plot(self, xkeyws={'1':['', 'LFIR']}, ykeyws={'1':['[CII]158', 'Lum'], '2':['','LFIR','/']}, zkeyws=None, pre_select={}, outdir='./figures/', r_cross=0.01, color='red', xlims=None, ylims=None, **kwargs):
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
        
        if self.z.data.size == 0:
            print('WARNING: There are no data given the prompted axes')
        else:
            
            # Set up axes
            # PLOT
            print('Generating plot')
            plotname = outdir + self.get_filename(xkeyws, ykeyws, zkeyws=zkeyws)
            pdfname = mpl.backends.backend_pdf.PdfPages(plotname+'.pdf')
            
            # Write data table
            self.write_table(self.x, xkeyws, self.y, ykeyws, self.z, zkeyws, plotname)
            
            #nicePlot.nicePlot()
            
            if zkeyws is not None:
                if isinstance(self.z.data[0], float):
                    fig, axs = plt.subplots(figsize=(12.2, 8.5*12.2/11.))
                    plt.subplots_adjust(left=0.135, bottom=0.14, right=1.01, top=0.98)
                else:
                    fig, axs = plt.subplots(figsize=(11., 8.5))
                    plt.subplots_adjust(left=0.145, bottom=0.14, right=0.96, top=0.98)
            else:
                fig, axs = plt.subplots(figsize=(11., 8.5))
                plt.subplots_adjust(left=0.145, bottom=0.14, right=0.96, top=0.98)
        
            axs.minorticks_on()
            for side in axs.spines.keys(): axs.spines[side].set_linewidth(2.0)
            axs.tick_params(axis='both', which='both', direction='in', top=True, right=True, labelsize=24, pad=10.)
            axs.tick_params(axis='both', which='major', length=8, width=2.0)
            axs.tick_params(axis='both', which='minor', length=4, width=2.0)
            
            axs.set_xlabel(self.x.label[0]+' '+self.x.label[1], fontsize=32)
            axs.set_ylabel(self.y.label[0]+' '+self.y.label[1], fontsize=32)
            #axs.set_xlabel(r'x', fontsize=20)
            #axs.set_ylabel(r'y', fontsize=20)
            
            if xlims is None:
                if self.x.keyws['1'][0] == 'z': axs.set(xlim=[0.8, 15.], xscale='log')
                else: axs.set(xlim=[np.nanmin(self.x.data)/2., np.nanmax(self.x.data)*2.], xscale='log')
            else:
                axs.set(xlim=[xlims[0], xlims[1]], xscale=xlims[2])
            if ylims is None:
                axs.set(ylim=[np.nanmin(self.y.data)/2., np.nanmax(self.y.data)*2.], yscale='log')
            else:
                axs.set(ylim=[ylims[0], ylims[1]], yscale=ylims[2])
                
            #ax2 = ax.twiny()
            #ax2.set_xlim(ax.get_xlim())
            #ax2.set_xticks(ax.get_xticks()[1:-1], np.round(cosmo.age(ax.get_xticks()[1:-1]).value,1), size=14)
            #ax2.set_xlabel(r'Age of the Universe [Gyr]', size=16, labelpad=10)
            
            self.x.err[self.x.lim != 0] = self.x.data[self.x.lim != 0] * np.log10(axs.get_xlim()[1]/axs.get_xlim()[0]*4.) / 25.
            self.y.err[self.y.lim != 0] = self.y.data[self.y.lim != 0] * np.log10(axs.get_ylim()[1]/axs.get_ylim()[0]*4.) / 25.
            axs.errorbar(self.x.data, self.y.data, xerr=self.x.err, yerr=self.y.err,
                         uplims = self.y.lim == -1., lolims = self.y.lim == 1., xuplims = self.x.lim == -1., xlolims = self.x.lim == 1.,
                         ecolor='gray', elinewidth=1., linestyle='none', zorder=0) #fmt='o', alpha=1., mfc='none', ms=15., mec='black', mew=1., 
            
            
            if zkeyws is not None:
                # Plot the color
                if isinstance(self.z.data[0], float):
                    colors = plt.cm.get_cmap('rainbow')
                    vmin, vmax = [1., 15.] if self.z.keyws['1'][0] == 'z' else [np.nanmin(self.z.data), np.nanmax(self.z.data)]
                    if vmax/vmin > 10:
                        sc = plt.scatter(self.x.data, self.y.data, c=self.z.data, cmap=colors, alpha=0.9, marker='o', s=15**2, edgecolors='black', linewidth=1., norm=mpl.colors.LogNorm(vmin=vmin, vmax=vmax))
                    else:
                        sc = plt.scatter(self.x.data, self.y.data, c=self.z.data, cmap=colors, alpha=0.9, marker='o', s=15**2, edgecolors='black', linewidth=1., vmin=vmin, vmax=vmax)
                else:
                    #colors = plt.cm.get_cmap('gist_rainbow_r')
                    #colors = plt.cm.get_cmap('Set1')
                    if zkeyws['1'][1] == 'Simplified':
                        self.z.data[np.where(self.z.data == 'Dwarf')[0]] = 'MS/SFG'
                        self.z.data[np.where(self.z.data == 'Candidate')[0]] = 'MS/SFG'
                        #self.z.data[np.where(self.z.data == 'DLAHost')[0]] = 'DLAHost'
                        self.z.data[np.where(self.z.data == 'Hot-DOG')[0]] = 'QSO/AGN'
                        self.z.data[np.where(self.z.data == 'LAB')[0]] = 'Opt-Sel'
                        self.z.data[np.where(self.z.data == 'LAE')[0]] = 'Opt-Sel'
                        self.z.data[np.where(self.z.data == 'LBG')[0]] = 'Opt-Sel'
                        self.z.data[np.where(self.z.data == 'MS')[0]] = 'MS/SFG'
                        self.z.data[np.where(self.z.data == 'QSO')[0]] = 'QSO/AGN'
                        self.z.data[np.where(self.z.data == 'AGN')[0]] = 'QSO/AGN'
                        #self.z.data[np.where(self.z.data == 'Quiescent')[0]] = 'QSC'
                        self.z.data[np.where(self.z.data == 'SB')[0]] = 'SB/SMG'
                        self.z.data[np.where(self.z.data == 'SFG')[0]] = 'MS/SFG'
                        self.z.data[np.where(self.z.data == 'DSFG')[0]] = 'MS/SFG'
                        self.z.data[np.where(self.z.data == 'SMG')[0]] = 'SB/SMG'
                        self.z.data[np.where(self.z.data == '[CII]-emitter')[0]] = 'ALMA-Sel'
                        self.z.data[np.where(self.z.data == 'PCM')[0]] = 'Cluster'
                        self.z.data[np.where(self.z.data == 'SMG-candidate')[0]] = 'SB/SMG'
                        
                    labels, indices = np.unique(self.z.data, return_inverse=True)
                    for i in range(len(labels)):
                        colors = self.z.get_color('types')
                        type_inds = np.where(indices == i)[0]
                        sc = plt.scatter(self.x.data[type_inds], self.y.data[type_inds], c=[colors[ind] for ind in type_inds], alpha=0.9, marker='o', s=15**2, edgecolors='black', linewidth=1., label=labels[i]) #, cmap=colors
                        
                    legend = axs.legend(loc='lower left', frameon=True, edgecolor='inherit', fontsize=16, borderaxespad=1.5) #, handletextpad=1)
                    frame = legend.get_frame()
                    frame.set_boxstyle('Square')
                    frame.set_linewidth(2.0)
                    frame.set_edgecolor('black')
                    
                if isinstance(self.z.data[0], float):
                    cbar = plt.colorbar(sc, aspect=30, pad=0.02)
                    cbar.ax.tick_params(labelsize=24, length=4, width=2.)
                    cbar.set_label(self.z.label[0]+' '+self.z.label[1], rotation=90, size=32, labelpad=10.)
                    if isinstance(self.z.data[0], str): cbar.ax.set_yticklabels(labels)
                    cbar.outline.set_linewidth(2.0)
                else:
                    #cbar = plt.colorbar(sc, aspect=30, pad=0.02, ticks=range(len(labels)))
                    pass
            else:
                linec = self.y.get_color('lines')
                sc = plt.scatter(self.x.data, self.y.data, color=linec, alpha=1., marker='o', s=15**2, edgecolors='black', linewidth=1.)
                
            pdfname.savefig(fig)
            pdfname.close()
            
            plt.savefig(plotname+'.png')
            
            #plt.close()
            
            
            #ipdb.set_trace()
