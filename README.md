# fslcat
A tool for handling and plotting data from the FSL catalog compiled by Decarli &amp; Diaz-Santos 2024

# Usage in iPython

run fslcat.py

cat = fslcat('/fslcat_directory/FSL_catalog_z_1_20230825.csv')

cat.plot(xkeyws={'1':['', 'LFIR_LIR']}, ykeyws={'1':['[CII]158', 'Lum'], '2':['','LFIR_LIR','/']}, zkeyws={'1':['[OIII]88', 'Lum']})
