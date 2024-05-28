#!/usr/bin/env python3

import os, sys, copy
import pdb, ipdb
import numpy as np
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord

from arrayop import arrayop

data_dict = {'lines':['[OIII]52um', '[NIII]57um', '[OI]63um', '[OIII]88um', '[NII]122um','[CII]158um', '[OI]146um', '[NII]205um', '[CI]370um', '[CI]609um'],
             'types':['MS/SFG','SB/SMG','QSO/AGN','Opt-Sel','ALMA-Sel','Cluster','DLAHost']}

color_dict = {'lines':['skyblue',   'magenta',    'steelblue', 'dodgerblue', 'palegreen', 'crimson',      'royalblue',  'limegreen',      'coral', 'orange'],
              'types':['forestgreen','red','blue','deepskyblue','darkorchid','darkorange','brown']}


##### Function that performs a self cross match within a catalog, removing duplicates and returning (the dataframe entries of) individual sources
def self_cross_corr(cat, axis_keyws, r_cross):
    
    cross_ids = []
    tmpcat = cat.copy()

    # Create coordinate catalog
    coord_cat = SkyCoord(ra=np.array(tmpcat['RA']), dec=np.array(tmpcat['Dec']), unit=(u.hourangle, u.deg))

    # Run through the entire catalog
    while len(tmpcat) > 0:
        
        # Do not consider sources without coordinates or that have NaN values for the requested quantity
        exclude = False
        if tmpcat.iloc[0]['RA'] is np.nan: exclude = True
        if isinstance(tmpcat.iloc[0][axis_keyws[0]], float):
            if np.isnan(tmpcat.iloc[0][axis_keyws[0]]): exclude = True
        else:
            if tmpcat.iloc[0][axis_keyws[0]] == '': exclude = True
        
        #if tmpcat.iloc[0]['RA'] is np.nan or np.isnan(tmpcat.iloc[0][axis_keyws[0]]): exclude = True

        if exclude == True:
            coord_cat = np.delete(coord_cat, [0])
            tmpcat.drop(tmpcat.index.values[0], inplace=True)
            continue
        
        c = coord_cat[[0]]
        idxc, idxcat, _, _ = coord_cat.search_around_sky(c, r_cross*u.arcsec)
        #print(idxc,idxcat)

        # Build the cross_ids
        if len(idxcat) == 1:
            cross_ids.append(tmpcat.index.values[idxcat[0]])
        elif len(idxcat) > 1:
            # Find valid Ids
            if isinstance(tmpcat.iloc[0][axis_keyws[0]], float):
                v_ids = np.where(np.isnan(tmpcat.iloc[idxcat][axis_keyws[0]]).values == False)[0]
                # Select the most recent value from valid cross_ids
            else:
                v_ids = np.where(tmpcat.iloc[idxcat][axis_keyws[0]] != '')[0]
            cross_ids.append(tmpcat.index.values[idxcat[v_ids[np.nanargmax(tmpcat.iloc[idxcat[v_ids]]['Line_year'])]]])
            #if np.isnan(tmpcat.loc[cross_ids[-1]][axis_keyws[0]]): ipdb.set_trace()
        else:
            raise ValueError('No entries were found, which is impossible')

        # Remove already matched entries
        coord_cat = np.delete(coord_cat, idxcat)
        tmpcat.drop(tmpcat.index.values[idxcat], inplace=True)

    print('Out of', len(cat), 'entries in the', axis_keyws[1], axis_keyws[0], 'catalog,', len(cross_ids), 'independent entries were found')

    # Return the dataframe cross_ids
    return np.array(cross_ids)



