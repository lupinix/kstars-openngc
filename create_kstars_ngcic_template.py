#!/usr/bin/python3
#
# MIT License
#
# Copyright (c) 2017 Christian Dersch <lupinix@mailbox.org>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from astropy.io import ascii
import numpy as np


def getnum(ngcstr):
    # Function to extract the integer number of an object,
    # returns 0 for non-main objects to avoid duplicates
    if ngcstr[0] == "N":
        if len(ngcstr) == 7:
            return ngcstr[3:7]
        elif len(ngcstr) == 8:
            return ngcstr[3:8]
        else:
            return "0"
    elif ngcstr[0] == "I":
        if len(ngcstr) == 6:
            return ngcstr[2:6]
        elif len(ngcstr) == 7:
            return ngcstr[2:7]
        else:
            return "0"
    else:
        return "0"

def readable_names(ngcstr):
    # Generate better readable names, e.g. NGC 224 instead of NGC0224
    if ngcstr[0] == "N":
        readable_name = "N" + ngcstr[3:].lstrip("0").rjust(4)
    elif ngcstr[0] == "I":
        readable_name = "I" + ngcstr[2:].lstrip("0").rjust(4)
    else:
        # Change nothing if don't know what to do
        readable_name = ngcstr
    return readable_name.ljust(6)

def reformat_ra(ra):
    if ra[0] == "0" or ra[0] == "1" or ra[0] == "2": 
        ra_string = ra.replace(":","")
        if len(ra_string) > 8:
            return ra_string[:-1]
        else:
            return ra_string
    else:
        return 8*" "

def reformat_dec(dec):
    # Omit rows with empty coordinates (nonex objects)
    if dec[0] == "-" or dec[0] == "+":
        dec_string = dec.replace(":","")
        if len(dec_string) == 7:
            return dec_string
        elif len(dec_string) == 9:
            return dec_string[:dec_string.index(".")]
        else:
            return 7*" "
    else:
        return 7*" "

def map_classification(classification):
    """
    Mapping KStars ngcic.dat → OpenNGC
    
    OpenNGC      KStars ngcic     Type
    
    *                1            Star
    **               17           Double Star
    *Ass             13           Association of stars (13 matches better than 5)
    Ocl              3            Open Cluster
    Gcl              4            Globular Cluster
    Cl+N             5            Star cluster + Nebula
    G                8            Galaxy
    GPair            8            Galaxy Pair
    GTrpl            8            Galaxy Triplet
    GGroup           8            Group of galaxies
    PN               6            Planetary Nebula
    HII              5            HII Ionized region
    EmN              5            Emission Nebula
    Neb              5            Nebula
    RfN              5            Reflection Nebula
    SNR              7            Supernova remnant
    Nova                          Nova star
    NonEx                         Nonexistent object
    Dup                           Duplicate
    Other                         Other
    """
    mapping = {
        "*": "1",
        "**": "17",
        "*Ass": "13",
        "OCl": "3",
        "GCl": "4",
        "Cl+N": "5",
        "G": "8",
        "GPair": "8",
        "GTrpl": "8",
        "GGroup": "8",
        "PN": "6",
        "HII": "5",
        "EmN": "5",
        "Neb": "5",
        "RfN": "5",
        "SNR": "7"
    }
    return mapping.get(classification, " ").rjust(2)


def extract_pgcnum(id_list):
    if id_list != "--":
        s = id_list.split(",")
        for id in s:
            if id[0:3] == "PGC":
                pgc = id[3:].strip().lstrip("0").rjust(6)
                if len(pgc) <= 6:
                    return pgc
        return 6*" "
    else:
        return 6*" "
        

def extract_ugcnum(id_list):
    if id_list != "--":
        s = id_list.split(",")
        for id in s:
            if id[0:3] == "UGC":
                return ("UGC" + id[3:].strip().lstrip("0").rjust(6)).ljust(15)
        return 15*" "
    else:
        return 15*" "

def messier_str(messier):
    if messier != "--":
        return "M " + str(messier).rjust(3)
    else:
        return 5*" "

