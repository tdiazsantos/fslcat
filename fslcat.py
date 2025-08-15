import os, sys, copy
import pdb, ipdb
import numpy as np
import pandas as pd
import importlib as impl
import math

import scipy.ndimage
from scipy import stats
from astropy import units as u
from astropy import constants as c
from astropy.stats import sigma_clip
from astropy.coordinates import SkyCoord
from astropy.io import ascii
from astropy.table import Table

from astropy.cosmology import FlatLambdaCDM

import matplotlib as mpl, matplotlib.backends.backend_pdf, matplotlib.pyplot as plt, matplotlib.cm as cm, matplotlib.patheffects as PathEffects
from matplotlib.colors import Normalize, LogNorm

#import nicePlot
#imp.reload(nicePlot)
import axis, linfit
impl.reload(axis)
impl.reload(linfit)


line_list = ['[OIII]52um', '[NIII]57um', '[OI]63um', '[OIII]88um', '[NII]122um','[CII]158um', '[OI]146um', '[NII]205um', '[CI]370um', '[CI]609um']
color_list = ['dodgerblue', 'limegreen', 'lightseagreen', 'dodgerblue', 'green', 'red',  'lightseagreen',  'green',      'violet',    'violet']

#'[CII]', '[NIII]', '[OIV]', '[NII]', '[OIII]', '[NeV]', '[NeIII]', '[NeII]', '[SiII]', '[SIII]', '[ArV]', '[ArIII]', '[ArII]'
#'red','limegreen','deepskyblue','green','dodgerblue','coral','orange','gold','silver','darkviolet','indigo','darkslateblue','navy'

