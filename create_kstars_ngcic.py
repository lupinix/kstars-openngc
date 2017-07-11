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
    return readable_name

def reformat_ra(ra):
    if ra[0] == "0" or ra[0] == "1" or ra[0] == "2": 
        ra_string = ra.replace(":","")
        return ra_string[:-1] 
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
    return mapping.get(classification, " ")

# Vectorize functions for string reformat operations to run them on whole table
getnum_vect = np.vectorize(getnum)
readable_names_vect = np.vectorize(readable_names)
reformat_ra_vect = np.vectorize(reformat_ra)
reformat_dec_vect = np.vectorize(reformat_dec)

def create_kstars_table_line(name, ra, dec, bmag, classification, smin, smax, pa, pgc, other, messier, longname):
    pass


#ngc_full = ascii.read("OpenNGC/NGC.csv", delimiter=";")
#ngc = ngc_full[getnum_vect(ngc_full["Name"])!="0"]
#n = readable_names_vect(ngc["Name"])
#print(n[n=="N7713BA"])
print(map_classification("*s*"))