# Vectorize functions for string reformat operations to run them on whole table
getnum_vect = np.vectorize(getnum)
readable_names_vect = np.vectorize(readable_names)
reformat_ra_vect = np.vectorize(reformat_ra)
reformat_dec_vect = np.vectorize(reformat_dec)
map_classification_vect = np.vectorize(map_classification)
extract_pgcnum_vect = np.vectorize(extract_pgcnum)
extract_ugcnum_vect = np.vectorize(extract_ugcnum)

def create_kstars_table_line(name, ra, dec, bmag, classification, smax, smin, pa, others, messier, longname):
    s = ""
    s += readable_names(name)
    if ra != "--":
        s += reformat_ra(ra)
    else:
        s += 8*" "
    s += " "
    if dec != "--":
        s += reformat_dec(dec)
    else:
        s += 7*" "
    s += " "
    if bmag != "--":
        s += "{:05.2f}".format(bmag)
    else:
        s += 5*" "
    s += map_classification(classification)
    s += " "
    if smax != "--":
        if smax < 100:
            s += "{:05.2f}".format(smax)
        else:
            s += "{:05.1f}".format(smax)
    else:
        s += 5*" "
    s += " "
    if smin != "--":
        if smin < 100:
            s += "{:05.2f}".format(smin)
        else:
            s += "{:05.1f}".format(smin)
    else:
        s += 5*" "
    s += " "
    if pa != "--":
        s += "{:3d}".format(pa)
    else:
        s+= 3*" "
    s += " "
    s += extract_pgcnum(others)
    s += " "
    s += extract_ugcnum(others)
    s += " "
    s += messier_str(messier)
    s += " "
    if longname != "--":
        s += str(longname)
    s += "\n"
    return s


ngc_full = ascii.read("OpenNGC/NGC.csv", delimiter=";")
ngc = ngc_full[getnum_vect(ngc_full["Name"])!="0"]
f = open("ngcic.dat","w")
# Header
f.write("# OpenNGC - A license friendly NGC/IC objects database\n")
f.write("# Catalog created by: Mattia Verga <mattia dot verga at tiscali dot it>\n")
f.write("# Converted for KStars by: Christian Dersch <lupinix at mailbox dot org>\n")
f.write("# License: CC-BY-SA-4.0\n#\n")
f.write("# Created using OPENNGC_COMMIT from\n# https://github.com/mattiaverga/OpenNGC\n")
f.write("# Conversion script: https://github.com/lupinix/kstars-openngc\n#\n")
f.write("#ID     RA        Dec  BMag type  a     b   pa   PGC  other           Messr Longname\n#\n")
# Some non-ngcic-objects
f.write("    0 052334.5 -694522  0.9  8   0.0            17223 ESO  56- G 115        Large Magellanic Cloud\n\
    0 181654.0 -182900  4.6  3  15.0                                  M  24 Delle Caustiche\n\
    0 034700.0 +240700  1.6  3  70.0                                  M  45 Pleiades\n\
    0 122224.0 +580500  8.4  1   0.0   0.0                            M  40\n\
    0 192524.0 +201100  3.6  3  60.0                  Collinder 399         Brocchi's Cluster, Coathanger Asterism\n\
    0 122230.3 +255042  1.8  3 270.0                  Melotte 111           Melotte 111, Coma Star Cluster\n")

for i in range(len(ngc)):
    ngc1 = ngc[i]
    if ngc1["Name"] == "NGC5866":
        # Workaround for M 102 which is referenced to NGC 5866 nowadays, we want the user to be able to search for M 102 although not in catalog
        f.write(create_kstars_table_line(ngc1["Name"],ngc1["RA"],ngc1["Dec"],ngc1["B-Mag"],ngc1["Type"],ngc1["MajAx"],ngc1["MinAx"],ngc1["PosAng"],ngc1["Identifiers"],"102",ngc1["Common names"]))
    else:
        f.write(create_kstars_table_line(ngc1["Name"],ngc1["RA"],ngc1["Dec"],ngc1["B-Mag"],ngc1["Type"],ngc1["MajAx"],ngc1["MinAx"],ngc1["PosAng"],ngc1["Identifiers"],ngc1["M"],ngc1["Common names"]))
f.close()