class fslcat:

    def __init__(self, cat_name):

        self.fslcat = pd.read_csv(cat_name, skiprows=[1])
        self.fslcat['RA'] = [i.replace('"','') if type(i) == str else i for i in self.fslcat['RA'].values]
        self.fslcat['Dec'] = [i.replace('"','') if type(i) == str else i for i in self.fslcat['Dec'].values]



    def get_filename(self, xkeyws, ykeyws, zkeyws=None, pre_select={}):
        
        plotname = ''.join(ykeyws['1'])
        if '2' in ykeyws.keys(): plotname += '-'+''.join(ykeyws['2'])
        plotname += '_vs_'        
        plotname += ''.join(xkeyws['1'])
        if '2' in xkeyws.keys(): plotname += '-'+''.join(xkeyws['2'])
        if zkeyws != None:
            plotname += '_sort_'        
            plotname += ''.join(zkeyws['1'])
            if '2' in zkeyws.keys(): plotname += '-'+''.join(zkeyws['2'])
        if pre_select != {}:
            plotname += '_presel_'
            presel_items = list(pre_select.items())[0]
            plotname += ''.join(presel_items[0])
            plotname += ''.join(str(presel_items[1][0]))
            if presel_items[0] == 'z':
                plotname += '-'+''.join(str(presel_items[1][1]))                

        plotname = plotname.replace('/','')

        return plotname



    def pre_select(self, pre_select):

        # Start from a fresh copy of the catalog
        fslcat_select = self.fslcat.copy()

        for key, value in pre_select.items():
            if type(value) == list:
                if value[0] != 0 and value[1] != 0:
                    fslcat_select = fslcat_select[(fslcat_select[key] >= value[0]) & (fslcat_select[key] <= value[1])]
                elif np.isinf(value[0]) and value[1] != 0:
                    fslcat_select = fslcat_select[(fslcat_select[key] <= value[1])]
                elif value[0] != 0 and np.isinf(value[1]):
                    fslcat_select = fslcat_select[(fslcat_select[key] >= value[0])]
                else:
                    raise ValueError('Value limits could not be parsed')
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
        if len(ax.keyws) >= 3:
            if ax.keyws[0] == 'Lum' and ax.keyws[2] == 'Flux':
                ax.data *= 961.54 / ax.cat['LDist'].values**2 / (ax.cat['Line_rf'].values / (1+ax.cat['z'].values)) / (1+ax.cat['z'].values)  # Sdv = L * 961.54 / DL^2 / nu_obs, then / nu_obs to go to Sdv_restf
                ax.err *= 961.54 / ax.cat['LDist'].values**2 / (ax.cat['Line_rf'].values / (1+ax.cat['z'].values)) / (1+ax.cat['z'].values)

        if 'MagCorr' in ax.keyws:
            ax.data /= (ax.cat['Mag_min'].values + ax.cat['Mag_max'].values)/2
            ax.err /= (ax.cat['Mag_min'].values + ax.cat['Mag_max'].values)/2

        return ax



    def generate_axis(self, keyws, pre_select, r_cross, newest, **kwargs):
        
        if '[' in keyws['1'][1] and keyws['1'][1]+'um' not in line_list: raise ValueError('Emission line not available in the catalog')

        # AXIS1
        print('Generating catalog for axis'+list(keyws.keys())[0])
        ax_pre_selection = {'Valid':'S', **pre_select, 'Line':keyws['1'][1]+'um'} if keyws['1'][1]+'um' in line_list else {'Valid':'S', **pre_select}
        # Select on the line, if any, and on other properties, if any
        ax_cat = self.pre_select(ax_pre_selection)
        # Build the data dictionary of the axis
        ax = axis.axis(keyws['1'], cat=ax_cat, newest=newest, **kwargs)
        ax = self.check_scale(ax)
        
        # AXIS2
        if '2' in keyws.keys():
            print('Generating catalog for axis'+list(keyws.keys())[1])
            ax2_pre_selection = {'Valid':'S', **pre_select, 'Line':keyws['2'][1]+'um'} if keyws['2'][1]+'um' in line_list  else {'Valid':'S', **pre_select}
            ax2_cat = self.pre_select(ax2_pre_selection)
            if len(keyws['2']) < 3:
                raise ValueError('An operator is needed for one of the axes. Check it out.')
            else:            
                ax2 = axis.axis(keyws['2'], cat=ax2_cat, newest=newest, op=keyws['2'][2], **kwargs)
                ax2 = self.check_scale(ax2)
            
                print('Cross matching 1 and 2-axes')
                cross_ids, ids = axis.cross_corr(ax.cat, ax2.cat, ax.keyws, ax2.keyws, r_cross=r_cross, newest=newest, **kwargs)
                ax.update(cross_ids)
                ax2.update(ids)
                
                ax = ax.operate(ax2)
        
        else:
            ax.keyws = {'1':ax.keyws}

        return ax

    

    def write_table(self, xax, xkeyws, yax, ykeyws, zax, zkeyws, stdata, plotname):

        tbl = Table()
        
        tbl['Source'] = xax.cat['Source']
        tbl['RA'] = xax.cat['RA']
        tbl['Dec'] = xax.cat['Dec']
        tbl['Redshift'] = xax.cat['z']
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

            sthead = 'SourceType'
            tbl[sthead] = stdata

            if isinstance(zax.data[0], float):
                ascii.write(tbl, plotname+'.ecsv', overwrite=True, format='fixed_width', delimiter='', formats={'Source':'%s', 'RA':'%s', 'Dec':'%s', 'Redshift':'%f', 'LDist':'%.1f',
                                                                                                                xhead:'%.3e', xhead+'_err':'%.3e', xhead+'_lim':'%.0f', yhead:'%.3e', yhead+'_err':'%.3e', yhead+'_lim':'%.0f',
                                                                                                                zhead:'%.3e', zhead+'_err':'%.3e', zhead+'_lim':'%.0f', sthead:'%s'})
            else:
                ascii.write(tbl, plotname+'.ecsv', overwrite=True, format='fixed_width', delimiter='', formats={'Source':'%s', 'RA':'%s', 'Dec':'%s', 'Redshift':'%f', 'LDist':'%.1f',
                                                                                                                xhead:'%.3e', xhead+'_err':'%.3e', xhead+'_lim':'%.0f', yhead:'%.3e', yhead+'_err':'%.3e', yhead+'_lim':'%.0f',
                                                                                                                zhead:'%s', zhead+'_err':'%s', zhead+'_lim':'%s', sthead:'%s'})
                
        else:
            sthead = 'SourceType'
            tbl[sthead] = stdata

            ascii.write(tbl, plotname+'.ecsv', overwrite=True, formats={'Source':'%s', 'RA':'%s', 'Dec':'%s', 'Redshift':'%f', 'LDist':'%.1f',
                                                                        xhead:'%.3e', xhead+'_err':'%.3e', xhead+'_lim':'%.0f', yhead:'%.3e', yhead+'_err':'%.3e', yhead+'_lim':'%.0f', sthead:'%s'})



    def nearby_catalog(self, fig_label, file_dir=None):
        # Import nearby galaxy data for deficit plots
        if file_dir == None: file_dir = '/catalogs/'
        local_file_name = ''
        if '2' in ykeyws.keys():
            if ykeyws['2'][0] == 'LFIR_LIR' and xkeyws['1'][0] == 'LFIR_LIR':
                if ykeyws['1'][1] == '[OI]63': local_file_name = 'linefluxoi639-firfluxip609-log_vs_firfluxip609-log_sort_firfluxip609-log.dat'
                elif ykeyws['1'][1] == '[OIII]88': local_file_name = 'linefluxoiii889-firfluxip609-log_vs_firfluxip609-log_sort_firfluxip609-log.dat'
                elif ykeyws['1'][1] == '[NII]122': local_file_name = 'linefluxnii1229-firfluxip609-log_vs_firfluxip609-log_sort_firfluxip609-log.dat'
                elif ykeyws['1'][1] == '[CII]158': local_file_name = 'linefluxcii1589-firfluxip609-log_vs_firfluxip609-log_sort_firfluxip609-log.dat'
                elif ykeyws['1'][1] == '[NII]205': local_file_name = 'linefluxnii2058-firfluxip608-log_vs_firfluxip608-log_sort_firfluxip608-log.dat'
                elif ykeyws['1'][1] == '[CI]370': local_file_name = 'linefluxci3728-firfluxip608-log_vs_firfluxip608-log_sort_firfluxip608-log.dat'
                elif ykeyws['1'][1] == '[CI]609': local_file_name = 'linefluxci6098-firfluxip608-log_vs_firfluxip608-log_sort_firfluxip608-log.dat'
                fig_label = ykeyws['1'][1]+r'$\mu$m'
            elif xkeyws['1'][0] == 'LFIR_LIR':
                if ykeyws['1'][1] == '[OIII]88' and ykeyws['2'][1] == '[NII]122': local_file_name = 'linefluxoiii889-linefluxnii1229-log_vs_firfluxip609-log_sort_firfluxip609-log.dat'
                elif ykeyws['1'][1] == '[OIII]88' and ykeyws['2'][1] == '[CII]158': local_file_name = 'linefluxoiii889-linefluxcii1589-log_vs_firfluxip609-log_sort_firfluxip609-log.dat'
                elif ykeyws['1'][1] == '[CII]158' and ykeyws['2'][1] == '[NII]205': local_file_name = 'linefluxcii1588-linefluxnii2058-log_vs_firfluxip608-log_sort_firfluxip608-log.dat'
                elif ykeyws['1'][1] == '[NII]122' and ykeyws['2'][1] == '[NII]205': local_file_name = 'linefluxnii1228-linefluxnii2058-log_vs_firfluxip608-log_sort_firfluxip608-log.dat'
                elif ykeyws['1'][1] == '[CI]370' and ykeyws['2'][1] == '[CI]609': local_file_name = 'linefluxci3728-linefluxci6098-log_vs_firfluxip608-log_sort_firfluxip608-log.dat'
            elif xkeyws['1'][0] == 'FWHM':
                if xkeyws['1'][1] == '[CII]158': local_file_name = 'linefluxcii1589-firfluxip609-log_vs_linesigmacii1589-log_sort_firfluxip609-log.dat'
                
        if '2' not in ykeyws.keys():
            if xkeyws['1'][0] == 'FWHM':
                if ykeyws['1'][1] == '[CII]158': local_file_name = 'linefluxcii1589-log_vs_linesigmacii1589-log_sort_firfluxip609-log.dat'
                
        if local_file_name != '':
            print('Loading nearby galaxy data')
            try:
                tab = Table.read(file_dir+local_file_name, format='ascii.basic', data_start=3, comment='#', names=('0,','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'))
            except:
                raise IOError('Local data table not found:', file_dir+local_file_name)
            goals_lfir = {'data': tab['7'], 'err': tab['8']}
            goals_def = {'data': tab['10'], 'err': tab['11']}
            if xkeyws['1'][0] == 'FWHM':
                goals_lfir['data'] *= 2.355
                goals_lfir['err'] *= 2.355

        return goals_lfir, goals_def

    

    def plot(self, xkeyws={'1':['LFIR_LIR', 'MagCorr']}, ykeyws={'1':['Lum', '[CII]158'], '2':['LFIR_LIR', '', '/']}, zkeyws=None, pre_select={}, outdir='./figures/', r_cross=0.01, color='red', xlims=None, ylims=None, fit=False, hist=False, newest=True, nearby_data=False, **kwargs):
        """
        The axis keywords specify the quantity to be ploted in the x, y (and optionally z) axes.
        Each axis is constructed from one or two quantities from the catalog.
        If two quantities are chosen, an operator must be passed, which will sum, subtract, multiply or divide the two.
        The quantity/quantities of each axis keyword is given via a list.
        For lines:
           The first element of the list specifies the type of measurement ('Flux', 'Lum'(inosity), 'Cont'(inuum), 'FWHM'), the second specifies the emission line, and the third the operator (in case two parameters are given)
        For other quantities:
           The first element of the list specifies the quantity ('LIR', 'LIR_LFIR', 'LFIR', 'LFIR_LIR', 'z', 'LDist', 'Type', 'Instrument'), the second specifies any modulation (such as 'MagCorr' for LIRs and LFIRs)

        pre_select: Filter entries by conditional arguments (e.g., pre_select={'z': [6,np.inf]} will select galaxies at z > 6). Default: {} (empty = no pre-selection; all catalog is used)
        outdir: Folder to store the figures and sub-catalogs. Default: './figures/'
        r_cross: Radius for cross-correlating sources (obsolete)
        color: Color for the datapoints in case a color-coding is not used. Default: 'black'
        xlims, ylims: Force the figure to plot only the axis ranges within those limits. Default: Plot the entire range of the dataset
        fit: if [True], fit the data with a linear regresion. Default: [False]
        hist: if [True], plot histogram of the axes in adjacent sub-panels. Default: [False]
        newest: if [False], the entry kept for generating the plot and catalog will be the first ever measured, instead of the latest/newest. Default: [True]
        nearby_data: if [True], plot a heat map of nearby dusty sources for comparison with the high-z data. Default: [False]
        
        """
        
        # XAXIS
        self.x = self.generate_axis(xkeyws, pre_select, r_cross, newest)
        if len(self.x.data) == 0:
            print('No x-axis data found')
            pass
        # YAXIS
        self.y = self.generate_axis(ykeyws, pre_select, r_cross, newest)
        if len(self.y.data) == 0:
            print('No y-axis data found')
            pass
        # ZAXIS
        if zkeyws is not None:
            self.z = self.generate_axis(zkeyws, pre_select, r_cross, newest)
        else:
            self.z = None
            
        print('Cross matching x and y-axes')
        xids, yids = axis.cross_corr(self.x.cat, self.y.cat, self.x.keyws, self.y.keyws, r_cross=r_cross, newest=newest, **kwargs)
        print('Updating x and y-axes')
        self.x.update(xids)
        self.y.update(yids)

        if zkeyws is not None:
            print('Cross matching x and z-axes')
            # Here we cross match but we keep all the entries in the x/y-axis even if they have NaN values in the z-axis
            xids, zids = axis.cross_corr(self.x.cat, self.z.cat, self.x.keyws, self.z.keyws, keep_all=True, r_cross=r_cross, newest=newest, **kwargs)
            print('Updating z-axis')
            self.z.update(zids, self.x.cat)
        
        if np.isnan(self.x.data).all() or np.isnan(self.y.data).all():
            pass

        else:
            # Set up axes
            # PLOT
            print('Generating plot')
            plotname = outdir + self.get_filename(xkeyws, ykeyws, zkeyws=zkeyws, pre_select=pre_select)
            pdfname = mpl.backends.backend_pdf.PdfPages(plotname+'.pdf')
            
            # Write data table
            sourcetypes = self.x.cat['Type'].values
            self.write_table(self.x, xkeyws, self.y, ykeyws, self.z, zkeyws, sourcetypes, plotname)
                        
            # Fit data
            if fit != False:
                xfitdata = np.copy(self.x.data)
                xfiterr = np.copy(self.x.err)
                yfitdata = np.copy(self.y.data)
                yfiterr = np.copy(self.y.err)

                xdataliminds = self.x.lim == -1.
                xfiterr[xdataliminds] = xfitdata[xdataliminds] #* np.log10(xfitdata[xdataliminds]) * np.log(10)
                xfitdata[xdataliminds] = 0. # np.nanmin(xfitdata)
                ydataliminds = self.y.lim == -1.
                yfiterr[ydataliminds] = yfitdata[ydataliminds] #* np.log10(yfitdata[ydataliminds]) * np.log(10)
                yfitdata[ydataliminds] = 0. # np.nanmin(yfitdata)

                censinds = (xfiterr > 0.) & (yfiterr > 0.)

                myfit = linfit.linfit(xfitdata[censinds], yfitdata[censinds], xfiterr[censinds], yfiterr[censinds], log=True)

                tmpbeta = [1., 1e5]
                while True:
                    bestfit = myfit.run(tmpbeta)
                    if np.sqrt((abs(bestfit.beta[0]-tmpbeta[0])/abs(tmpbeta[0]))**2 + (abs(bestfit.beta[1]-tmpbeta[1])/abs(tmpbeta[1]))**2) <= 1e-5:
                        break
                    else:
                        tmpbeta = bestfit.beta
                    
                ysig = np.std(yfitdata[censinds]-myfit.exp_func(bestfit.beta, xfitdata[censinds]))
                xsig = np.std(xfitdata[censinds]-myfit.exp_invfunc(bestfit.beta, yfitdata[censinds]))

                # FIT IN LOG SPACE!

                from hyperfit.linfit import LinFit
                ndata = len(xfitdata[censinds])
                data, cov = np.empty((2, ndata)), np.empty((2, 2, ndata))
                for i, (x, y, ex, ey, rho_xy) in enumerate(zip(xfitdata[censinds], yfitdata[censinds], xfiterr[censinds], yfiterr[censinds], np.zeros(ndata))):
                    cov[:, :, i] = np.array([[ex ** 2, ex * ey * rho_xy], [ex * ey * rho_xy, ey ** 2]])
                    data[:, i] = [x, y]
                hf = LinFit(data, cov)
                ipdb.set_trace()

            fig_label = None

            # Load catalog of nearby galaxy data if available
            if nearby_data == True:
                goals_lfir, goals_def = self.nearby_catalog(fig_label)

            # Set up figure
            if zkeyws is not None:
                if self.z.data.size == 0: print('WARNING: There are no data given the requested z-axis')

                if isinstance(self.z.data[0], float):
                    if hist == True: raise ValueError('Side histograms and color bars representing numerical values are not compatible. Please, switch off one of them.')
                    fig, axs = plt.subplots(figsize=(12.2, 8.5*12.2/11.))
                    plt.subplots_adjust(left=0.13, bottom=0.14, right=0.985, top=0.98)
                else:
                    #fig, axs = plt.subplots(figsize=(11., 8.5))
                    fig = plt.figure(figsize=(11., 8.5))
                    if hist == False:
                        plt.subplots_adjust(left=0.145, bottom=0.14, right=0.98, top=0.98)
                        axs = fig.add_subplot(1, 1, 1)
                    else:
                        gs = fig.add_gridspec(2, 2, width_ratios=(4, 1), height_ratios=(1, 4),
                                              left=0.145, bottom=0.14, right=0.98, top=0.98,
                                              wspace=0.05, hspace=0.05)
                        axs = fig.add_subplot(gs[1, 0])
                        axs_xhist = fig.add_subplot(gs[0, 0], sharex=axs)
                        axs_yhist = fig.add_subplot(gs[1, 1], sharey=axs)
                        
            else:
                #fig, axs = plt.subplots(figsize=(11., 8.5))
                fig = plt.figure(figsize=(11., 8.5))
                if hist == False:
                    plt.subplots_adjust(left=0.145, bottom=0.14, right=0.96, top=0.98)
                    axs = fig.add_subplot(1, 1, 1)
                else:
                    gs = fig.add_gridspec(2, 2, width_ratios=(4, 1), height_ratios=(1, 4),
                                          left=0.145, bottom=0.14, right=0.98, top=0.98,
                                          wspace=0.05, hspace=0.05)
                    axs = fig.add_subplot(gs[1, 0])
                    axs_xhist = fig.add_subplot(gs[0, 0], sharex=axs)
                    axs_yhist = fig.add_subplot(gs[1, 1], sharey=axs)
               

            # Set up axis style
            axs.minorticks_on()
            for side in axs.spines.keys(): axs.spines[side].set_linewidth(2.0)
            axs.tick_params(axis='both', which='both', direction='in', width=2.0, top=True, right=True, labelsize=24, pad=10.)
            axs.tick_params(axis='both', which='major', length=8)
            axs.tick_params(axis='both', which='minor', length=4)
            
            axs.set_xlabel(self.x.label[0]+' '+self.x.label[1], fontsize=32)
            axs.set_ylabel(self.y.label[0]+' '+self.y.label[1], fontsize=32)
            
            # Set axes limits
            if xlims is None:
                if self.x.keyws['1'][0] == 'z':
                    xlims = [0.8, 15.]
                else:
                    xlims = [np.nanmin(self.x.data)/2., np.nanmax(self.x.data)*2.]                        
                    axs.set(xlim=xlims, xscale='log')
            else:
                axs.set(xlim=[xlims[0], xlims[1]], xscale=xlims[2])
                
            if ylims is None:
                ylims = [np.nanmin(self.y.data)/2., np.nanmax(self.y.data)*2.]
                axs.set(ylim=ylims, yscale='log')
            else:
                axs.set(ylim=[ylims[0], ylims[1]], yscale=ylims[2])
                
            #ax2 = ax.twiny()
            #ax2.set_xlim(ax.get_xlim())
            #ax2.set_xticks(ax.get_xticks()[1:-1], np.round(cosmo.age(ax.get_xticks()[1:-1]).value,1), size=14)
            #ax2.set_xlabel(r'Age of the Universe [Gyr]', size=16, labelpad=10)
            
            self.x.err[self.x.lim == 1] = self.x.data[self.x.lim == 1] / 2. * np.log10(xlims[1]/xlims[0]) / 6.
            self.x.err[self.x.lim == -1] = self.x.data[self.x.lim == -1] / 4. * np.log10(xlims[1]/xlims[0]) / 6.
            self.y.err[self.y.lim == 1] = self.y.data[self.y.lim == 1] / 2. * np.log10(ylims[1]/ylims[0]) / 7.
            self.y.err[self.y.lim == -1] = self.y.data[self.y.lim == -1] / 4. * np.log10(ylims[1]/ylims[0]) / 5.5
            
            axs.errorbar(self.x.data, self.y.data,
                         xerr=self.x.err, yerr=self.y.err,
                         uplims = self.y.lim == -1., lolims = self.y.lim == 1., xuplims = self.x.lim == -1., xlolims = self.x.lim == 1.,
                         ecolor='gray', elinewidth=1., linestyle='none', zorder=0, fmt='o', mfc='black', mec='black', ms=0.) #fmt='o', alpha=1., mfc='none', ms=15., mec='black', mew=1., 
            
            if zkeyws is not None:

                # Plot nearby galaxies
                if nearby_data == True:
                    if zkeyws['1'][0] == 'z': contc = 'gray'
                    elif zkeyws['1'][0] == 'Type': contc = 'lightcoral'
                    
                    import seaborn as sns
                    sns.kdeplot(x=goals_lfir['data'][(np.isnan(goals_lfir['data']) == False) & (np.isnan(goals_def['data']) == False)], y=goals_def['data'][(np.isnan(goals_lfir['data']) == False) & (np.isnan(goals_def['data']) == False)], levels=5, alpha=.5, color=contc, fill=True)
                    
                # Plot the color
                if isinstance(self.z.data[0], float):

                    if np.sum(np.isnan(self.z.data)) > 0:
                        z_nans = np.isnan(self.z.data)
                        sc = axs.scatter(self.x.data[z_nans], self.y.data[z_nans], color='black', alpha=1.0, marker='o', s=10**2, edgecolors='black', linewidth=1.)
                        
                    colors = plt.cm.get_cmap('rainbow')
                    vmin, vmax = [1., 15.] if self.z.keyws['1'][0] == 'z' else [np.nanmin(self.z.data), np.nanmax(self.z.data)]
                    if vmax/vmin > 10:
                        sc = axs.scatter(self.x.data, self.y.data, c=self.z.data, cmap=colors, alpha=1.0, marker='o', s=15**2, edgecolors='black', linewidth=1., norm=mpl.colors.LogNorm(vmin=vmin, vmax=vmax))
                    else:
                        sc = axs.scatter(self.x.data, self.y.data, c=self.z.data, cmap=colors, alpha=1.0, marker='o', s=15**2, edgecolors='black', linewidth=1., vmin=vmin, vmax=vmax)
                else:
                    if zkeyws['1'][1] == 'Simplified': self.z.simplify_type()
                    labels, indices = np.unique(self.z.data, return_inverse=True)
                    
                    if hist == True:
                        for side in axs_xhist.spines.keys(): axs_xhist.spines[side].set_linewidth(2.0)
                        axs_xhist.tick_params(axis='both', which='both', direction='in', width=2.0, top=True, right=True, labelbottom=False)
                        axs_xhist.tick_params(axis='y', labelsize=20, pad=10.)
                        for side in axs_yhist.spines.keys(): axs_yhist.spines[side].set_linewidth(2.0)
                        axs_yhist.tick_params(axis='both', which='both', direction='in', width=2.0, top=True, right=True, labelleft=False)
                        axs_yhist.tick_params(axis='x', labelsize=20, pad=10.)
                        hstyle = {'linewidth':2.0}
                        
                    for i in range(len(labels)):
                        colors = self.z.get_color('types')
                        type_inds = np.where(indices == i)[0]
                        sc = axs.scatter(self.x.data[type_inds], self.y.data[type_inds], c=[colors[ind] for ind in type_inds], alpha=1.0, marker='o', s=15**2, edgecolors='black', linewidth=1., label=labels[i]) #, cmap=colors

                        if hist == True:
                            xbins = np.geomspace(xlims[0], xlims[1], 10) if axs.get_xaxis().get_scale() == 'log' else np.linspace(xlims[0], xlims[1], 10)
                            ybins = np.geomspace(ylims[0], ylims[1], 10) if axs.get_yaxis().get_scale() == 'log' else np.linspace(ylims[0], ylims[1], 10)
                            
                            axs_xhist.hist(self.x.data[type_inds], bins=xbins, color=colors[type_inds[0]], histtype='step', **hstyle)
                            axs_yhist.hist(self.y.data[type_inds], bins=ybins, orientation='horizontal', color=colors[type_inds[0]], histtype='step', **hstyle)
                            
                    legend = axs.legend(loc='lower left', frameon=True, edgecolor='inherit', fontsize=16, borderaxespad=1.5) #, handletextpad=1)
                    frame = legend.get_frame()
                    frame.set_boxstyle('Square')
                    frame.set_linewidth(2.0)
                    frame.set_edgecolor('black')

                if isinstance(self.z.data[0], float):
                    cbar = plt.colorbar(sc, aspect=30, pad=0.02)
                    cbar.ax.tick_params(labelsize=24, length=8, width=2.)
                    cbar.ax.tick_params(which='minor', length=4, width=2.)
                    cbar.set_label(self.z.label[0]+' '+self.z.label[1], rotation=90, size=32, labelpad=10.)
                    if isinstance(self.z.data[0], str): cbar.ax.set_yticklabels(labels)
                    cbar.outline.set_linewidth(2.0)
                else:
                    #cbar = plt.colorbar(sc, aspect=30, pad=0.02, ticks=range(len(labels)))
                    pass

                if fig_label is not None:
                    txt = axs.text(0.6, 0.88, fig_label, fontsize=36, fontweight='heavy', color='k', transform=axs.transAxes)

            else:
                linec = self.y.get_color('lines')[0]
                if fig_label is not None:
                    txt = axs.text(0.6, 0.88, fig_label, fontsize=36, fontweight='heavy', color=linec, transform=axs.transAxes)
                    txt.set_path_effects([PathEffects.withStroke(linewidth=2., foreground='black')])
                

                if ykeyws['2'][0] == 'LFIR_LIR':
                    lfir_ofm = np.nanmedian(np.log10(self.x.data))
                    def_ofm = np.nanmedian(np.log10(self.y.data))
                    axs.plot(np.array([1e-6, 1e6])*10**lfir_ofm, np.array([1e6, 1e-6])*10**def_ofm, color='gray', linestyle='dashed')

                # Plot nearby galaxies
                if nearby_data == True:
                    import seaborn as sns
                    sns.kdeplot(x=goals_lfir['data'][(np.isnan(goals_lfir['data']) == False) & (np.isnan(goals_def['data']) == False)], y=goals_def['data'][(np.isnan(goals_lfir['data']) == False) & (np.isnan(goals_def['data']) == False)], levels=5, alpha=.5, color=linec, fill=True)

                sc = axs.scatter(self.x.data, self.y.data, color=linec, alpha=1., marker='o', s=15**2, edgecolors='black', linewidth=1.)
                
                if hist == True:
                    for side in axs_xhist.spines.keys(): axs_xhist.spines[side].set_linewidth(2.0)
                    axs_xhist.tick_params(axis='both', which='both', direction='in', width=2.0, top=True, right=True, labelbottom=False)
                    axs_xhist.tick_params(axis='y', labelsize=20, pad=10.)
                    for side in axs_yhist.spines.keys(): axs_yhist.spines[side].set_linewidth(2.0)
                    axs_yhist.tick_params(axis='both', which='both', direction='in', width=2.0, top=True, right=True, labelleft=False)
                    axs_yhist.tick_params(axis='x', labelsize=20, pad=10.)
                    hstyle = {'linewidth':2.0}
                    
                    xbins = np.geomspace(xlims[0], xlims[1], 10) if axs.get_xaxis().get_scale() == 'log' else np.linspace(xlims[0], xlims[1], 10)
                    ybins = np.geomspace(ylims[0], ylims[1], 10) if axs.get_yaxis().get_scale() == 'log' else np.linspace(ylims[0], ylims[1], 10)
                    axs_xhist.hist(self.x.data, bins=xbins, color=linec, histtype='step', **hstyle)
                    axs_yhist.hist(self.y.data, bins=ybins, orientation='horizontal', color=linec, histtype='step', **hstyle)
                    

            # Plot fit
            if fit != False:
                xfit = np.geomspace(xlims[0], xlims[1], 100)
                yfit = myfit.exp_func(bestfit.beta, xfit)
                axs.plot(xfit, yfit, color='black', linewidth=2)
                axs.plot(xfit, yfit+ysig, color='black', linestyle='dashdot')
                axs.plot(xfit, yfit-ysig, color='black', linestyle='dashdot')
                
                print('The best fit parameters are: y = x ^', round(bestfit.beta[0], 3), '(+/-', round(bestfit.sd_beta[0], 3), ') *', round(bestfit.beta[1], 3), '(+/-', round(bestfit.sd_beta[1], 3), ')')

                
            pdfname.savefig(fig)
            pdfname.close()
            
            plt.savefig(plotname+'.png', dpi=300, transparent=False)
            
            #plt.close()
            
            
            #ipdb.set_trace()