##### Function that performs a cross match between two catalogs
def cross_corr(cat1, cat2, axis1_list, axis2_list, r_cross, keep_all=False):
    
    ids = []
    cross_ids = []
    tmpcat1 = cat1.copy()
    tmpcat2 = cat2.copy()
    
    # Create coordinate catalogs
    coord_cat1 = SkyCoord(ra=np.array(tmpcat1['RA']), dec=np.array(tmpcat1['Dec']), unit=(u.hourangle, u.deg))
    coord_cat2 = SkyCoord(ra=np.array(tmpcat2['RA']), dec=np.array(tmpcat2['Dec']), unit=(u.hourangle, u.deg))

    for i in range(len(tmpcat1)):
        
        c = coord_cat1[[i]]
        idxc, idxcat, d2d, d3d = coord_cat2.search_around_sky(c, r_cross*u.arcsec)
        #print(idxc,idxcat)

        # Build the ids (cat1) and cross_ids (cat2)
        if len(idxcat) == 0:
            # Keep all ids (cat1), even if there is no cross match in cat2
            # This is useful when the quantity in cat2 is not critical (e.g., for the z-axis)
            if keep_all == True:
                ids.append(tmpcat1.index.values[i])
                cross_ids.append(np.nan)
            #continue
        elif len(idxcat) == 1:
            ids.append(tmpcat1.index.values[i])
            cross_ids.append(tmpcat2.index.values[idxcat[0]])
        else:
            # Select the most recent value from valid cross_ids
            ids.append(tmpcat1.index.values[i])
            v_ids = np.where(np.isnan(tmpcat2.iloc[idxcat][axis2_keyws[0]]).values == False)[0]
            cross_ids.append(tmpcat2.index.values[idxcat[v_ids[np.nanargmax(tmpcat2.iloc[idxcat[v_ids]]['Line_year'])]]])
        
    print('Out of', len(cat1), 'entries in the', axis1_list, 'catalog(s),', len(cross_ids), 'independent cross-matches were found in the', axis2_list, 'catalog(s) containing', len(cat2), 'entries')
    if keep_all == True: print('Because keep_all=True, the cross-match kept all', len(cross_ids), 'entries of', axis1_list, 'catalog(s), although', np.count_nonzero(~np.isnan(cross_ids)), 'were actually found in the', axis2_list, 'catalog(s)')

    # Return the dataframe ids (cat1) and cross_ids (cat2)
    return np.array(ids), np.array(cross_ids)
        


