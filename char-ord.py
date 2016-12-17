#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

import unicodedata

try:
    np = sys.argv[1]
except:
    np = "транспортная карта"

def decline(np):
    for i in np:
        try:
            print(i + "\t" + str(ord(i)) + "\t" + "{:04x}".format(ord(i)) + "\t" + unicodedata.category(i) + "\t" + unicodedata.name(i))
        except ValueError:
            print(i + "\t" + str(ord(i)) + "\t" + "{:04x}".format(ord(i)) + "\t" + unicodedata.category(i))

decline(np)
#print(":".join("{:04x}".format(ord(i)) for i in np))