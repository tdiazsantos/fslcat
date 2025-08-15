# fslcat
A tool for handling and plotting data from the FSL catalog compiled by Decarli &amp; Diaz-Santos 2024

# Usage in iPython

run fslcat.py

cat = fslcat('/fslcat_directory/FSL_catalog_z_1_20230825.csv')

cat.plot(xkeyws={'1':['', 'LFIR_LIR']}, ykeyws={'1':['[CII]158', 'Lum'], '2':['','LFIR_LIR','/']}, zkeyws={'1':['[OIII]88', 'Lum']})


Fine Structure Line Catalog and Plotting Tools
====

# Purpose and content

The catalog
-------
This repository contains the catalog of sources used to generate the figures included in the review paper entitled "Infrared fine-structure lines at high redshift" by Decarli and Diaz-Santos 2025 published on The Astronomy and Astrophysics Review (A&ARv) by Springer Nature. The data in the catalog is, to the best of the authors' knowledge, a complete collection of all observations carried out by infrared telescope facilities of far-infrared fine-structure emission lines from galaxies at redshifts larger than 1. The catalog contains 1550 entries, with more than 500 individual sources that have been observed in one emission line at least once.

The catalog can be downloaded from XXX and contain the following information:

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

Documentation
-------------
Hosted by readthedocs: <https://goals-cafe.readthedocs.io/en/latest/>

Referencing
-----------
If you use ``fslcat`` to make plots of the catalog or generate tables, please reference it as *Diaz-Santos et al. (2025)* (see bibcode below) and add a link to the GitHub repository: https://github.com/tdiazsantos/fslcat

Contributors
------------
* Tanio Diaz-Santos
* Roberto Decarli

Bibcode
-------
| @software{2025ascl.soft01001D,
| author = {{Diaz-Santos}, Tanio and {Lai}, Thomas S. -Y. and {Finnerty}, Luke and {Privon}, George and {Bonfini}, Paolo and {Larson}, Kirsten and {Marshall}, Jason and {Armus}, Lee and {Charmandaris}, Vassilis}, \
| title = "{CAFE: Continuum And Feature Extraction tool}",
| howpublished = {Astrophysics Source Code Library, record ascl:2501.001},
| year = 2025,
| month = jan,
| eid = {ascl:2501.001},
| adsurl = {https://ui.adsabs.harvard.edu/abs/2025ascl.soft01001D},
| adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