class axis:

    def __init__(self, axis_keyws, cat=None, cross_match=True, r_cross=0.01, data=None, err=None, lim=None, op=None, name=''):

        self.keyws = axis_keyws
        self.name = name

        if cat is not None:
            # If we want to do a self cross match to generate a catalog of unique sources
            if cross_match == True:
                cross_ids = self_cross_corr(cat, axis_keyws, r_cross)
                self.cross_ids = cross_ids
                
                data = cat.loc[cross_ids][axis_keyws[0]].values
                turn2float = True
                if len(data) > 0:
                    if isinstance(data[0], str):
                        if data[0].isdigit() == False: turn2float = False

                if turn2float:
                    try:
                        data = pd.to_numeric(cat.loc[cross_ids][axis_keyws[0]], errors='coerce').astype('float').values
                    except:
                        ipdb.set_trace()
                
                if axis_keyws[0]+'_err' in cat.columns:
                    if turn2float == True:
                        err = pd.to_numeric(cat.loc[cross_ids][axis_keyws[0]+'_err'], errors='coerce').astype('float').values
                    else:
                        err = cat.loc[cross_ids][axis_keyws[0]+'_err'].values
                    lim_inds = cat.loc[cross_ids][axis_keyws[0]].values == 0.
                    data[lim_inds] = err[lim_inds]
                    err[lim_inds] = np.nan
                    lim = np.zeros(len(cross_ids))
                    lim[lim_inds] = -1.
                else:
                    err = np.full_like(data, np.nan)
                    lim = np.full_like(data, 0.)
                    
                self.cat = cat.loc[cross_ids]

            # Otherwise take the catalog at face value
            else:
                self.cat = cat
                if data is None: ValueError('Data needs to be provided if there is no catalog.')

        elif data is None:
            # In this case no catalog will be attached to the self
            raise ValueError('Data needs to be provided if there is no catalog.')

        self.data = data
        self.err = err
        self.lim = lim
        
        self.op = op
        self.get_label()
        


    ##### Function that updates the axis data and catalog given an array of dataframe ids
    def update(self, ids, match_cat=None):
        
        # If the catalog does not have missing sources (likely the x- and y-axis)
        if np.isnan(ids).any() == False:
            ith_ids = []
            for i, row_id in enumerate(self.cat.index):
                if row_id in ids: ith_ids.append(i)
            ith_ids = np.array(ith_ids, dtype=int)

            self.data = self.data[ith_ids]
            self.err = self.err[ith_ids]
            self.lim = self.lim[ith_ids]
            self.cat = self.cat.loc[ids]

        else:
            # Otherwise (likely z-axis) we need to provide the catalog used for the cross matching with the self (likely the x- or y-axis)
            if match_cat is not None:
                tmpcat = match_cat.copy()
                data = np.full(len(match_cat), np.nan)
                err = np.full(len(match_cat), np.nan)
                lim = np.full(len(match_cat), np.nan)
                for i, id in enumerate(ids):
                    if np.isnan(id) == False:
                        tmpcat.iloc[i] = self.cat.loc[id]
                        ith_id = np.where(self.cat.index.values == id)[0]
                        data[i] = self.data[ith_id]
                        err[i] = self.err[ith_id]
                        lim[i] = self.lim[ith_id]
                    else:
                        tmpcat.iloc[i] = np.nan
                
                self.data = data
                self.err = err
                self.lim = lim
                self.cat = tmpcat
                
            else:
                raise ValueError('This update likely comes from a keep_all=True cross match. If so, the original catalog must be provided')



    ##### Function that performs arithmetic operations between two axes
    def operate(self, axis2, operator=None, nanneg=False, **kwargs):
        
        op = operator
        if op is None: op = axis2.op
        if op is None: raise ValueError('An operator is needed for one of the axes. Check it out.')

        keyws = {'1':self.keyws, '2':axis2.keyws}

        # Perform the operation and propagate the errors
        if op != 'join':
            data, err = arrayop(self.data, self.err, axis2.data, axis2.err, op)
            lim = self.lim + axis2.lim
            
        # These if/elses handle the limits
        if op == '+' or op == '*' or op == 'ave' or op == '+^2':
            nullinds = np.where((np.isnan(err)) & (((lim == 0.) & (self.lim != axis2.lim)) | (np.isnan(lim))))[0]
            data[nullinds] = np.nan
            lim[nullinds] = np.nan
            liminds = np.where((np.isnan(err)) & ((lim != 0.) & (np.isnan(lim) == False)))[0]
            lim[liminds] = lim[liminds]/abs(lim[liminds])

        elif op == '-' or op == '/' or op == '-^2' or op == '/^2':
            liminds = np.where((np.isnan(err)) & (lim == 0.))[0]
            lim[liminds] = self.lim[liminds]
            nullinds = np.where((np.isnan(err)) & ((lim != 0.) | (np.isnan(lim))) & (self.lim == axis2.lim))[0]
            data[nullinds] = np.nan
            lim[nullinds] = np.nan
            invinds = np.where((self.lim == 0.) & (axis2.lim == 0.))[0]
            lim[invinds] = -1. * lim[invinds]
            
            if op == '-' and nanneg == True:
                nullinds = np.where(data <= 0.)[0]
                data[nullinds] = np.nan
                err[nullinds] = np.nan

        else:
            raise ValueError('Operator not found')
            
        # Create the new resulting axis and combine the labels and units
        if op != 'joint':
            axis12 = axis(keyws['1'], cat=self.cat, cross_match=False, data=data, err=err, lim=lim)
            axis12.label = self.add_labels(axis2.label, op, **kwargs)
        else:
            axis12 = axis(keyws['1'], cat=pd.concat([self.cat,axis2.cat]), data=np.concatenate((self.data,axis2.data)),
                          err=np.concatenate((self.err,axis2.err)), lim=np.concatenate((self.lim,axis2.lim)))
            axis12.label = ['Joint lab','']

        axis12.keyws = keyws

        print('Note that the provided axes must have been cross matched before, as the new axis will inherit the catalog of the first axis (which should be the same as the second axis).')
        
        return axis12
        


    ##### Function that assigns a label and a unit to the axis based on the quantity requested
    def get_label(self):
        
        unit = ''
        if self.keyws[0] == 'z':
            label = r'z'
        elif self.keyws[0] == 'Ldist':
            label = r'D\,$\rm{_{L}}$'
        elif self.keyws[0] == 'Type':
            label = r'Type'
        elif self.keyws[0] == 'Instrument':
            label = r'Instrument'
        elif self.keyws[0] == 'Line':
            label = r'Line'
        elif self.keyws[0] == 'LIR' or self.keyws[0] == 'LIR_LFIR':
            label = r'L$\rm{_{IR}}$'
            unit = r'[L$\rm{_\odot}$]'
        elif self.keyws[0] == 'LFIR' or self.keyws[0] == 'LFIR_LIR':
            label = r'L$\rm{_{FIR}}$'
            unit = r'[L$\rm{_\odot}$]'
        elif self.keyws[0] == 'Line_year':
            label = r'Year'
        elif self.keyws[0] == 'Mag':
            label = r'Magnification'
        elif self.keyws[0] == 'Line_rf':
            label = r'Line rest-frame'
        else:
            unit = ''
            if self.keyws[1]+'um' in data_dict['lines']:
                if self.keyws[0] == 'Flux':
                    label = r'f$\rm{_{'+self.keyws[1]+'}}$'
                    unit = r'[Jy km s$^{-1}$]'
                elif self.keyws[0] == 'Lum':
                    if len(self.keyws) == 3:
                        if self.keyws[2] == 'Flux':
                            label = r'f$\rm{^{rest}_{'+self.keyws[1]+'}}$'
                            unit = r'[Jy km s$^{-1}$]'
                    else:
                        label = r'L$\rm{_{'+self.keyws[1]+'}}$'
                        unit = r'[L$\rm{_\odot}$]'
                elif self.keyws[0] == 'FWHM':
                    label = r'FWHM$\rm{_{'+self.keyws[1]+'}}$'
                    unit = r'[km s$^{-1}$]'
                elif self.keyws[0] == 'Cont':
                    label = r'Cont$\rm{^{rest}_{'+self.keyws[1]+'}}$'
                    unit = r'[mJy]'
            else:
                raise ValueError('Line not found in list of lines')

        self.label = [label, unit]



    ##### Function that merges/combines the labels and units of two axes
    def add_labels(self, lab2, op, parenth=False, nospace=False, plot=False):

        lab = ['','']
        sp = '' if nospace == True else ' '
        
        if plot == True:
            if lab2[1] == self.label[1]:
                lab = self.label[0]+sp+op+sp+lab2[0] if op == '/' else self.label[0]+sp+self.label[1]+sp+op+sp+lab2[0]+sp+lab2[1]
            elif lab2[1] == '':
                lab = self.label[0]+sp+self.label[1]+sp+op+sp+lab2[0]
            else:
                lab = self.label[0]+sp+self.label[1]+sp+op+sp+lab2[0]+sp+lab2[1]

        else:
            lab[0] = self.label[0]+sp+op+sp+lab2[0]
            if parenth == True: lab[0] = '('+lab[0]+')'

            if lab2[1] == self.label[1]:
                if op == '/': lab[1] = ''
                elif op == '*': lab[1] = self.label[1]+'$^2$' if self.label[1] != '' else self.label[1]
                else: lab[1] = self.label[1]
            elif lab2[1] == '':
                lab[1] = self.label[1]
            else:
                lab[1]='['+(self.label[1].replace('[','')).replace(']','')+sp+op+sp+(lab2[1].replace('[','')).replace(']','')+']'
                if parenth == True: lab[1]='('+lab[1]+')'

        return lab



    def get_color(self, lab):

        if lab == 'lines':
            try:
                color_ind = []
                color_ind.append(data_dict[lab].index(self.keyws['1'][1]+'um'))
            except:
                ipdb.set_trace()
                raise ValueError('At least one line in',self.keyws['1'][1],'is not present in line list')
        elif lab == 'types':
            try:
                color_ind = []
                for i in range(len(self.data)): color_ind.append(data_dict[lab].index(self.data[i]))
            except:
                ipdb.set_trace()
                raise ValueError('At least one type in',self.data, 'is not present in type list')


        return [color_dict[lab][k] for k in color_ind]

