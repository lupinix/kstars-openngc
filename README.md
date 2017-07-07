# kstars-openngc
OpenNGC catalog for KStars

This repository contains the script to create ngcic.dat to use the OpenNGC catalogue [1] with KStars

Licensing:
  * License for the code is MIT, check file LICENSE
  * License for the data is CC-BY-SA-4.0 as for the OpenNGC catalog itself, check file LICENSE_OpenNGC

Content:
  * create_kstars_ngcic.py – script to generate ngcic.dat from NGC.csv
  * ngcic.dat – replacement for ngcic.dat shipped by KStars

Requirements:
  * astropy is required to run the Python scripts, we use it for table handling

[1] https://github.com/mattiaverga/OpenNGC
