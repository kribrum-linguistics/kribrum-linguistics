#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

import unicodedata

try:
    np = sys.argv[1]
except:
    np = "транспортная карта"

<<<<<<< HEAD
def print_data(np):
=======
def decline(np):
>>>>>>> 78012edac79e631049e971035b8c9d2aa18ff0c0
    for i in np:
        try:
            print(i + "\t" + str(ord(i)) + "\t" + "{:04x}".format(ord(i)) + "\t" + unicodedata.category(i) + "\t" + unicodedata.name(i))
        except ValueError:
            print(i + "\t" + str(ord(i)) + "\t" + "{:04x}".format(ord(i)) + "\t" + unicodedata.category(i))

<<<<<<< HEAD
print_data(np)
=======
decline(np)
#print(":".join("{:04x}".format(ord(i)) for i in np))
>>>>>>> 78012edac79e631049e971035b8c9d2aa18ff0c0
