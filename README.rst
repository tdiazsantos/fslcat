**FSLCAT: A catalog of fine-structure lines of galaxies at z > 1, and tools for handling and plotting the data**
============

Purpose and content
-----------
This repository contains the catalog of sources used to generate the figures included in the review paper entitled "Infrared fine-structure lines at high redshift" by Decarli and Diaz-Santos 2025 published on The Astronomy and Astrophysics Review (A&ARv) by Springer Nature. The data in the catalog is, to the best of the authors' knowledge, a complete collection of all observations carried out by infrared telescope facilities of far-infrared fine-structure emission lines from galaxies at redshifts larger than 1. The catalog contains 1550 entries, with more than 500 individual sources that have been observed in one emission line at least once.

The catalog
~~~~~~~~~~~
The catalog can be downloaded from `this Google spreadsheet`_ <https://docs.google.com/spreadsheets/d/1GBEhRR3zSSVupEGh4PbrzMAKzs3w1x2MC6JLtsIIgbk/edit?usp=sharing> and contains the following information:

* Column (1): Flag indicating whether the observation is considered as valid for the catalog
* Column (2): Flag indicating whether the source is the main targeted galaxy (M) or a companion (C)
* Column (3): Source name
* Column (4): Right ascension
* Column (5): Declination
* Column (6): Redshift
* Column (7): Cosmology used to calculate the luminosity distance
* Column (8): Luminosity distance, in [Mpc]
* Column (9): Homogenized source type as extracted from the literature search

   - quasars and AGN from various classification techniques
   - sub-mm galaxies and starbursts, mostly selected via their luminous dust continuum emission in the infrared wavelengths
   - main sequence and more `typical' star-forming galaxies
   - optically--selected galaxies (primarily Lyman Break Galaxies and Ly$\alpha$ emitters)
   - line emitters identified with interferometric observations
   - cluster members of diverse type
* Column (10): Instrument that carried out the observation
* Column (11): Emission line name
* Column (12): Line flux, in [Jy km/s]
* Column (13): Line flux uncertainty, in [Jy km/s]
* Column (14): Line luminosity, in [Lsun]
* Column (15): Line luminosity uncertainty, in [Lsun]
* Column (16): Line full-width at half maximum (FWHM), in [km/s]
* Column (17): Line FWHM uncertainty, in [km/s]
* Column (18): Observed-frame continuum flux density, in [mJy]
* Column (19): Observed-frame continuum flux density uncertainty, in [mJy]
* Column (20): Far-infrared luminosity, in [Lsun]
* Column (21): Far-infrared luminosity uncertainty, in [Lsun]
* Column (22): Far-infrared luminosity when Column (24) is LFIR, or infrared luminosity (to be scaled internally down to far-infrared luminosity by the ``fslcat`` tool) when Column (24) is LIR, in [Lsun]
* Column (23): Uncertainty of Column (22)
* Column (24): Whether the Column (22-23) measurement is LFIR or LIR
* Column (25): Infrared luminosity, in [Lsun]
* Column (26): Infrared luminosity uncertainty, in [Lsun]
* Column (27): Infrared luminosity when Column (29) is LIR, or far-infrared luminosity (to be scaled internally up to infrared luminosity by the ``fslcat`` tool) when Column (29) is LFIR, in [Lsun]
* Column (28): Uncertainty of Column (27)
* Column (29): Whether the Column (26-27) measurement is LIR or LFIR
* Column (30): Reference publication of the emission line observation
* Column (31): Year of the publication
* Column (32): Link to the publication
* Column (33): Reference publication of the dust continuum observation
* Column (34): Year of the publication
* Column (35): Minimum magnification
* Column (36): Maximum magnification
* Column (37): Rest-frame frequency of the emission line
* Column (38): Logarithm of the emission line luminosity
* Column (39): Lower uncertainty of the logarithm of the emission line luminosity
* Column (40): Upper uncertainty of the logarithm of the emission line luminosity

The tool
~~~~~~~~~
The ``fslcat`` python tool uses the master catalog described above to make scatter plots using the available data. The user can plot the entire catalog or a specific sub-sample by selecting sources based on conditions applied to any of the quantities.

To make plots, the user needs to specify the axes they want to visualize via keyword arguments using the syntaxis described below. Scatter plots can be simple (quantity A vs. quantity B) but also more complex. For instance, ``fslcat`` is capable of adding, subtracting, multiplicating or dividing quantities and plotting them in any axis. It also can color-code the data according to a third, simple or complex quantity. ``fslcat`` will automatically cross-correlate the data available for each dataset/column and trim the entries, selecting only the most updated (latest published) value of the quantities to be plotted.

Labels, color-bars, axes and legends are generated automatically. Uncertainties, as well as upper and lower limits of simple or complex quantities are also propagated, calculated and constructed automatically.

In addition to the plot, ``fslcat`` will also output the trimmed sub-sample of the catalog used to generate the figure. This is useful, independently of the plot, to extract and create sub-catalogs based on conditions applied to any of the quantities.

The notebook
~~~~~~~~~~~~
The repository also includes a jupyter notebook with the set-up necessary to solve the equations of statistical equilibrium and calculate the population levels of atoms and ions with different number of electrons. The code not only calculates the emission line luminosities of a variety of species as a function of the parameters that control the gas excitation (Tkin, n_c), but also provides useful quantities related to the line transitions, such as their optical depths as a function of the column density, or their critical densities as a function of the gas temperature and the type of collisional partners. The notebook also includes the scripts necessary to reproduce all the plots included in the review.

Usage in iPython
------------
Run the python code:

> ``run fslcat.py``

Load the catalog:

> ``cat = fslcat('/fslcat_directory/FSL_catalog_v4.csv')``

A few plot examples:

* A plot of [CII]158 luminosity over the far-infrared luminosity as a function of the far-infrared luminosity (corrected for magnification), color-coded as a function of galaxy type:

> ``cat.plot(xkeyws={'1':['LFIR_LIR', 'MagCorr']}, ykeyws={'1':['Lum', '[CII]158'], '2':['LFIR_LIR', '', '/']}, zkeyws={'1':['Type', 'Simplified']})``

* A plot of the [CII]158/[CI]609 line ratio as a function of the [CII]158/LFIR ratio, color-coded as a function of redshift:

> ``cat.plot(xkeyws={'1':['Lum', '[CII]158'], '2':['LFIR_LIR', '', '/']}, ykeyws={'1':['Lum', '[CII]158'], '2':['Lum', '[CI]609', '/']}, zkeyws={'1':['z', '']})``

* A plot of the [CII]158/[CI]609 line ratio as a function of the [CII]158 FWHM, color-coded as a function of redshift, only showing galaxies at z >= 6 that have been observed with ALMA:

> ``cat.plot(xkeyws={'1':['FWHM', '[CII]158']}, ykeyws={'1':['Lum', '[CII]158'], '2':['Lum', '[CI]370', '/']}, zkeyws={'1':['z', '']}, pre_select={'z':[6,np.inf], 'Instrument':'ALMA'})``

Requirements
~~~~~~~~~
``scipy``, ``astropy``, ``numpy``, ``pandas``, ``importlib``, ``math``, ``matplotlib``

Referencing
-----------
If you use ``fslcat`` to make plots of the catalog or generate tables, please add a link to the GitHub repository: https://github.com/tdiazsantos/fslcat

Contributors
~~~~~~~~~~
* Tanio Diaz-Santos
* Roberto Decarli

Bibcode
~~~~~~~~~
TBD
